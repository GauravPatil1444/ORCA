# app/agent/tools.py
import json
import re
from typing import Optional, List
from langchain_core.tools import tool
from astrapy import Collection
from groq import Groq
from langfuse import observe, get_client

from app.core.config import get_settings

settings = get_settings()
groq_client = Groq(api_key=settings.GROQ_API_KEY)
langfuse_client = get_client()

def create_agent_tools(user_collection: Collection):
    
    @tool
    @observe(as_type="span", name="universal_knowledge_search")
    def universal_knowledge_search(query: str) -> str:
        """Performs a semantic similarity sweep across the user's entire knowledge collection."""

        vector_match = user_collection.find(
            sort={"$vectorize": query}, 
            limit=5, 
            projection={"data": True, "metadata": True}
        )
        results = [f"Source: {doc.get('metadata', {}).get('source', 'Unknown')}\nContent: {doc['data']}" for doc in vector_match]
        return "\n\n".join(results) if results else "No relevant information found in the knowledge base."

    @tool
    @observe(as_type="span", name="filtered_knowledge_search")
    def filtered_knowledge_search(query: str, sources: Optional[List[str]] = None, categories: Optional[List[str]] = None) -> str:
        """Performs a scoped semantic search limited to specific file sources or ingestion categories."""
        filter_dict = {}
        if sources: filter_dict["metadata.source"] = {"$in": sources}
        if categories: filter_dict["metadata.category"] = {"$in": categories}
            
        vector_match = user_collection.find(
            sort={"$vectorize": query},
            filter=filter_dict, 
            limit=5, 
            projection={"data": True, "metadata": True}
        )
        results = [f"Source: {doc.get('metadata', {}).get('source', 'Unknown')}\nContent: {doc['data']}" for doc in vector_match]
        return "\n\n".join(results) if results else "No relevant information found matching the specified filters."

    @tool
    @observe(as_type="span", name="owst_live_search")
    def owst_live_search(query: str, base_domain: Optional[str] = None) -> str:
        """Searches the live web to find the most relevant deep-link URL for a given query."""
        llm_output = ""
        try:
            owst_prompt = langfuse_client.get_prompt("owst_router")
            link_context = base_domain if base_domain else "the general web"
            
            try:
                compiled_prompt = owst_prompt.compile(link=link_context, query=query)
            except Exception:
                search_context = f"{link_context} {query}"
                compiled_prompt = owst_prompt.compile(query=search_context)
            
            messages = []
            for msg in compiled_prompt:
                role = str(msg.get("role", "user") if isinstance(msg, dict) else getattr(msg, "role", "user")).lower()
                content = msg.get("content", "") if isinstance(msg, dict) else getattr(msg, "content", "")
                if isinstance(content, list):
                    content = " ".join([b.get("text", "") for b in content if isinstance(b, dict)])
                messages.append({"role": role, "content": str(content)})
                
            models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
            
            for model in models:
                try:
                    langfuse_client.update_current_span(
                        input=messages,
                        metadata={"model": model}
                    )
                    
                    chat_completion = groq_client.chat.completions.create(
                        messages=messages, model=model, temperature=0.0
                    )
                    llm_output = chat_completion.choices[0].message.content.strip()
                    
                    usage = None
                    if hasattr(chat_completion, 'usage') and chat_completion.usage:
                        usage = {
                            "prompt_tokens": chat_completion.usage.prompt_tokens,
                            "completion_tokens": chat_completion.usage.completion_tokens,
                            "total_tokens": chat_completion.usage.total_tokens
                        }
                    
                    langfuse_client.update_current_span(
                        output=llm_output,
                        metadata={"model": model, "usage": usage} if usage else {"model": model}
                    )
                    break
                except Exception as e:
                    langfuse_client.update_current_span(output=f"Error: {str(e)}")
                    continue
                    
            if not llm_output:
                return json.dumps({"error": "LLM unavailable"})
                
            if llm_output.startswith("```"):
                llm_output = llm_output.strip("`").replace("json", "", 1).strip()
                
            # 🛡️ ROBUST JSON EXTRACTION (Fixes "Extra data" errors)
            # Isolates only the first valid {...} block, ignoring trailing garbage like "}}
            json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
            if json_match:
                try:
                    parsed = json.loads(json_match.group(0))
                    target_url = parsed.get("link") or parsed.get("target_url")
                    if target_url:
                        return json.dumps({"target_url": target_url})
                except json.JSONDecodeError:
                    pass
                    
        except Exception as e:
            print(f"❌ [OWST Tool] Critical error: {str(e)}")
            
        # 🛡️ BULLETPROOF URL REGEX FALLBACK
        # Strictly stops at spaces, quotes, or braces to prevent swallowing trailing "}}
        match = re.search(r'(https?://[^\s\\"\'{}]+)', llm_output or "")
        if match:
            clean_url = match.group(1).rstrip('.,)')
            return json.dumps({"target_url": clean_url})
            
        return json.dumps({"error": f"Failed to find a valid URL. Raw output: {llm_output[:100]}"})

    return [universal_knowledge_search, filtered_knowledge_search, owst_live_search]