from typing import List, Optional
from uuid import uuid4, UUID
from fastapi import HTTPException, status
from schemas.user_schema import UserModel, User

class UserService:
    users_db = {}

    @staticmethod
    def create_user(user: UserModel) -> User:
        user_id = uuid4()  # Generate a unique UUID for the user
        new_user = user.dict()
        new_user["id"] = user_id
        new_user["is_active"] = True  # Default to active status
        UserService.users_db[user_id] = new_user
        return User(**new_user)

    @staticmethod
    def get_user(user_id: str) -> Optional[User]:
        # Validate and convert user_id to UUID
        try:
            uuid_obj = UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

        # Retrieve user from the database
        user = UserService.users_db.get(uuid_obj)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return User(**user)

    @staticmethod
    def update_user(user_id: str, updated_user: UserModel) -> Optional[User]:
        user = UserService.get_user(user_id)  # This raises HTTPException if user not found
        for key, value in updated_user.dict().items():
            setattr(user, key, value)
        UserService.users_db[user.id] = user.dict()  # Update user in the database
        return user

    @staticmethod
    def deactivate_user(user_id: str) -> bool:
        user = UserService.get_user(user_id)  # This raises HTTPException if user not found
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already inactive"
            )
        user.is_active = False
        UserService.users_db[user.id] = user.dict()  # Update user in the database
        return True

    @staticmethod
    def delete_user(user_id: str) -> None:
        # Validate and convert user_id to UUID
        try:
            uuid_obj = UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

        # Check if the user exists
        if uuid_obj not in UserService.users_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        del UserService.users_db[uuid_obj]  # Delete user from the database

