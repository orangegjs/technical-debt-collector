from datetime import date
from sqlalchemy.orm import Session
from entities.fra_activity import FRAActivity


class SearchCompletedFRAController:
    def searchHistory(
        self,
        db: Session,
        ownerID: int,
        keyword: str = "",
        serviceType: "str | None" = None,
        startDate: "date | None" = None,
        endDate: "date | None" = None,
    ) -> list:
        entity = FRAActivity()
        return entity.searchHistory(db, ownerID, keyword, serviceType, startDate, endDate)
