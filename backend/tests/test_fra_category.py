import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# In-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_fra_category.db"
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
    """Create fresh database tables and set DB override before each test"""
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


def test_create_fra_category_success():
    response = client.post(
        "/api/categories",
        json={
            "categoryName": "Education",
            "categoryDescription": "Supporting educational initiatives.",
            "categoryStatus": "Active",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["categoryName"] == "Education"
    assert data["categoryDescription"] == "Supporting educational initiatives."
    assert data["categoryStatus"] == "Active"
    assert "categoryID" in data


def test_create_fra_category_duplicate():
    client.post(
        "/api/categories",
        json={"categoryName": "Healthcare", "categoryDescription": "Medical support.", "categoryStatus": "Active"},
    )
    response = client.post(
        "/api/categories",
        json={"categoryName": "Healthcare", "categoryDescription": "Duplicate category.", "categoryStatus": "Active"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "displayDuplicateCategory"


def test_retrieve_fra_category_success():
    create_resp = client.post(
        "/api/categories",
        json={"categoryName": "Environment", "categoryDescription": "Green initiatives.", "categoryStatus": "Active"},
    )
    category_id = create_resp.json()["categoryID"]

    response = client.get(f"/api/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["categoryName"] == "Environment"
    assert data["categoryID"] == category_id


def test_retrieve_fra_category_not_found():
    response = client.get("/api/categories/99999")
    assert response.status_code == 404


def test_update_fra_category_success():
    create_resp = client.post(
        "/api/categories",
        json={"categoryName": "Sports", "categoryDescription": "Original description.", "categoryStatus": "Active"},
    )
    category_id = create_resp.json()["categoryID"]

    response = client.put(
        f"/api/categories/{category_id}",
        json={"categoryDescription": "Updated description."},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["categoryDescription"] == "Updated description."
    assert data["categoryName"] == "Sports"


def test_suspend_fra_category_sets_inactive():
    create_resp = client.post(
        "/api/categories",
        json={"categoryName": "Arts", "categoryDescription": "Cultural arts.", "categoryStatus": "Active"},
    )
    category_id = create_resp.json()["categoryID"]

    response = client.put(f"/api/categories/{category_id}/suspend")
    assert response.status_code == 200
    data = response.json()
    assert data["categoryStatus"] == "Inactive"


def test_search_fra_category_returns_matches():
    client.post(
        "/api/categories",
        json={"categoryName": "Technology Alpha", "categoryDescription": "Tech category.", "categoryStatus": "Active"},
    )
    client.post(
        "/api/categories",
        json={"categoryName": "Technology Beta", "categoryDescription": "Another tech.", "categoryStatus": "Active"},
    )
    client.post(
        "/api/categories",
        json={"categoryName": "Unrelated Category", "categoryDescription": "Something else.", "categoryStatus": "Active"},
    )

    response = client.get("/api/categories/search?q=Technology")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    names = [r["categoryName"] for r in results]
    assert "Technology Alpha" in names
    assert "Technology Beta" in names
