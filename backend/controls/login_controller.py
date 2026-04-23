import bcrypt
from sqlalchemy.orm import Session
from entities.user_account import UserAccount


class LoginController:
    def login(self, db: Session, username: str, password: str) -> UserAccount | None:
        user = db.query(UserAccount).filter(UserAccount.username == username).first()
        if user and bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return user
        return None
