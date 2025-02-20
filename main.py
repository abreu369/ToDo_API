from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_db
from models import Todo
from schemas import TodoSchema
from database import Session

app = FastAPI()

@app.get("/todos")
def get_todos(db: Session = Depends(get_db)): # type: ignore
    todos = db.query(Todo).all()
    return JSONResponse(content=[todo.to_dict() for todo in todos], media_type="application/json")

@app.post("/todos")
def create_todo(todo: TodoSchema, db: Session = Depends(get_db)): # type: ignore
    new_todo = Todo(title=todo.title, description=todo.description)
    db.add(new_todo)
    db.commit()
    return JSONResponse(content=new_todo.to_dict(), media_type="application/json")

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)): # type: ignore
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return JSONResponse(content=todo.to_dict(), media_type="application/json")

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoSchema, db: Session = Depends(get_db)): # type: ignore
    existing_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    existing_todo.title = todo.title
    existing_todo.description = todo.description
    db.commit()
    return JSONResponse(content=existing_todo.to_dict(), media_type="application/json")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)): # type: ignore
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return JSONResponse(content={"message": "Todo deleted"}, media_type="application/json")
