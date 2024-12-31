from typing import List, Optional
from uuid import uuid4
from schemas.user_schema import User, Create_User, Login_User, Update_User

class UserManager:
    # In-memory user database with fake user data
    user_db = {
        str(uuid4()): User(id=str(uuid4()), name="John Doe", email="johndoe@example.com", is_active=False),
        str(uuid4()): User(id=str(uuid4()), name="Jane Smith", email="janesmith@example.com", is_active=False),
        str(uuid4()): User(id=str(uuid4()), name="Alice Brown", email="alicebrown@example.com", is_active=False),
        str(uuid4()): User(id=str(uuid4()), name="Bob Johnson", email="bobjohnson@example.com", is_active=False)
    }

    @staticmethod
    def generate_user_id() -> str:
        return str(uuid4())

    @staticmethod
    def get_all_users() -> List[User]:
        """Get all users."""
        return list(UserManager.user_db.values())

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return UserManager.user_db.get(user_id)

    @staticmethod
    def create_user(user_data: Create_User) -> User:
        """Create a new user."""
        user_id = UserManager.generate_user_id()  # Generate a string ID for the user
        new_user = User(id=user_id, **user_data.dict())
        UserManager.user_db[user_id] = new_user
        return new_user

    @staticmethod
    def update_user(user_id: str, user_data: Update_User) -> Optional[User]:
        """Update an existing user."""
        existing_user = UserManager.user_db.get(user_id)
        if not existing_user:
            return None

        updated_data = user_data.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(existing_user, key, value)
        return existing_user

    @staticmethod
    def delete_user(user_id: str) -> bool:
        """Delete a user."""
        if user_id in UserManager.user_db:
            del UserManager.user_db[user_id]
            return True
        return False

    @staticmethod
    def login_user(login_data: Login_User) -> Optional[User]:
        """Login a user."""
        for user in UserManager.user_db.values():
            if user.email == login_data.email and user.name == login_data.name:
                user.is_active = True  # Mark the user as active
                return user
        return None

# Example usage
login_data = Login_User(name="John Doe", email="johndoe@example.com")
logged_in_user = UserManager.login_user(login_data)

if logged_in_user:
    print(f"User {logged_in_user.name} logged in successfully.")
else:
    print("Login failed.")
