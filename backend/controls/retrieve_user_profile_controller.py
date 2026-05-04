from sqlalchemy.orm import Session
from entities.user_profile import UserProfile


class RetrieveUserProfileController:
    def retrieveUserProfile(self, db: Session, profileID: int) -> "UserProfile | None":
        return UserProfile.retrieveUserProfile(db, profileID)
