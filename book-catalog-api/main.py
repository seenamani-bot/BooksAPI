import json
from fastapi import FastAPI,HTTPException
from pathlib import Path

from pydantic import BaseModel


app=FastAPI()

DATA_FILE=Path(__file__).parent /"data"/"books.json"

with open (DATA_FILE,"r") as f:
    books=json.load(f)
    
class Book(BaseModel):
    id:int
    title:str
    author:str
    genre:str
    year:int
    
    
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/books/{book_id}")
def list_books_id(book_id:int):
        for book in books:
            if book_id==book["id"]:
                return book
        raise HTTPException(status_code=404,detail="book not found")
    
@app.get("/books")
def list_books(author: str | None = None):
    if author is None:
        return books
    results = [book for book in books if author.casefold() in book["author"].casefold()]
    if not results:
        raise HTTPException(status_code=404, detail="books not found")
    return results
    