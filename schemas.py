from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class ToDo(BaseModel):
    name: str
    notes: str | None = None
    status: str = "pending"


class ToDoUUID(ToDo):
    id: int

    class Config:
        orm_mode = True


class ToDoCreate(ToDo):
    pass

