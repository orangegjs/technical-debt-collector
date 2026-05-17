from datetime import date
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Session, relationship
from database import Base


class Donation(Base):
    __tablename__ = "donation"

    donationID     = Column(Integer,        primary_key=True, autoincrement=True)
    donationAmount = Column(Numeric(12, 2),  nullable=False)
    donationDate   = Column(Date,            nullable=False)
    donationStatus = Column(String,          default="Completed")
    fraID          = Column(Integer, ForeignKey("fra_activity.fraID"), nullable=False)
    userID         = Column(Integer, ForeignKey("user_account.userID"), nullable=False)

    fra   = relationship("FRAActivity", back_populates="donations")
    donee = relationship("UserAccount",  back_populates="donations")

    def searchDonation(
        self,
        db: Session,
        userID: int,
        keyword: str,
        category: "str | None" = None,
        startDate: "date | None" = None,
        endDate: "date | None" = None,
    ) -> list:
        from entities.fra_activity import FRAActivity
        from entities.fra_category import FRACategory
        from sqlalchemy import String as SAString

        query = (
            db.query(Donation)
            .join(FRAActivity, Donation.fraID == FRAActivity.fraID)
            .join(FRACategory, FRAActivity.fraCategoryID == FRACategory.categoryID)
            .filter(Donation.userID == userID)
        )
        if keyword:
            query = query.filter(
                FRAActivity.fraName.ilike(f"%{keyword}%")
                | FRAActivity.fraID.cast(SAString).ilike(f"%{keyword}%")
            )
        if category:
            query = query.filter(FRACategory.categoryName == category)
        if startDate:
            query = query.filter(Donation.donationDate >= startDate)
        if endDate:
            query = query.filter(Donation.donationDate <= endDate)

        return query.order_by(Donation.donationDate.desc()).all()

    @staticmethod
    def retrieveDonation(db: Session, donationID: int) -> "Donation | None":
        return db.query(Donation).filter(Donation.donationID == donationID).first()
