# 🏠 UniEv — University Housing Platform

> A full-stack web platform for university students to find verified rental 
> housing and compatible roommates — built with FastAPI, Socket.IO, and SQLAlchemy.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🔗 Live Demo
**[uniev.yourdomain.com](https://uniev.yourdomain.com)** ← add this after hosting

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 FraudScore Engine | Automatically rates listing trustworthiness 0–100 using 6 signals |
| 🤝 Match Engine | Finds compatible roommates based on lifestyle and budget preferences |
| 🗺️ SafetyMap | Neighborhood safety index via Haversine coordinate queries |
| 💬 Real-time Chat | Socket.IO messaging with read receipts and media support |
| 🔐 JWT Auth | Argon2 password hashing, account lockout, token versioning |
| 📋 KVKK Compliant | Full Turkish data protection law compliance |
| 🗺️ Google Maps | Interactive maps on listing pages |
| 👮 Admin Panel | Full moderation system with AuditLog |

## 🛠️ Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy ORM
- **Database:** SQLite (dev) / PostgreSQL (production)
- **Real-time:** Socket.IO (python-socketio)
- **Frontend:** Jinja2, Tailwind CSS
- **Auth:** JWT (HS256), Argon2
- **Email:** aiosmtplib (async SMTP)

## 🚀 Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/uniev.git
cd uniev
pip install -r requirements.txt
cp .env.example .env    # Fill in your values
python seed_safety.py   # Add sample safety data
uvicorn main:socket_app --host 0.0.0.0 --port 8000
```
