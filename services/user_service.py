from schemas.user_schema import User, Create_User, Login_User, Update_User
from database.database import db, add_user
from typing import List, Optional

# In-memory user ID counter
user_id_counter = 1

# Get all users
def get_all_users() -> List[User]:
    return list(db["users"].values())

# Get a user by ID
def get_user_by_id(user_id: int) -> User:
    return db["users"].get(user_id, {"error": "User not found"})

# Create a new user
def create_user(user: Create_User) -> User:
    global user_id_counter
    new_user = {"id": user_id_counter, **user.dict()}
    add_user(
        user_id=user_id_counter,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
    )
    user_id_counter += 1
    return new_user

# Update a user
def update_user(user_id: int, user_data: Update_User) -> dict:
    existing_user = db["users"].get(user_id)
    if not existing_user:
        return {"error": "User not found"}
    
    # Only update fields that are provided
    updated_data = user_data.dict(exclude_unset=True)
    existing_user.update(updated_data)
    
    # Ensure that the updated data is saved back to the database
    db["users"][user_id] = existing_user
    return existing_user

# Delete a user
def delete_user(user_id: int) -> dict:
    if user_id in db["users"]:
        del db["users"][user_id]
        return {"message": "User deleted successfully"}
    return {"error": "User not found"}

# Login user
def login_user(login_data: Login_User) -> dict:
    # Check if user exists based on the provided login credentials (name and email)
    for user in db["users"].values():
        if user["email"] == login_data.email and user["name"] == login_data.name:
            user["is_active"] = True  # Mark the user as active
            return {"message": "Login successful", "user_id": user["id"]}
    return {"error": "Invalid login credentials"}
