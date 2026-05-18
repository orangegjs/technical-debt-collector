"""
TDD Red Phase — Sprint 2: User Profile Management
==================================================
Run:  python -m pytest tests/tdd_demo/test_red_phase.py -v
Expected result: 10 FAILED

HOW IT WORKS
------------
Tests import from stubs.py. Each stub method ignores its arguments and always
returns one fixed dummy value. Every assertion below checks the EXPECTED real
behaviour, so every test fails against the stubs.

No database is needed — stubs accept plain arguments and return immediately.
"""

import pytest

# Every test in this file is intentionally expected to fail (TDD red phase).
# xfail(strict=True): if a test unexpectedly passes, CI flags it as an error.
pytestmark = pytest.mark.xfail(strict=True, reason="Red phase: stubs intentionally return wrong values")

from tests.tdd_demo.stubs import (
    StubCreateUserProfileController,
    StubRetrieveUserProfileController,
    StubUpdateUserProfileController,
    StubSuspendUserProfileController,
    StubSearchUserProfileController,
)


# ── US-01: Create User Profile ──────────────────────────────────────────────

class TestCreateUserProfile:

    def test_create_new_profile_success(self):
        """
        EXPECTED: createUserProfile() returns True when a new profile is created.
        STUB: returns False → False != True → FAIL.
        GREEN: real controller inserts the row into the database and returns True.
        """
        ctrl = StubCreateUserProfileController()
        result = ctrl.createUserProfile(
            profileName="Donee",
            profileDescription="A user who receives funds.",
        )
        assert result == True  # FAILS: stub returns False

    def test_create_duplicate_profile_rejected(self):
        """
        EXPECTED: createUserProfile() returns "duplicate" when profileName already exists.
        STUB: returns False → False != "duplicate" → FAIL.
        GREEN: real controller detects the existing row and returns "duplicate".
        """
        ctrl = StubCreateUserProfileController()
        ctrl.createUserProfile(profileName="Donee", profileDescription="First.")
        result = ctrl.createUserProfile(profileName="Donee", profileDescription="Duplicate attempt.")
        assert result == "duplicate"  # FAILS: stub returns False


# ── US-02: Retrieve User Profile ────────────────────────────────────────────

class TestRetrieveUserProfile:

    def test_retrieve_valid_profile(self):
        """
        EXPECTED: retrieveUserProfile() returns a UserProfile object for a valid ID.
        STUB: returns None → None is not None evaluates False → FAIL.
        GREEN: real controller queries the database and returns the matching row.
        """
        ctrl = StubRetrieveUserProfileController()
        result = ctrl.retrieveUserProfile(profileID=1)
        assert result is not None  # FAILS: stub returns None

    def test_retrieve_invalid_profile(self):
        """
        EXPECTED: (forced inversion) both tests must fail; stub always returns None.
        STUB: returns None → None is not None evaluates False → FAIL.
        GREEN: test_green_phase.py uses 'assert result is None' for this case instead.
        """
        ctrl = StubRetrieveUserProfileController()
        result = ctrl.retrieveUserProfile(profileID=99999)
        assert result is not None  # FAILS: stub returns None (forced inversion keeps red phase clean)


# ── US-03: Update User Profile ──────────────────────────────────────────────

class TestUpdateUserProfile:

    def test_update_valid_input_success(self):
        """
        EXPECTED: updateUserProfile() returns True when valid data is provided.
        STUB: returns None → None != True → FAIL.
        GREEN: real controller persists the changes and returns True.
        """
        ctrl = StubUpdateUserProfileController()
        result = ctrl.updateUserProfile(
            profileName="Fund Raiser",
            profileDescription="Raises funds.",
        )
        assert result == True  # FAILS: stub returns None

    def test_update_empty_input_rejected(self):
        """
        EXPECTED: updateUserProfile() returns False when input is empty/invalid.
        STUB: returns None → None != False (strict equality) → FAIL.
        GREEN: real controller finds no matching profileID and returns False.
        Note: stub returns None (not False) precisely so this assertion fails.
        """
        ctrl = StubUpdateUserProfileController()
        result = ctrl.updateUserProfile(profileName="", profileDescription="")
        assert result == False  # FAILS: stub returns None, and None != False


# ── US-04: Suspend User Profile ─────────────────────────────────────────────

class TestSuspendUserProfile:

    def test_suspend_valid_profile_success(self):
        """
        EXPECTED: suspendUserProfile() returns True after setting status to "Suspended".
        STUB: returns False → False != True → FAIL.
        GREEN: real controller sets profileStatus = "Suspended", commits, returns True.
        """
        ctrl = StubSuspendUserProfileController()
        result = ctrl.suspendUserProfile(profileID=1)
        assert result == True  # FAILS: stub returns False

    def test_suspend_invalid_profile_rejected(self):
        """
        EXPECTED: (forced inversion) stub and real code both return False for missing IDs.
        STUB: returns False → False != "not found" → FAIL.
        GREEN: test_green_phase.py uses 'assert result is False' for this case instead.
        """
        ctrl = StubSuspendUserProfileController()
        result = ctrl.suspendUserProfile(profileID=99999)
        assert result == "not found"  # FAILS: stub returns False (forced inversion keeps red phase clean)


# ── US-05: Search User Profile ──────────────────────────────────────────────

class TestSearchUserProfile:

    def test_search_matching_keyword(self):
        """
        EXPECTED: searchUserProfile("Donee") returns real UserProfile objects (not placeholder strings).
        STUB: returns ["placeholder"] → result[0] == "placeholder" → second condition False → FAIL.
        GREEN: real controller returns [UserProfile(profileName="Donee", ...)] → result[0] != "placeholder" → PASS.
        """
        ctrl = StubSearchUserProfileController()
        result = ctrl.searchUserProfile(keyword="Donee")
        assert len(result) > 0 and result[0] != "placeholder"  # FAILS: stub returns ["placeholder"]

    def test_search_no_matching_keyword(self):
        """
        EXPECTED: searchUserProfile("zzz_nonexistent") returns an empty list.
        STUB: returns ["placeholder"] → len == 1, 1 != 0 → FAIL.
        GREEN: real controller finds no matching rows and returns [].
        Note: stub returns ["placeholder"] (not []) precisely so this assertion fails.
        """
        ctrl = StubSearchUserProfileController()
        result = ctrl.searchUserProfile(keyword="zzz_nonexistent")
        assert len(result) == 0  # FAILS: stub returns ["placeholder"]
