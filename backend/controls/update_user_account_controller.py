import bcrypt
from sqlalchemy.orm import Session
from entities.user_account import UserAccount


class UpdateUserAccountController:
    def updateUserAccount(self, db: Session, user_acc: dict) -> bool:
        try:
            uid = user_acc.get("userID") or user_acc.get("user_id")
            user = db.query(UserAccount).filter(UserAccount.userID == uid).first()
            if not user:
                return False
            for field in ("username", "email", "accountStatus", "role", "profile_picture_url"):
                if field in user_acc and user_acc[field] is not None:
                    setattr(user, field, user_acc[field])
            if "password" in user_acc and user_acc["password"]:
                user.password = bcrypt.hashpw(user_acc["password"].encode(), bcrypt.gensalt()).decode()
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
