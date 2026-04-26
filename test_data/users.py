import os

USERS = {
    "standard": {
        "username": os.getenv("STANDARD_USERNAME"),
        "password": os.getenv("STANDARD_PASSWORD"),
    },
    "admin": {
        "username": os.getenv("ADMIN_USERNAME"),
        "password": os.getenv("ADMIN_PASSWORD"),
    },
}


def get_user(user_type: str) -> dict:
    if user_type not in USERS:
        raise ValueError(f"Invalid user type: {user_type}")

    user = USERS[user_type]

    if not user["username"] or not user["password"]:
        raise ValueError(f"Missing credentials for {user_type} in environment variables")

    return user

