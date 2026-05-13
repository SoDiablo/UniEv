"""
FraudScore Tests
================
Tests for fraud score calculation algorithm.
Each factor must be tested individually.
"""

import pytest
from services.fraud_service import calculate_fraud_score


class TestFraudScoreFactors:
    """Test each fraud score factor individually"""
    
    def test_short_description_adds_15(self, db_session):
        """Short description (< 100 chars) → score includes +15"""
        from database import Listing, User
        
        # Create mock listing with short description
        listing = Listing(
            owner_id="test",
            title="Test",
            description="Short",  # < 100 chars
            price=5000
        )
        
        score, factors = calculate_fraud_score(listing, None)
        
        assert "short_description" in factors
        assert score >= 15
    
    def test_no_photos_adds_20(self, db_session):
        """No photos → score includes +20"""
        from database import Listing
        
        listing = Listing(
            owner_id="test",
            title="Test",
            description="A" * 150,  # Long enough
            price=5000,
            photos=[]  # No photos
        )
        
        score, factors = calculate_fraud_score(listing, None)
        
        assert "no_photos" in factors
        assert score >= 20
    
    def test_no_location_adds_10(self, db_session):
        """No location → score includes +10"""
        from database import Listing, ListingPhoto
        
        listing = Listing(
            owner_id="test",
            title="Test",
            description="A" * 150,
            price=5000,
            latitude=None,  # No location
            longitude=None
        )
        # Add photo object
        photo = ListingPhoto(url="/uploads/photo1.jpg", order=0)
        listing.photos = [photo]
        
        score, factors = calculate_fraud_score(listing, None)
        
        assert "no_location" in factors
        assert score >= 10
    
    def test_price_under_1000_adds_5(self, db_session):
        """Price < 1000 → score includes +5"""
        from database import Listing, ListingPhoto
        
        listing = Listing(
            owner_id="test",
            title="Test",
            description="A" * 150,
            price=500,  # Suspicious low price
            latitude=40.0,
            longitude=29.0
        )
        photo = ListingPhoto(url="/uploads/photo1.jpg", order=0)
        listing.photos = [photo]
        
        score, factors = calculate_fraud_score(listing, None)
        
        assert "suspicious_price" in factors
        assert score >= 5
    
    def test_price_over_50000_adds_5(self, db_session):
        """Price > 50000 → score includes +5"""
        from database import Listing, ListingPhoto
        
        listing = Listing(
            owner_id="test",
            title="Test",
            description="A" * 150,
            price=60000,  # Suspicious high price
            latitude=40.0,
            longitude=29.0
        )
        photo = ListingPhoto(url="/uploads/photo1.jpg", order=0)
        listing.photos = [photo]
        
        score, factors = calculate_fraud_score(listing, None)
        
        assert "suspicious_price" in factors
        assert score >= 5
    
    def test_title_contains_acil_adds_5(self, db_session):
        """Title contains "acil" → score includes +5"""
        from database import Listing, ListingPhoto
        
        listing = Listing(
            owner_id="test",
            title="Acil Kiralık Ev",  # Contains "acil" (lowercase works)
            description="A" * 150,
            price=5000,
            latitude=40.0,
            longitude=29.0
        )
        photo = ListingPhoto(url="/uploads/photo1.jpg", order=0)
        listing.photos = [photo]
        
        score, factors = calculate_fraud_score(listing, None)
        
        assert "urgent_keyword" in factors
        assert score >= 5
    
    def test_description_contains_acil_adds_5(self, db_session):
        """Description contains "acil" → score includes +5"""
        from database import Listing, ListingPhoto
        
        listing = Listing(
            owner_id="test",
            title="Kiralık Ev",
            description="Acil kiralık " + "A" * 150,  # Contains "acil"
            price=5000,
            latitude=40.0,
            longitude=29.0
        )
        photo = ListingPhoto(url="/uploads/photo1.jpg", order=0)
        listing.photos = [photo]
        
        score, factors = calculate_fraud_score(listing, None)
        
        assert "urgent_keyword" in factors
        assert score >= 5
    
    def test_owner_multiple_listings_subtracts_10(self, db_session):
        """Owner has multiple listings → score includes -10"""
        from database import Listing, ListingPhoto, User
        
        # Create mock owner with multiple listings
        class MockOwner:
            listings = [Listing(), Listing(), Listing()]  # 3 listings
        
        listing = Listing(
            owner_id="test",
            title="Test",
            description="A" * 150,
            price=5000,
            latitude=40.0,
            longitude=29.0
        )
        photo = ListingPhoto(url="/uploads/photo1.jpg", order=0)
        listing.photos = [photo]
        
        score, factors = calculate_fraud_score(listing, MockOwner())
        
        assert "experienced_owner" in factors
        # Score should be reduced (negative factor)
    
    def test_score_never_exceeds_100(self, db_session):
        """Score never exceeds 100"""
        from database import Listing
        
        # Create worst possible listing
        listing = Listing(
            owner_id="test",
            title="ACIL",
            description="Short",  # All bad factors
            price=100,
            latitude=None,
            longitude=None
        )
        listing.photos = []
        
        score, factors = calculate_fraud_score(listing, None)
        
        assert score <= 100
    
    def test_score_never_below_0(self, db_session):
        """Score never goes below 0"""
        from database import Listing, ListingPhoto
        
        # Create best possible listing with experienced owner
        class MockOwner:
            listings = [Listing() for _ in range(10)]  # Many listings
        
        listing = Listing(
            owner_id="test",
            title="Güzel Ev",
            description="A" * 200,  # Long description
            price=5000,  # Normal price
            latitude=40.0,
            longitude=29.0
        )
        photo1 = ListingPhoto(url="/uploads/p1.jpg", order=0)
        photo2 = ListingPhoto(url="/uploads/p2.jpg", order=1)
        photo3 = ListingPhoto(url="/uploads/p3.jpg", order=2)
        listing.photos = [photo1, photo2, photo3]
        
        score, factors = calculate_fraud_score(listing, MockOwner())
        
        assert score >= 0


class TestFraudScoreCombinations:
    """Test combinations of factors"""
    
    def test_perfect_listing_low_score(self, db_session):
        """Perfect listing with experienced owner → low score"""
        from database import Listing, ListingPhoto
        
        class MockOwner:
            listings = [Listing(), Listing()]
        
        listing = Listing(
            owner_id="test",
            title="Güzel Ev",
            description="A" * 200,
            price=5000,
            latitude=40.0,
            longitude=29.0
        )
        photo1 = ListingPhoto(url="/uploads/p1.jpg", order=0)
        photo2 = ListingPhoto(url="/uploads/p2.jpg", order=1)
        listing.photos = [photo1, photo2]
        
        score, factors = calculate_fraud_score(listing, MockOwner())
        
        # Should have low score (only -10 from experienced owner)
        assert score <= 10
    
    def test_suspicious_listing_high_score(self, db_session):
        """Suspicious listing → high score"""
        from database import Listing
        
        listing = Listing(
            owner_id="test",
            title="ACIL SATILIK",
            description="Hemen",  # Short + urgent
            price=100,  # Too cheap
            latitude=None,
            longitude=None
        )
        listing.photos = []
        
        score, factors = calculate_fraud_score(listing, None)
        
        # Should have high score (15+20+10+5+5 = 55)
        assert score >= 50
