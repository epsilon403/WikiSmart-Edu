# User routes: get_profile, update_profile, get_history
from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
async def get_profile():
    """Get current user profile"""
    return {"message": "Get profile endpoint"}

@router.get("/history")
async def get_history():
    """Get user history"""
    return {"message": "Get history endpoint"}
