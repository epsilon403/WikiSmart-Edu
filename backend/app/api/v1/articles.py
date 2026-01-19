# Article routes: process_article, get_articles, get_article_by_id
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Optional
import os
import tempfile
from app.api.deps import get_db, get_current_user
from app.services.pdf_service import extract_text_from_pdf
from app.services.content_extractor import get_wikipedia_content
from app.services.llm_service import LLMService
from app.schemas.article import WikiRequest
from app.models.user import User
from app.models.article import Article, ActionType

router = APIRouter()

# Initialize LLM Service
llm_service = LLMService()

@router.post("/extract-pdf")
async def extract_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Extract text content from uploaded PDF file
    
    Args:
        file: PDF file uploaded by user
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Extracted text content with metadata
    """

    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
   
    temp_file = None
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Extract text from PDF
        extraction_result = await extract_text_from_pdf(temp_file_path, clean_up=True)
        
        # Save article to database
        new_article = Article(
            user_id=current_user.id,
            url=f"pdf://{file.filename}",
            title=file.filename,
            action=ActionType.SUMMARY  # Default action for PDF extraction
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        
        return {
            "status": "success",
            "message": "PDF extracted successfully",
            "article_id": new_article.id,
            "data": extraction_result
        }
    
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing PDF: {str(e)}"
        )

@router.post("/extract-wiki")
async def extract_wikipedia(
    request: WikiRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Extract content from Wikipedia URL and generate AI summary
    
    Args:
        request: Wikipedia URL
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Wikipedia article content with AI-generated summaries
    """
    try:
        # Extract content from Wikipedia
        wiki_content = get_wikipedia_content(str(request.url))
        
        # Generate AI summaries using Groq
        try:
            # Generate short summary (bullet points)
            short_summary = llm_service.generate_summary(
                wiki_content["content"][:8000],  # Limit content length
                summary_type="short"
            )
            
            # Generate medium summary (paragraphs)
            medium_summary = llm_service.generate_summary(
                wiki_content["content"][:8000],
                summary_type="medium"
            )
            
            wiki_content["ai_summary_short"] = short_summary
            wiki_content["ai_summary_medium"] = medium_summary
        except Exception as e:
            print(f"Warning: Could not generate AI summary: {str(e)}")
            wiki_content["ai_summary_short"] = None
            wiki_content["ai_summary_medium"] = None
        
        # Save article to database
        new_article = Article(
            user_id=current_user.id,
            url=str(request.url),
            title=wiki_content["title"],
            action=ActionType.SUMMARY
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        
        return {
            "status": "success",
            "message": "Wikipedia content extracted successfully",
            "article_id": new_article.id,
            "data": wiki_content
        }
    
    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Wikipedia URL: {str(e)}"
        )
    except Exception as e:
 
        import traceback
        print(f"Error extracting Wikipedia content: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting Wikipedia content: {str(e)}"
        )


@router.get("/")
async def get_articles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    action: Optional[str] = None
):
    """
    Get all articles for current user with optional filtering
    
    Args:
        current_user: Authenticated user
        db: Database session
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        action: Filter by action type (summary, translation, quiz)
    
    Returns:
        List of articles with metadata
    """
    query = db.query(Article).filter(Article.user_id == current_user.id)
    
    # Filter by action type if provided
    if action:
        query = query.filter(Article.action == action)
    
    # Order by most recent first
    query = query.order_by(Article.created_at.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    articles = query.offset(skip).limit(limit).all()
    
    # Format response
    articles_data = [
        {
            "id": article.id,
            "title": article.title,
            "url": article.url,
            "action": article.action.value,
            "created_at": article.created_at.isoformat(),
        }
        for article in articles
    ]
    
    return {
        "articles": articles_data,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/{article_id}")
async def get_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get article by ID"""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.user_id == current_user.id
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    return {"article": article}
# Temp
