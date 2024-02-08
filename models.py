##models.py

from sqlalchemy import Boolean, DateTime, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base
from datetime import datetime


class Todo(Base):
    __tablename__ = "todos"

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    deadline = Column(DateTime, default=datetime.utcnow)
    memo = Column(String)

    steps = relationship("Step", back_populates="todo")


class Step(Base):
    __tablename__ = "steps"

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    todo_id = Column(Integer, ForeignKey("todos.id"))

    todo = relationship("Todo", back_populates="steps")