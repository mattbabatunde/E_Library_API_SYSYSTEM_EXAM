from pydantic import BaseModel
from typing import Optional



class BookModel(BaseModel):
    title: str
    author: str
    is_available: Optional[bool] = True


class Book(BookModel):
    id: int  


class Create_Book(BookModel):
    title: str
    author: str
    is_available: bool = True


class Update_Book(BookModel):
    title: Optional[str] = None  # Allow partial updates for title
    author: Optional[str] = None  # Allow partial updates for author
    is_available: Optional[bool] = None  # Allow partial updates for availability


# In-memory storage for books, now using UUID as the key
books: dict[int, Book] = {}
