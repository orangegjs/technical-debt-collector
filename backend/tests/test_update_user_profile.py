"""
TDD — Sprint 2 User Profile: Update User Profile
BCE Boundary: :UpdateUserProfilePage
Controller:   UpdateUserProfileController
Entity:       UserProfile.updateUserProfile()

Red  phase: Stub controller returns False → PUT always returns 400 (happy path fails).
Green phase: Real controller persists changes → updated profile returned with 200.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_update_user_profile.db"
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


def test_update_user_profile_description_success():
    """PUT /api/profiles/{id} with a new description returns 200 and updated data."""
    create_resp = client.post(
        "/api/profiles",
        json={"profileName": "Fund Raiser", "profileDescription": "Original description.", "profileStatus": "Active"},
    )
    profile_id = create_resp.json()["profileID"]

    response = client.put(
        f"/api/profiles/{profile_id}",
        json={"profileDescription": "Updated description."},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["profileDescription"] == "Updated description."
    assert data["profileName"] == "Fund Raiser"


def test_update_user_profile_name_success():
    """PUT /api/profiles/{id} changing the profileName persists the new name."""
    create_resp = client.post(
        "/api/profiles",
        json={"profileName": "Old Name", "profileDescription": "Some desc.", "profileStatus": "Active"},
    )
    profile_id = create_resp.json()["profileID"]

    response = client.put(
        f"/api/profiles/{profile_id}",
        json={"profileName": "New Name"},
    )
    assert response.status_code == 200
    assert response.json()["profileName"] == "New Name"


def test_update_user_profile_not_found_returns_400():
    """PUT /api/profiles/{id} for a non-existent ID returns 400 (displayInputErrorMessage)."""
    response = client.put(
        "/api/profiles/99999",
        json={"profileDescription": "Ghost update."},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "displayInputErrorMessage"
