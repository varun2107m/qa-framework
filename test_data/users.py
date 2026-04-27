import os

# Fallbacks for local dev convenience only — never commit real credentials here
_FALLBACKS = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "locked":   {"username": "locked_out_user", "password": "secret_sauce"},
    "problem":  {"username": "problem_user",    "password": "secret_sauce"},
    "admin":    {"username": "admin_user",       "password": ""},
}

USERS = {
    "standard": {
        "username": os.getenv("STANDARD_USERNAME"),
        "password": os.getenv("STANDARD_PASSWORD"),
    },
    "admin": {
        "username": os.getenv("ADMIN_USERNAME"),
        "password": os.getenv("ADMIN_PASSWORD"),
    },
    "locked": {
        "username": os.getenv("LOCKED_USERNAME"),
        "password": os.getenv("LOCKED_PASSWORD"),
    },
    "problem": {
        "username": os.getenv("PROBLEM_USERNAME"),
        "password": os.getenv("PROBLEM_PASSWORD"),
    },
}


def get_user(user_type: str) -> dict:
    if user_type not in USERS:
        raise ValueError(
            f"Unknown user type: '{user_type}'. Valid types: {list(USERS.keys())}"
        )

    user = USERS[user_type]
    fallback = _FALLBACKS.get(user_type, {})

    # ✅ falls back gracefully — no crash without env vars
    return {
        "username": user["username"] or fallback.get("username", ""),
        "password": user["password"] or fallback.get("password", ""),
    }


