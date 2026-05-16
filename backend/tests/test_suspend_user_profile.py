"""
TDD — Sprint 2 User Profile: Suspend User Profile
BCE Boundary: :SuspendUserProfilePage
Controller:   SuspendUserProfileController
Entity:       UserProfile.suspendUserProfile()

Red  phase: Stub controller returns False → PUT /suspend always 404 (happy path fails).
Green phase: Real controller sets profileStatus = "Suspended" and returns 200.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_suspend_user_profile.db"
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


def test_suspend_user_profile_sets_suspended():
    """PUT /api/profiles/{id}/suspend sets profileStatus to 'Suspended' and returns 200."""
    create_resp = client.post(
        "/api/profiles",
        json={"profileName": "Donee", "profileDescription": "Receives funds.", "profileStatus": "Active"},
    )
    assert create_resp.status_code == 201
    profile_id = create_resp.json()["profileID"]

    response = client.put(f"/api/profiles/{profile_id}/suspend")
    assert response.status_code == 200
    data = response.json()
    assert data["profileStatus"] == "Suspended"
    assert data["profileID"] == profile_id


def test_suspend_user_profile_not_found_returns_404():
    """PUT /api/profiles/{id}/suspend for a non-existent ID returns 404 (displaySuspendFail)."""
    response = client.put("/api/profiles/99999/suspend")
    assert response.status_code == 404
    assert response.json()["detail"] == "displaySuspendFail"
