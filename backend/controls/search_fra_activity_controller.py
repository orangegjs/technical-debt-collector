from sqlalchemy.orm import Session
from entities.fra_activity import FRAActivity


class SearchFRAActivityController:
    def searchFRA(self, db: Session, keyword: str, ownerID: "int | None" = None) -> list:
        entity = FRAActivity()
        return entity.searchFRA(db, keyword, ownerID)
