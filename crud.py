##crud.py

from sqlalchemy.orm import Session
from sqlalchemy import desc

from models import Todo, Step
from schemas import TodoCreate, StepCreate

def create_todo(db: Session, todo: TodoCreate):
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).order_by(desc(Todo.created_at)).offset(skip).limit(limit).all()

def create_todo_step(db: Session, step: StepCreate, todo_id: int):
    db_step = Step(**step.model_dump(), todo_id=todo_id)
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step

def get_todo_steps(db: Session, todo_id: int):
    return db.query(Step).filter(Step.todo_id == todo_id).all()

def search_todos_by_title(db: Session, title: str):
    return db.query(Todo).filter(Todo.title.ilike(f"%{title}%")).all()
