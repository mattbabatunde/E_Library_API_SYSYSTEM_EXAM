from fastapi import APIRouter, HTTPException
from services.borrow_service import BorrowManager
from schemas.borrow_book_schema import BorrowModel, BorrowRecord
from typing import List
from uuid import UUID

borrow_router = APIRouter()

# Endpoint to borrow a book
@borrow_router.post("/borrow")
def borrow_book_route(borrow_data: BorrowModel):
    return BorrowManager.borrow_book(borrow_data)

# Endpoint to return a book
@borrow_router.post("/return")
def return_book_route(borrow_data: BorrowModel):
    return BorrowManager.return_book(borrow_data)

# Endpoint to view borrowing records for a specific user
@borrow_router.get("/records/{user_id}", response_model=List[BorrowRecord])
def view_borrow_records(user_id: UUID):
    records = BorrowManager.get_borrow_records_by_user(user_id)
    if not records:
        raise HTTPException(status_code=404, detail="No borrow records found for this user")
    return records

# Endpoint to get all borrow records
@borrow_router.get("/get_all_borrow_records", response_model=List[BorrowRecord])
def get_all_borrow_records() -> List[BorrowRecord]:
    # Using BorrowManager's static method to get all borrow records
    return list(BorrowManager.get_all_borrow_records().values())
