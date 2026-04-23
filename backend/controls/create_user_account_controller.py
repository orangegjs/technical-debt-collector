from sqlalchemy.orm import Session
from passlib.context import CryptContext
from entities.user_account import UserAccount

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserAccountController:
    def createUserAccount(
        self,
        db: Session,
        username: str,
        password: str,
        name: str,
        email: str,
        accountStatus: str,
        role: str,
    ) -> bool:
        try:
            existing = db.query(UserAccount).filter(
                (UserAccount.username == username) | (UserAccount.email == email)
            ).first()
            if existing:
                return False
            hashed = pwd_context.hash(password)
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
