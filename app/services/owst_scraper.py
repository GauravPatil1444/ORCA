# app/services/owst_scraper.py
import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

def fetch_and_clean_html(url: str, classes_to_remove: list[str]) -> str:
    """
    Fetches a target URL, parses the HTML, and removes specified DOM elements 
    (like navbars, footers, sidebars) based on CSS classes to create a clean 
    sandbox view for the frontend iframe.
    """
    try:
        # Fetch the raw HTML with a strict timeout
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch the page: {str(e)}")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Apply class exclusions (Spec 2.2 / 4.5)
    if classes_to_remove:
        for class_name in classes_to_remove:
            # Find all tags matching the class and decompose (remove) them from the DOM tree
            for tag in soup.find_all(class_=class_name):
                tag.decompose()
                
    # Return the cleaned HTML string
    return str(soup)