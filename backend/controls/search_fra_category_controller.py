from sqlalchemy.orm import Session
from entities.fra_category import FRACategory


class SearchFRACategoryController:
    def searchCategory(self, db: Session, keyword: str) -> list:
        entity = FRACategory()
        return entity.searchCategory(db, keyword)
