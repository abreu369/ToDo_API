from typing import List
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_db
from models import Todo
from schemas import TodoSchema
from database import Session

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")
tasks: List[str] = []


@app.get("/todos")
def get_todos(db: Session = Depends(get_db)): 
    todos = db.query(Todo).all()
    return JSONResponse(content=[todo.to_dict() for todo in todos], media_type="application/json")

@app.post("/todos")
def create_todo(data: dict, db: Session = Depends(get_db)):
    # Extraindo o título do objeto JSON recebido
    title = data.get("title")
    if not title:
        return JSONResponse(content={"error": "Title is required"}, status_code=400)
    
    # Criando o novo Todo
    new_todo = Todo(title=title)
    
    # Adicionando ao banco de dados
    db.add(new_todo)
    db.commit()
    todos = db.query(Todo).all()
    return templates.TemplateResponse("index.html", {"request": request, "todo": todos})


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


@app.get("/", response_class=HTMLResponse)
async def main(request: Request, db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return templates.TemplateResponse("index.html", {"request": request, "todo": todos})
