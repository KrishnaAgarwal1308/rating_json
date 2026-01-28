from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import json
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    # id:int
    name:str
    author:str
    rating:float
    no_rating:int = 0
FILE_PATH = "data.json"


def read_books():
    try:
        with open(FILE_PATH,"r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data


def write_book(books):
    try:
        with open(FILE_PATH, "w") as f:
            json.dump(books,f,indent=4)
    except FileNotFoundError:
        pass

def book_key(author:str, name:str):
    return f"{author.strip().lower()}::{name.strip().lower()}"

# print(type(data))

@app.get("/")
async def root():
    return {"message":"hello world"}
        
@app.post("/create")
def create(book:Book):
    books = read_books()
    key = book_key(book.author, book.name)

    if key in books:
        raise HTTPException(status_code=400, detail="book already exists")
    books[key] = {
        "name": book.name,
        "author": book.author,
        "rating": book.rating,
        "no_rating": 1,

    }
    write_book(books)
    return{"message":"book added successfully"}

@app.post("/update")
def update(book:Book):
    books = read_books()
    key = book_key(book.author, book.name)
    if key not in books:
        raise HTTPException (400, detail="book not found")
    b = books[key]
    total_rating = b["rating"]*b["no_rating"]
    b["no_rating"] += 1
    b["rating"] = (total_rating + book.rating)/b["no_rating"]

    write_book(books)
    return{"message":"book updated"}

@app.get("/get_all_books")
def get_all_books():
    return list(read_books().values())


@app.get("/get_book")
def get_book(author:str, name:str):
    key = book_key(author, name)
    books = read_books()
    if key not in books:
        raise HTTPException(404, "book not found")
    return books[key]

# Serve static files (must be last)
app.mount("/", StaticFiles(directory=".", check_dir=True), name="static")

