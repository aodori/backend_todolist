##schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    deadline: Optional[datetime] = None
    memo: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class StepBase(BaseModel):
    title: str

class StepCreate(StepBase):
    pass

class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True

class Step(StepBase):
    id: int
    todo_id: int

    class Config:
        orm_mode = True
