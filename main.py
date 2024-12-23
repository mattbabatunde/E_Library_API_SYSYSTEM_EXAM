from fastapi import FastAPI
from routers import user, book, borrow_record

app = FastAPI()

app.include_router(user.user_router, prefix="/users", tags=["Users"])
app.include_router(book.book_router, prefix="/books", tags=["Books"])
app.include_router(borrow_record.borrow_router, prefix="/borrow_records", tags=["Borrow Records"])



@app.get("/")
def Home():
    return {"message": "Welcome to the E-Library API System!"}