from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.authentication.CURD.auth import Auth
from src.core.database.session import get_session
from ..config import Settings
from datetime import datetime, timedelta
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

setting =Settings()
SECRET_KEY = setting.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    auth = Auth(db)
    user = await auth.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user

async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    result = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return result