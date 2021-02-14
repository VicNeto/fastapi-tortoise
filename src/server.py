from typing import List, Optional

from fastapi import FastAPI, HTTPException, Header
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from models import Author_Pydantic, AuthorIn_Pydantic, Author, Book, Book_Pydantic, BookIn_Pydantic
from pydantic import BaseModel
from .db import TORTOISE_ORM


app = FastAPI(title="Tortoise ORM")

register_tortoise(
    app,
    generate_schemas=True,
    config=TORTOISE_ORM,
    modules={"models": ["models"]},
    add_exception_handlers=True,
)

class Status(BaseModel):
    message: str

class DataResponse(BaseModel):
    data: list = []

@app.get('/ping')
async def pong():
    return "Pong"


@app.get("/authors", response_model=List[Author_Pydantic])
async def get_authors():
    # print(Book_Pydantic.schema_json(indent=4))
    # print(Author_Pydantic.schema_json(indent=4))
    return await Author_Pydantic.from_queryset(Author.all())

@app.post("/authors", response_model=Author_Pydantic)
async def create_author(author: AuthorIn_Pydantic):
    author_obj = await Author.create(**author.dict(exclude_unset=True))
    return await Author_Pydantic.from_tortoise_orm(author_obj)

@app.get("/books", response_model=List[Book_Pydantic])
async def get_books():
    return await Book_Pydantic.from_queryset(Book.all())

@app.post("/books", response_model=Book_Pydantic)
async def create_book(book: BookIn_Pydantic, user: Optional[str] = Header(None)):
    author = await Author.get(id=book.author_id)
    book_obj = await Book.create(**book.dict(exclude_unset=True), author=author)
    return await Book_Pydantic.from_tortoise_orm(book_obj)


@app.get(
    "/authors/{author_id}", response_model=Author_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_author(author_id: int):
    return await Author_Pydantic.from_queryset_single(Author.get(id=author_id))

@app.get(
    "/authors/{author_id}/books", response_model=List[Book_Pydantic], responses={404: {"model": HTTPNotFoundError}}
)
async def get_author_books(author_id: int):
    return await Book_Pydantic.from_queryset(Book.filter(author_id=author_id))


@app.put(
    "/authors/{author_id}", response_model=Author_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_author(author_id: int, author: AuthorIn_Pydantic):
    await Author.filter(id=author_id).update(**author.dict(exclude_unset=True))
    return await Author_Pydantic.from_queryset_single(Author.get(id=author_id))


@app.delete("/authors/{author_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_author(author_id: int):
    deleted_count = await Author.filter(id=author_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Author {author_id} not found")
    return Status(message=f"Deleted Author {author_id}")
