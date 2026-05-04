from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from database import Base


class UserProfile(Base):
    __tablename__ = "user_profile"

    profileID          = Column(Integer, primary_key=True, autoincrement=True)
    profileName        = Column(String, unique=True, nullable=False)
    profileDescription = Column(String, nullable=True)
    profileStatus      = Column(String, default="Active")  # "Active" or "Suspended"

    def createUserProfile(self, db: Session, profileName: str, profileDescription: str) -> bool:
        try:
            existing = db.query(UserProfile).filter(UserProfile.profileName == profileName).first()
            if existing:
                return False
            new_profile = UserProfile(
                profileName=profileName,
                profileDescription=profileDescription,
            )
            db.add(new_profile)
            db.commit()
            db.refresh(new_profile)
            return True
        except Exception:
            db.rollback()
            return False

    @staticmethod
    def retrieveUserProfile(db: Session, profileID: int) -> "UserProfile | None":
        return db.query(UserProfile).filter(UserProfile.profileID == profileID).first()

    def updateUserProfile(self, db: Session, user_pro: dict) -> bool:
        try:
            pid = user_pro.get("profileID")
            profile = db.query(UserProfile).filter(UserProfile.profileID == pid).first()
            if not profile:
                return False
            if "profileName" in user_pro and user_pro["profileName"] is not None:
                profile.profileName = user_pro["profileName"]
            if "profileDescription" in user_pro:
                profile.profileDescription = user_pro["profileDescription"]
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    def suspendUserProfile(self, db: Session, profileID: int) -> bool:
        try:
            profile = db.query(UserProfile).filter(UserProfile.profileID == profileID).first()
            if not profile:
                return False
            profile.profileStatus = "Suspended"
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    def searchUserProfile(self, db: Session, keyword: str) -> list:
        from sqlalchemy import String as SAString
        results = db.query(UserProfile).filter(
            UserProfile.profileName.ilike(f"%{keyword}%")
            | UserProfile.profileID.cast(SAString).ilike(f"%{keyword}%")
        ).all()
        return results
