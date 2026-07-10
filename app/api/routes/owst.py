# app/api/routes/owst.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from app.services.owst_scraper import fetch_and_clean_html

router = APIRouter()

@router.get("/owst", response_class=HTMLResponse)
async def owst_iframe(link: str, classes_to_remove: str = ""):
    try:
        classes_list = classes_to_remove.split(',') if classes_to_remove else []
        cleaned_html = fetch_and_clean_html(link, classes_list)
        return HTMLResponse(content=cleaned_html, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to render OWST page: {str(e)}")