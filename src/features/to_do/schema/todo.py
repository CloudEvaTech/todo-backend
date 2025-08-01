from typing import Optional

from pydantic import BaseModel


class StatusCreate(BaseModel):
    completed: bool = False
    task_id: str

    class Config:
        orm_mode = True


class ToDoCreate(BaseModel):
    title: str
    description: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Build AI model",
                "description": "Develop a machine learning model for predicting stock prices",
            }
        }


class StatusResponseSchema(BaseModel):
    id: str
    completed: bool
    task_id: str

    class Config:
        orm_mode = True


class ToDoResponseSchema(BaseModel):
    id: str
    title: str
    description: Optional[str]
    user_id: str
    status: Optional[StatusResponseSchema]

    class Config:
        orm_mode = True


class DeleteResponseSchema(BaseModel):
    message: str

    class Config:
        orm_mode = True
        json_schema_extra = {"example": {"message": "Task deleted successfully"}}
