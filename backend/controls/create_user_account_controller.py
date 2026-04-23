import bcrypt
from sqlalchemy.orm import Session
from entities.user_account import UserAccount


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
