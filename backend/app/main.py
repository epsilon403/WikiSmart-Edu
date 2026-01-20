"""
FastAPI main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, users, articles, quiz, content, admin
from app.middleware.error_handler import add_exception_handlers
from app.middleware.logging import add_logging_middleware
from app.database import engine
from app.models import user, article, quiz_attempt

# Create database tables
user.Base.metadata.create_all(bind=engine)
article.Base.metadata.create_all(bind=engine)
quiz_attempt.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="WikiSmart-Edu: Educational Content Generation Platform"
)

# Configure CORS - Must be added before other middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    expose_headers=["*"],
    max_age=3600,
    allow_methods=["*"],
   
 
    allow_headers=["*"],
)

# Add custom middleware
add_exception_handlers(app)
add_logging_middleware(app)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(articles.router, prefix="/api/v1/articles", tags=["Articles"])
app.include_router(quiz.router, prefix="/api/v1/quiz", tags=["Quiz"])
app.include_router(content.router, prefix="/api/v1/content", tags=["Content"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to WikiSmart-Edu API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
