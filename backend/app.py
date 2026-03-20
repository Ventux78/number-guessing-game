"""Main Flask application with Socket.IO integration."""
import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config


def create_app(config_class=Config):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure CORS for both HTTP and WebSocket
    CORS(app)
    
    # Initialize Socket.IO with CORS configuration
    allowed_origins = os.getenv('ALLOWED_ORIGINS', '*').split(',')
    socketio = SocketIO(
        app, 
        cors_allowed_origins=allowed_origins,
        async_mode='threading',
        ping_timeout=60,
        ping_interval=25,
        engineio_logger=False,
        socketio_logger=False
    )
    
    # Register event handlers
    from handlers import register_handlers
    register_handlers(socketio)
    
    return app, socketio


# Create app and socketio instances for production
app, socketio = create_app()


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
