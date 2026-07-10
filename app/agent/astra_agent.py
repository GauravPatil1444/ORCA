# astra_agent.py
import os
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from app.agent.tools import create_agent_tools
from app.core.langfuse_client import get_system_prompt
from dotenv import load_dotenv

load_dotenv()

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    workspace_type: str # Added to track workspace classification

class AstraAgent:
    def __init__(self, user_collection):
        # Initialize LLM and Tools (Stateless components)
        self.llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
        self.tools = create_agent_tools(user_collection)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Build Graph
        workflow = StateGraph(GraphState)
        
        def agent_node(state: GraphState):
            messages = state["messages"]
            workspace = state.get("workspace_type", "default")
            
            # Dynamically fetch the latest prompt from Langfuse per execution
            system_prompt = get_system_prompt(workspace)
            
            # Inject system prompt if not already present in the history
            if not any(isinstance(m, SystemMessage) for m in messages):
                messages = [SystemMessage(content=system_prompt)] + list(messages)
            
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
        
        # Compile with in-memory checkpointer for multi-turn session state
        self.graph = workflow.compile(checkpointer=MemorySaver())

    async def astream_chat(self, user_input: str, workspace_type: str, config: dict):
        """Asynchronous generator for streaming LangGraph events."""
        inputs = {
            "messages": [HumanMessage(content=user_input)],
            "workspace_type": workspace_type
        }
        async for event in self.graph.astream_events(inputs, config=config, version="v2"):
            yield event