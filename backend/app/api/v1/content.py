# Content routes: summarize, translate, export_pdf, export_txt
from fastapi import APIRouter

router = APIRouter()

@router.post("/summarize")
async def summarize():
    """Summarize content"""
    return {"message": "Summarize endpoint"}

@router.post("/translate")
async def translate():
    """Translate content"""
    return {"message": "Translate endpoint"}
