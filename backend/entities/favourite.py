from datetime import date
from sqlalchemy import Column, Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Session, relationship
from database import Base


class Favourite(Base):
    __tablename__ = "favourite"

    favouriteID = Column(Integer, primary_key=True, autoincrement=True)
    savedDate   = Column(Date, nullable=False, default=date.today)
    fraID       = Column(Integer, ForeignKey("fra_activity.fraID"), nullable=False)
    userID      = Column(Integer, ForeignKey("user_account.userID"), nullable=False)

    __table_args__ = (UniqueConstraint("userID", "fraID", name="uq_user_fra"),)

    fra   = relationship("FRAActivity", back_populates="favourites")
    donee = relationship("UserAccount",  back_populates="favourites")

    def saveFRA(self, db: Session, fraID: int, userID: int) -> "str | bool":
        try:
            existing = db.query(Favourite).filter(
                Favourite.fraID == fraID,
                Favourite.userID == userID,
            ).first()
            if existing:
                return "duplicate"

            new_fav = Favourite(fraID=fraID, userID=userID, savedDate=date.today())
            db.add(new_fav)
            db.flush()  # write Favourite row; keep transaction open

            from entities.fra_activity import FRAActivity  # deferred to avoid circular import
            fra = db.query(FRAActivity).filter(FRAActivity.fraID == fraID).first()
            if fra:
                fra.fraShortlistCount = (fra.fraShortlistCount or 0) + 1

            db.commit()
            db.refresh(new_fav)
            return True
        except Exception:
            db.rollback()
            return False

    def searchFavourite(self, db: Session, userID: int, keyword: str) -> list:
        from entities.fra_activity import FRAActivity
        from sqlalchemy import String as SAString

        query = (
            db.query(Favourite)
            .join(FRAActivity, Favourite.fraID == FRAActivity.fraID)
            .filter(Favourite.userID == userID)
        )
        if keyword:
            query = query.filter(
                FRAActivity.fraName.ilike(f"%{keyword}%")
                | FRAActivity.fraID.cast(SAString).ilike(f"%{keyword}%")
            )
        return query.all()

    @staticmethod
    def retrieveFavourite(db: Session, userID: int, fraID: int) -> "Favourite | None":
        return db.query(Favourite).filter(
            Favourite.userID == userID,
            Favourite.fraID  == fraID,
        ).first()
