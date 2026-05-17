from sqlalchemy.orm import Session
from entities.fra_activity import FRAActivity


class SearchAvailableFRAController:
    def searchAvailableFRA(self, db: Session, userID: int, keyword: str) -> list:
        entity = FRAActivity()
        return entity.searchAvailableFRA(db, userID, keyword)
