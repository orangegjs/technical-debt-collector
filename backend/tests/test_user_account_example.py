"""
Example test file for User Account creation
Place this in: backend/tests/test_user_account.py

To run: pytest backend/tests/
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Create a test database (in-memory SQLite for testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency to use test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create fresh database tables before each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Creates a new user via POST /api/users and checks it returns status 201 with the correct data
def test_create_user_account_success():
    """Test creating a user account successfully"""
    response = client.post(
        "/api/users",
        json={
            "username": "testuser",
            "password": "TestP@ssw0rd123!",
            "name": "Test User",
            "email": "test@example.com",
            "accountStatus": "Active",
            "role": "User Admin"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["accountStatus"] == "Active"
    assert data["role"] == "User Admin"
    assert "password" not in data  # Password should NOT be in response

# Tries to create two users with the same username and checks the second one is rejected with status 400
def test_create_user_account_duplicate_username():
    """Test that duplicate username is rejected"""
    # Create first user
    client.post(
        "/api/users",
        json={
            "username": "duplicate",
            "password": "TestP@ssw0rd123!",
            "name": "First User",
            "email": "first@example.com",
            "accountStatus": "Active",
            "role": "Donee"
        }
    )
    
    # Try to create second user with same username
    response = client.post(
        "/api/users",
        json={
            "username": "duplicate",  # Same username!
            "password": "DifferentP@ss123!",
            "name": "Second User",
            "email": "second@example.com",
            "accountStatus": "Active",
            "role": "Fund Raiser"
        }
    )
    
    assert response.status_code == 400  # Should fail

# Creates a user then logs in via POST /api/auth/login with correct credentials, checks it returns status 200.
def test_login_success():
    """Test logging in with correct credentials"""
    # First create a user
    client.post(
        "/api/users",
        json={
            "username": "logintest",
            "password": "LoginP@ss123!",
            "name": "Login Test",
            "email": "login@example.com",
            "accountStatus": "Active",
            "role": "User Admin"
        }
    )
    
    # Try to login
    response = client.post(
        "/api/auth/login",
        json={
            "username": "logintest",
            "password": "LoginP@ss123!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "logintest"

# Tries to log in with the wrong password and checks it returns status 401 (Unauthorized)
def test_login_wrong_password():
    """Test that login fails with wrong password"""
    # First create a user
    client.post(
        "/api/users",
        json={
            "username": "failtest",
            "password": "CorrectP@ss123!",
            "name": "Fail Test",
            "email": "fail@example.com",
            "accountStatus": "Active",
            "role": "Donee"
        }
    )
    
    # Try to login with wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "username": "failtest",
            "password": "WrongP@ss123!"  # Wrong password!
        }
    )
    
    assert response.status_code == 401  # Unauthorized
