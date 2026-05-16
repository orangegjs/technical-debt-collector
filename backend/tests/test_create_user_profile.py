"""
TDD — Sprint 2 User Profile: Create User Profile
BCE Boundary: :CreateUserProfilePage
Controller:   CreateUserProfileController
Entity:       UserProfile.createUserProfile()

Red  phase: Stub controller returns "duplicate"/False for everything → tests fail.
Green phase: Real controller delegates to entity → tests pass.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_create_user_profile.db"
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


def test_create_user_profile_success():
    """POST /api/profiles with valid data returns 201 and the created profile."""
    response = client.post(
        "/api/profiles",
        json={
            "profileName": "Donee",
            "profileDescription": "A user who receives funds.",
            "profileStatus": "Active",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["profileName"] == "Donee"
    assert data["profileDescription"] == "A user who receives funds."
    assert data["profileStatus"] == "Active"
    assert "profileID" in data


def test_create_user_profile_duplicate_returns_400():
    """Second POST with the same profileName triggers displayDuplicateProfile (400)."""
    client.post(
        "/api/profiles",
        json={"profileName": "Fund Raiser", "profileDescription": "Raises funds.", "profileStatus": "Active"},
    )
    response = client.post(
        "/api/profiles",
        json={"profileName": "Fund Raiser", "profileDescription": "Duplicate attempt.", "profileStatus": "Active"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "displayDuplicateProfile"


def test_create_user_profile_default_status_is_active():
    """profileStatus defaults to 'Active' when omitted from the payload."""
    response = client.post(
        "/api/profiles",
        json={"profileName": "Platform Management"},
    )
    assert response.status_code == 201
    assert response.json()["profileStatus"] == "Active"
