from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_generate_report.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database():
    previous_override = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if previous_override is not None:
        app.dependency_overrides[get_db] = previous_override
    else:
        app.dependency_overrides.pop(get_db, None)


client = TestClient(app)


def _create_category(name="Health"):
    resp = client.post("/api/categories", json={
        "categoryName": name,
        "categoryDescription": "Test",
        "categoryStatus": "Active",
    })
    assert resp.status_code == 201, resp.text
    return resp.json()["categoryID"]


def _create_user(username="user1", email="user1@test.com"):
    resp = client.post("/api/users", json={
        "username": username,
        "password": "TestPass123!",
        "email": email,
        "accountStatus": "Active",
    })
    assert resp.status_code == 201, resp.text
    return resp.json()["userID"]


def _create_fra(cat_id, owner_id, name, start_date: str):
    resp = client.post("/api/fras", json={
        "fraName": name,
        "fraDescription": "Test",
        "fraGoalAmount": 1000.0,
        "fraStartDate": start_date,
        "fraEndDate": "2099-12-31",
        "fraStatus": "Active",
        "fraCategoryID": cat_id,
        "fraOwnerID": owner_id,
    })
    assert resp.status_code == 201, resp.text
    return resp.json()["fraID"]


def _create_donation(fra_id, user_id, donation_date: str, status="Completed"):
    from entities.donation import Donation
    db = TestingSessionLocal()
    try:
        don = Donation(
            donationAmount=100,
            donationDate=date.fromisoformat(donation_date),
            donationStatus=status,
            fraID=fra_id,
            userID=user_id,
        )
        db.add(don)
        db.commit()
        db.refresh(don)
        return don.donationID
    finally:
        db.close()


# --- Tests ---

def test_generate_daily_report_date_range():
    resp = client.post("/api/reports/generate?reportType=daily")
    assert resp.status_code == 201
    data = resp.json()
    today = date.today().isoformat()
    assert data["startDate"] == today
    assert data["endDate"] == today
    assert data["reportType"] == "daily"


def test_generate_weekly_report_date_range():
    resp = client.post("/api/reports/generate?reportType=weekly")
    assert resp.status_code == 201
    data = resp.json()
    today = date.today()
    assert data["startDate"] == (today - timedelta(days=6)).isoformat()
    assert data["endDate"] == today.isoformat()
    assert data["reportType"] == "weekly"


def test_generate_monthly_report_date_range():
    resp = client.post("/api/reports/generate?reportType=monthly")
    assert resp.status_code == 201
    data = resp.json()
    today = date.today()
    assert data["startDate"] == (today - timedelta(days=29)).isoformat()
    assert data["endDate"] == today.isoformat()
    assert data["reportType"] == "monthly"


def test_generate_report_invalid_type_returns_400():
    resp = client.post("/api/reports/generate?reportType=yearly")
    assert resp.status_code == 400


def test_generate_report_total_fra_count():
    today = date.today().isoformat()
    cat_id  = _create_category()
    user_id = _create_user()
    _create_fra(cat_id, user_id, "FRA Today 1", today)
    _create_fra(cat_id, user_id, "FRA Today 2", today)

    resp = client.post("/api/reports/generate?reportType=daily")
    assert resp.status_code == 201
    assert resp.json()["totalFRA"] >= 2


def test_generate_report_total_donation_count():
    cat_id  = _create_category(name="Charity")
    user_id = _create_user(username="donor", email="donor@test.com")
    fra_id  = _create_fra(cat_id, user_id, "Donation FRA", date.today().isoformat())

    today = date.today().isoformat()
    _create_donation(fra_id, user_id, today, status="Completed")
    _create_donation(fra_id, user_id, today, status="Completed")
    _create_donation(fra_id, user_id, today, status="Failed")   # should not count

    resp = client.post("/api/reports/generate?reportType=daily")
    assert resp.status_code == 201
    assert resp.json()["totalDonation"] >= 2


def test_generate_report_total_account_is_system_wide():
    _create_user(username="acct1", email="acct1@test.com")
    _create_user(username="acct2", email="acct2@test.com")
    _create_user(username="acct3", email="acct3@test.com")

    resp = client.post("/api/reports/generate?reportType=daily")
    assert resp.status_code == 201
    assert resp.json()["totalAccount"] >= 3


def test_generate_report_persists_all_fields():
    resp = client.post("/api/reports/generate?reportType=weekly")
    assert resp.status_code == 201
    data = resp.json()
    assert "reportID" in data
    assert data["reportID"] > 0
    assert "totalFRA" in data
    assert "totalDonation" in data
    assert "totalAccount" in data
    assert data["reportType"] == "weekly"
    assert data["startDate"] is not None
    assert data["endDate"] is not None


def test_generate_report_with_explicit_dates():
    resp = client.post(
        "/api/reports/generate?reportType=daily"
        "&startDate=2024-01-01&endDate=2024-01-01"
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["startDate"] == "2024-01-01"
    assert data["endDate"] == "2024-01-01"
