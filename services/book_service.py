from typing import List, Optional
from schemas.book_schema import Book, Create_Book, Update_Book

# In-memory storage for books
book_db = {}

# Helper function to generate the next book ID (this is a very simple approach for demo purposes)
def generate_book_id() -> int:
    return len(book_db) + 1

# Get all books
def get_all_books() -> List[Book]:
    return list(book_db.values())

# Create a new book
def add_book(book: Create_Book) -> Book:
    book_id = generate_book_id()
    new_book = Book(id=book_id, **book.dict())
    book_db[book_id] = new_book
    return new_book

# Get a book by ID
def get_book_by_id(book_id: int) -> Optional[Book]:
    return book_db.get(book_id)

# Update a book (full update)
def update_book(book_id: int, book_update: Update_Book) -> Optional[Book]:
    existing_book = book_db.get(book_id)
    if existing_book:
        # Update only the fields that are provided in the request body
        updated_data = book_update.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(existing_book, key, value)
        return existing_book
    return None

# Mark a book as unavailable (deactivate)
def mark_book_unavailable(book_id: int) -> Optional[Book]:
    book = book_db.get(book_id)
    if book:
        book.is_available = False
        return book
    return None

# Delete a book
def delete_book(book_id: int) -> Optional[Book]:
    return book_db.pop(book_id, None)