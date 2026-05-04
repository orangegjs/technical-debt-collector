from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from database import get_db
from controls.login_controller import LoginController
from controls.logout_controller import LogoutController
from controls.create_user_account_controller import CreateUserAccountController
from controls.retrieve_user_account_controller import RetrieveUserAccountController
from controls.update_user_account_controller import UpdateUserAccountController
from controls.suspend_user_account_controller import SuspendUserAccountController
from controls.search_user_account_controller import SearchUserAccountController

router = APIRouter(prefix="/api")

# ── Pydantic schemas ────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class UserAccountCreate(BaseModel):
    username: str
    password: str
    email: str
    accountStatus: str = "Active"
    role: str
    profile_picture_url: Optional[str] = None


class UserAccountUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    accountStatus: Optional[str] = None
    role: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UserAccountResponse(BaseModel):
    userID: int
    username: str
    email: Optional[str]
    accountStatus: str
    role: Optional[str]
    profile_picture_url: Optional[str] = None

    class Config:
        from_attributes = True


# ── Auth routes ────────────────────────────────────────────────────────────────

# BCE Boundary: :LoginPage
# Methods: displayUserAdminDashboard(), displayLoginFail()
@router.post("/auth/login", response_model=UserAccountResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    ctrl = LoginController()
    user = ctrl.login(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user


# BCE Boundary: :LogoutPage
@router.post("/auth/logout")
def logout():
    ctrl = LogoutController()
    return ctrl.logout()


# ── User account routes ────────────────────────────────────────────────────────

# BCE Boundary: :CreateAccountPage
# Methods: validateInput(username, password, name, email, accountStatus, role), displayInvalidInput(),
#          displayUserAccountCreatedSuccess(), displayUserAccountCreatedFail()
@router.post("/users", response_model=UserAccountResponse, status_code=201)
def create_user(payload: UserAccountCreate, db: Session = Depends(get_db)):
    ctrl = CreateUserAccountController()
    success = ctrl.createUserAccount(
        db,
        username=payload.username,
        password=payload.password,
        email=payload.email,
        accountStatus=payload.accountStatus,
        role=payload.role,
        profile_picture_url=payload.profile_picture_url,
    )
    if not success:
        raise HTTPException(status_code=400, detail="displayUserAccountCreatedFail")
    from entities.user_account import UserAccount as UA
    user = db.query(UA).filter(UA.username == payload.username).first()
    return user


# BCE Boundary: :SearchUserAccountPage
# Methods: displayUserFound(result_list), displayUserNotFound()
@router.get("/users/search")
def search_users(q: str = "", db: Session = Depends(get_db)):
    ctrl = SearchUserAccountController()
    results = ctrl.searchUserAcc(db, q)
    return [UserAccountResponse.model_validate(u) for u in results]


# BCE Boundary: :RetrieveUserAccountPage
# Methods: displayAccountDetails()
@router.get("/users/{user_id}", response_model=UserAccountResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    ctrl = RetrieveUserAccountController()
    user = ctrl.retrieveUserAccount(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# BCE Boundary: :UpdateUserAccountPage
# Methods: displayInputErrorMessage()
@router.put("/users/{user_id}", response_model=UserAccountResponse)
def update_user(user_id: int, payload: UserAccountUpdate, db: Session = Depends(get_db)):
    ctrl = UpdateUserAccountController()
    data = payload.model_dump(exclude_unset=True)
    data["userID"] = user_id
    success = ctrl.updateUserAccount(db, data)
    if not success:
        raise HTTPException(status_code=400, detail="displayInputErrorMessage")
    retrieve_ctrl = RetrieveUserAccountController()
    return retrieve_ctrl.retrieveUserAccount(db, user_id)


# BCE Boundary: :SuspendUserAccountPage
# Methods: displayConfirmationMessage(), displaySuspendSuccess(), displaySuspendFail()
@router.put("/users/{user_id}/suspend", response_model=UserAccountResponse)
def suspend_user(user_id: int, db: Session = Depends(get_db)):
    ctrl = SuspendUserAccountController()
    success = ctrl.suspendUserAccount(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="displaySuspendFail")
    retrieve_ctrl = RetrieveUserAccountController()
    return retrieve_ctrl.retrieveUserAccount(db, user_id)
