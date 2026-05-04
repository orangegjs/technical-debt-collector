from sqlalchemy.orm import Session
from entities.user_profile import UserProfile


class UpdateUserProfileController:
    def updateUserProfile(self, db: Session, user_pro: dict) -> bool:
        entity = UserProfile()
        return entity.updateUserProfile(db, user_pro)
