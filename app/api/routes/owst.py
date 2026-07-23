# app/api/routes/owst.py
import json
import re
import time
from typing import Union, List
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import HTMLResponse
from groq import Groq
from app.services.owst_scraper import fetch_and_clean_html
from app.core.langfuse_client import langfuse
from app.core.config import get_settings

from langfuse.decorators import observe, langfuse_context

settings = get_settings()
router = APIRouter()
groq_client = Groq(api_key=settings.GROQ_API_KEY)

@observe(as_type="generation")
def execute_groq_routing(messages: list, model_name: str) -> str:
    """Wraps the raw Groq SDK call to manually log the generation to Langfuse."""
    langfuse_context.update_current_observation(
        model=model_name,
        input=messages
    )
    
    chat_completion = groq_client.chat.completions.create(
        messages=messages,
        model=model_name,
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    
    output = chat_completion.choices[0].message.content
    
    usage = None
    if hasattr(chat_completion, 'usage') and chat_completion.usage:
        usage = {
            "prompt_tokens": chat_completion.usage.prompt_tokens,
            "completion_tokens": chat_completion.usage.completion_tokens,
            "total_tokens": chat_completion.usage.total_tokens
        }
        
    langfuse_context.update_current_observation(
        output=output,
        usage=usage
    )
    
    return output

@observe()
@router.get("/owst", response_class=HTMLResponse)
async def owst_iframe(
    link: str = Query(..., description="Base website or domain context"), 
    query: str = Query(..., description="User's question"),
    classes_to_remove: Union[str, List[str]] = Query("", description="CSS classes to strip")
):
    
    llm_output = ""
    try:
        # @observe() automatically captures the route arguments as the trace input!
        langfuse_context.update_current_trace(
            name="OWST_Iframe_Routing"
        )

        # 1. Fetch & compile prompt from Langfuse
        owst_prompt = langfuse.get_prompt("owst_router")
        compiled_prompt = owst_prompt.compile(query=f"{link} {query}")
        
        # 2. Safe message construction for Groq
        messages = []
        for msg in compiled_prompt:
            role = str(msg.get("role", "user") if isinstance(msg, dict) else getattr(msg, "role", "user")).lower()
            content = msg.get("content", "") if isinstance(msg, dict) else getattr(msg, "content", "")
            if isinstance(content, list):
                content = " ".join([b.get("text", "") for b in content if isinstance(b, dict)])
            messages.append({"role": role, "content": str(content)})

        # 3. Two-LLM Cycle Fallback
        models = ["groq/compound", "groq/compound-mini"]
        
        for model in models:
            try:
                llm_output = execute_groq_routing(messages, model)
                break 
            except Exception as e:
                error_str = str(e).lower()
                if any(k in error_str for k in ["rate", "limit", "overloaded", "502", "503", "429", "413"]):
                    print(f"[OWST] {model} hit limit/error. Falling back...")
                    time.sleep(1)
                    continue
                raise e 
                
        if not llm_output:
            raise HTTPException(status_code=503, detail="All LLM models are currently unavailable.")
            
        # 4. Parse JSON & Scrape
        if llm_output.startswith("```"):
            llm_output = llm_output.strip("`").replace("json", "", 1).strip()
            
        parsed_output = json.loads(llm_output)
        target_url = parsed_output.get("link")
        
        if not target_url:
            raise ValueError("Missing 'link' key in LLM output")
            
        # Handle classes_to_remove
        if isinstance(classes_to_remove, str):
            classes_list = [c.strip() for c in classes_to_remove.split(',') if c.strip()]
        else:
            classes_list = [str(c).strip() for c in classes_to_remove if str(c).strip()]

        langfuse_context.update_current_trace(
            metadata={"target_url": target_url, "classes_removed": classes_list}
        )

        cleaned_html = fetch_and_clean_html(target_url, classes_list)
        return HTMLResponse(content=cleaned_html, status_code=200)
        
    except json.JSONDecodeError:
        langfuse_context.update_current_trace(metadata={"error": f"Invalid JSON: {llm_output}"})
        raise HTTPException(status_code=500, detail=f"Invalid JSON from LLM: {llm_output}")
        
    except Exception as e:
        # Langfuse automatically captures raised exceptions, but we add it to metadata for easy dashboard filtering
        langfuse_context.update_current_trace(metadata={"error": str(e)})
        raise HTTPException(status_code=500, detail=f"OWST routing failed: {str(e)}")
        
    finally:
        # CRITICAL: Force flush the trace to Langfuse before closing the request
        langfuse_context.flush()