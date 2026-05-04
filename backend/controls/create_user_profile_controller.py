from sqlalchemy.orm import Session
from entities.user_profile import UserProfile


class CreateUserProfileController:
    def createUserProfile(self, db: Session, profileName: str, profileDescription: str, profileStatus: str = "Active"):
        existing = db.query(UserProfile).filter(UserProfile.profileName == profileName).first()
        if existing:
            return "duplicate"
        entity = UserProfile()
        success = entity.createUserProfile(db, profileName, profileDescription, profileStatus)
        return success  # True or False
