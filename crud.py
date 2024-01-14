from sqlalchemy.orm import Session
import models
import schemas


def create_todo(db: Session, todo: schemas.ToDo):
    db_todo = models.ToDo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo(db: Session, todo_id: int):
    return db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ToDo).offset(skip).limit(limit).all()


def update_todo(db: Session, todo: schemas.ToDoUUID):
    found_todo = db.query(models.ToDo).filter(models.ToDo.id == todo.id).first()
    found_todo.name = todo.name
    found_todo.notes = todo.notes
    found_todo.status = todo.status
    db.commit()
    return found_todo
