# app/core/langfuse_client.py
import os
from pathlib import Path
from dotenv import load_dotenv
from langfuse import Langfuse, get_client
from langfuse.langchain import CallbackHandler

# 1. Force dotenv to find the .env file at the project root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# 2. Add a failsafe check to catch this immediately during startup
if not os.getenv("LANGFUSE_PUBLIC_KEY"):
    raise ValueError("🚨 LANGFUSE_PUBLIC_KEY is missing! Check your .env file path.")

# 3. Initialize the global Langfuse client explicitly
Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL") 
)

langfuse = get_client()
langfuse_handler = CallbackHandler()

def get_system_prompt(workspace_type: str = "default", scope_filters=None, attached_domain="") -> str:
    """
    Fetches the latest compiled system prompt from the Langfuse Prompt Registry.
    The Langfuse SDK automatically handles local caching.
    """
    try:
        prompt = langfuse.get_prompt(workspace_type)
        return prompt.compile(
            workspace=workspace_type, 
            scope_filters=scope_filters or [], 
            domain=attached_domain
        )
    except Exception as e:
        print(f"[Langfuse] Fetch failed for workspace '{workspace_type}': {e}. Using fallback prompt.")
        return "You are ORCA, an advanced virtual assistant. Use your tools to find accurate information before answering."