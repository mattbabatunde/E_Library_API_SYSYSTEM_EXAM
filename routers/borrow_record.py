from fastapi import APIRouter, Depends, HTTPException
from services.borrow_service import borrow_book, return_book, get_borrow_records_by_user, get_all_borrow_records
from schemas.borrow_book_schema import BorrowModel, BorrowRecord
from typing import List

borrow_router = APIRouter()

# Endpoint to borrow a book
@borrow_router.post("/borrow")
def borrow_book_route(borrow_data: BorrowModel):
    return borrow_book(borrow_data)

# Endpoint to return a book
@borrow_router.post("/return")
def return_book_route(borrow_data: BorrowModel):
    return return_book(borrow_data)

# Endpoint to view borrowing records for a specific user
@borrow_router.get("/records/{user_id}", response_model=List[BorrowRecord])
def view_borrow_records(user_id: int):
    records = get_borrow_records_by_user(user_id)
    if not records:
        raise HTTPException(status_code=404, detail="No borrow records found for this user")
    return records

# Endpoint to view all borrow records
@borrow_router.get("/records", response_model=List[BorrowRecord])
def view_all_borrow_records():
    return get_all_borrow_records()
