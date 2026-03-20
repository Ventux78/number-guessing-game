"""Configuration settings for the application."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SOCKETIO_ASYNC_MODE = "threading"
    RECONNECTION_TIMEOUT = 30  # seconds