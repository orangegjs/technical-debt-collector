from sqlalchemy.orm import Session
from passlib.context import CryptContext
from entities.user_account import UserAccount

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UpdateUserAccountController:
    def updateUserAccount(self, db: Session, user_acc: dict) -> bool:
        try:
            user = db.query(UserAccount).filter(
                UserAccount.user_id == user_acc["user_id"]
            ).first()
            if not user:
                return False
            for field in ("username", "email", "name", "age", "status", "role", "profile_picture_url"):
                if field in user_acc and user_acc[field] is not None:
                    setattr(user, field, user_acc[field])
            if "password" in user_acc and user_acc["password"]:
                user.password_hash = pwd_context.hash(user_acc["password"])
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
