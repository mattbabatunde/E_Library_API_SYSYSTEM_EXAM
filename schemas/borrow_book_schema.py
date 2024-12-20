from pydantic import BaseModel
from datetime import datetime
from schemas.book_schema import books

class BorrowModel(BaseModel):
    user_id: int
    book_id: int = books["id"]
    borrow_date: datetime = datetime.now() 
    return_date: datetime = datetime.today()

class BorrowRecord(BorrowModel):
    id: int

borrow_records:dict[int, BorrowModel] = {}

