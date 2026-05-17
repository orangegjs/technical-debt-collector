import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_retrieve_completed_fra.db"
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
    assert resp.status_code == 201, resp.text
    return resp.json()["categoryID"]


def _create_user(username="fraowner", email="owner@test.com"):
    resp = client.post("/api/users", json={
        "username": username,
        "password": "TestPass123!",
        "email": email,
        "accountStatus": "Active",
    })
    assert resp.status_code == 201, resp.text
    return resp.json()["userID"]


def _create_fra(cat_id, owner_id, name="Test FRA", status="Completed"):
    resp = client.post("/api/fras", json={
        "fraName": name,
        "fraDescription": "A test fundraising activity",
        "fraGoalAmount": 5000.0,
        "fraStartDate": "2024-01-01",
        "fraEndDate": "2024-06-30",
        "fraStatus": status,
        "fraCategoryID": cat_id,
        "fraOwnerID": owner_id,
    })
    assert resp.status_code == 201, resp.text
    return resp.json()["fraID"]


# --- Tests ---

def test_retrieve_completed_fra_success():
    cat_id   = _create_category()
    owner_id = _create_user()
    fra_id   = _create_fra(cat_id, owner_id, name="Completed FRA", status="Completed")

    resp = client.get(f"/api/fras/history/{fra_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["fraID"] == fra_id
    assert data["fraStatus"] == "Completed"
    assert data["fraName"] == "Completed FRA"


def test_retrieve_completed_fra_returns_404_for_active():
    cat_id   = _create_category()
    owner_id = _create_user()
    fra_id   = _create_fra(cat_id, owner_id, name="Active FRA", status="Active")

    resp = client.get(f"/api/fras/history/{fra_id}")
    assert resp.status_code == 404


def test_retrieve_completed_fra_returns_404_for_suspended():
    cat_id   = _create_category()
    owner_id = _create_user()
    fra_id   = _create_fra(cat_id, owner_id, name="Suspended FRA", status="Suspended")

    resp = client.get(f"/api/fras/history/{fra_id}")
    assert resp.status_code == 404


def test_retrieve_completed_fra_returns_404_for_nonexistent_id():
    resp = client.get("/api/fras/history/99999")
    assert resp.status_code == 404


def test_retrieve_completed_fra_does_not_increment_view_count():
    cat_id   = _create_category()
    owner_id = _create_user()
    fra_id   = _create_fra(cat_id, owner_id, name="View Count FRA", status="Completed")

    resp1 = client.get(f"/api/fras/history/{fra_id}")
    assert resp1.status_code == 200
    view1 = resp1.json()["fraViewCount"]

    resp2 = client.get(f"/api/fras/history/{fra_id}")
    assert resp2.status_code == 200
    view2 = resp2.json()["fraViewCount"]

    assert view1 == view2  # no side-effect unlike retrieveAvailableFRA
