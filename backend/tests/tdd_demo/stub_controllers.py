"""
TDD Red Phase — Stub Controllers for Sprint 2: User Profile Management

These are the placeholder controllers written BEFORE any real implementation.
Every method accepts the correct parameters but returns a dummy value:
  - False  for operations that should return True on success
  - None   for operations that should return a domain object
  - []     for operations that should return a list of results

Running tests against these stubs produces the Red phase: all tests FAIL.
After replacing these with the real controllers in backend/controls/, the
same tests produce the Green phase: all tests PASS.
"""


class StubCreateUserProfileController:
    """
    Stub for: controls/create_user_profile_controller.py
    Real behaviour: returns True on success, "duplicate" if name already exists.
    Stub behaviour: always returns False — createUserProfile never succeeds.
    """

    def validateRepeatProfile(self, db, profile_name: str) -> bool:
        return False  # should return True when profile_name is NOT yet taken

    def createUserProfile(self, db, profileName: str, profileDescription: str, profileStatus: str = "Active"):
        return False  # should return True on successful creation


class StubRetrieveUserProfileController:
    """
    Stub for: controls/retrieve_user_profile_controller.py
    Real behaviour: returns the UserProfile object matching the given ID.
    Stub behaviour: always returns None — no profile is ever found.
    """

    def retrieveUserProfile(self, db, profileID: int):
        return None  # should return a UserProfile instance when the ID exists


class StubUpdateUserProfileController:
    """
    Stub for: controls/update_user_profile_controller.py
    Real behaviour: persists the changed fields and returns True.
    Stub behaviour: always returns False — no update ever succeeds.
    """

    def validateEnteredData(self, profile_name: str) -> bool:
        return False  # should return True when input data passes validation

    def updateUserProfile(self, db, user_pro: dict) -> bool:
        return False  # should return True after a successful database update


class StubSuspendUserProfileController:
    """
    Stub for: controls/suspend_user_profile_controller.py
    Real behaviour: sets profileStatus = "Suspended" and returns True.
    Stub behaviour: always returns False — no suspension ever succeeds.
    """

    def suspendUserProfile(self, db, profileID: int) -> bool:
        return False  # should return True after the profile is suspended


class StubSearchUserProfileController:
    """
    Stub for: controls/search_user_profile_controller.py
    Real behaviour: returns a list of UserProfile objects matching the keyword.
    Stub behaviour: always returns [] — no search ever finds anything.
    """

    def searchUserProfile(self, db, keyword: str) -> list:
        return []  # should return matching profiles; empty only when nothing matches
