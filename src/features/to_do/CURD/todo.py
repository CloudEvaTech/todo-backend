from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.core.utils.exceptions import CustomException

from ..models.tasks import Status, ToDoItem


class ToDO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, data, current_user):
        try:
            task = ToDoItem(
                title=data.title, description=data.description, user_id=current_user.id
            )
            self.db.add(task)
            await self.db.flush()

            status = Status(completed=False, task_id=task.id)
            self.db.add(status)
            await self.db.commit()
            await self.db.refresh(task)
            return task
        except Exception as e:
            await self.db.rollback()
            raise CustomException(f"Error creating task: {str(e)}", status_code=500)

    async def get_task(self, title: str):
        result = await self.db.execute(select(ToDoItem).where(ToDoItem.title == title))
        return result.scalar_one_or_none()

    async def get_task_by_id(self, task_id: str):
        result = await self.db.execute(select(ToDoItem).where(ToDoItem.id == task_id))
        return result.scalar_one_or_none()

    async def get_tasks_by_user(self, user_id: str):
        result = await self.db.execute(
            select(ToDoItem)
            .options(selectinload(ToDoItem.status))
            .where(ToDoItem.user_id == user_id)
        )
        return result.scalars().all()

    async def get_all_tasks(self):
        result = await self.db.execute(
            select(ToDoItem).options(selectinload(ToDoItem.status))
        )
        return result.scalars().all()

    async def delete_task(self, task_id: str):
        task = await self.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        status_result = await self.db.execute(
            select(Status).where(Status.task_id == task_id)
        )
        status = status_result.scalar_one_or_none()
        if status:
            await self.db.delete(status)
        await self.db.delete(task)
        await self.db.commit()
        return True

    async def update_task_with_status(self, task_id: str, data):
        task = await self.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if hasattr(data, "title") and data.title is not None:
            task.title = data.title
        if hasattr(data, "description"):
            task.description = data.description

        if hasattr(data, "completed"):
            status_result = await self.db.execute(
                select(Status).where(Status.task_id == task_id)
            )
            status = status_result.scalar_one_or_none()
            if status:
                status.completed = data.completed

        await self.db.commit()
        await self.db.refresh(task)
        return task
