from typing import List, Optional
from uuid import uuid4, UUID
from fastapi import HTTPException, status
from schemas.book_schema import BookModel, Book

class BookService:
    books_db = {}

    @staticmethod
    def create_book(book: BookModel) -> Book:
        book_id = uuid4()  # Generate a unique UUID for the book
        new_book = book.dict()
        new_book["id"] = book_id
        new_book["is_available"] = True  # Default to available status
        BookService.books_db[book_id] = new_book
        return Book(**new_book)

    @staticmethod
    def get_book(book_id: str) -> Optional[Book]:
        # Validate and convert book_id to UUID
        try:
            uuid_obj = UUID(book_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid book ID format"
            )

        # Retrieve book from the database
        book = BookService.books_db.get(uuid_obj)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return Book(**book)

    @staticmethod
    def update_book(book_id: str, updated_book: BookModel) -> Optional[Book]:
        book = BookService.get_book(book_id)  # This raises HTTPException if book not found
        for key, value in updated_book.dict().items():
            setattr(book, key, value)
        BookService.books_db[book.id] = book.dict()  # Update book in the database
        return book

    @staticmethod
    def mark_unavailable(book_id: str) -> bool:
        book = BookService.get_book(book_id)  # This raises HTTPException if book not found
        if not book.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is already unavailable"
            )
        book.is_available = False
        BookService.books_db[book.id] = book.dict()  # Update book in the database
        return True

    @staticmethod
    def delete_book(book_id: str) -> None:
        # Validate and convert book_id to UUID
        try:
            uuid_obj = UUID(book_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid book ID format"
            )

        # Check if the book exists
        if uuid_obj not in BookService.books_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        del BookService.books_db[uuid_obj]  # Delete book from the database
