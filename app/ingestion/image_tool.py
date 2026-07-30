# image_tool.py
import os
import mimetypes
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from app.ingestion.metadata_utils import create_metadata

def create_robust_render_session():
    """
    Creates a requests Session configured to handle Render's free-tier 
    spin-up delays and transient SSL proxy drops (SSLEOFError).
    """
    session = requests.Session()
    
    # Exponential backoff: 10s, 20s, 40s, 80s... perfect for Render's 50s cold starts
    retry_strategy = Retry(
        total=5,  
        backoff_factor=10,  
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    return session

# Initialize globally to take advantage of connection pooling
render_session = create_robust_render_session()

def process_image(file_path):
    uploadDocs = []
    
    #  Safely guess the MIME type instead of hardcoding "image/png"
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "image/png"  # Fallback
        
    try:
        with open(file_path, "rb") as img_file:
            files = {"file": (os.path.basename(file_path), img_file, mime_type)}
            
            #  Use the robust session with a generous timeout for Render cold starts
            response = render_session.post(
                'https://ocr-1-0-0.onrender.com/ocr', 
                files=files,
                timeout=120 
            )
            response.raise_for_status()
            
        json_response = response.json()
        extracted_text = json_response.get("text", "")
        
        # Only process if we actually got text back
        if extracted_text and extracted_text.strip():
            source = os.path.basename(file_path)
            metadata = create_metadata(source, "image", {})
            
            uploadDocs.append({
                "data": extracted_text,
                "$vectorize": extracted_text,
                "metadata": metadata
            })
            
    except requests.exceptions.RequestException as e:
        print(f" [Image Tool] OCR request failed for {file_path}: {e}")
    except ValueError as e:
        print(f" [Image Tool] Failed to parse OCR JSON response for {file_path}: {e}")
    except Exception as e:
        print(f" [Image Tool] Unexpected error processing {file_path}: {e}")
        
    return uploadDocs