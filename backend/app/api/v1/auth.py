# Authentication routes: login, register, refresh_token
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.auth_service import AuthService
from app.core.exceptions import InvalidCredentialsException, UserNotFoundException
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse
)

router = APIRouter()
@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        user = AuthService.register_user(
            db=db,
            username=request.username,
            email=request.email,
            password=request.password
        )
        
        # Generate tokens
        access_token = AuthService.create_access_token(
            data={"sub": user.username, "user_id": user.id}
        )
        refresh_token = AuthService.create_refresh_token(
            data={"sub": user.username, "user_id": user.id}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login with username and password"""
    try:
        user = AuthService.authenticate_user(
            db=db,
            username=request.username,
            password=request.password
        )
        
        # Generate tokens
        access_token = AuthService.create_access_token(
            data={"sub": user.username, "user_id": user.id}
        )
        refresh_token = AuthService.create_refresh_token(
            data={"sub": user.username, "user_id": user.id}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    try:
        payload = AuthService.verify_refresh_token(request.refresh_token)
        user_id: int = payload.get("user_id")
        username: str = payload.get("sub")
        
        if user_id is None:
            raise InvalidCredentialsException("Invalid refresh token")
        
        # Verify user still exists
        user = AuthService.get_user_by_id(db=db, user_id=user_id)
        
        # Generate new access token
        access_token = AuthService.create_access_token(
            data={"sub": username, "user_id": user_id}
        )
        
        # Generate new refresh token
        new_refresh_token = AuthService.create_refresh_token(
            data={"sub": username, "user_id": user_id}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token
        )
    except (InvalidCredentialsException, UserNotFoundException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user info"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        created_at=current_user.created_at.isoformat()
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout (client-side token deletion)"""
    return {"message": "Successfully logged out"}
