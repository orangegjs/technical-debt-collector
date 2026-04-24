import bcrypt
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from database import Base


class UserAccount(Base):
    __tablename__ = "user_account"

    userID        = Column(Integer, primary_key=True, autoincrement=True)
    username      = Column(String, unique=True, nullable=False)
    email         = Column(String, unique=True)
    password      = Column(String, nullable=False)   # stores bcrypt hash
    accountStatus = Column(String, default="Active")  # "Active" or "Inactive"
    role          = Column(String)                    # "User Admin", "Donee", "Platform Management", "Fund Raiser"

    # Backward-compat alias so LoginController (untouched) can access user.password_hash
    @property
    def password_hash(self):
        return self.password

    def login(self, db: Session, username: str, password: str) -> "UserAccount | None":
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
        role: str,
    ) -> bool:
        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = UserAccount(
                username=username,
                password=hashed,
                email=email,
                accountStatus=accountStatus,
                role=role,
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
            if "username" in user_acc and user_acc["username"] is not None:
                user.username = user_acc["username"]
            if "email" in user_acc and user_acc["email"] is not None:
                user.email = user_acc["email"]
            # Accept both "accountStatus" (new) and "status" (legacy) from callers
            if "accountStatus" in user_acc and user_acc["accountStatus"] is not None:
                user.accountStatus = user_acc["accountStatus"]
            elif "status" in user_acc and user_acc["status"] is not None:
                user.accountStatus = user_acc["status"]
            if "role" in user_acc and user_acc["role"] is not None:
                user.role = user_acc["role"]
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
