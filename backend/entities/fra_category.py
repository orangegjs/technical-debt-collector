from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from database import Base


class FRACategory(Base):
    __tablename__ = "fra_category"

    categoryID          = Column(Integer, primary_key=True, autoincrement=True)
    categoryName        = Column(String, unique=True, nullable=False)
    categoryDescription = Column(String, nullable=True)
    categoryStatus      = Column(String, default="Active")  # "Active" or "Inactive"

    def createCategory(self, db: Session, categoryName: str, categoryDescription: str, categoryStatus: str = "Active") -> bool:
        try:
            existing = db.query(FRACategory).filter(FRACategory.categoryName == categoryName).first()
            if existing:
                return False
            new_cat = FRACategory(
                categoryName=categoryName,
                categoryDescription=categoryDescription,
                categoryStatus=categoryStatus,
            )
            db.add(new_cat)
            db.commit()
            db.refresh(new_cat)
            return True
        except Exception:
            db.rollback()
            return False

    @staticmethod
    def retrieveCategory(db: Session, categoryID: int) -> "FRACategory | None":
        return db.query(FRACategory).filter(FRACategory.categoryID == categoryID).first()

    def updateCategory(self, db: Session, cat: dict) -> bool:
        try:
            cid = cat.get("categoryID")
            category = db.query(FRACategory).filter(FRACategory.categoryID == cid).first()
            if not category:
                return False
            if "categoryName" in cat and cat["categoryName"] is not None:
                category.categoryName = cat["categoryName"]
            if "categoryDescription" in cat:
                category.categoryDescription = cat["categoryDescription"]
            if "categoryStatus" in cat and cat["categoryStatus"] is not None:
                category.categoryStatus = cat["categoryStatus"]
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    def suspendCategory(self, db: Session, categoryID: int) -> bool:
        try:
            category = db.query(FRACategory).filter(FRACategory.categoryID == categoryID).first()
            if not category:
                return False
            category.categoryStatus = "Inactive"
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    def searchCategory(self, db: Session, keyword: str) -> list:
        from sqlalchemy import String as SAString
        results = db.query(FRACategory).filter(
            FRACategory.categoryName.ilike(f"%{keyword}%")
            | FRACategory.categoryID.cast(SAString).ilike(f"%{keyword}%")
        ).all()
        return results
