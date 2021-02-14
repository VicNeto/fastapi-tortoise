from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from .author import Author, Book

Tortoise.init_models(["models"], "models")

Book_Pydantic = pydantic_model_creator(Book, name="Book")
BookIn_Pydantic = pydantic_model_creator(Book, name="BookIn", exclude_readonly=True)

Author_Pydantic = pydantic_model_creator(Author, name="Author")
AuthorIn_Pydantic = pydantic_model_creator(Author, name="AuthorIn", exclude_readonly=True)
