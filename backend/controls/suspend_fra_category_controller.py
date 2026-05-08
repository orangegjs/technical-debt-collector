from sqlalchemy.orm import Session
from entities.fra_category import FRACategory


class SuspendFRACategoryController:
    def suspendCategory(self, db: Session, categoryID: int) -> bool:
        entity = FRACategory()
        return entity.suspendCategory(db, categoryID)
