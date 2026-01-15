# Admin routes: get_statistics, manage_users, delete_user
from fastapi import APIRouter

router = APIRouter()

@router.get("/statistics")
async def get_statistics():
    """Get statistics"""
    return {"message": "Get statistics endpoint"}

@router.get("/users")
async def get_users():
    """Get all users"""
    return {"message": "Get users endpoint"}
