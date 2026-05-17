from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, model_validator
from sqlalchemy.orm import Session

from controls.create_fra_activity_controller import CreateFRAActivityController
from controls.retrieve_fra_activity_controller import RetrieveFRAActivityController
from controls.search_fra_activity_controller import SearchFRAActivityController
from controls.suspend_fra_activity_controller import SuspendFRAActivityController
from controls.update_fra_activity_controller import UpdateFRAActivityController
from controls.search_available_fra_controller import SearchAvailableFRAController
from controls.retrieve_available_fra_controller import RetrieveAvailableFRAController
from database import get_db
from entities.fra_activity import FRAActivity
from entities.fra_category import FRACategory
from entities.user_account import UserAccount

router = APIRouter(prefix="/api")


class FRAActivityCreate(BaseModel):
    fraName: str = Field(min_length=1)
    fraDescription: Optional[str] = None
    fraGoalAmount: float
    fraStartDate: date
    fraEndDate: date
    fraStatus: Optional[str] = "Active"
    fraCategoryID: int
    fraOwnerID: int

    @model_validator(mode="after")
    def validate_dates_and_goal(self):
        if self.fraGoalAmount <= 0:
            raise ValueError("fraGoalAmount must be greater than 0")
        if self.fraEndDate < self.fraStartDate:
            raise ValueError("fraEndDate must be on or after fraStartDate")
        return self


class FRAActivityUpdate(BaseModel):
    fraName: Optional[str] = None
    fraDescription: Optional[str] = None
    fraGoalAmount: Optional[float] = None
    fraStartDate: Optional[date] = None
    fraEndDate: Optional[date] = None
    fraStatus: Optional[str] = None
    fraCategoryID: Optional[int] = None
    fraOwnerID: Optional[int] = None

    @model_validator(mode="after")
    def validate_dates_and_goal(self):
        if self.fraGoalAmount is not None and self.fraGoalAmount <= 0:
            raise ValueError("fraGoalAmount must be greater than 0")
        if self.fraStartDate is not None and self.fraEndDate is not None and self.fraEndDate < self.fraStartDate:
            raise ValueError("fraEndDate must be on or after fraStartDate")
        return self


class NestedCategory(BaseModel):
    categoryID: int
    categoryName: str

    class Config:
        from_attributes = True


class NestedOwner(BaseModel):
    userID: int
    username: str

    class Config:
        from_attributes = True


class FRAActivityResponse(BaseModel):
    fraID: int
    fraName: str
    fraDescription: Optional[str]
    fraGoalAmount: float
    fraStartDate: date
    fraEndDate: date
    fraStatus: str
    fraViewCount: int = 0
    fraShortlistCount: int = 0
    fraCategoryID: int
    fraOwnerID: int
    fra_category: Optional[NestedCategory] = None
    fra_owner: Optional[NestedOwner] = None

    class Config:
        from_attributes = True


def _ensure_relations_exist(db: Session, category_id: int, owner_id: int):
    category = db.query(FRACategory).filter(FRACategory.categoryID == category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid fraCategoryID")
    owner = db.query(UserAccount).filter(UserAccount.userID == owner_id).first()
    if not owner:
        raise HTTPException(status_code=400, detail="Invalid fraOwnerID")


# BCE Boundary: :CreateFRAPage
# Methods: validateRepeatFRA(...), displayDuplicateFRA(), displayFRACreatedSuccess(), displayFRACreatedFail()
@router.post("/fras", response_model=FRAActivityResponse, status_code=201)
def create_fra(payload: FRAActivityCreate, db: Session = Depends(get_db)):
    _ensure_relations_exist(db, payload.fraCategoryID, payload.fraOwnerID)
    ctrl = CreateFRAActivityController()
    result = ctrl.createFRA(
        db,
        payload.fraName,
        payload.fraDescription,
        payload.fraGoalAmount,
        payload.fraStartDate,
        payload.fraEndDate,
        payload.fraStatus or "Active",
        payload.fraCategoryID,
        payload.fraOwnerID,
    )
    if result == "duplicate":
        raise HTTPException(status_code=400, detail="displayDuplicateFRA")
    if not result:
        raise HTTPException(status_code=400, detail="displayFRACreatedFail")
    fra = db.query(FRAActivity).filter(FRAActivity.fraName == payload.fraName).first()
    return FRAActivityResponse.model_validate(fra)


# BCE Boundary: :SearchFRAPage
# Methods: displayFRAFound(result_list), displayFRANotFound()
@router.get("/fras", response_model=list[FRAActivityResponse])
def list_fras(db: Session = Depends(get_db)):
    ctrl = SearchFRAActivityController()
    results = ctrl.searchFRA(db, "")
    return [FRAActivityResponse.model_validate(r) for r in results]


# BCE Boundary: :SearchFRAPage
# Methods: displayFRAFound(result_list), displayFRANotFound()
@router.get("/fras/search", response_model=list[FRAActivityResponse])
def search_fras(q: str = "", db: Session = Depends(get_db)):
    ctrl = SearchFRAActivityController()
    results = ctrl.searchFRA(db, q)
    return [FRAActivityResponse.model_validate(r) for r in results]


# BCE Boundary: :SearchAvailableFRAPage
# Methods: displayFRA(result_list), displayFRANotFound()
@router.get("/fras/available/search", response_model=list[FRAActivityResponse])
def search_available_fras(userID: int, q: str = "", db: Session = Depends(get_db)):
    ctrl = SearchAvailableFRAController()
    results = ctrl.searchAvailableFRA(db, userID, q)
    return [FRAActivityResponse.model_validate(r) for r in results]


# BCE Boundary: :RetrieveAvailableFRAPage
# Methods: displayFRA(FRA activity)
# Side-effect: increments fraViewCount on the FRA (handled in entity).
@router.get("/fras/available/{fra_id}", response_model=FRAActivityResponse)
def get_available_fra(fra_id: int, db: Session = Depends(get_db)):
    ctrl = RetrieveAvailableFRAController()
    fra = ctrl.retrieveAvailableFRA(db, fra_id)
    if not fra:
        raise HTTPException(status_code=404, detail="FRA not found or not available")
    return FRAActivityResponse.model_validate(fra)


# BCE Boundary: :RetrieveFRAPage
@router.get("/fras/{fra_id}", response_model=FRAActivityResponse)
def get_fra(fra_id: int, db: Session = Depends(get_db)):
    ctrl = RetrieveFRAActivityController()
    fra = ctrl.retrieveFRA(db, fra_id)
    if not fra:
        raise HTTPException(status_code=404, detail="FRA not found")
    return FRAActivityResponse.model_validate(fra)


# BCE Boundary: :UpdateFRAPage
# Methods: validateEnteredData(FRA activity), displayInputErrorMessage(), displayUpdateSuccess()
@router.put("/fras/{fra_id}", response_model=FRAActivityResponse)
def update_fra(fra_id: int, payload: FRAActivityUpdate, db: Session = Depends(get_db)):
    current = FRAActivity.retrieveFRA(db, fra_id)
    if not current:
        raise HTTPException(status_code=404, detail="FRA not found")

    data = payload.model_dump(exclude_unset=True)
    data["fraID"] = fra_id

    target_category = data.get("fraCategoryID", current.fraCategoryID)
    target_owner = data.get("fraOwnerID", current.fraOwnerID)
    _ensure_relations_exist(db, target_category, target_owner)

    target_start = data.get("fraStartDate", current.fraStartDate)
    target_end = data.get("fraEndDate", current.fraEndDate)
    if target_end < target_start:
        raise HTTPException(status_code=400, detail="displayInputErrorMessage")

    ctrl = UpdateFRAActivityController()
    success = ctrl.updateFRA(db, data)
    if not success:
        raise HTTPException(status_code=400, detail="displayInputErrorMessage")
    retrieve_ctrl = RetrieveFRAActivityController()
    return FRAActivityResponse.model_validate(retrieve_ctrl.retrieveFRA(db, fra_id))


# BCE Boundary: :SuspendFRAPage
# Methods: displaySuspendSuccess(), displaySuspendFail()
@router.put("/fras/{fra_id}/suspend", response_model=FRAActivityResponse)
def suspend_fra(fra_id: int, db: Session = Depends(get_db)):
    ctrl = SuspendFRAActivityController()
    success = ctrl.suspendFRA(db, fra_id)
    if not success:
        raise HTTPException(status_code=404, detail="displaySuspendFail")
    retrieve_ctrl = RetrieveFRAActivityController()
    return FRAActivityResponse.model_validate(retrieve_ctrl.retrieveFRA(db, fra_id))
