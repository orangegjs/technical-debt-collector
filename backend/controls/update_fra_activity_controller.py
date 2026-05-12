from sqlalchemy.orm import Session
from entities.fra_activity import FRAActivity


class UpdateFRAActivityController:
    def updateFRA(self, db: Session, fra: dict) -> bool:
        entity = FRAActivity()
        return entity.updateFRA(db, fra)
