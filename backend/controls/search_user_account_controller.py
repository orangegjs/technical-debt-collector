from sqlalchemy import String
from sqlalchemy.orm import Session
from entities.user_account import UserAccount
from entities.user_profile import UserProfile


class SearchUserAccountController:
    def searchUserAcc(self, db: Session, keyword: str) -> list:
        results = (
            db.query(UserAccount)
            .outerjoin(UserProfile, UserAccount.profile_id == UserProfile.profileID)
            .filter(
                UserAccount.username.ilike(f"%{keyword}%")
                | UserAccount.userID.cast(String).ilike(f"%{keyword}%")
                | UserProfile.profileName.ilike(f"%{keyword}%")
            )
            .all()
        )
        return results
