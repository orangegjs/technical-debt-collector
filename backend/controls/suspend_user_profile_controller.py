from sqlalchemy.orm import Session
from entities.user_profile import UserProfile


class SuspendUserProfileController:
    def suspendUserProfile(self, db: Session, profileID: int) -> bool:
        entity = UserProfile()
        return entity.suspendUserProfile(db, profileID)
