from datetime import date
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship
from database import Base


class FRAActivity(Base):
    __tablename__ = "fra_activity"

    fraID = Column(Integer, primary_key=True, autoincrement=True)
    fraName = Column(String, unique=True, nullable=False)
    fraDescription = Column(String, nullable=True)
    fraGoalAmount = Column(Float, nullable=False)
    fraStartDate = Column(Date, nullable=False)
    fraEndDate = Column(Date, nullable=False)
    fraStatus = Column(String, default="Active")
    fraCategoryID = Column(Integer, ForeignKey("fra_category.categoryID"), nullable=False)
    fraOwnerID = Column(Integer, ForeignKey("user_account.userID"), nullable=False)

    fra_category = relationship("FRACategory", back_populates="fra_activities")
    fra_owner = relationship("UserAccount", back_populates="fra_activities")

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

    def searchFRA(self, db: Session, keyword: str) -> list:
        from sqlalchemy import String as SAString

        return db.query(FRAActivity).filter(
            FRAActivity.fraName.ilike(f"%{keyword}%")
            | FRAActivity.fraID.cast(SAString).ilike(f"%{keyword}%")
        ).all()
