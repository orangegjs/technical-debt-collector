from sqlalchemy.orm import Session
from entities.favourite import Favourite


class SaveFRAController:
    def saveFRA(self, db: Session, fraID: int, userID: int):
        entity = Favourite()
        return entity.saveFRA(db, fraID, userID)
