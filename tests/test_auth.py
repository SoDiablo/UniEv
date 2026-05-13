"""
Authentication Tests
====================
Tests for user registration, login, email verification, and account lockout.
"""

import pytest
from datetime import datetime, timedelta


class TestRegistration:
    """Test user registration"""
    
    def test_register_valid_data(self, client):
        """Register with valid data → 201, JWT returned"""
        response = client.post("/api/auth/register", json={
            "email": "newuser@test.com",
            "password": "Password123",
            "first_name": "New",
            "last_name": "User",
            "birth_date": "2000-01-01",
            "phone": "5551112233",
            "role": "STUDENT",
            "accept_terms": True,
            "accept_kvkk": True
        })
        
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "newuser@test.com"
        assert data["user"]["role"] == "STUDENT"
    
    def test_register_under_18(self, client):
        """Register with age < 18 → 400"""
        response = client.post("/api/auth/register", json={
            "email": "minor@test.com",
            "password": "Password123",
            "first_name": "Minor",
            "last_name": "User",
            "birth_date": "2010-01-01",  # 16 years old
            "phone": "5551112233",
            "role": "STUDENT",
            "accept_terms": True,
            "accept_kvkk": True
        })
        
        assert response.status_code == 400
        assert "18 yaşından büyük" in response.json()["detail"]
    
    def test_register_duplicate_email(self, client, sample_student):
        """Register with duplicate email → 400"""
        response = client.post("/api/auth/register", json={
            "email": "student@test.com",  # Already exists
            "password": "Password123",
            "first_name": "Duplicate",
            "last_name": "User",
            "birth_date": "2000-01-01",
            "phone": "5559998877",
            "role": "STUDENT",
            "accept_terms": True,
            "accept_kvkk": True
        })
        
        assert response.status_code == 400
        assert "zaten kayıtlı" in response.json()["detail"]
    
    def test_register_without_kvkk(self, client):
        """Register without acceptKvkk → 400"""
        response = client.post("/api/auth/register", json={
            "email": "nokvkk@test.com",
            "password": "Password123",
            "first_name": "No",
            "last_name": "KVKK",
            "birth_date": "2000-01-01",
            "phone": "5551112233",
            "role": "STUDENT",
            "accept_terms": True,
            "accept_kvkk": False  # Not accepted
        })
        
        assert response.status_code == 400
        assert "KVKK" in response.json()["detail"]


class TestLogin:
    """Test user login"""
    
    def test_login_correct_credentials(self, client, sample_student):
        """Login correct credentials → 200, JWT"""
        response = client.post("/api/auth/login", json={
            "email": "student@test.com",
            "password": "Password123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "student@test.com"
    
    def test_login_wrong_password(self, client, sample_student):
        """Login wrong password → 401"""
        response = client.post("/api/auth/login", json={
            "email": "student@test.com",
            "password": "WrongPassword"
        })
        
        assert response.status_code == 401
        assert "hatalı" in response.json()["detail"].lower()
    
    def test_login_5_times_wrong_locks_account(self, client, sample_student):
        """Login 5 times wrong → account locked → 403"""
        # Try 5 times with wrong password
        for i in range(5):
            response = client.post("/api/auth/login", json={
                "email": "student@test.com",
                "password": "WrongPassword"
            })
            if i < 4:
                assert response.status_code == 401
        
        # 6th attempt should be locked
        response = client.post("/api/auth/login", json={
            "email": "student@test.com",
            "password": "Password123"  # Even correct password
        })
        
        assert response.status_code == 403
        assert "kilitli" in response.json()["detail"].lower()
    
    def test_login_suspended_account(self, client, sample_student, db_session):
        """Login suspended account → 403"""
        # Suspend the account
        sample_student.is_suspended = True
        db_session.commit()
        
        response = client.post("/api/auth/login", json={
            "email": "student@test.com",
            "password": "Password123"
        })
        
        assert response.status_code == 403
        assert "askıya" in response.json()["detail"].lower()


class TestPasswordReset:
    """Test password reset functionality"""
    
    def test_security_question_reset_valid(self, client, sample_student):
        """Security question reset with valid data → 200"""
        response = client.post("/api/auth/reset-password-security", json={
            "email": "student@test.com",
            "full_name": "Test Student",
            "birth_date": "2000-01-01",
            "new_password": "NewPassword123"
        })
        
        assert response.status_code == 200
        
        # Try login with new password
        login_response = client.post("/api/auth/login", json={
            "email": "student@test.com",
            "password": "NewPassword123"
        })
        assert login_response.status_code == 200
    
    def test_security_question_reset_wrong_name(self, client, sample_student):
        """Security question reset with wrong name → 400"""
        response = client.post("/api/auth/reset-password-security", json={
            "email": "student@test.com",
            "full_name": "Wrong Name",
            "birth_date": "2000-01-01",
            "new_password": "NewPassword123"
        })
        
        assert response.status_code == 400
        assert "eşleşmiyor" in response.json()["detail"].lower()
    
    def test_security_question_reset_weak_password(self, client, sample_student):
        """Security question reset with weak password → 400"""
        response = client.post("/api/auth/reset-password-security", json={
            "email": "student@test.com",
            "full_name": "Test Student",
            "birth_date": "2000-01-01",
            "new_password": "weak"  # Too short, no digit
        })
        
        assert response.status_code == 400
        assert "8 karakter" in response.json()["detail"]
