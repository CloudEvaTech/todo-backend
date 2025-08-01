from pydantic import field_validator,BaseModel, EmailStr
from pydantic.types import StringConstraints
import re
from typing import Annotated


class PasswordValidationMixin:
    @field_validator("password")
    def validate_password(cls, v):
        return None if v is None else validate_password_strength(v)


def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")

    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")

    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")

    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError("Password must contain at least one special character")

    return password


class SignupRequest(PasswordValidationMixin, BaseModel):
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True, to_lower=True)]
    password: Annotated[str, StringConstraints(strip_whitespace=True, min_length=8)]
    username: str


    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doc@gmail.com",
                "username": "john_doe",
                "password": "Secret@123"
            }
        }
class SignRequest(PasswordValidationMixin, BaseModel):
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True, to_lower=True)]
    password: Annotated[str, StringConstraints(strip_whitespace=True, min_length=8)]

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doc@gmail.com",
                "password": "Secret@123"
            }
        }


class SignupResponse(BaseModel):
    message: str
    user_id: str
    email: str
    username: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "User created successfully",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "john.doc@example.com",
                "username": "john_doe"
            }
        }

class SignResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user_id: str
    email: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Login successful",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "john.doc@example.com"
            }
        }