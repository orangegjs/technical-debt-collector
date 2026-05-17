from sqlalchemy.orm import Session
from entities.favourite import Favourite


class SearchFavouriteController:
    def searchFavourite(self, db: Session, userID: int, keyword: str) -> list:
        entity = Favourite()
        return entity.searchFavourite(db, userID, keyword)
