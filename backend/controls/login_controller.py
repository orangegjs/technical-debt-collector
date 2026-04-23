from sqlalchemy.orm import Session
from passlib.context import CryptContext
from entities.user_account import UserAccount

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginController:
    def login(self, db: Session, username: str, password: str) -> UserAccount | None:
        user = db.query(UserAccount).filter(UserAccount.username == username).first()
        if user and pwd_context.verify(password, user.password_hash):
            return user
        return None
