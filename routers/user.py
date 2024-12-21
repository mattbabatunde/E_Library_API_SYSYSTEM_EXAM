from fastapi import APIRouter
from schemas.user_schema import Create_User, Login_User, Update_User
from services.user_service import *

user_router = APIRouter()

@user_router.get("/")
def get_users():
    return get_all_users()

@user_router.get("/{user_id}")
def get_user(user_id: str):
    return get_user_by_id(user_id)

@user_router.post("/")
def create_user_endpoint(user: Create_User):
    return create_user(user)

@user_router.put("/{user_id}")
def update_user_endpoint(user_id: str, user: Update_User):
    return update_user(user_id, user)

@user_router.delete("/{user_id}")
def delete_user_endpoint(user_id: str):
    return delete_user(user_id)

@user_router.post("/login")
def login_user_endpoint(login_data: Login_User):
    return login_user(login_data)
