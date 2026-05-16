"""
TDD — Sprint 2 User Profile: Search User Profile
BCE Boundary: :SearchUserProfilePage / :UserProfileManagementPage
Controller:   SearchUserProfileController
Entity:       UserProfile.searchUserProfile()

Red  phase: Stub controller returns [] for every keyword → match assertions fail.
Green phase: Real controller does ILIKE filter → correct profiles returned.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_search_user_profile.db"
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


def _seed_profiles():
    """Insert 3 profiles for search tests."""
    client.post("/api/profiles", json={"profileName": "Donee", "profileDescription": "Receives funds.", "profileStatus": "Active"})
    client.post("/api/profiles", json={"profileName": "Fund Raiser", "profileDescription": "Raises funds.", "profileStatus": "Active"})
    client.post("/api/profiles", json={"profileName": "Platform Management", "profileDescription": "Manages platform.", "profileStatus": "Active"})


def test_search_returns_matching_profiles():
    """GET /api/profiles/search?q=Fund returns only profiles whose name contains 'Fund'."""
    _seed_profiles()

    response = client.get("/api/profiles/search?q=Fund")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["profileName"] == "Fund Raiser"


def test_search_empty_keyword_returns_all():
    """GET /api/profiles/search?q= (empty string) returns every profile."""
    _seed_profiles()

    response = client.get("/api/profiles/search?q=")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_search_no_match_returns_empty_list():
    """GET /api/profiles/search?q=nonexistent returns an empty list (not 404)."""
    _seed_profiles()

    response = client.get("/api/profiles/search?q=nonexistent")
    assert response.status_code == 200
    assert response.json() == []


def test_list_all_profiles_via_get_profiles():
    """GET /api/profiles (no query param) returns every profile — used by management page on load."""
    _seed_profiles()

    response = client.get("/api/profiles")
    assert response.status_code == 200
    assert len(response.json()) == 3
