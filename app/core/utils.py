# app/core/utils.py
import re

def sanitize_url(url: str) -> str:
    """
    Cleans LLM and user-provided URLs, ensuring they have a valid HTTP/HTTPS protocol.
    Strips markdown formatting, quotes, and brackets.
    """
    if not url:
        return url
    
    # Strip whitespace and common wrapping characters
    url = url.strip().strip('"').strip("'").strip("<").strip(">").strip("()")
    
    # Extract URL from markdown links like [text](https://...)
    markdown_match = re.search(r'\((https?://[^\s]+)\)', url)
    if markdown_match:
        url = markdown_match.group(1)

    # Inject https:// if the protocol is missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    return url