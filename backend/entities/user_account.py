import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship
from database import Base


class UserAccount(Base):
    __tablename__ = "user_account"

    userID              = Column(Integer, primary_key=True, autoincrement=True)
    username            = Column(String, unique=True, nullable=False)
    email               = Column(String, unique=True)
    password            = Column(String, nullable=False)   # stores bcrypt hash
    accountStatus       = Column(String, default="Active")  # "Active" or "Inactive"
    profile_id          = Column(Integer, ForeignKey("user_profile.profileID"), nullable=True)
    profile_picture_url = Column(String, nullable=True)

    user_profile = relationship("UserProfile", back_populates="user_accounts")
    fra_activities = relationship("FRAActivity", back_populates="fra_owner")

    # Backward-compat alias so LoginController (untouched) can access user.password_hash
    @property
    def password_hash(self):
        return self.password

    @staticmethod
    def login(db: Session, username: str, password: str) -> "UserAccount | None":
        user = db.query(UserAccount).filter(UserAccount.username == username).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
        return None

    def createUserAccount(
        self,
        db: Session,
        username: str,
        password: str,
        email: str,
        accountStatus: str,
        profile_id: int = None,
        profile_picture_url: str = None,
    ) -> bool:
        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = UserAccount(
                username=username,
                password=hashed,
                email=email,
                accountStatus=accountStatus,
                profile_id=profile_id,
                profile_picture_url=profile_picture_url,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return True
        except Exception:
            db.rollback()
            return False

    def updateUserAccount(self, db: Session, user_acc: dict) -> bool:
        try:
            uid = user_acc.get("userID") or user_acc.get("user_id")
            user = db.query(UserAccount).filter(UserAccount.userID == uid).first()
            if not user:
                return False
            for field in ("username", "email", "accountStatus", "profile_picture_url"):
                if field in user_acc and user_acc[field] is not None:
                    setattr(user, field, user_acc[field])
            if "profileID" in user_acc:
                user.profile_id = user_acc["profileID"]  # nullable — None is a valid clear
            if "password" in user_acc and user_acc["password"]:
                user.password = bcrypt.hashpw(user_acc["password"].encode(), bcrypt.gensalt()).decode()
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

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

    def searchUserAcc(self, db: Session, keyword: str) -> list:
        results = db.query(UserAccount).filter(
            UserAccount.username.ilike(f"%{keyword}%")
            | UserAccount.userID.cast(String).ilike(f"%{keyword}%")
        ).all()
        return results

    @staticmethod
    def retrieveUserAccount(db: Session, userID: int) -> "UserAccount | None":
        return db.query(UserAccount).filter(UserAccount.userID == userID).first()
