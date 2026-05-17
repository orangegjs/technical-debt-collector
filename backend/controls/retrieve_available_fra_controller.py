from sqlalchemy.orm import Session
from entities.fra_activity import FRAActivity


class RetrieveAvailableFRAController:
    def retrieveAvailableFRA(self, db: Session, fraID: int):
        # Must instantiate (not call as @staticmethod) because retrieveAvailableFRA
        # is an instance method that writes fraViewCount to the database.
        entity = FRAActivity()
        return entity.retrieveAvailableFRA(db, fraID)
