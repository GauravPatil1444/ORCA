from typing import TypedDict, Annotated, List, Optional
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from app.agent.tools import create_agent_tools
from app.core.langfuse_client import get_system_prompt
from app.core.config import get_settings
from langfuse import observe

settings = get_settings()

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    workspace_type: str
    scope_filters: Optional[List[str]]
    owst_context: Optional[List[dict]]

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
        
        @observe(as_type="span", name="agent_node")
        def agent_node(state: GraphState):
            messages = list(state["messages"])
            workspace = state.get("workspace_type", "default")
            
            scope_filters = state.get("scope_filters")
            owst_context = state.get("owst_context")
            
            attached_domain = ""
            if owst_context and len(owst_context) > 0:
                attached_domain = owst_context[0].get("base_url", "")

            system_prompt = get_system_prompt(
                workspace,
                scope_filters=scope_filters,
                attached_domain=attached_domain
            )
            
            system_msg_exists = False
            for i, m in enumerate(messages):
                if isinstance(m, SystemMessage):
                    messages[i] = SystemMessage(content=system_prompt)
                    system_msg_exists = True
                    break
            
            if not system_msg_exists:
                messages.insert(0, SystemMessage(content=system_prompt))
            
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

    async def ainvoke(self, inputs: dict, config: dict):
        if "callbacks" not in config:
            try:
                from app.core.langfuse_client import langfuse_handler
                config["callbacks"] = [langfuse_handler]
            except ImportError:
                pass

        return await self.graph.ainvoke(inputs, config=config)