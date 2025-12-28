from app.models.user import User
from app.core.security import hash_password, is_strong_password, verify_password
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def create_user(self, username: str, email: str, role: str, password: str):
        if self.repo.get_by_email(email):
            raise HTTPException(status_code=400, detail="Email already exists")

        if not is_strong_password(password):
            raise HTTPException(
                status_code=400,
                detail="Password too weak. Must be 8+ chars, include uppercase, lowercase, number & special char."
            )

        new_user = User(
            username=username,
            email=email,
            role=role,
            password=hash_password(password)
        )
        return self.repo.create(new_user)

    def authenticate_user(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def list_users(self):
        return self.repo.list()
