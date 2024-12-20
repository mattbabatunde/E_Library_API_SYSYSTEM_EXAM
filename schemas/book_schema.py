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
            title: str | None = None
            author: str
            is_available: Optional[bool] = True


books: dict[str, Book] = {}