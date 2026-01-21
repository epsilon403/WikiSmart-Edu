# Content routes: summarize, translate, export_pdf, export_txt
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.llm_service import LLMService
from app.api.deps import get_current_user

router = APIRouter()

class TranslationRequest(BaseModel):
    text: str
    target_language: str

class TranslationResponse(BaseModel):
    translated_text: str
    target_language: str

@router.post("/summarize")
async def summarize():
    """Summarize content"""
    return {"message": "Summarize endpoint"}

@router.post("/translate", response_model=TranslationResponse)
async def translate(
    request: TranslationRequest,
    current_user = Depends(get_current_user)
):
    """Translate content using Gemini AI"""
    try:
        llm_service = LLMService()
        translated_text = llm_service.get_translation(
            text=request.text,
            target_language=request.target_language
        )
        
        return TranslationResponse(
            translated_text=translated_text,
            target_language=request.target_language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
