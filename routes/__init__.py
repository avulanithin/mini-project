"""
Routes module for handling HTTP requests
"""
from flask import Blueprint

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import route handlers
from . import main_routes
from . import api_routes

__all__ = ['main_bp', 'api_bp']
