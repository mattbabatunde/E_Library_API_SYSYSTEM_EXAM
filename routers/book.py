from fastapi import APIRouter, HTTPException, Path, status
from typing import List
from services.book_service import (
    get_all_books,
    add_book,
    update_book,
    mark_book_unavailable,
    delete_book,
    get_book_by_id,
)
from schemas.book_schema import Book, Create_Book, Update_Book

book_router = APIRouter()

# Get all books
@book_router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books_endpoint():
    books = get_all_books()
    return books  # No wrapper needed

# Create a new book
@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book_endpoint(new_book: Create_Book):
    book = add_book(new_book)
    return book  # No wrapper needed

# Get a book by ID
@book_router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id_endpoint(book_id: int = Path(..., description="The ID of the book")):
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book  # No wrapper needed

# Update a book (Full update)
@book_router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book_endpoint(book_id: int, new_book: Update_Book):
    book = update_book(book_id, new_book)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book  # No wrapper needed

# Partially update a book (Partial update)
@book_router.patch("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def partially_update_book_endpoint(book_id: int, new_book: Update_Book):
    book = update_book(book_id, new_book)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book  # No wrapper needed

# Mark a book as unavailable (Deactivate)
@book_router.patch("/{book_id}/deactivate", response_model=Book, status_code=status.HTTP_200_OK)
async def deactivate_book_endpoint(book_id: int):
    book = mark_book_unavailable(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book  # No wrapper needed

# Delete a book
@book_router.delete("/{book_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_endpoint(book_id: int):
    book = delete_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return None  # Return no content
