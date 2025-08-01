from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.session import get_session
from ..schema.todo import ToDoResponseSchema, ToDoCreate, DeleteResponseSchema
from ..CURD.todo import ToDO
from src.core.utils.dependencies import get_current_user

router = APIRouter()

@router.post("/todo", response_model=ToDoResponseSchema)
async def create_todo_item(data: ToDoCreate, db: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    todo = ToDO(db=db)
    existing_task = await todo.get_task(title=data.title)
    if existing_task:
        raise HTTPException(status_code=400, detail="Task with this title already exists") 
    
    new_task = await todo.create_task(data=data, current_user=current_user)
    await db.refresh(new_task, attribute_names=["status"])
    return {
        "message": "Task created successfully",
        "id": str(new_task.id),
        "title": new_task.title,
        "description": new_task.description,
        "user_id": str(current_user.id),
        "status": {
            "id": str(new_task.status.id),
            "completed": new_task.status.completed,
            "task_id": str(new_task.status.task_id)
        } if new_task.status else None
    }

@router.delete("/todo/{task_id}", response_model=DeleteResponseSchema)
async def delete_todo_item(task_id: str, db: AsyncSession = Depends(get_session),current_user = Depends(get_current_user)):
    todo = ToDO(db=db)
    deleted = await todo.delete_task(task_id=task_id)
    if deleted:
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@router.get("/todo", response_model=list[ToDoResponseSchema])
async def get_todo_items(db: AsyncSession = Depends(get_session),current_user = Depends(get_current_user)):
    todo = ToDO(db=db)
    if current_user.id:
        tasks = await todo.get_tasks_by_user(user_id=current_user.id)
        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks found for this user")
        return tasks
    else:
        tasks = await todo.get_all_tasks()

@router.put("/todo/{task_id}", response_model=ToDoResponseSchema)
async def update_todo_item(
    task_id: str,
    data: ToDoCreate,
    db: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    todo = ToDO(db=db)
    updated_task = await todo.update_task_with_status(task_id, data)
    await db.refresh(updated_task, attribute_names=["status"])
    return updated_task