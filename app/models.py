from pydantic import BaseModel, Field

class Item(BaseModel):
    id: str
    text: str
    desc: str | None = None
    completed: bool = Field(default = False, validate_default=True)