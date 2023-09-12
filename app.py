from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.responses import FileResponse 

app = FastAPI()
todo_list={}

templates = Jinja2Templates("static")

item_id = 0

def get_next_item_id():
    global item_id
    item_id +=1
    return item_id

class Item(BaseModel):
    name: str
    description: str


@app.post("/todo/")
def create_todo(request: Request, item:Item):
    todo_list[get_next_item_id()] = item
    print("******recieved*****")
    print (todo_list)
    return templates.TemplateResponse("todoList.html", context = {"request": request, "todo_list":todo_list})


@app.get("/todo/")
def return_all():
    return list(todo_list.values())

@app.get("/todo/edit/{todo_id}/")
def edit_todo_item(request: Request, todo_id:str):
    return templates.TemplateResponse("edit-row.html", context = {"request": request,"id":todo_id, "todo_item":todo_list[int(todo_id)]})

@app.put("/todo/edit/{todo_id}/")
async def save_edited_todo_item(request: Request, todo_id:str):
    body = await request.json()
    print(body)
    todo_list[int(todo_id)] = Item(**body)
    return templates.TemplateResponse("reload_row.html", context = {"request": request,"id":todo_id, "todo_item":todo_list[int(todo_id)]})


@app.get("/", response_class=HTMLResponse)
async def homepage():
    return FileResponse('static/homepage.html')
