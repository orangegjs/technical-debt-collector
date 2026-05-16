"""
TDD — Sprint 2 User Profile: Retrieve User Profile
BCE Boundary: :RetrieveUserProfilePage
Controller:   RetrieveUserProfileController
Entity:       UserProfile.retrieveUserProfile()

Red  phase: Stub controller returns None for every ID → 404 for the happy path fails.
Green phase: Real controller queries the DB → correct profile returned.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_retrieve_user_profile.db"
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


def test_retrieve_user_profile_success():
    """GET /api/profiles/{id} returns the profile that was just created."""
    create_resp = client.post(
        "/api/profiles",
        json={"profileName": "Donee", "profileDescription": "Receives funds.", "profileStatus": "Active"},
    )
    assert create_resp.status_code == 201
    profile_id = create_resp.json()["profileID"]

    response = client.get(f"/api/profiles/{profile_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["profileID"] == profile_id
    assert data["profileName"] == "Donee"
    assert data["profileStatus"] == "Active"


def test_retrieve_user_profile_not_found():
    """GET /api/profiles/{id} for a non-existent ID returns 404."""
    response = client.get("/api/profiles/99999")
    assert response.status_code == 404
