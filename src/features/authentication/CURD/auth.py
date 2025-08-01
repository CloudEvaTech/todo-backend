from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.utils.exceptions import CustomException

from ..models.user import User


class Auth:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: str):
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, data):
        try:
            user = User(
                email=data.email, username=data.username, password=data.password
            )
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise CustomException(f"Error creating user: {str(e)}", status_code=500)
