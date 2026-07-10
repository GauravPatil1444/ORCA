# app/agent/tools.py
import json
import requests
from typing import Optional, List
from langchain_core.tools import tool
from astrapy import Collection
from groq import Groq
from app.core.config import get_settings

settings = get_settings()
groq_client = Groq(api_key=settings.GROQ_API_KEY)

def create_agent_tools(user_collection: Collection):
    """Factory function to bind the specific user's collection to the agent tools."""
    
    @tool
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
    def filtered_knowledge_search(query: str, sources: Optional[List[str]] = None, categories: Optional[List[str]] = None) -> str:
        """Performs a scoped semantic search limited to specific file sources or ingestion categories."""
        filter_dict = {}
        if sources:
            filter_dict["metadata.source"] = {"$in": sources}
        if categories:
            filter_dict["metadata.category"] = {"$in": categories}
            
        vector_match = user_collection.find(
            sort={"$vectorize": query},
            filter=filter_dict,
            limit=5,
            projection={"data": True, "metadata": True}
        )
        results = [f"Source: {doc.get('metadata', {}).get('source', 'Unknown')}\nContent: {doc['data']}" for doc in vector_match]
        return "\n\n".join(results) if results else "No relevant information found matching the specified filters."

    @tool
    def owst_live_search(query: str) -> str:
        """Acts as an automated navigation router across live web resources. Returns a JSON payload with a target URL and CSS classes to remove."""
        params = {'q': query, 'key': settings.GOOGLE_SEARCH_KEY, 'cx': settings.GOOGLE_SEARCH_CX, 'num': 10}
        response = requests.get(settings.GOOGLE_SEARCH_URL, params=params)
        results = response.json()
        links = [item["link"] for item in results.get("items", [])]
        
        if not links:
            return json.dumps({"error": "No live web results found."})

        message = [
            {
                "role": "user",
                "content": f"""Based on the provided query, select the most suitable link from the results. 
                Only output the exact URL string, nothing else.
                "results": {links}
                "query": {query}""",
            }
        ]
        chat_completion = groq_client.chat.completions.create(
            messages=message,
            model="llama-3.1-8b-instant",
        )
        target_url = chat_completion.choices[0].message.content.strip()
        
        payload = {
            "target_url": target_url,
            "classes_to_remove": [
                "header-middle p-0 bg-heder xs-text-center",
                "inner-header bg-black-222",
                "widget no-border m-0",
                "header-nav",
                "side-bar",
                "navbar",
                "footer"
            ]
        }
        return json.dumps(payload)

    return [universal_knowledge_search, filtered_knowledge_search, owst_live_search]