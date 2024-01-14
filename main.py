import uvicorn
from fastapi import FastAPI, Depends
from schemas import ToDo, ToDoUUID
import crud
import models
import schemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

origins = ["*"]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/todos", response_model=list[ToDoUUID])
async def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos


"""add not found exception"""


@app.get("/todos/{todo_id}", response_model=ToDoUUID)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    return db_todo


@app.post("/todos", response_model=ToDoUUID)
async def create_todo(todo: ToDo, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)


@app.delete("/todos/{todo_id}", response_model=ToDoUUID)
async def delete_todo(todo_id: str):
    pass


@app.put("/todos/{todo_id}", response_model=ToDoUUID)
async def update_todos(todo_id: str, todo: ToDo, db: Session = Depends(get_db)):
    updated_todo = schemas.ToDoUUID(name=todo.name, notes=todo.notes, status=todo.status, id=todo_id)
    return crud.update_todo(db=db, todo=updated_todo)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
