from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import Config
from routes import auth_bp, video_bp
from models import Video


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for React Native app
    # Enable CORS for React Native app
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Configure Logging
    import logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    # Initialize Limiter
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )
    app.limiter = limiter # Attach to app for blueprints to use
    
    # Initialize MongoDB connection
    client = MongoClient(Config.MONGODB_URI)
    app.db = client.get_database()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(video_bp)
    
    # Seed initial video data
    with app.app_context():
        video_model = Video(app.db)
        video_model.seed_videos()
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'service': 'video-app-api'}, 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("\n🚀 Flask API Server running on http://localhost:5000")
    print("📱 Ready for React Native app connections\n")
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
