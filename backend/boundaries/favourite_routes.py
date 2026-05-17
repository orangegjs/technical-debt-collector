from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from controls.save_fra_controller import SaveFRAController
from controls.search_favourite_controller import SearchFavouriteController
from controls.retrieve_favourite_controller import RetrieveFavouriteController
from database import get_db
from boundaries.fra_activity_routes import FRAActivityResponse

router = APIRouter(prefix="/api")


class SaveFRARequest(BaseModel):
    fraID: int
    userID: int


class FavouriteResponse(BaseModel):
    favouriteID: int
    savedDate: date
    fraID: int
    userID: int
    fra: Optional[FRAActivityResponse] = None

    class Config:
        from_attributes = True


# BCE Boundary: :SaveFRAPage
# Methods: displaySaveSuccess(), displayDuplicateFRASaved()
# Side-effect: increments fraShortlistCount on the FRA (handled in entity).
@router.post("/favourites", response_model=FavouriteResponse, status_code=201)
def save_favourite(payload: SaveFRARequest, db: Session = Depends(get_db)):
    ctrl = SaveFRAController()
    result = ctrl.saveFRA(db, payload.fraID, payload.userID)
    if result == "duplicate":
        raise HTTPException(status_code=400, detail="displayDuplicateFRASaved")
    if not result:
        raise HTTPException(status_code=400, detail="Failed to save favourite")
    from entities.favourite import Favourite
    fav = db.query(Favourite).filter(
        Favourite.userID == payload.userID,
        Favourite.fraID  == payload.fraID,
    ).first()
    return FavouriteResponse.model_validate(fav)


# BCE Boundary: :SearchFavouritePage
# Methods: displayFavourite(result_list), displayFavouriteNotFound()
@router.get("/favourites/search", response_model=list[FavouriteResponse])
def search_favourites(userID: int, q: str = "", db: Session = Depends(get_db)):
    ctrl = SearchFavouriteController()
    results = ctrl.searchFavourite(db, userID, q)
    return [FavouriteResponse.model_validate(r) for r in results]


# BCE Boundary: :RetrieveFavouritePage
# Methods: displayFavourite(Favourite fav)
@router.get("/favourites/{user_id}/{fra_id}", response_model=FavouriteResponse)
def get_favourite(user_id: int, fra_id: int, db: Session = Depends(get_db)):
    ctrl = RetrieveFavouriteController()
    fav = ctrl.retrieveFavourite(db, user_id, fra_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favourite not found")
    return FavouriteResponse.model_validate(fav)
