from datetime import date
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from controls.search_donation_controller import SearchDonationController
from controls.retrieve_donation_controller import RetrieveDonationController
from database import get_db
from boundaries.fra_activity_routes import FRAActivityResponse

router = APIRouter(prefix="/api")


class DonationResponse(BaseModel):
    donationID: int
    donationAmount: Decimal
    donationDate: date
    donationStatus: str
    fraID: int
    userID: int
    fra: Optional[FRAActivityResponse] = None
    fraProgress: Optional[float] = None  # 0.0–1.0+, computed server-side

    class Config:
        from_attributes = True


def _compute_progress(db: Session, fraID: int, fraGoalAmount: float) -> float:
    from entities.donation import Donation
    total = db.query(func.sum(Donation.donationAmount)).filter(
        Donation.fraID == fraID,
        Donation.donationStatus == "Completed",
    ).scalar() or 0
    if fraGoalAmount and fraGoalAmount > 0:
        return float(total) / float(fraGoalAmount)
    return 0.0


def _to_donation_response(don, db: Session) -> DonationResponse:
    progress = None
    if don.fra:
        progress = _compute_progress(db, don.fraID, float(don.fra.fraGoalAmount))
    resp = DonationResponse.model_validate(don)
    resp.fraProgress = progress
    return resp


# BCE Boundary: :SearchDonationPage
# Methods: displayDonation(result_list), displayDonationNotFound()
@router.get("/donations/search", response_model=list[DonationResponse])
def search_donations(
    userID: int,
    q: str = "",
    category: Optional[str] = None,
    startDate: Optional[date] = Query(None),
    endDate: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    ctrl = SearchDonationController()
    results = ctrl.searchDonation(db, userID, q, category, startDate, endDate)
    return [_to_donation_response(r, db) for r in results]


# BCE Boundary: :RetrieveDonationPage
# Methods: displayDonation(Donation don)
@router.get("/donations/{donation_id}", response_model=DonationResponse)
def get_donation(donation_id: int, db: Session = Depends(get_db)):
    ctrl = RetrieveDonationController()
    don = ctrl.retrieveDonation(db, donation_id)
    if not don:
        raise HTTPException(status_code=404, detail="Donation not found")
    return _to_donation_response(don, db)
