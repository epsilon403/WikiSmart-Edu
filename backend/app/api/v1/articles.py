from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Optional, List
from pydantic import BaseModel
import tempfile
import os

# App Imports
from app.api.deps import get_db, get_current_user
from app.services.pdf_service import extract_text_from_pdf
from app.services.content_extractor import get_wikipedia_content
from app.services.llm_service import LLMService
from app.schemas.article import WikiRequest
from app.models.user import User
from app.models.article import Article, ActionType

router = APIRouter()
llm_service = LLMService()

# --- Schemas ---
class TranslationRequest(BaseModel):
    text: str
    target_language: str

# --- Routes ---

@router.post("/extract-pdf")
async def extract_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        # Save and Read Temp File
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        # Process
        extraction_result = await extract_text_from_pdf(temp_path, clean_up=True)
        
        # Save to DB
        new_article = Article(
            user_id=current_user.id,
            url=f"pdf://{file.filename}",
            title=file.filename,
            action=ActionType.SUMMARY
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)

        return {
            "status": "success",
            "article_id": new_article.id,
            "data": extraction_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF Processing failed: {str(e)}")


@router.post("/extract-wiki")
async def extract_wikipedia(
    request: WikiRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    try:
        # 1. Extract
        wiki_content = get_wikipedia_content(str(request.url))
        
        # 2. Generate Summaries (Fail silently if AI fails to keep app running)
        try:
            content_snippet = wiki_content["content"][:8000]
            wiki_content["ai_summary_short"] = llm_service.generate_summary(content_snippet, "short")
            wiki_content["ai_summary_medium"] = llm_service.generate_summary(content_snippet, "medium")
        except Exception as e:
            print(f"AI Summary warning: {e}")

        # 3. Save to DB
        new_article = Article(
            user_id=current_user.id,
            url=str(request.url),
            title=wiki_content.get("title", "Unknown Title"),
            action=ActionType.SUMMARY
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)

        return {
            "status": "success",
            "article_id": new_article.id,
            "data": wiki_content
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Wiki extraction failed: {str(e)}")


@router.post("/translate")
async def translate_text(
    request: TranslationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Translates provided text into the target language using Gemini.
    """
    try:
        # 1. Call the LLM Service
        translated_text = llm_service.get_translation(
            text=request.text, 
            target_language=request.target_language
        )

        # 2. Save the Translation Action to DB
        # (Assuming you might want to save translations as articles/records too)
        new_article = Article(
            user_id=current_user.id,
            url="text://translation",
            title=f"Translation to {request.target_language}",
            action=ActionType.TRANSLATION # Ensure this exists in your Enum or use a string
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)

        return {
            "status": "success",
            "original_text": request.text,
            "translated_text": translated_text,
            "article_id": new_article.id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.get("/")
async def get_articles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    action: Optional[str] = None
):
    query = db.query(Article).filter(Article.user_id == current_user.id)
    
    if action:
        query = query.filter(Article.action == action)
    
    articles = query.order_by(Article.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": query.count(),
        "articles": articles
    }

@router.get("/{article_id}")
async def get_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    article = db.query(Article).filter(
        Article.id == article_id, 
        Article.user_id == current_user.id
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return {"article": article}