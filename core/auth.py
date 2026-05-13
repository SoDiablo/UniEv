# core/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from database import get_db, User
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

SECRET_KEY = os.getenv("JWT_SECRET", "change-me")
ALGORITHM = "HS256"
EXPIRE_DAYS = int(os.getenv("JWT_EXPIRE_DAYS", 7))


def create_token(user: User) -> str:
    payload = {
        "sub": user.id,
        "email": user.email,
        "role": user.role,
        "tv": user.token_version,
        "exp": datetime.utcnow() + timedelta(days=EXPIRE_DAYS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    payload = decode_token(token)
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
    if user.token_version != payload.get("tv", 0):
        raise HTTPException(status_code=401, detail="Token geçersiz kılındı, lütfen tekrar giriş yapın")
    return user


def require_verified(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to require email verification
    
    Usage:
        @router.get("/protected")
        def protected_route(user: User = Depends(require_verified)):
            return {"message": "Access granted"}
    
    Returns HTTP 403 if user is not verified
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=403, 
            detail="Please verify your email before accessing this feature"
        )
    return current_user
    if current_user.is_suspended:
        raise HTTPException(status_code=403, detail="Hesabınız askıya alınmıştır")
    return current_user


def require_landlord(current_user: User = Depends(require_verified)) -> User:
    if current_user.role != "LANDLORD":
        raise HTTPException(status_code=403, detail="Bu işlem için ev sahibi yetkisi gereklidir")
    return current_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Bu işlem için admin yetkisi gereklidir")
    return current_user
