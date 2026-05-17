from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from controls.generate_report_controller import GenerateReportController
from database import get_db

router = APIRouter(prefix="/api")


class ReportResponse(BaseModel):
    reportID: int
    reportType: str
    startDate: date
    endDate: date
    totalFRA: int
    totalDonation: int
    totalAccount: int

    class Config:
        from_attributes = True


# BCE Boundary: :GenerateReportPage
# US#38/39/40: displayReport(Report result)
@router.post("/reports/generate", response_model=ReportResponse, status_code=201)
def generate_report(
    reportType: str,
    startDate: Optional[date] = Query(None),
    endDate: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    if reportType not in ("daily", "weekly", "monthly"):
        raise HTTPException(status_code=400, detail="reportType must be daily, weekly, or monthly")
    ctrl = GenerateReportController()
    try:
        report = ctrl.generateReport(db, reportType, startDate, endDate)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ReportResponse.model_validate(report)
