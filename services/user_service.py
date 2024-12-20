from typing import List, Optional
from schemas.user_schema import User, Create_User, Login_User, Update_User

# In-memory user database and ID counter
user_db = {}
user_id_counter = 1

# Helper function to generate the next user ID
def generate_user_id() -> int:
    global user_id_counter
    current_id = user_id_counter
    user_id_counter += 1
    return current_id

# Get all users
def get_all_users() -> List[User]:
    return list(user_db.values())

# Get a user by ID
def get_user_by_id(user_id: int) -> Optional[User]:
    return user_db.get(user_id)

# Create a new user
def create_user(user_data: Create_User) -> User:
    user_id = generate_user_id()
    new_user = User(id=user_id, **user_data.dict())
    user_db[user_id] = new_user
    return new_user

# Update a user
def update_user(user_id: int, user_data: Update_User) -> Optional[User]:
    existing_user = user_db.get(user_id)
    if not existing_user:
        return None

    # Update only provided fields
    updated_data = user_data.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(existing_user, key, value)
    return existing_user

# Delete a user
def delete_user(user_id: int) -> bool:
    if user_id in user_db:
        del user_db[user_id]
        return True
    return False

# Login user
def login_user(login_data: Login_User) -> Optional[User]:
    for user in user_db.values():
        if user.email == login_data.email and user.name == login_data.name:
            user.is_active = True  # Mark the user as active
            return user
    return None
