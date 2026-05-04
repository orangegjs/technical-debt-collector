from sqlalchemy.orm import Session
from entities.user_profile import UserProfile


class SearchUserProfileController:
    def searchUserProfile(self, db: Session, keyword: str) -> list:
        entity = UserProfile()
        return entity.searchUserProfile(db, keyword)
