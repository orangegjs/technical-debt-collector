from datetime import date, timedelta
from sqlalchemy.orm import Session
from entities.fra_activity import FRAActivity
from entities.donation import Donation
from entities.user_account import UserAccount
from entities.report import Report


class GenerateReportController:
    """US#38/39/40: Queries FRA, Donation, and UserAccount entities,
    then persists results via the Report entity."""

    def generateReport(
        self,
        db: Session,
        reportType: str,
        startDate: "date | None" = None,
    ) -> Report:
        if startDate is None:
            startDate = date.today()

        if reportType == "daily":
            endDate = startDate
        elif reportType == "weekly":
            endDate = startDate + timedelta(days=6)
        elif reportType == "monthly":
            endDate = startDate + timedelta(days=29)
        else:
            raise ValueError(f"Invalid reportType: {reportType}")

        totalFRA      = FRAActivity.getTotalFRA(db, startDate, endDate)
        totalDonation = Donation.getTotalDonation(db, startDate, endDate)
        totalAccount  = UserAccount.getTotalAccount(db, startDate, endDate)

        return Report.generateReport(
            db, reportType, startDate, endDate, totalFRA, totalDonation, totalAccount
        )
