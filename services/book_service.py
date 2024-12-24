from typing import List, Optional
from fastapi import HTTPException, status
from schemas.book_schema import Book, Create_Book, Update_Book

# In-memory book database with fake book data
book_db = {
    1: Book(id=1, title="The Great Gatsby", author="F. Scott Fitzgerald", is_available=True),
    2: Book(id=2, title="1984", author="George Orwell", is_available=True),
    3: Book(id=3, title="To Kill a Mockingbird", author="Harper Lee", is_available=True),
    4: Book(id=4, title="Moby-Dick", author="Herman Melville", is_available=True),
}

# Helper function to generate a unique book ID
def generate_book_id() -> int:
    return max(book_db.keys(), default=0) + 1

# Get all books
def get_all_books() -> List[Book]:
    return list(book_db.values())

# Get a book by ID
def get_book_by_id(book_id: int) -> Optional[Book]:
    return book_db.get(book_id)

# Create a new book
def add_book(book_data: Create_Book) -> Book:
    # Check if the book already exists by title and author
    for book in book_db.values():
        if book.title == book_data.title and book.author == book_data.author:
            # Raise HTTPException with 404 status if book already exists
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book '{book_data.title}' by {book_data.author} already exists in the database."
            )
    
    book_id = generate_book_id()  # Generate a unique integer ID for the book
    new_book = Book(id=book_id, **book_data.dict())
    book_db[book_id] = new_book
    return new_book

# Update a book
def update_book(book_id: int, book_data: Update_Book) -> Optional[Book]:
    existing_book = book_db.get(book_id)
    if not existing_book:
        # Raise HTTPException with 404 status if book is not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found."
        )
    
    updated_data = book_data.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(existing_book, key, value)
    return existing_book

# Mark a book as unavailable
def mark_book_unavailable(book_id: int) -> Optional[Book]:
    book = book_db.get(book_id)
    if book:
        book.is_available = False
        return book
    # Raise HTTPException with 404 status if book is not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found."
    )

# Delete a book
def delete_book(book_id: int) -> bool:
    if book_id in book_db:
        del book_db[book_id]
        return True
    # Raise HTTPException with 404 status if book is not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found."
    )

# Example usage for adding a book
new_book_data = Create_Book(title="Pride and Prejudice", author="Jane Austen", is_available=True)

try:
    added_book = add_book(new_book_data)
    print(f"Book '{added_book.title}' added successfully.")
except HTTPException as e:
    print(f"Error: {e.detail}")

# Example usage for updating a book
book_to_update = Update_Book(title="Pride and Prejudice - Updated")
try:
    updated_book = update_book(added_book.id, book_to_update)
    print(f"Book '{updated_book.title}' updated successfully.")
except HTTPException as e:
    print(f"Error: {e.detail}")
