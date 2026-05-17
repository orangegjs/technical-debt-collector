from sqlalchemy.orm import Session
from entities.favourite import Favourite


class RetrieveFavouriteController:
    def retrieveFavourite(self, db: Session, userID: int, fraID: int):
        return Favourite.retrieveFavourite(db, userID, fraID)
