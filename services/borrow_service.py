from fastapi import HTTPException
from schemas.borrow_book_schema import BorrowModel, BorrowRecord
from memory_db.books_db import books  # Import books in-memory database

from datetime import datetime
from typing import List

# Global dictionaries for borrow records
borrow_records: dict[int, BorrowRecord] = {}

# Borrow a book logic
def borrow_book(borrow_data: BorrowModel):
    # Check if book exists and is available
    book = books.get(borrow_data.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is not available")

    # Borrow the book
    book.is_available = False
    borrow_id = len(borrow_records) + 1
    borrow_record = BorrowRecord(
        id=borrow_id,
        user_id=borrow_data.user_id,
        book_id=borrow_data.book_id,
        borrow_date=borrow_data.borrow_date or datetime.now(),
    )
    borrow_records[borrow_id] = borrow_record

    return {"message": "Book borrowed successfully", "borrow_record": borrow_record}

# Return a borrowed book logic
def return_book(borrow_data: BorrowModel):
    # Find the borrow record for the book and user
    borrow_record = next((record for record in borrow_records.values()
                         if record.user_id == borrow_data.user_id and record.book_id == borrow_data.book_id), None)

    if not borrow_record:
        raise HTTPException(status_code=404, detail="No borrow record found for this book and user")
    
    # Update the return date in the borrow record
    borrow_record.return_date = borrow_data.borrow_date or datetime.now()
    
    # Mark the book as available again
    book = books.get(borrow_data.book_id)
    if book:
        book.is_available = True

    return {"message": "Book returned successfully", "borrow_record": borrow_record}

# View borrowing records for a specific user
def get_borrow_records_by_user(user_id: int) -> List[BorrowRecord]:
    # Return all records for the given user
    records = [record for record in borrow_records.values() if record.user_id == user_id]
    return records

# View all borrow records
def get_all_borrow_records() -> List[BorrowRecord]:
    return list(borrow_records.values())
