from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.session import get_session
from src.core.utils.dependencies import create_access_token
from src.core.utils.exceptions import CustomException

from ..CURD.auth import Auth
from ..schema.auth import (SignRequest, SignResponse, SignupRequest,
                           SignupResponse)

router = APIRouter()


@router.post("/signup/", response_model=SignupResponse)
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_session)):
    auth = Auth(db)
    user = await auth.get_user_by_email(email=data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await auth.create_user(data)
    return {
        "message": "User created successfully",
        "user_id": str(new_user.id),
        "email": new_user.email,
        "username": new_user.username,
    }


@router.post("/login", response_model=SignResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    auth = Auth(db)
    user = await auth.get_user_by_email(email=form_data.username)
    if not user or user.check_password(form_data.password) is False:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token = await create_access_token(data={"sub": str(user.id)})
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
        "email": user.email,
        "username": user.username,
    }


