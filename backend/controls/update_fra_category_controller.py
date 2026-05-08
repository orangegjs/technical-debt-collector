from sqlalchemy.orm import Session
from entities.fra_category import FRACategory


class UpdateFRACategoryController:
    def updateCategory(self, db: Session, cat: dict) -> bool:
        entity = FRACategory()
        return entity.updateCategory(db, cat)
