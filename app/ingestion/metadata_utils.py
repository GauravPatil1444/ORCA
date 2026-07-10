from datetime import datetime, timezone

def create_metadata(source: str, category: str, configuration: dict) -> dict:
    """
    Generates the standardized metadata schema required for the 
    Stateful Single-Collection Agentic Architecture.
    """
    return {
        "source": source,
        "category": category,
        "configuration": configuration,
        "uploaded_at": datetime.now(timezone.utc).isoformat()
    }