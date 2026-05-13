# database.py
from sqlalchemy import (
    create_engine, Column, String, Integer, Boolean,
    DateTime, Float, ForeignKey, UniqueConstraint, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from cuid2 import cuid_wrapper

cuid_generator = cuid_wrapper()

def generate_id():
    return cuid_generator()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./uniev.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─────────────────────────────────────────────
# USER
# ─────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_id)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    role = Column(String, nullable=False, default="STUDENT")  # STUDENT | LANDLORD | ADMIN

    # Email verification
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verification_token = Column(String, nullable=True)
    email_verification_code = Column(String, nullable=True)  # 6-digit code
    email_verification_code_expires = Column(DateTime, nullable=True)  # Code expiry time

    # Account status
    is_suspended = Column(Boolean, default=False, nullable=False)
    login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)

    # Password reset
    password_reset_token = Column(String, nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    password_reset_code = Column(String, nullable=True)  # 6-digit code for password reset
    password_reset_code_expires = Column(DateTime, nullable=True)  # Code expiry time
    token_version = Column(Integer, default=0, nullable=False)

    # KVKK
    kvkk_consent_at = Column(DateTime, nullable=True)
    delete_requested_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    listings = relationship("Listing", back_populates="owner", cascade="all, delete-orphan")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender", cascade="all, delete-orphan")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="reporter", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    consents = relationship("UserConsent", back_populates="user", cascade="all, delete-orphan")
    data_requests = relationship("DataRequest", back_populates="user", cascade="all, delete-orphan")
    login_history = relationship("LoginHistory", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="admin", cascade="all, delete-orphan")


# ─────────────────────────────────────────────
# PROFILE
# ─────────────────────────────────────────────
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=generate_id)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)
    name_display_format = Column(String, default="FULL", nullable=False)  # FULL | ABBREVIATED | INITIALS

    budget_min = Column(Integer, nullable=True)
    budget_max = Column(Integer, nullable=True)

    smoking_ok = Column(Boolean, nullable=True)
    pet_ok = Column(Boolean, nullable=True)
    sleep_schedule = Column(String, nullable=True)   # NIGHT_OWL | EARLY_BIRD | FLEXIBLE
    cleanliness = Column(String, nullable=True)       # LOW | MEDIUM | HIGH

    document_url = Column(String, nullable=True)
    document_verified = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="profile")


# ─────────────────────────────────────────────
# LISTING
# ─────────────────────────────────────────────
class Listing(Base):
    __tablename__ = "listings"

    id = Column(String, primary_key=True, default=generate_id)
    owner_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    district = Column(String, nullable=True)
    rules = Column(Text, nullable=True)
    status = Column(String, default="ACTIVE", nullable=False)  # ACTIVE | PENDING | SUSPENDED | DELETED
    fraud_score = Column(Integer, nullable=True)
    safety_index = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="listings")
    photos = relationship("ListingPhoto", back_populates="listing", cascade="all, delete-orphan", order_by="ListingPhoto.order")
    reports = relationship("Report", back_populates="listing")
    fraud_records = relationship("FraudScoreRecord", back_populates="listing", cascade="all, delete-orphan")
    favorited_by = relationship("Favorite", back_populates="listing", cascade="all, delete-orphan")


# ─────────────────────────────────────────────
# LISTING PHOTO
# ─────────────────────────────────────────────
class ListingPhoto(Base):
    __tablename__ = "listing_photos"

    id = Column(String, primary_key=True, default=generate_id)
    listing_id = Column(String, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    url = Column(String, nullable=False)
    order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    listing = relationship("Listing", back_populates="photos")


# ─────────────────────────────────────────────
# MESSAGE
# ─────────────────────────────────────────────
class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=generate_id)
    sender_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=True)  # Made nullable for media-only messages
    message_type = Column(String, default="TEXT", nullable=False)  # TEXT | IMAGE | VIDEO | AUDIO
    file_url = Column(String, nullable=True)  # URL to uploaded file
    file_name = Column(String, nullable=True)  # Original filename
    duration = Column(Integer, nullable=True)  # For audio/video duration in seconds
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")


# ─────────────────────────────────────────────
# FAVORITE
# ─────────────────────────────────────────────
class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "listing_id", name="uq_favorite_user_listing"),)

    id = Column(String, primary_key=True, default=generate_id)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    listing_id = Column(String, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="favorites")
    listing = relationship("Listing", back_populates="favorited_by")


# ─────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────
class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=generate_id)
    listing_id = Column(String, ForeignKey("listings.id", ondelete="SET NULL"), nullable=True)
    reporter_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    report_type = Column(String, nullable=False)  # FRAUD | INAPPROPRIATE | SPAM | OTHER
    description = Column(Text, nullable=True)
    status = Column(String, default="PENDING", nullable=False)  # PENDING | APPROVED | SUSPENDED | DELETED

    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    listing = relationship("Listing", back_populates="reports")
    reporter = relationship("User", back_populates="reports")


# ─────────────────────────────────────────────
# FRAUD SCORE RECORD
# ─────────────────────────────────────────────
class FraudScoreRecord(Base):
    __tablename__ = "fraud_score_records"

    id = Column(String, primary_key=True, default=generate_id)
    listing_id = Column(String, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)
    factors = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    listing = relationship("Listing", back_populates="fraud_records")


# ─────────────────────────────────────────────
# SAFETY MAP POINT
# ─────────────────────────────────────────────
class SafetyMapPoint(Base):
    __tablename__ = "safety_map_points"

    id = Column(String, primary_key=True, default=generate_id)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    district = Column(String, nullable=False)
    city = Column(String, nullable=False)
    safety_index = Column(Integer, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# ─────────────────────────────────────────────
# AUDIT LOG
# ─────────────────────────────────────────────
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=generate_id)
    admin_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action = Column(String, nullable=False)
    target_type = Column(String, nullable=False)
    target_id = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    admin = relationship("User", back_populates="audit_logs")


# ─────────────────────────────────────────────
# NOTIFICATION
# ─────────────────────────────────────────────
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=generate_id)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=True)
    link = Column(String, nullable=True)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="notifications")


# ─────────────────────────────────────────────
# USER CONSENT
# ─────────────────────────────────────────────
class UserConsent(Base):
    __tablename__ = "user_consents"

    id = Column(String, primary_key=True, default=generate_id)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    consent_type = Column(String, nullable=False)
    granted = Column(Boolean, default=True, nullable=False)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    version = Column(String, default="1.0", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    revoked_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="consents")


# ─────────────────────────────────────────────
# COOKIE PREFERENCE
# ─────────────────────────────────────────────
class CookiePreference(Base):
    __tablename__ = "cookie_preferences"

    id = Column(String, primary_key=True, default=generate_id)
    session_id = Column(String, nullable=True)
    necessary = Column(Boolean, default=True, nullable=False)
    analytics = Column(Boolean, default=False, nullable=False)
    marketing = Column(Boolean, default=False, nullable=False)
    performance = Column(Boolean, default=False, nullable=False)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# ─────────────────────────────────────────────
# DATA REQUEST
# ─────────────────────────────────────────────
class DataRequest(Base):
    __tablename__ = "data_requests"

    id = Column(String, primary_key=True, default=generate_id)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    request_type = Column(String, nullable=False)
    status = Column(String, default="PENDING", nullable=False)
    reason = Column(Text, nullable=True)

    response = Column(Text, nullable=True)
    processed_by = Column(String, nullable=True)
    processed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="data_requests")


# ─────────────────────────────────────────────
# LOGIN HISTORY
# ─────────────────────────────────────────────
class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(String, primary_key=True, default=generate_id)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ip_address = Column(String, nullable=False)
    user_agent = Column(String, nullable=False)
    success = Column(Boolean, default=True, nullable=False)
    fail_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="login_history")


# ─────────────────────────────────────────────
# SYSTEM LOG
# ─────────────────────────────────────────────
class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(String, primary_key=True, default=generate_id)
    level = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    meta_data = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# ─────────────────────────────────────────────
# RATING
# ─────────────────────────────────────────────
class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (UniqueConstraint("rater_id", "rated_id", "rating_number", name="uq_rating_user_number"),)

    id = Column(String, primary_key=True, default=generate_id)
    rater_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rated_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    rating_number = Column(Integer, nullable=False)  # 1 or 2 (each user can rate twice)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    rater = relationship("User", foreign_keys=[rater_id], backref="ratings_given")
    rated = relationship("User", foreign_keys=[rated_id], backref="ratings_received")


# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)
