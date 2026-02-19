"""
Configuration settings for Blood Donation Camp Queue Simulation System
"""
import os

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configuration
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'blood_camp.db')

# Flask configuration
SECRET_KEY = 'blood-donation-camp-simulation-secret-key-2026'
DEBUG = True

# Application settings
APP_NAME = "Blood Donation Camp Queue Simulation & Planning System"
VERSION = "1.0.0"

# Simulation default parameters
DEFAULT_ARRIVAL_RATE = 5  # donors per hour
DEFAULT_SCREENING_TIME = 10  # minutes
DEFAULT_DONATION_TIME = 15  # minutes
DEFAULT_SERVERS = 3

# Queue simulation parameters
SIMULATION_TIME_STEP = 1  # minutes
