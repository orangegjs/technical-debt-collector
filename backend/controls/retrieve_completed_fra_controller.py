from sqlalchemy.orm import Session
from entities.fra_activity import FRAActivity


class RetrieveCompletedFRAController:
    def retrieveCompletedFRA(self, db: Session, fraID: int):
        return FRAActivity.retrieveCompletedFRA(db, fraID)
