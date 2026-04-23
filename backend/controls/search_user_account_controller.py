from sqlalchemy import String
from sqlalchemy.orm import Session
from entities.user_account import UserAccount


class SearchUserAccountController:
    def searchUserAcc(self, db: Session, keyword: str) -> list:
        results = db.query(UserAccount).filter(
            UserAccount.username.ilike(f"%{keyword}%")
            | UserAccount.user_id.cast(String).ilike(f"%{keyword}%")
        ).all()
        return results
