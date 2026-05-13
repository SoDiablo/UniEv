"""
Pytest Configuration and Fixtures
==================================
This file contains shared fixtures for all tests.
"""

import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set test environment variables
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET"] = "test-secret-key"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_EXPIRE_DAYS"] = "7"

from database import Base, get_db
from main import app
from core.security import hash_password


# Create in-memory test database with StaticPool to share connection
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # This ensures all sessions use the same connection
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables once at module level
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_student(db_session):
    """Create a sample student user"""
    from database import User, Profile
    from datetime import datetime
    
    user = User(
        email="student@test.com",
        password_hash=hash_password("Password123"),
        first_name="Test",
        last_name="Student",
        birth_date=datetime(2000, 1, 1),
        phone="5551234567",
        role="STUDENT",
        is_verified=True,
        kvkk_consent_at=datetime.utcnow()
    )
    db_session.add(user)
    db_session.flush()
    
    profile = Profile(user_id=user.id)
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(user)
    
    return user


@pytest.fixture
def sample_landlord(db_session):
    """Create a sample landlord user"""
    from database import User, Profile
    from datetime import datetime
    
    user = User(
        email="landlord@test.com",
        password_hash=hash_password("Password123"),
        first_name="Test",
        last_name="Landlord",
        birth_date=datetime(1980, 1, 1),
        phone="5559876543",
        role="LANDLORD",
        is_verified=True,
        kvkk_consent_at=datetime.utcnow()
    )
    db_session.add(user)
    db_session.flush()
    
    profile = Profile(user_id=user.id)
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(user)
    
    return user


@pytest.fixture
def sample_admin(db_session):
    """Create a sample admin user"""
    from database import User, Profile
    from datetime import datetime
    
    user = User(
        email="admin@test.com",
        password_hash=hash_password("Password123"),
        first_name="Test",
        last_name="Admin",
        birth_date=datetime(1990, 1, 1),
        phone="5555555555",
        role="ADMIN",
        is_verified=True,
        kvkk_consent_at=datetime.utcnow()
    )
    db_session.add(user)
    db_session.flush()
    
    profile = Profile(user_id=user.id)
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(user)
    
    return user


@pytest.fixture
def auth_headers_student(client, sample_student):
    """Get authentication headers for student"""
    response = client.post("/api/auth/login", json={
        "email": "student@test.com",
        "password": "Password123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_landlord(client, sample_landlord):
    """Get authentication headers for landlord"""
    response = client.post("/api/auth/login", json={
        "email": "landlord@test.com",
        "password": "Password123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_admin(client, sample_admin):
    """Get authentication headers for admin"""
    response = client.post("/api/auth/login", json={
        "email": "admin@test.com",
        "password": "Password123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
