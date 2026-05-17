from datetime import date
from sqlalchemy.orm import Session
from entities.donation import Donation


class SearchDonationController:
    def searchDonation(
        self,
        db: Session,
        userID: int,
        keyword: str,
        category: "str | None" = None,
        startDate: "date | None" = None,
        endDate: "date | None" = None,
    ) -> list:
        entity = Donation()
        return entity.searchDonation(db, userID, keyword, category, startDate, endDate)
