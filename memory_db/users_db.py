# memory_db/user_db.py

from schemas.user_schema import User  # Assuming you have a User schema defined in your schemas folder

# In-memory database for users
users = {
    1: User(id=1, username="john_doe", email="john@example.com"),
    2: User(id=2, username="jane_doe", email="jane@example.com"),
    3: User(id=2, username="jane_doe", email="jane@example.com"),
    4: User(id=2, username="jane_doe", email="jane@example.com"),
    5: User(id=2, username="jane_doe", email="jane@example.com"),
    6: User(id=2, username="jane_doe", email="jane@example.com"),
    7: User(id=2, username="jane_doe", email="jane@example.com"),
    8: User(id=2, username="jane_doe", email="jane@example.com"),
    9: User(id=2, username="jane_doe", email="jane@example.com"),
    10: User(id=2, username="jane_doe", email="jane@example.com")
    
}
