import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/video_app')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    JWT_EXPIRY_HOURS = int(os.getenv('JWT_EXPIRY_HOURS', 24))
    PLAYBACK_SECRET_KEY = os.getenv('PLAYBACK_SECRET_KEY', 'playback-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
