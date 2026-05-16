"""
TDD Red Phase — Stub Controllers for Sprint 2: User Profile Management

One class per user story. Each class has exactly ONE method that always
returns a fixed dummy value regardless of input — no logic, no branching.

Dummy values are chosen so that every red-phase assertion fails naturally:

  StubCreate      createUserProfile      → False
  StubRetrieve    retrieveUserProfile    → None
  StubUpdate      updateUserProfile      → None   (not False — so assert == False also fails)
  StubSuspend     suspendUserProfile     → False
  StubSearch      searchUserProfile      → ["placeholder"]  (non-empty — so assert len==0 fails)
"""


class StubCreateUserProfileController:
    """Stub for controls/create_user_profile_controller.py"""

    def createUserProfile(self, profileName: str, profileDescription: str):
        return False


class StubRetrieveUserProfileController:
    """Stub for controls/retrieve_user_profile_controller.py"""

    def retrieveUserProfile(self, profileID: int):
        return None


class StubUpdateUserProfileController:
    """Stub for controls/update_user_profile_controller.py
    Returns None (not False) so that 'assert result == False' also fails —
    None is not equal to False in Python.
    """

    def updateUserProfile(self, profileName: str, profileDescription: str):
        return None


class StubSuspendUserProfileController:
    """Stub for controls/suspend_user_profile_controller.py"""

    def suspendUserProfile(self, profileID: int):
        return False


class StubSearchUserProfileController:
    """Stub for controls/search_user_profile_controller.py
    Returns a non-empty list so that 'assert len(result) == 0' fails.
    The placeholder string also makes 'result[0] != "placeholder"' fail.
    """

    def searchUserProfile(self, keyword: str):
        return ["placeholder"]
