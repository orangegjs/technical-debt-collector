from sqlalchemy.orm import Session
from entities.fra_category import FRACategory


class RetrieveFRACategoryController:
    def retrieveCategory(self, db: Session, categoryID: int) -> "FRACategory | None":
        return FRACategory.retrieveCategory(db, categoryID)
