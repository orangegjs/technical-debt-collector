import pytest
from datetime import date, timedelta
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from entities.donation import Donation

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_donation.db"
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


def _create_category(name="Test Category"):
    resp = client.post("/api/categories", json={
        "categoryName": name,
        "categoryDescription": "Test",
        "categoryStatus": "Active",
    })
    return resp.json()["categoryID"]


def _create_user(username="testuser", email="test@test.com"):
    resp = client.post("/api/users", json={
        "username": username,
        "password": "TestPass123!",
        "email": email,
        "accountStatus": "Active",
    })
    return resp.json()["userID"]


def _create_fra(cat_id, owner_id, name="Test FRA"):
    resp = client.post("/api/fras", json={
        "fraName": name,
        "fraDescription": "Test FRA",
        "fraGoalAmount": 5000.0,
        "fraStartDate": "2024-01-01",
        "fraEndDate": "2025-12-31",
        "fraStatus": "Active",
        "fraCategoryID": cat_id,
        "fraOwnerID": owner_id,
    })
    assert resp.status_code == 201, resp.text
    return resp.json()["fraID"]


def _insert_donation(fra_id, user_id, amount=100.0, status="Completed", days_ago=0):
    db = TestingSessionLocal()
    try:
        don = Donation(
            donationAmount=Decimal(str(amount)),
            donationDate=date.today() - timedelta(days=days_ago),
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


def test_search_donation_with_keyword():
    cat_id = _create_category()
    owner_id = _create_user("owner1", "owner1@test.com")
    donee_id = _create_user("donee1", "donee1@test.com")
    fra_id = _create_fra(cat_id, owner_id, "Clean Water FRA")
    _insert_donation(fra_id, donee_id, amount=150.0)

    resp = client.get(f"/api/donations/search?userID={donee_id}&q=Clean")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["fra"]["fraName"] == "Clean Water FRA"


def test_search_donation_with_category():
    cat_id = _create_category("Health Category")
    owner_id = _create_user("owner2", "owner2@test.com")
    donee_id = _create_user("donee2", "donee2@test.com")
    fra_id = _create_fra(cat_id, owner_id, "Health FRA")
    _insert_donation(fra_id, donee_id, amount=200.0)

    resp = client.get(f"/api/donations/search?userID={donee_id}&category=Health+Category")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1


def test_search_donation_with_date_range():
    cat_id = _create_category()
    owner_id = _create_user("owner3", "owner3@test.com")
    donee_id = _create_user("donee3", "donee3@test.com")
    fra_id = _create_fra(cat_id, owner_id, "Date Range FRA")
    _insert_donation(fra_id, donee_id, amount=100.0, days_ago=10)
    _insert_donation(fra_id, donee_id, amount=100.0, days_ago=60)

    start = (date.today() - timedelta(days=20)).isoformat()
    end = date.today().isoformat()
    resp = client.get(f"/api/donations/search?userID={donee_id}&startDate={start}&endDate={end}")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1


def test_search_donation_all_filters_combined():
    cat_id = _create_category("Combined Cat")
    owner_id = _create_user("owner4", "owner4@test.com")
    donee_id = _create_user("donee4", "donee4@test.com")
    fra_id = _create_fra(cat_id, owner_id, "Combined FRA")
    _insert_donation(fra_id, donee_id, amount=300.0, days_ago=5)

    start = (date.today() - timedelta(days=10)).isoformat()
    end = date.today().isoformat()
    resp = client.get(
        f"/api/donations/search?userID={donee_id}&q=Combined&category=Combined+Cat"
        f"&startDate={start}&endDate={end}"
    )
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1


def test_search_donation_empty_returns_empty_not_404():
    donee_id = _create_user("donee5", "donee5@test.com")
    resp = client.get(f"/api/donations/search?userID={donee_id}&q=NOMATCH")
    assert resp.status_code == 200
    assert resp.json() == []


def test_retrieve_donation_success_with_fra_progress():
    cat_id = _create_category()
    owner_id = _create_user("owner6", "owner6@test.com")
    donee_id = _create_user("donee6", "donee6@test.com")
    fra_id = _create_fra(cat_id, owner_id, "Progress FRA")
    don_id = _insert_donation(fra_id, donee_id, amount=500.0, status="Completed")

    resp = client.get(f"/api/donations/{don_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["donationID"] == don_id
    assert "fraProgress" in data
    assert data["fraProgress"] is not None
    assert isinstance(data["fraProgress"], float)


def test_retrieve_donation_not_found_returns_404():
    resp = client.get("/api/donations/99999")
    assert resp.status_code == 404
