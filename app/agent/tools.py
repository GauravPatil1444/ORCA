# app/agent/tools.py
import json
import re
from typing import Optional, List
from langchain_core.tools import tool
from astrapy import Collection
from groq import Groq
from app.core.config import get_settings
from app.core.langfuse_client import langfuse # Adjust import if yours is app.core.langfuse

settings = get_settings()
groq_client = Groq(api_key=settings.GROQ_API_KEY)

def create_agent_tools(user_collection: Collection):
    
    @tool
    def universal_knowledge_search(query: str) -> str:
        """Performs a semantic similarity sweep across the user's entire knowledge collection."""
        vector_match = user_collection.find(
            sort={"$vectorize": query}, limit=5, projection={"data": True, "metadata": True}
        )
        results = [f"Source: {doc.get('metadata', {}).get('source', 'Unknown')}\nContent: {doc['data']}" for doc in vector_match]
        return "\n\n".join(results) if results else "No relevant information found in the knowledge base."

    @tool
    def filtered_knowledge_search(query: str, sources: Optional[List[str]] = None, categories: Optional[List[str]] = None) -> str:
        """Performs a scoped semantic search limited to specific file sources or ingestion categories."""
        filter_dict = {}
        if sources: filter_dict["metadata.source"] = {"$in": sources}
        if categories: filter_dict["metadata.category"] = {"$in": categories}
            
        vector_match = user_collection.find(
            sort={"$vectorize": query}, filter=filter_dict, limit=5, projection={"data": True, "metadata": True}
        )
        results = [f"Source: {doc.get('metadata', {}).get('source', 'Unknown')}\nContent: {doc['data']}" for doc in vector_match]
        return "\n\n".join(results) if results else "No relevant information found matching the specified filters."

    @tool
    def owst_live_search(query: str, base_domain: Optional[str] = None) -> str:
        """
        Searches the live web to find the most relevant deep-link URL for a given query.
        Use this when the user asks for current events, live web pages, or specific documentation 
        that is not available in the local knowledge base.
        """
        try:
            owst_prompt = langfuse.get_prompt("owst_router")
            search_context = f"{base_domain or 'the web'} {query}"
            compiled_prompt = owst_prompt.compile(query=search_context)
            
            messages = []
            for msg in compiled_prompt:
                role = str(msg.get("role", "user") if isinstance(msg, dict) else getattr(msg, "role", "user")).lower()
                content = msg.get("content", "") if isinstance(msg, dict) else getattr(msg, "content", "")
                if isinstance(content, list):
                    content = " ".join([b.get("text", "") for b in content if isinstance(b, dict)])
                messages.append({"role": role, "content": str(content)})
                
            models = ["groq/compound", "groq/compound-mini", "llama-3.1-8b-instant"]
            llm_output = ""
            for model in models:
                try:
                    chat_completion = groq_client.chat.completions.create(
                        messages=messages, model=model, temperature=0.0
                    )
                    llm_output = chat_completion.choices[0].message.content.strip()
                    break
                except Exception:
                    continue
                    
            if not llm_output:
                return json.dumps({"error": "LLM unavailable"})
                
            if llm_output.startswith("```"):
                llm_output = llm_output.strip("`").replace("json", "", 1).strip()
                
            parsed = json.loads(llm_output)
            target_url = parsed.get("link") or parsed.get("target_url")
            if target_url:
                return json.dumps({"target_url": target_url})
        except Exception:
            pass
            
        # Fallback regex if JSON parsing fails
        match = re.search(r'(https?://\S+)', llm_output or "")
        if match:
            return json.dumps({"target_url": match.group(1).rstrip('.,)"\'')})
            
        return json.dumps({"error": "Failed to find a valid URL."})

    return [universal_knowledge_search, filtered_knowledge_search, owst_live_search]