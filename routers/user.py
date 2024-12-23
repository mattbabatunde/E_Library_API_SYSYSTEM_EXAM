from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import Create_User, Login_User, Update_User
from services.user_service import *

user_router = APIRouter()

@user_router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: Create_User):
    return {
        "message": "Successfully created new user",
        "data": create_user(user)
    }

@user_router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login_user_endpoint(login_data: Login_User):
    return {
        "message": "Login successful",
        "data": login_user(login_data)
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
    updated_user = update_user(user_id, user)
    if updated_user:
        return {
            "message": "User updated successfully",
            "data": updated_user
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

@user_router.get("/", status_code=status.HTTP_200_OK)
def get_users():
    return {
        "message": "Users retrieved successfully",
        "data": get_all_users()
    }

@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user_endpoint(user_id: str):
    deleted_user = delete_user(user_id)
    if deleted_user:
        return {
            "message": "User deleted successfully",
            "data": deleted_user
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

