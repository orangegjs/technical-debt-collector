from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from controls.create_fra_category_controller import CreateFRACategoryController
from controls.retrieve_fra_category_controller import RetrieveFRACategoryController
from controls.update_fra_category_controller import UpdateFRACategoryController
from controls.suspend_fra_category_controller import SuspendFRACategoryController
from controls.search_fra_category_controller import SearchFRACategoryController

router = APIRouter(prefix="/api")

# ── Pydantic schemas ─────────────────────────────────────────────────────────────

class FRACategoryCreate(BaseModel):
    categoryName: str
    categoryDescription: Optional[str] = None
    categoryStatus: Optional[str] = "Active"


class FRACategoryUpdate(BaseModel):
    categoryName: Optional[str] = None
    categoryDescription: Optional[str] = None
    categoryStatus: Optional[str] = None


class FRACategoryResponse(BaseModel):
    categoryID: int
    categoryName: str
    categoryDescription: Optional[str]
    categoryStatus: str

    class Config:
        from_attributes = True


# ── FRA Category routes ──────────────────────────────────────────────────────────

# BCE Boundary: :CreateFRACategoryPage
# Methods: validateRepeatCategory(...), displayDuplicateCategory(), displayFRACategoryCreatedSuccess(), displayFRACategoryCreatedFail()
@router.post("/categories", response_model=FRACategoryResponse, status_code=201)
def create_category(payload: FRACategoryCreate, db: Session = Depends(get_db)):
    ctrl = CreateFRACategoryController()
    result = ctrl.createCategory(db, payload.categoryName, payload.categoryDescription, payload.categoryStatus or "Active")
    if result == "duplicate":
        raise HTTPException(status_code=400, detail="displayDuplicateCategory")
    if not result:
        raise HTTPException(status_code=400, detail="displayFRACategoryCreatedFail")
    from entities.fra_category import FRACategory
    category = db.query(FRACategory).filter(FRACategory.categoryName == payload.categoryName).first()
    return category


# BCE Boundary: :FRACategoryManagementPage
# Methods: displayCategoryFound(result_list)
@router.get("/categories", response_model=list[FRACategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    ctrl = SearchFRACategoryController()
    results = ctrl.searchCategory(db, "")
    return [FRACategoryResponse.model_validate(c) for c in results]


# BCE Boundary: :SearchFRACategoryPage
# Methods: displayCategoryFound(result_list), displayCategoryNotFound()
@router.get("/categories/search")
def search_categories(q: str = "", db: Session = Depends(get_db)):
    ctrl = SearchFRACategoryController()
    results = ctrl.searchCategory(db, q)
    return [FRACategoryResponse.model_validate(c) for c in results]


# BCE Boundary: :RetrieveFRACategoryPage
# Methods: displayFRACategory(category)
@router.get("/categories/{category_id}", response_model=FRACategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    ctrl = RetrieveFRACategoryController()
    category = ctrl.retrieveCategory(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# BCE Boundary: :UpdateFRACategoryPage
# Methods: validateEnteredData(), displayInputErrorMessage(), displayUpdateSuccess()
@router.put("/categories/{category_id}", response_model=FRACategoryResponse)
def update_category(category_id: int, payload: FRACategoryUpdate, db: Session = Depends(get_db)):
    ctrl = UpdateFRACategoryController()
    data = payload.model_dump(exclude_unset=True)
    data["categoryID"] = category_id
    success = ctrl.updateCategory(db, data)
    if not success:
        raise HTTPException(status_code=400, detail="displayInputErrorMessage")
    retrieve_ctrl = RetrieveFRACategoryController()
    return retrieve_ctrl.retrieveCategory(db, category_id)


# BCE Boundary: :SuspendFRACategoryPage
# Methods: displayConfirmationMessage(), displaySuspendSuccess(), displaySuspendFail()
@router.put("/categories/{category_id}/suspend", response_model=FRACategoryResponse)
def suspend_category(category_id: int, db: Session = Depends(get_db)):
    ctrl = SuspendFRACategoryController()
    success = ctrl.suspendCategory(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="displaySuspendFail")
    retrieve_ctrl = RetrieveFRACategoryController()
    return retrieve_ctrl.retrieveCategory(db, category_id)
