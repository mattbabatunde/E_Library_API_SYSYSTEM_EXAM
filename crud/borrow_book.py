from typing import List, Optional
from uuid import uuid4, UUID
from fastapi import HTTPException, status
from schemas.borrow_book_schema import BorrowModel, BorrowRecord

class BorrowRecordService:
    borrow_records_db = {}

    @staticmethod
    def create_borrow_record(record: BorrowModel) -> BorrowRecord:
        record_id = uuid4()  # Generate a unique UUID for the borrow record
        new_record = record.dict()
        new_record["id"] = record_id
        BorrowRecordService.borrow_records_db[record_id] = new_record
        return BorrowRecord(**new_record)

    @staticmethod
    def get_borrow_records() -> List[BorrowRecord]:
        return [
            BorrowRecord(**record)
            for record in BorrowRecordService.borrow_records_db.values()
        ]

    @staticmethod
    def get_user_borrow_records(user_id: str) -> List[BorrowRecord]:
        try:
            uuid_obj = UUID(user_id)  # Validate and convert user_id to UUID
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        user_records = [
            BorrowRecord(**record)
            for record in BorrowRecordService.borrow_records_db.values()
            if record["user_id"] == str(uuid_obj)
        ]

        if not user_records:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No borrow records found for the given user ID"
            )

        return user_records
