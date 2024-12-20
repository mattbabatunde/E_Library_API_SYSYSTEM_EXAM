from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional


# Base model for a user
class UserModel(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True

# Model for user with ID
class User(UserModel):
    id: UUID


# Model for creating a new user
class Create_User(UserModel):
    name: str = "john doe"
    email: EmailStr = "example@gmail.com"
    is_active: bool = True

# Model for login user, includes login_time
class Login_User(BaseModel):
    name: str = "john doe"
    email: EmailStr = "example@gmail.com"
    login_time: datetime = datetime.now()
    is_active: bool = True

# Model for updating user details (optional fields)
class Update_User(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

# Users dictionary (use ID as the key, instead of name)
users: dict[int, User] = {}
