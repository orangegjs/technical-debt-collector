import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_search_completed_fra.db"
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


def _create_user(username="owner1", email="owner1@test.com"):
    resp = client.post("/api/users", json={
        "username": username,
        "password": "TestPass123!",
        "email": email,
        "accountStatus": "Active",
    })
    assert resp.status_code == 201, resp.text
    return resp.json()["userID"]


def _create_fra(cat_id, owner_id, name="Test FRA", status="Completed",
                start="2024-01-01", end="2024-03-31"):
    resp = client.post("/api/fras", json={
        "fraName": name,
        "fraDescription": "A test fundraising activity",
        "fraGoalAmount": 5000.0,
        "fraStartDate": start,
        "fraEndDate": end,
        "fraStatus": status,
        "fraCategoryID": cat_id,
        "fraOwnerID": owner_id,
    })
    assert resp.status_code == 201, resp.text
    return resp.json()["fraID"]


# --- Tests ---

def test_search_completed_fra_empty_returns_empty_list():
    cat_id = _create_category()
    owner_id = _create_user()
    resp = client.get(f"/api/fras/history/search?ownerID={owner_id}&q=")
    assert resp.status_code == 200
    assert resp.json() == []


def test_search_completed_fra_only_completed_returned():
    cat_id = _create_category()
    owner_id = _create_user()
    _create_fra(cat_id, owner_id, name="Completed One", status="Completed")
    _create_fra(cat_id, owner_id, name="Active One",    status="Active")
    _create_fra(cat_id, owner_id, name="Suspended One", status="Suspended")

    resp = client.get(f"/api/fras/history/search?ownerID={owner_id}&q=")
    assert resp.status_code == 200
    names = [r["fraName"] for r in resp.json()]
    assert "Completed One" in names
    assert "Active One" not in names
    assert "Suspended One" not in names


def test_search_completed_fra_by_keyword_name():
    cat_id = _create_category()
    owner_id = _create_user()
    _create_fra(cat_id, owner_id, name="Clean Water Project", status="Completed")
    _create_fra(cat_id, owner_id, name="Education Fund",      status="Completed")

    resp = client.get(f"/api/fras/history/search?ownerID={owner_id}&q=Clean")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["fraName"] == "Clean Water Project"


def test_search_completed_fra_by_keyword_no_match():
    cat_id = _create_category()
    owner_id = _create_user()
    _create_fra(cat_id, owner_id, name="Help Campaign", status="Completed")

    resp = client.get(f"/api/fras/history/search?ownerID={owner_id}&q=NOMATCH_XYZ")
    assert resp.status_code == 200
    assert resp.json() == []


def test_search_completed_fra_by_service_type():
    cat_health = _create_category(name="Health")
    cat_edu    = _create_category(name="Education")
    owner_id   = _create_user()
    _create_fra(cat_health, owner_id, name="Health FRA", status="Completed")
    _create_fra(cat_edu,    owner_id, name="Edu FRA",    status="Completed")

    resp = client.get(f"/api/fras/history/search?ownerID={owner_id}&q=&serviceType=Health")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["fraName"] == "Health FRA"


def test_search_completed_fra_by_date_range():
    cat_id   = _create_category()
    owner_id = _create_user()
    _create_fra(cat_id, owner_id, name="Early FRA", status="Completed",
                start="2023-01-01", end="2023-06-30")
    _create_fra(cat_id, owner_id, name="Late FRA",  status="Completed",
                start="2024-01-01", end="2024-12-31")

    resp = client.get(
        f"/api/fras/history/search?ownerID={owner_id}&q="
        f"&startDate=2024-01-01&endDate=2024-12-31"
    )
    assert resp.status_code == 200
    results = resp.json()
    names = [r["fraName"] for r in results]
    assert "Late FRA" in names
    assert "Early FRA" not in names


def test_search_completed_fra_all_filters_combined():
    cat_health = _create_category(name="Health")
    cat_edu    = _create_category(name="Education")
    owner_id   = _create_user()
    _create_fra(cat_health, owner_id, name="Health 2024", status="Completed",
                start="2024-01-01", end="2024-06-30")
    _create_fra(cat_edu,    owner_id, name="Edu 2024",    status="Completed",
                start="2024-01-01", end="2024-06-30")
    _create_fra(cat_health, owner_id, name="Health 2023", status="Completed",
                start="2023-01-01", end="2023-06-30")

    resp = client.get(
        f"/api/fras/history/search?ownerID={owner_id}"
        f"&q=Health&serviceType=Health"
        f"&startDate=2024-01-01&endDate=2024-12-31"
    )
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["fraName"] == "Health 2024"


def test_search_completed_fra_only_own_owner_returned():
    cat_id   = _create_category()
    owner1   = _create_user(username="owner1", email="o1@test.com")
    owner2   = _create_user(username="owner2", email="o2@test.com")
    _create_fra(cat_id, owner1, name="Owner1 FRA", status="Completed")
    _create_fra(cat_id, owner2, name="Owner2 FRA", status="Completed")

    resp = client.get(f"/api/fras/history/search?ownerID={owner1}&q=")
    assert resp.status_code == 200
    names = [r["fraName"] for r in resp.json()]
    assert "Owner1 FRA" in names
    assert "Owner2 FRA" not in names
