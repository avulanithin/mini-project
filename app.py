"""
Blood Donation Camp Queue Simulation & Planning System
Main Flask application entry point
"""
from flask import Flask
import os
from config import SECRET_KEY, DEBUG, DATABASE_PATH
from models import init_db
from routes import main_bp, api_bp


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = DEBUG
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("=" * 70)
    print("Blood Donation Camp Queue Simulation & Planning System")
    print("=" * 70)
    print(f"Database: {DATABASE_PATH}")
    print("Server starting on http://127.0.0.1:5000")
    print("=" * 70)
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
