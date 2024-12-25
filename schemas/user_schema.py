from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional



class UserModel(BaseModel):
    name: str 
    email: EmailStr
    is_active: bool = True


class User(UserModel):
    id: UUID



class Create_User(UserModel):
    name: str = "john doe"
    email: EmailStr = "example@gmail.com"
    is_active: bool = True


class Login_User(BaseModel):
    name: str = "john doe"
    email: EmailStr = "example@gmail.com"
    login_time: datetime = datetime.now()
    is_active: bool = True


class Update_User(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


users: dict[UUID, User] = {}



