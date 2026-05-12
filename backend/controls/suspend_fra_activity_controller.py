from sqlalchemy.orm import Session
from entities.fra_activity import FRAActivity


class SuspendFRAActivityController:
    def suspendFRA(self, db: Session, fraID: int) -> bool:
        entity = FRAActivity()
        return entity.suspendFRA(db, fraID)
