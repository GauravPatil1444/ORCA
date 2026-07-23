# app/api/routes/chat.py
import json
import re
from typing import List, Optional
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langgraph.errors import GraphRecursionError
from langfuse.callback import CallbackHandler as LangfuseCallbackHandler

from app.api.deps import get_user_collection
from app.agent.astra_agent import AstraAgent
from app.core.config import get_settings

settings = get_settings()
router = APIRouter()

class OWSTContext(BaseModel):
    source_id: str
    base_url: str
    classes_to_remove: List[str] = []

class ChatRequest(BaseModel):
    session_id: str
    user_id: str
    query: str
    scope_filters: Optional[List[str]] = None
    owst_context: Optional[List[OWSTContext]] = None 
    workspace_type: Optional[str] = "default"


@router.post("/chat/stream")
async def stream_chat(req: ChatRequest, request: Request):
    
    async def event_generator():
        yield ": Agent thinking...\n\n"
        
        langfuse_handler = LangfuseCallbackHandler(
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key=settings.LANGFUSE_SECRET_KEY,
            host=settings.LANGFUSE_HOST,
            session_id=req.session_id,
            user_id=req.user_id,
            tags=[req.workspace_type or "default"]
        )

        config = {
            "configurable": {"thread_id": req.session_id},
            "recursion_limit": 50,
            "callbacks": [langfuse_handler]
        }
        
        user_collection = get_user_collection(request, req.user_id)
        agent = AstraAgent(user_collection)
        
        
        inputs = {
            "messages": [HumanMessage(content=req.query)],
            "workspace_type": req.workspace_type or "default",
            "scope_filters": req.scope_filters,
            "owst_context": [ctx.model_dump() for ctx in req.owst_context] if req.owst_context else None
        }
        
        try:
            async for event in agent.astream_events(inputs, config=config, version="v2"):
                kind = event["event"]
                
                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        yield f"data: {json.dumps({'token': content})}\n\n"
                        
                # Intercept Knowledge Search Tools for Sources
                elif kind == "on_tool_end" and event["name"] in ["universal_knowledge_search", "filtered_knowledge_search"]:
                    tool_output = event["data"].get("output", "")
                    if isinstance(tool_output, str):
                        sources = re.findall(r"Source:\s*(.+?)(?:\n|$)", tool_output)
                        clean_sources = list(set([s.strip() for s in sources if s.strip() and s.strip() != 'Unknown']))
                        if clean_sources:
                            yield f"data: {json.dumps({'sources': clean_sources})}\n\n"
                            
                # 🚨 Intercept OWST Tool for Raw URL Macro
                elif kind == "on_tool_end" and event["name"] == "owst_live_search":
                    tool_output = event["data"].get("output", "")
                    try:
                        payload = json.loads(tool_output)
                        target_url = payload.get("target_url")
                        if target_url:
                            macro = f"RENDER_OWST: {target_url}"
                            yield f"data: {json.dumps({'macro': macro})}\n\n"
                    except Exception:
                        pass
                        
        except GraphRecursionError:
            yield f"data: {json.dumps({'token': '\n\nI reached my maximum search limit. Please try rephrasing.'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            langfuse_handler.flush()

        yield "data: [DONE]\n\n"
        
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    )