from sqlalchemy.orm import Session
from entities.fra_activity import FRAActivity


class RetrieveFRAActivityController:
    def retrieveFRA(self, db: Session, fraID: int) -> "FRAActivity | None":
        return FRAActivity.retrieveFRA(db, fraID)
