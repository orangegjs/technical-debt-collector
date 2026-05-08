from sqlalchemy.orm import Session
from entities.fra_category import FRACategory


class CreateFRACategoryController:
    def createCategory(self, db: Session, categoryName: str, categoryDescription: str, categoryStatus: str = "Active"):
        existing = db.query(FRACategory).filter(FRACategory.categoryName == categoryName).first()
        if existing:
            return "duplicate"
        entity = FRACategory()
        success = entity.createCategory(db, categoryName, categoryDescription, categoryStatus)
        return success  # True or False
