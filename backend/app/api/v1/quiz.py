# Quiz routes: generate_quiz, submit_quiz, get_quiz_results
from fastapi import APIRouter

router = APIRouter()

@router.post("/generate")
async def generate_quiz():
    """Generate quiz"""
    return {"message": "Generate quiz endpoint"}

@router.post("/submit")
async def submit_quiz():
    """Submit quiz"""
    return {"message": "Submit quiz endpoint"}
