from fastapi import APIRouter, HTTPException, Path, status
from typing import List
from schemas.book_schema import Book, Create_Book, Update_Book
from services.book_service import BookManager  # Import the BookManager class

book_router = APIRouter()

# Get all books
@book_router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books_endpoint():
    return BookManager.get_all_books()

# Create a new book
@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book_endpoint(new_book: Create_Book):
    return BookManager.add_book(new_book)

# Get a book by ID
@book_router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id_endpoint(book_id: int = Path(..., description="The ID of the book")):
    book = BookManager.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Update a book
@book_router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book_endpoint(book_id: int, updated_book: Update_Book):
    return BookManager.update_book(book_id, updated_book)

# Mark a book as unavailable
@book_router.patch("/{book_id}/deactivate", response_model=Book, status_code=status.HTTP_200_OK)
async def deactivate_book_endpoint(book_id: int):
    return BookManager.mark_book_unavailable(book_id)

# Delete a book
@book_router.delete("/{book_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_endpoint(book_id: int):
    BookManager.delete_book(book_id)
    return None
