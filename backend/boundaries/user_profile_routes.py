from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from controls.create_user_profile_controller import CreateUserProfileController
from controls.retrieve_user_profile_controller import RetrieveUserProfileController
from controls.update_user_profile_controller import UpdateUserProfileController
from controls.suspend_user_profile_controller import SuspendUserProfileController
from controls.search_user_profile_controller import SearchUserProfileController

router = APIRouter(prefix="/api")

# ── Pydantic schemas ─────────────────────────────────────────────────────────────

class UserProfileCreate(BaseModel):
    profileName: str
    profileDescription: Optional[str] = None


class UserProfileUpdate(BaseModel):
    profileName: Optional[str] = None
    profileDescription: Optional[str] = None


class UserProfileResponse(BaseModel):
    profileID: int
    profileName: str
    profileDescription: Optional[str]
    profileStatus: str

    class Config:
        from_attributes = True


# ── Profile routes ───────────────────────────────────────────────────────────────

# BCE Boundary: :CreateUserProfilePage
# Methods: validateRepeatProfile(), displayDuplicateProfile(), displayUserProfileCreatedSuccess(), displayUserProfileCreatedFail()
@router.post("/profiles", response_model=UserProfileResponse, status_code=201)
def create_profile(payload: UserProfileCreate, db: Session = Depends(get_db)):
    ctrl = CreateUserProfileController()
    result = ctrl.createUserProfile(db, payload.profileName, payload.profileDescription)
    if result == "duplicate":
        raise HTTPException(status_code=400, detail="displayDuplicateProfile")
    if not result:
        raise HTTPException(status_code=400, detail="displayUserProfileCreatedFail")
    from entities.user_profile import UserProfile
    profile = db.query(UserProfile).filter(UserProfile.profileName == payload.profileName).first()
    return profile


# BCE Boundary: :SearchUserProfilePage
# Methods: displayProfileFound(result_list), displayProfileNotFound()
@router.get("/profiles/search")
def search_profiles(q: str = "", db: Session = Depends(get_db)):
    ctrl = SearchUserProfileController()
    results = ctrl.searchUserProfile(db, q)
    return [UserProfileResponse.model_validate(p) for p in results]


# BCE Boundary: :RetrieveUserProfilePage
# Methods: displayUserProfile()
@router.get("/profiles/{profile_id}", response_model=UserProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    ctrl = RetrieveUserProfileController()
    profile = ctrl.retrieveUserProfile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


# BCE Boundary: :UpdateUserProfilePage
# Methods: validateEnteredData(), displayInputErrorMessage(), displayUpdateSuccess()
@router.put("/profiles/{profile_id}", response_model=UserProfileResponse)
def update_profile(profile_id: int, payload: UserProfileUpdate, db: Session = Depends(get_db)):
    ctrl = UpdateUserProfileController()
    data = payload.model_dump(exclude_unset=True)
    data["profileID"] = profile_id
    success = ctrl.updateUserProfile(db, data)
    if not success:
        raise HTTPException(status_code=400, detail="displayInputErrorMessage")
    retrieve_ctrl = RetrieveUserProfileController()
    return retrieve_ctrl.retrieveUserProfile(db, profile_id)


# BCE Boundary: :SuspendUserProfilePage
# Methods: displayConfirmationMessage(), displaySuspendSuccess(), displaySuspendFail()
@router.put("/profiles/{profile_id}/suspend", response_model=UserProfileResponse)
def suspend_profile(profile_id: int, db: Session = Depends(get_db)):
    ctrl = SuspendUserProfileController()
    success = ctrl.suspendUserProfile(db, profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="displaySuspendFail")
    retrieve_ctrl = RetrieveUserProfileController()
    return retrieve_ctrl.retrieveUserProfile(db, profile_id)
