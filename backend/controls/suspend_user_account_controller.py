from sqlalchemy.orm import Session
from entities.user_account import UserAccount


class SuspendUserAccountController:
    def suspendUserAccount(self, db: Session, userID: int) -> bool:
        try:
            user = db.query(UserAccount).filter(UserAccount.userID == userID).first()
            if not user:
                return False
            user.accountStatus = "Inactive"
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
