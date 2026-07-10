# langfuse_client.py
from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Langfuse client using environment variables
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

def get_system_prompt(workspace_type: str = "default") -> str:
    """
    Fetches the latest compiled system prompt from the Langfuse Prompt Registry.
    The Langfuse SDK automatically handles local caching to prevent API rate limits.
    """
    try:
        # Fetches the prompt named 'default' (or 'legal', 'medical', etc.) from Langfuse
        prompt = langfuse.get_prompt(workspace_type)
        return prompt.prompt
    except Exception as e:
        # Fallback in case the registry is unreachable or the prompt name doesn't exist yet
        print(f"[Langfuse] Fetch failed for workspace '{workspace_type}': {e}. Using fallback prompt.")
        return "You are ORCA, an advanced virtual assistant. Use your tools to find accurate information before answering."