from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Form
import datahandler

app = FastAPI()

response = datahandler.response
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/read-list/{subject}/{classroom}/{id}")
async def update_item(subject: str, classroom: str, id: str):
     return datahandler.read(subject, classroom, id)

@app.post("/api/add-list/{subject}/{classroom}/{id}")
async def update_item(subject: str, classroom: str, id: str, lone: str = Form(default=None), ltwo: str = Form(default=None)):
    datahandler.save(subject, classroom, id, lone, ltwo)
    print(response, "lol")
    print(datahandler.response, "Hallo")
    return {datahandler.response}
