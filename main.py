##main.py

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Form
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from typing import List
from models import Todo
from schemas import Todo

from database import SessionLocal, engine

from backend_todolist import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)

@app.get("/todos/", response_model=List[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

@app.get("/todos/{todo_id}/steps/", response_model=List[schemas.Step])
def read_todo_steps(todo_id: int, db: Session = Depends(get_db)):
    return crud.get_todo_steps(db=db, todo_id=todo_id)

@app.post("/todos/{todo_id}/steps/", response_model=schemas.Step)
def create_todo_step(todo_id: int, step: schemas.StepCreate, db: Session = Depends(get_db)):
    return crud.create_todo_step(db=db, todo_id=todo_id, step=step)

@app.get("/todos/search/", response_model=List[schemas.Todo])
def search_todos_by_title(title: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    todos = crud.search_todos_by_title(db, title=title)
    if not todos:
        raise HTTPException(status_code=404, detail="No matching todos found")
    return todos
