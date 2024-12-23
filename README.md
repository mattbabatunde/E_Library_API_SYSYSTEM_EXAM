# **E-Library API System**
## Project Overview
The E-Library API System is a simple API designed to manage an online library. It allows users to:

Borrow and return books.
Manage user accounts and track activity.
Monitor the availability of books.
The system focuses on maintaining clear and consistent functionality while enforcing borrowing constraints and validation rules.

| Attribute   | Description                                      |
|-------------|--------------------------------------------------|
| id          | Unique identifier for the user.                 |
| name        | Name of the user.                               |
| email       | Email address of the user.                      |
| is_active   | Indicates if the user account is active. Defaults to True. |


## BorrowRecord

Tracks book borrowing activity.

| Attribute    | Description                                     |
|--------------|-------------------------------------------------|
| `id`         | Unique identifier for the borrowing record.     |
| `user_id`    | ID of the user who borrowed the book.           |
| `book_id`    | ID of the borrowed book.                        |
| `borrow_date`| Date the book was borrowed.                     |
| `return_date`| Date the book was returned (if applicable).     |






A lightweight API for managing users, books, and borrowing records in an e-library system.

---

## **Features**

### **User Management**
- CRUD operations for user accounts.
- Deactivate a user by setting `is_active` to `False`.

### **Book Management**
- CRUD operations for books.
- Mark a book as unavailable (e.g., if lost or under maintenance).

### **Borrowing Operations**
- **Borrow a Book:**
  - Active users can borrow available books.
  - Users cannot borrow:
    - A book that is unavailable.
    - A book they have already borrowed.
  - On successful borrowing:
    - Create a new `BorrowRecord`.
    - Update the book’s `is_available` status to `False`.
- **Return a Book:**
  - Mark a borrowed book as returned:
    - Update the `return_date` in the `BorrowRecord`.
    - Set the book’s `is_available` status to `True`.

### **Borrowing Record Management**
- View borrowing records for a specific user.
- View all borrowing records.

---

## **Key Features & Validation**

- **Database**: Uses in-memory data structures (`dict`) for storage.
- **Validation**: All inputs are validated using Pydantic models.
- **Constraints**:
  - Users must be active to perform any operations.
  - Books must be available to be borrowed.
  - Every borrowing operation creates a unique `BorrowRecord`.
- **Status Codes**:
  - Uses appropriate HTTP status codes for success and error responses.

---

## **API Endpoints**

### **User Management**
| Method | Endpoint                        | Description                           |
|--------|---------------------------------|---------------------------------------|
| POST   | `/users/create_user`                        | Create a new user account.            |
| GET    | `/users/{user_id}`              | Fetch a user by their ID.             |
| PUT    | `/users/{user_id}`              | Update user information.              |
| DELETE | `/users/{user_id}`              | Delete a user account.                |

### **Book Management**
| Method | Endpoint                               | Description                           |
|--------|----------------------------------------|---------------------------------------|
| POST   | `/books`                               | Add a new book.                       |
| GET    | `/books/{book_id}`                     | Fetch details of a book.              |
| PUT    | `/books/{book_id}`                     | Update book information.              |
| DELETE | `/books/{book_id}/delete`                     | Remove a book from the library.       |
| PATCH  | `/books/{book_id}/deactivate`    | Mark a book as unavailable.           |


### **Borrowing Operations**
| Method | Endpoint                      | Description                                 |
|--------|-------------------------------|---------------------------------------------|
| POST   | `/borrow_records/borrow`                     | Borrow a book.                              |
| PATCH  | `/borrow_records/return`  | Return a borrowed book.                     |
| GET    | `/borrow_records/records/{user_id}`          | View borrowing records for a specific user. |
| GET    | `/borrow_records/get_all_borrow_records`                    | View all borrowing records.                 |

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/mattbabatunde/E_Library_API_SYSYSTEM_EXAM
