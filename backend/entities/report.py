from datetime import date
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import Session
from database import Base


class Report(Base):
    __tablename__ = "report"

    reportID      = Column(Integer, primary_key=True, autoincrement=True)
    reportType    = Column(String,  nullable=False)   # "daily" | "weekly" | "monthly"
    startDate     = Column(Date,    nullable=False)
    endDate       = Column(Date,    nullable=False)
    totalFRA      = Column(Integer, nullable=False, default=0)
    totalDonation = Column(Integer, nullable=False, default=0)
    totalAccount  = Column(Integer, nullable=False, default=0)

    @staticmethod
    def generateReport(
        db: Session,
        reportType: str,
        startDate: date,
        endDate: date,
        totalFRA: int,
        totalDonation: int,
        totalAccount: int,
    ) -> "Report":
        """US#38/39/40: Construct, persist, and return a Report row."""
        new_report = Report(
            reportType=reportType,
            startDate=startDate,
            endDate=endDate,
            totalFRA=totalFRA,
            totalDonation=totalDonation,
            totalAccount=totalAccount,
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report
