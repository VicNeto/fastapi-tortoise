from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
# from .book import Book

class Author(models.Model):

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    category = fields.CharField(max_length=30, default="misc")
    password_hash = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    active = fields.BooleanField(default=True)

    books: fields.ReverseRelation["Book"]

    def __str__(self):
        return self.username

    class PydanticMeta:
        exclude = ["password_hash"]

class Book(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50)
    isbn = fields.CharField(max_length=50)
    number_of_pages = fields.IntField()
    edition = fields.CharField(max_length=50, default="Axolotl Editions")
    
    author: fields.ForeignKeyRelation[Author] = fields.ForeignKeyField("models.Author", related_name='books')

    def __str__(self):
        return self.title


Book_Pydantic = pydantic_model_creator(Book, name="Book")
BookIn_Pydantic = pydantic_model_creator(Book, name="BookIn", exclude_readonly=True)

Author_Pydantic = pydantic_model_creator(Author, name="Author")
AuthorIn_Pydantic = pydantic_model_creator(Author, name="AuthorIn", exclude_readonly=True)
