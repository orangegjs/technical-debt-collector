import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_available_fra.db"
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


def _create_user(username="fraowner", email="owner@test.com"):
    resp = client.post("/api/users", json={
        "username": username,
        "password": "TestPass123!",
        "email": email,
        "accountStatus": "Active",
    })
    return resp.json()["userID"]


def _create_fra(cat_id, owner_id, name="Test FRA", status="Active"):
    resp = client.post("/api/fras", json={
        "fraName": name,
        "fraDescription": "A test fundraising activity",
        "fraGoalAmount": 5000.0,
        "fraStartDate": "2024-01-01",
        "fraEndDate": "2025-12-31",
        "fraStatus": status,
        "fraCategoryID": cat_id,
        "fraOwnerID": owner_id,
    })
    assert resp.status_code == 201, resp.text
    return resp.json()["fraID"]


def test_search_available_fra_matches_keyword():
    cat_id = _create_category()
    owner_id = _create_user()
    _create_fra(cat_id, owner_id, name="Clean Water Campaign")
    _create_fra(cat_id, owner_id, name="Education Fund", status="Active")

    resp = client.get("/api/fras/available/search?userID=1&q=Clean")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["fraName"] == "Clean Water Campaign"


def test_search_available_fra_empty_keyword_returns_all_active():
    cat_id = _create_category()
    owner_id = _create_user()
    _create_fra(cat_id, owner_id, name="Active FRA 1")
    _create_fra(cat_id, owner_id, name="Active FRA 2")
    _create_fra(cat_id, owner_id, name="Suspended FRA", status="Suspended")

    resp = client.get("/api/fras/available/search?userID=1&q=")
    assert resp.status_code == 200
    results = resp.json()
    names = [r["fraName"] for r in results]
    assert "Active FRA 1" in names
    assert "Active FRA 2" in names
    assert "Suspended FRA" not in names


def test_search_available_fra_no_match_returns_empty_not_404():
    cat_id = _create_category()
    owner_id = _create_user()
    _create_fra(cat_id, owner_id, name="Help Campaign")

    resp = client.get("/api/fras/available/search?userID=1&q=NOMATCH_XYZ")
    assert resp.status_code == 200
    assert resp.json() == []


def test_retrieve_available_fra_success():
    cat_id = _create_category()
    owner_id = _create_user()
    fra_id = _create_fra(cat_id, owner_id)

    resp = client.get(f"/api/fras/available/{fra_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["fraID"] == fra_id
    assert data["fraStatus"] == "Active"


def test_retrieve_available_fra_not_found_returns_404():
    resp = client.get("/api/fras/available/99999")
    assert resp.status_code == 404


def test_retrieve_available_fra_increments_view_count():
    cat_id = _create_category()
    owner_id = _create_user()
    fra_id = _create_fra(cat_id, owner_id)

    resp1 = client.get(f"/api/fras/available/{fra_id}")
    assert resp1.status_code == 200
    assert resp1.json()["fraViewCount"] == 1

    resp2 = client.get(f"/api/fras/available/{fra_id}")
    assert resp2.status_code == 200
    assert resp2.json()["fraViewCount"] == 2
