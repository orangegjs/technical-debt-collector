"""
TDD Green Phase — Sprint 2: User Profile Management
====================================================
Run:  python -m pytest tests/tdd_demo/test_green_phase.py -v
Expected result: 10 PASSED

HOW IT WORKS
------------
Same 10 test names as test_red_phase.py, now calling the REAL controllers
in backend/controls/ against a SQLite in-memory database.

Two assertions differ from the red phase (marked with NOTE):
  test_retrieve_invalid_profile  — red used 'is not None' to force fail;
                                   green uses 'is None' (correct behaviour).
  test_suspend_invalid_profile_rejected — red used '== "not found"' to force fail;
                                          green uses 'is False' (correct behaviour).
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from entities.user_profile import UserProfile
import entities.user_account   # noqa: F401
import entities.fra_category   # noqa: F401
import entities.fra_activity   # noqa: F401
# All four entities must be imported before any mapper configuration so SQLAlchemy
# can resolve every cross-model relationship string (e.g. "UserAccount", "FRAActivity").
from controls.create_user_profile_controller import CreateUserProfileController
from controls.retrieve_user_profile_controller import RetrieveUserProfileController
from controls.update_user_profile_controller import UpdateUserProfileController
from controls.suspend_user_profile_controller import SuspendUserProfileController
from controls.search_user_profile_controller import SearchUserProfileController


@pytest.fixture
def db():
    """Fresh SQLite in-memory database for each test."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def seeded_db(db):
    """Database pre-loaded with one 'Donee' profile (profileID = 1)."""
    profile = UserProfile(
        profileName="Donee",
        profileDescription="A user who receives funds.",
        profileStatus="Active",
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return db


# ── US-01: Create User Profile ──────────────────────────────────────────────

class TestCreateUserProfile:

    def test_create_new_profile_success(self, db):
        """
        EXPECTED: createUserProfile() returns True when a new profile is created.
        STUB: returned False → test failed in red phase.
        GREEN: real controller inserts the row into SQLite and returns True.
        """
        ctrl = CreateUserProfileController()
        result = ctrl.createUserProfile(
            db=db,
            profileName="Donee",
            profileDescription="A user who receives funds.",
        )
        assert result == True

    def test_create_duplicate_profile_rejected(self, db):
        """
        EXPECTED: createUserProfile() returns "duplicate" when profileName already exists.
        STUB: returned False → test failed in red phase.
        GREEN: real controller detects the existing row and returns "duplicate".
        """
        ctrl = CreateUserProfileController()
        ctrl.createUserProfile(db=db, profileName="Donee", profileDescription="First.")
        result = ctrl.createUserProfile(db=db, profileName="Donee", profileDescription="Duplicate attempt.")
        assert result == "duplicate"


# ── US-02: Retrieve User Profile ────────────────────────────────────────────

class TestRetrieveUserProfile:

    def test_retrieve_valid_profile(self, seeded_db):
        """
        EXPECTED: retrieveUserProfile() returns a UserProfile object for a valid ID.
        STUB: returned None → test failed in red phase.
        GREEN: real controller queries the database and returns the matching row.
        """
        ctrl = RetrieveUserProfileController()
        result = ctrl.retrieveUserProfile(db=seeded_db, profileID=1)
        assert result is not None

    def test_retrieve_invalid_profile(self, seeded_db):
        """
        EXPECTED: retrieveUserProfile() returns None for a non-existent ID.
        STUB: returned None → red phase used 'is not None' to force failure.
        GREEN: NOTE — assertion corrected: real controller returns None for missing ID.
        """
        ctrl = RetrieveUserProfileController()
        result = ctrl.retrieveUserProfile(db=seeded_db, profileID=99999)
        assert result is None  # corrected from red phase forced inversion


# ── US-03: Update User Profile ──────────────────────────────────────────────

class TestUpdateUserProfile:

    def test_update_valid_input_success(self, seeded_db):
        """
        EXPECTED: updateUserProfile() returns True when valid data is provided.
        STUB: returned None → test failed in red phase.
        GREEN: real controller persists the changes and returns True.
        """
        ctrl = UpdateUserProfileController()
        result = ctrl.updateUserProfile(
            db=seeded_db,
            user_pro={"profileID": 1, "profileName": "Fund Raiser", "profileDescription": "Raises funds."},
        )
        assert result == True

    def test_update_empty_input_rejected(self, seeded_db):
        """
        EXPECTED: updateUserProfile() returns False when no valid profileID is supplied.
        STUB: returned None → None != False → test failed in red phase.
        GREEN: real controller receives no profileID → no row found → returns False.
        """
        ctrl = UpdateUserProfileController()
        result = ctrl.updateUserProfile(db=seeded_db, user_pro={"profileName": ""})
        assert result == False


# ── US-04: Suspend User Profile ─────────────────────────────────────────────

class TestSuspendUserProfile:

    def test_suspend_valid_profile_success(self, seeded_db):
        """
        EXPECTED: suspendUserProfile() returns True after setting status to "Suspended".
        STUB: returned False → test failed in red phase.
        GREEN: real controller sets profileStatus = "Suspended", commits, returns True.
        """
        ctrl = SuspendUserProfileController()
        result = ctrl.suspendUserProfile(db=seeded_db, profileID=1)
        assert result == True

    def test_suspend_invalid_profile_rejected(self, seeded_db):
        """
        EXPECTED: suspendUserProfile() returns False when the profile ID does not exist.
        STUB: returned False → red phase used '== "not found"' to force failure.
        GREEN: NOTE — assertion corrected: real controller returns False for missing profile.
        """
        ctrl = SuspendUserProfileController()
        result = ctrl.suspendUserProfile(db=seeded_db, profileID=99999)
        assert result is False  # corrected from red phase forced inversion


# ── US-05: Search User Profile ──────────────────────────────────────────────

class TestSearchUserProfile:

    def test_search_matching_keyword(self, seeded_db):
        """
        EXPECTED: searchUserProfile("Donee") returns real UserProfile objects.
        STUB: returned ["placeholder"] → result[0] == "placeholder" → FAIL in red phase.
        GREEN: real controller returns [UserProfile(profileName="Donee")] → result[0] != "placeholder" → PASS.
        """
        ctrl = SearchUserProfileController()
        result = ctrl.searchUserProfile(db=seeded_db, keyword="Donee")
        assert len(result) > 0 and result[0] != "placeholder"

    def test_search_no_matching_keyword(self, seeded_db):
        """
        EXPECTED: searchUserProfile("zzz_nonexistent") returns an empty list.
        STUB: returned ["placeholder"] → len == 1 → FAIL in red phase.
        GREEN: real controller finds no matching rows and returns [].
        """
        ctrl = SearchUserProfileController()
        result = ctrl.searchUserProfile(db=seeded_db, keyword="zzz_nonexistent")
        assert len(result) == 0
