import jwt
import hashlib
import time
from datetime import datetime, timedelta
from config import Config


def generate_jwt(user_id: str) -> str:
    """Generate JWT token for authenticated user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRY_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')


def decode_jwt(token: str) -> dict | None:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def generate_playback_token(video_id: str, user_id: str) -> str:
    """
    Generate a signed playback token for video streaming.
    Token includes video_id, user_id, and expiry (1 hour).
    """
    expiry = int(time.time()) + 3600  # 1 hour expiry
    data = f"{video_id}:{user_id}:{expiry}"
    signature = hashlib.sha256(
        f"{data}:{Config.PLAYBACK_SECRET_KEY}".encode()
    ).hexdigest()[:16]
    
    return f"{data}:{signature}"


def verify_playback_token(token: str, video_id: str) -> bool:
    """Verify playback token is valid and not expired"""
    try:
        parts = token.split(':')
        if len(parts) != 4:
            return False
        
        token_video_id, user_id, expiry_str, signature = parts
        
        # Check video ID matches
        if token_video_id != video_id:
            return False
        
        # Check expiry
        expiry = int(expiry_str)
        if time.time() > expiry:
            return False
        
        # Verify signature
        data = f"{token_video_id}:{user_id}:{expiry_str}"
        expected_signature = hashlib.sha256(
            f"{data}:{Config.PLAYBACK_SECRET_KEY}".encode()
        ).hexdigest()[:16]
        
        return signature == expected_signature
    except Exception:
        return False
