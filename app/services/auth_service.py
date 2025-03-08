from app.models.user_model import User
from app.utils.security import verify_password, get_password_hash, create_access_token

# Fake user database (replace with real DB)
fake_users_db = {
    "admin": {"username": "admin", "hashed_password": get_password_hash("password123")}
}

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def login_user(user: User):
    db_user = authenticate_user(user.username, user.password)
    if not db_user:
        return None
    return create_access_token({"sub": user.username})
