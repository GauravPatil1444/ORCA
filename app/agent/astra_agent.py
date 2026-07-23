# app/agent/graph.py
from typing import TypedDict, Annotated, List, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from app.agent.tools import create_agent_tools
from app.core.langfuse_client import get_system_prompt
from app.core.config import get_settings

settings = get_settings()

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    workspace_type: str
    scope_filters: Optional[List[str]]
    owst_context: Optional[List[dict]] # 🚨 Added back to state

class AstraAgent:
    def __init__(self, user_collection):
        self.llm = ChatGroq(
            model="openai/gpt-oss-120b", 
            temperature=0, 
            api_key=settings.GROQ_API_KEY
        )
        self.tools = create_agent_tools(user_collection)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        workflow = StateGraph(GraphState)
        
        def agent_node(state: GraphState):
            messages = list(state["messages"])
            workspace = state.get("workspace_type", "default")
            
            system_prompt = get_system_prompt(workspace)
            context_instructions = ""
            
            if state.get("scope_filters"):
                context_instructions += f"\n\n[LOCAL DB RESTRICTION]\nThe user restricted local search to: {state['scope_filters']}. Use `filtered_knowledge_search` with these exact `sources`.\n"

            # 🚨 MANDATORY OWST DIRECTIVE
            if state.get("owst_context"):
                ctx = state["owst_context"][0]
                base_url = ctx.get("base_url", "")
                context_instructions += "\n\n[MANDATORY LIVE WEB CONTEXT ATTACHED]\n"
                context_instructions += f"The user has explicitly attached a live web domain: {base_url}.\n"
                context_instructions += f"You MUST invoke the `owst_live_search` tool right now with `base_domain='{base_url}'`.\n"
                context_instructions += "DO NOT answer from internal training data. Use the tool to find the exact deep-link.\n"

            context_instructions += "\n\n[CRITICAL DIRECTIVE]\n"
            context_instructions += "If a tool returns empty results, DO NOT call the tool again. Immediately synthesize a final text response.\n"

            final_prompt = system_prompt + context_instructions
            
            system_msg_exists = False
            for i, m in enumerate(messages):
                if isinstance(m, SystemMessage):
                    messages[i] = SystemMessage(content=final_prompt)
                    system_msg_exists = True
                    break
            
            if not system_msg_exists:
                messages.insert(0, SystemMessage(content=final_prompt))
            
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}
            
        tool_node = ToolNode(self.tools)
        
        def should_continue(state: GraphState):
            last_message = state["messages"][-1]
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return "tools"
            return END
            
        workflow.add_node("agent", agent_node)
        workflow.add_node("tools", tool_node)
        
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
        workflow.add_edge("tools", "agent")
        
        self.graph = workflow.compile(checkpointer=MemorySaver())

    async def astream_events(self, inputs: dict, config: dict, version: str):
        async for event in self.graph.astream_events(inputs, config=config, version=version):
            yield event