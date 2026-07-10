# app/api/routes/chat.py
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json
from app.api.deps import get_user_collection
from app.agent.astra_agent import AstraAgent

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str
    workspace_type: Optional[str] = "default"
    scope_filters: Optional[List[str]] = None # For manual context scoping via UI "+" menu

async def event_generator(agent: AstraAgent, user_input: str, workspace_type: str, session_id: str):
    # Thread ID enables LangGraph MemorySaver to maintain multi-turn state
    config = {"configurable": {"thread_id": session_id}}
    
    async for event in agent.astream_chat(user_input, workspace_type, config):
        kind = event["event"]
        
        # 1. Stream LLM text tokens to the frontend
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield f"data: {json.dumps({'token': content})}\n\n"
                
        # 2. Intercept OWST Tool Payload (Spec 3.2 / 4.5)
        elif kind == "on_tool_end" and event["name"] == "owst_live_search":
            tool_output = event["data"].get("output", "")
            try:
                payload = json.loads(tool_output)
                target_url = payload.get("target_url")
                classes = payload.get("classes_to_remove", [])
                classes_str = ",".join(classes)
                
                # Emit the explicit system macro flag for the frontend to catch
                macro = f"RENDER_OWST: {target_url}&classes_to_remove={classes_str}"
                yield f"data: {json.dumps({'macro': macro})}\n\n"
            except Exception:
                pass # Fallback if tool output isn't the expected JSON

    yield "data: [DONE]\n\n"

@router.post("/chat/stream")
async def stream_chat(req: ChatRequest, request: Request):
    # Retrieve the user's single collection
    user_collection = get_user_collection(request, req.user_id)
    
    # Initialize the Stateful Agent
    agent = AstraAgent(user_collection)
    
    # Return the StreamingResponse (SSE)
    return StreamingResponse(
        event_generator(agent, req.message, req.workspace_type, req.session_id),
        media_type="text/event-stream"
    )