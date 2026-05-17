import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_favourite.db"
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
        "fraDescription": "Test FRA description",
        "fraGoalAmount": 5000.0,
        "fraStartDate": "2024-01-01",
        "fraEndDate": "2025-12-31",
        "fraStatus": "Active",
        "fraCategoryID": cat_id,
        "fraOwnerID": owner_id,
    })
    assert resp.status_code == 201, resp.text
    return resp.json()["fraID"]


def test_save_fra_success_returns_201():
    cat_id = _create_category()
    owner_id = _create_user("owner", "owner@test.com")
    donee_id = _create_user("donee", "donee@test.com")
    fra_id = _create_fra(cat_id, owner_id)

    resp = client.post("/api/favourites", json={"fraID": fra_id, "userID": donee_id})
    assert resp.status_code == 201
    data = resp.json()
    assert data["fraID"] == fra_id
    assert data["userID"] == donee_id
    assert "favouriteID" in data


def test_save_fra_increments_shortlist_count():
    cat_id = _create_category()
    owner_id = _create_user("owner2", "owner2@test.com")
    donee_id = _create_user("donee2", "donee2@test.com")
    fra_id = _create_fra(cat_id, owner_id)

    # Get initial shortlist count
    fra_resp = client.get(f"/api/fras/{fra_id}")
    initial = fra_resp.json()["fraShortlistCount"]

    client.post("/api/favourites", json={"fraID": fra_id, "userID": donee_id})

    fra_resp2 = client.get(f"/api/fras/{fra_id}")
    assert fra_resp2.json()["fraShortlistCount"] == initial + 1


def test_save_fra_duplicate_returns_400():
    cat_id = _create_category()
    owner_id = _create_user("owner3", "owner3@test.com")
    donee_id = _create_user("donee3", "donee3@test.com")
    fra_id = _create_fra(cat_id, owner_id)

    client.post("/api/favourites", json={"fraID": fra_id, "userID": donee_id})
    resp = client.post("/api/favourites", json={"fraID": fra_id, "userID": donee_id})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "displayDuplicateFRASaved"


def test_search_favourites_returns_correct_user_rows():
    cat_id = _create_category()
    owner_id = _create_user("owner4", "owner4@test.com")
    donee_a = _create_user("doneeA", "doneeA@test.com")
    donee_b = _create_user("doneeB", "doneeB@test.com")
    fra1 = _create_fra(cat_id, owner_id, "FRA Alpha")
    fra2 = _create_fra(cat_id, owner_id, "FRA Beta")

    client.post("/api/favourites", json={"fraID": fra1, "userID": donee_a})
    client.post("/api/favourites", json={"fraID": fra2, "userID": donee_b})

    resp = client.get(f"/api/favourites/search?userID={donee_a}")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["fraID"] == fra1


def test_search_favourites_keyword_filters_correctly():
    cat_id = _create_category()
    owner_id = _create_user("owner5", "owner5@test.com")
    donee_id = _create_user("donee5", "donee5@test.com")
    fra1 = _create_fra(cat_id, owner_id, "Clean Water Project")
    fra2 = _create_fra(cat_id, owner_id, "Education Initiative")
    client.post("/api/favourites", json={"fraID": fra1, "userID": donee_id})
    client.post("/api/favourites", json={"fraID": fra2, "userID": donee_id})

    resp = client.get(f"/api/favourites/search?userID={donee_id}&q=Clean")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["fra"]["fraName"] == "Clean Water Project"


def test_retrieve_favourite_success():
    cat_id = _create_category()
    owner_id = _create_user("owner6", "owner6@test.com")
    donee_id = _create_user("donee6", "donee6@test.com")
    fra_id = _create_fra(cat_id, owner_id)
    client.post("/api/favourites", json={"fraID": fra_id, "userID": donee_id})

    resp = client.get(f"/api/favourites/{donee_id}/{fra_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["fraID"] == fra_id
    assert data["userID"] == donee_id


def test_retrieve_favourite_not_found_returns_404():
    resp = client.get("/api/favourites/99999/99999")
    assert resp.status_code == 404
