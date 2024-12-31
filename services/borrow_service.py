from fastapi import HTTPException
from datetime import datetime
from uuid import UUID
from schemas.borrow_book_schema import BorrowModel, BorrowRecord
from typing import List


class BorrowManager:
    # In-memory database for borrowing records
    borrow_records: dict[int, BorrowRecord] = {
        1: BorrowRecord(
            id=1,
            user_id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            book_id=1,
            borrow_date=datetime.now(),
            return_date=None
        )
    }

    # Mock user database with UUIDs and activity status
    users = {
        UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"): {"id": UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"), "is_active": True},
        UUID("7fa85f64-5717-4562-b3fc-2c963f66afb7"): {"id": UUID("7fa85f64-5717-4562-b3fc-2c963f66afb7"), "is_active": True},
        UUID("8fa85f64-5717-4562-b3fc-2c963f66afc8"): {"id": UUID("8fa85f64-5717-4562-b3fc-2c963f66afc8"), "is_active": False},
        UUID("9fa85f64-5717-4562-b3fc-2c963f66afd9"): {"id": UUID("9fa85f64-5717-4562-b3fc-2c963f66afd9"), "is_active": True},
        UUID("2fa85f64-5717-4562-b3fc-2c963f66afe2"): {"id": UUID("2fa85f64-5717-4562-b3fc-2c963f66afe2"), "is_active": False}
    }

    # Mock book database with availability status
    books = {
        1: {"id": 1, "title": "The Great Gatsby", "is_available": False},
        2: {"id": 2, "title": "Star boy", "is_available": True},
        3: {"id": 3, "title": "The Great Gatsby", "is_available": False},
        4: {"id": 4, "title": "Jingle bell", "is_available": True},
        5: {"id": 5, "title": "Magic house", "is_available": False},
        6: {"id": 6, "title": "Killer Mike", "is_available": True}
    }

    @classmethod
    def borrow_book(cls, borrow_data: BorrowModel):
        # Validate user
        user = cls.users.get(borrow_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user["is_active"]:
            raise HTTPException(status_code=400, detail="User account is inactive")

        # Validate book
        book = cls.books.get(borrow_data.book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        if not book["is_available"]:
            raise HTTPException(status_code=400, detail="Book is currently unavailable")

        # Create a new borrow record
        book["is_available"] = False
        borrow_id = len(cls.borrow_records) + 1
        borrow_record = BorrowRecord(
            id=borrow_id,
            user_id=borrow_data.user_id,
            book_id=borrow_data.book_id,
            borrow_date=borrow_data.borrow_date or datetime.now()
        )
        cls.borrow_records[borrow_id] = borrow_record

        return {"message": "Book borrowed successfully", "borrow_record": borrow_record}

    @classmethod
    def return_book(cls, borrow_data: BorrowModel):
        # Validate user
        user = cls.users.get(borrow_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        borrow_record = next(
            (record for record in cls.borrow_records.values()
             if record.user_id == borrow_data.user_id and record.book_id == borrow_data.book_id),
            None
        )
        if not borrow_record:
            raise HTTPException(status_code=404, detail="No borrow record found for this book and user")

        borrow_record.return_date = borrow_data.return_date or datetime.now()
        book = cls.books.get(borrow_data.book_id)
        if book:
            book["is_available"] = True

        return {"message": "Book returned successfully", "borrow_record": borrow_record}

    @classmethod
    def get_borrow_records_by_user(cls, user_id: UUID) -> List[BorrowRecord]:
        return [record for record in cls.borrow_records.values() if record.user_id == user_id]

    @staticmethod
    def get_all_borrow_records():
        return BorrowManager.borrow_records
