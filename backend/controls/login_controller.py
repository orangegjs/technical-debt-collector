from sqlalchemy.orm import Session
from entities.user_account import UserAccount


class LoginController:
    def login(self, db: Session, username: str, password: str) -> UserAccount | None:
        return UserAccount.login(db, username, password)
