from sqlalchemy.orm import Session
from entities.user_account import UserAccount


class RetrieveUserAccountController:
    def retrieveUserAccount(self, db: Session, userID: int) -> UserAccount | None:
        return db.query(UserAccount).filter(UserAccount.userID == userID).first()
