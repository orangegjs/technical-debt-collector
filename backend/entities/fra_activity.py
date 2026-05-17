from datetime import date
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship
from database import Base


class FRAActivity(Base):
    __tablename__ = "fra_activity"

    fraID             = Column(Integer, primary_key=True, autoincrement=True)
    fraName           = Column(String, unique=True, nullable=False)
    fraDescription    = Column(String, nullable=True)
    fraGoalAmount     = Column(Float, nullable=False)
    fraStartDate      = Column(Date, nullable=False)
    fraEndDate        = Column(Date, nullable=False)
    fraStatus         = Column(String, default="Active")
    fraViewCount      = Column(Integer, default=0)
    fraShortlistCount = Column(Integer, default=0)
    fraCategoryID     = Column(Integer, ForeignKey("fra_category.categoryID"), nullable=False)
    fraOwnerID        = Column(Integer, ForeignKey("user_account.userID"), nullable=False)

    fra_category   = relationship("FRACategory", back_populates="fra_activities")
    fra_owner      = relationship("UserAccount",  back_populates="fra_activities")
    favourites     = relationship("Favourite",    back_populates="fra")
    donations      = relationship("Donation",     back_populates="fra")

    def createFRA(
        self,
        db: Session,
        fraName: str,
        fraDescription: str | None,
        fraGoalAmount: float,
        fraStartDate: date,
        fraEndDate: date,
        fraStatus: str,
        fraCategoryID: int,
        fraOwnerID: int,
    ) -> bool:
        try:
            existing = db.query(FRAActivity).filter(FRAActivity.fraName == fraName).first()
            if existing:
                return False
            new_fra = FRAActivity(
                fraName=fraName,
                fraDescription=fraDescription,
                fraGoalAmount=fraGoalAmount,
                fraStartDate=fraStartDate,
                fraEndDate=fraEndDate,
                fraStatus=fraStatus,
                fraCategoryID=fraCategoryID,
                fraOwnerID=fraOwnerID,
            )
            db.add(new_fra)
            db.commit()
            db.refresh(new_fra)
            return True
        except Exception:
            db.rollback()
            return False

    @staticmethod
    def retrieveFRA(db: Session, fraID: int) -> "FRAActivity | None":
        return db.query(FRAActivity).filter(FRAActivity.fraID == fraID).first()

    def updateFRA(self, db: Session, fra: dict) -> bool:
        try:
            fra_id = fra.get("fraID")
            record = db.query(FRAActivity).filter(FRAActivity.fraID == fra_id).first()
            if not record:
                return False
            if "fraName" in fra and fra["fraName"] is not None:
                record.fraName = fra["fraName"]
            if "fraDescription" in fra:
                record.fraDescription = fra["fraDescription"]
            if "fraGoalAmount" in fra and fra["fraGoalAmount"] is not None:
                record.fraGoalAmount = fra["fraGoalAmount"]
            if "fraStartDate" in fra and fra["fraStartDate"] is not None:
                record.fraStartDate = fra["fraStartDate"]
            if "fraEndDate" in fra and fra["fraEndDate"] is not None:
                record.fraEndDate = fra["fraEndDate"]
            if "fraStatus" in fra and fra["fraStatus"] is not None:
                record.fraStatus = fra["fraStatus"]
            if "fraCategoryID" in fra and fra["fraCategoryID"] is not None:
                record.fraCategoryID = fra["fraCategoryID"]
            if "fraOwnerID" in fra and fra["fraOwnerID"] is not None:
                record.fraOwnerID = fra["fraOwnerID"]
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    def suspendFRA(self, db: Session, fraID: int) -> bool:
        try:
            record = db.query(FRAActivity).filter(FRAActivity.fraID == fraID).first()
            if not record:
                return False
            record.fraStatus = "Suspended"
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    def searchFRA(self, db: Session, keyword: str, ownerID: "int | None" = None) -> list:
        from sqlalchemy import String as SAString

        query = db.query(FRAActivity)
        if ownerID is not None:
            query = query.filter(FRAActivity.fraOwnerID == ownerID)
        if keyword:
            query = query.filter(
                FRAActivity.fraName.ilike(f"%{keyword}%")
                | FRAActivity.fraID.cast(SAString).ilike(f"%{keyword}%")
            )
        return query.all()

    def searchAvailableFRA(self, db: Session, userID: int, keyword: str) -> list:
        from sqlalchemy import String as SAString

        query = db.query(FRAActivity).filter(FRAActivity.fraStatus == "Active")
        if keyword:
            query = query.filter(
                FRAActivity.fraName.ilike(f"%{keyword}%")
                | FRAActivity.fraID.cast(SAString).ilike(f"%{keyword}%")
            )
        return query.order_by(FRAActivity.fraStartDate.desc()).all()

    def retrieveAvailableFRA(self, db: Session, fraID: int) -> "FRAActivity | None":
        fra = db.query(FRAActivity).filter(
            FRAActivity.fraID == fraID,
            FRAActivity.fraStatus == "Active",
        ).first()
        if fra:
            try:
                fra.fraViewCount = (fra.fraViewCount or 0) + 1
                db.commit()
            except Exception:
                db.rollback()  # non-fatal — view counter failure must not block the read
        return fra
