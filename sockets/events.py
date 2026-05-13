# sockets/events.py
import socketio
from database import SessionLocal, Message, User, Notification
from datetime import datetime

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid, environ, auth):
    """Client connects and authenticates via JWT in auth data"""
    print(f"Client connected: {sid}")


@sio.event
async def join_conversation(sid, data):
    """
    Join a private chat room between two users.
    Room format: "chat_{smaller_id}_{larger_id}"
    """
    user_id = data["user_id"]
    other_id = data["other_user_id"]
    room = f"chat_{min(user_id, other_id)}_{max(user_id, other_id)}"
    await sio.enter_room(sid, room)
    await sio.emit("joined", {"room": room}, to=sid)


@sio.event
async def send_message(sid, data):
    """
    Send a message.
    Write to DB FIRST, then emit.
    """
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]
    content = data["content"]

    db = SessionLocal()
    try:
        # Always write to DB first
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            created_at=datetime.utcnow()
        )
        db.add(message)

        # Create notification for receiver
        notification = Notification(
            user_id=receiver_id,
            type="MESSAGE",
            title="Yeni mesaj",
            body=f"{content[:50]}..." if len(content) > 50 else content,
            link=f"/messages?with={sender_id}"
        )
        db.add(notification)
        db.commit()
        db.refresh(message)

        # Determine room name
        room = f"chat_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"

        # Emit to room
        await sio.emit("new_message", {
            "id": message.id,
            "sender_id": sender_id,
            "content": content,
            "created_at": message.created_at.isoformat()
        }, to=room)

    finally:
        db.close()


@sio.event
async def mark_read(sid, data):
    """Mark a message as read"""
    message_id = data["message_id"]
    db = SessionLocal()
    try:
        message = db.query(Message).filter(Message.id == message_id).first()
        if message and not message.read_at:
            message.read_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
