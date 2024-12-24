from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import Create_User, Login_User, Update_User
from services.user_service import *

user_router = APIRouter()

@user_router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: Create_User):
    # Check if user already exists before creating
    existing_user = next((u for u in get_all_users() if u.email == user.email), None)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Proceed with user creation if no conflict
    new_user = create_user(user)
    return {
        "message": "Successfully created new user",
        "data": new_user
    }

@user_router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login_user_endpoint(login_data: Login_User):
    # Check if the user exists with the provided credentials
    user = login_user(login_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or user does not exist"
        )
    
    return {
        "message": "Login successful",
        "data": user
    }

@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: str):
    user = get_user_by_id(user_id)
    if user:
        return {
            "message": "User retrieved successfully",
            "data": user
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

@user_router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user_endpoint(user_id: str, user: Update_User):
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    updated_user = update_user(user_id, user)
    return {
        "message": "User updated successfully",
        "data": updated_user
    }

@user_router.get("/", status_code=status.HTTP_200_OK)
def get_users():
    users = get_all_users()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    
    return {
        "message": "Users retrieved successfully",
        "data": users
    }

@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user_endpoint(user_id: str):
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    deleted_user = delete_user(user_id)
    return {
        "message": "User deleted successfully",
        "data": deleted_user
    }
