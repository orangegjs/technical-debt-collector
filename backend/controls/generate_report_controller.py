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
        endDate: "date | None" = None,
    ) -> Report:
        today = date.today()
        if startDate is None or endDate is None:
            if reportType == "daily":
                startDate = today
                endDate = today
            elif reportType == "weekly":
                startDate = today - timedelta(days=6)
                endDate = today
            elif reportType == "monthly":
                startDate = today - timedelta(days=29)
                endDate = today
            else:
                raise ValueError(f"Invalid reportType: {reportType}")

        totalFRA      = FRAActivity.getTotalFRA(db, startDate, endDate)
        totalDonation = Donation.getTotalDonation(db, startDate, endDate)
        totalAccount  = UserAccount.getTotalAccount(db, startDate, endDate)

        return Report.generateReport(
            db, reportType, startDate, endDate, totalFRA, totalDonation, totalAccount
        )
