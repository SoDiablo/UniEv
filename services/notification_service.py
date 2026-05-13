# services/notification_service.py
from database import Notification
from sqlalchemy.orm import Session
from datetime import datetime


def create_notification(
    db: Session,
    user_id: str,
    notification_type: str,
    title: str,
    body: str = None,
    link: str = None
):
    """Create a notification for a user"""
    notification = Notification(
        user_id=user_id,
        type=notification_type,
        title=title,
        body=body,
        link=link,
        created_at=datetime.utcnow()
    )
    db.add(notification)
    db.commit()
    return notification
