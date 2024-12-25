from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


# BorrowModel for user input
class BorrowModel(BaseModel):
    user_id: UUID  # UUID for user
    book_id: int  # ID of the book
    borrow_date: Optional[datetime] = None  
    return_date: Optional[datetime] = None 


# BorrowRecord for storing borrow records
class BorrowRecord(BorrowModel):
    id: int  
