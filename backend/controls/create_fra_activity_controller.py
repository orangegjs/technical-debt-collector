from sqlalchemy.orm import Session
from entities.fra_activity import FRAActivity


class CreateFRAActivityController:
    def createFRA(
        self,
        db: Session,
        fraName: str,
        fraDescription: str | None,
        fraGoalAmount: float,
        fraStartDate,
        fraEndDate,
        fraStatus: str,
        fraCategoryID: int,
        fraOwnerID: int,
    ):
        existing = db.query(FRAActivity).filter(FRAActivity.fraName == fraName).first()
        if existing:
            return "duplicate"
        entity = FRAActivity()
        success = entity.createFRA(
            db,
            fraName,
            fraDescription,
            fraGoalAmount,
            fraStartDate,
            fraEndDate,
            fraStatus,
            fraCategoryID,
            fraOwnerID,
        )
        return success
