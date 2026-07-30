# app/core/langfuse_client.py
import os
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

def get_langfuse_handler(session_id: str = None, user_id: str = None, tags: list = None):
    return CallbackHandler(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        session_id=session_id,
        user_id=user_id,
        tags=tags or []
    )

def get_system_prompt(workspace_type: str = "default", scope_filters=None, attached_domain=""):
    """
    Returns ONLY the compiled prompt string (backward compatible).
    """
    compiled, _ = get_system_prompt_with_object(workspace_type, scope_filters, attached_domain)
    return compiled

def get_system_prompt_with_object(workspace_type: str = "default", scope_filters=None, attached_domain=""):
    """
     NEW: Returns BOTH the compiled prompt string AND the raw Langfuse prompt object.
    The prompt object is needed to link the prompt version to the trace in Langfuse.
    """
    try:
        prompt_obj = langfuse.get_prompt(workspace_type)
        compiled = prompt_obj.compile(
            scope_filters=scope_filters,
            attached_domain=attached_domain
        )
        return compiled, prompt_obj
    except Exception as e:
        print(f"[Langfuse] Fetch failed for workspace '{workspace_type}': {e}. Using fallback.")
        fallback = "You are ORCA, an advanced virtual assistant. Use your tools to find accurate information."
        return fallback, None