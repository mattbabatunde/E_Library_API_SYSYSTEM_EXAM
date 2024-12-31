from typing import List, Optional
from fastapi import HTTPException, status
from schemas.book_schema import Book, Create_Book, Update_Book

class BookManager:
    # In-memory book database with fake book data
    book_db = {
        1: Book(id=1, title="The Great Gatsby", author="F. Scott Fitzgerald", is_available=True),
        2: Book(id=2, title="1984", author="George Orwell", is_available=True),
        3: Book(id=3, title="To Kill a Mockingbird", author="Harper Lee", is_available=True),
        4: Book(id=4, title="Moby-Dick", author="Herman Melville", is_available=True),
    }

    @staticmethod
    def generate_book_id() -> int:
        """Generate a unique book ID."""
        return max(BookManager.book_db.keys(), default=0) + 1

    @classmethod
    def get_all_books(cls) -> List[Book]:
        """Get all books."""
        return list(cls.book_db.values())

    @classmethod
    def get_book_by_id(cls, book_id: int) -> Optional[Book]:
        """Get a book by its ID."""
        return cls.book_db.get(book_id)

    @classmethod
    def add_book(cls, book_data: Create_Book) -> Book:
        """Add a new book to the database."""
        # Check if the book already exists by title and author
        for book in cls.book_db.values():
            if book.title == book_data.title and book.author == book_data.author:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Book '{book_data.title}' by {book_data.author} already exists in the database."
                )

        book_id = cls.generate_book_id()
        new_book = Book(id=book_id, **book_data.dict())
        cls.book_db[book_id] = new_book
        return new_book

    @classmethod
    def update_book(cls, book_id: int, book_data: Update_Book) -> Optional[Book]:
        """Update a book's details."""
        existing_book = cls.book_db.get(book_id)
        if not existing_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found."
            )

        updated_data = book_data.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(existing_book, key, value)
        return existing_book

    @classmethod
    def mark_book_unavailable(cls, book_id: int) -> Optional[Book]:
        """Mark a book as unavailable."""
        book = cls.book_db.get(book_id)
        if book:
            book.is_available = False
            return book
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found."
        )

    @classmethod
    def delete_book(cls, book_id: int) -> bool:
        """Delete a book from the database."""
        if book_id in cls.book_db:
            del cls.book_db[book_id]
            return True
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found."
        )

# Example usage
if __name__ == "__main__":
    # Example: Add a new book
    new_book_data = Create_Book(title="Pride and Prejudice", author="Jane Austen", is_available=True)
    try:
        added_book = BookManager.add_book(new_book_data)
        print(f"Book '{added_book.title}' added successfully.")
    except HTTPException as e:
        print(f"Error: {e.detail}")

    # Example: Update a book
    book_to_update = Update_Book(title="Pride and Prejudice - Updated")
    try:
        updated_book = BookManager.update_book(added_book.id, book_to_update)
        print(f"Book '{updated_book.title}' updated successfully.")
    except HTTPException as e:
        print(f"Error: {e.detail}")

    # Example: Mark a book as unavailable
    book_to_deactivate = 2
    try:
        deactivated_book = BookManager.mark_book_unavailable(book_to_deactivate)
        print(f"Book '{deactivated_book.title}' is now unavailable.")
    except HTTPException as e:
        print(f"Error: {e.detail}")

    # Example: Delete a book
    book_to_delete = 1
    try:
        deletion_result = BookManager.delete_book(book_to_delete)
        if deletion_result:
            print(f"Book with ID {book_to_delete} deleted successfully.")
    except HTTPException as e:
        print(f"Error: {e.detail}")

    # Example: Get all books
    all_books = BookManager.get_all_books()
    print("All Books:", all_books)

    # Example: Get a book by ID
    book_by_id = BookManager.get_book_by_id(3)
    if book_by_id:
        print(f"Book Found: {book_by_id.title}")
    else:
        print("Book not found.")
