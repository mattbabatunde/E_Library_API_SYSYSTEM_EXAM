from pydantic import BaseModel
from datetime import datetime
from schemas.book_schema import books  
from memory_db.books_db import *
from uuid import UUID


class BorrowModel(BaseModel):
    id: UUID
    user_id: int
    book_id: int 
    borrow_date: datetime = datetime.now() 
    return_date: datetime = None 

class BorrowRecord(BorrowModel):
    id: UUID


borrow_records: dict[int, BorrowRecord] = {} 
