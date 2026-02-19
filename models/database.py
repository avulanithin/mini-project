"""
Database initialization and connection management
"""
import sqlite3
import os
from config import DATABASE_PATH


def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def close_db(conn):
    """Close database connection"""
    if conn:
        conn.close()


def init_db():
    """Initialize database schema"""
    # Create database directory if it doesn't exist
    db_dir = os.path.dirname(DATABASE_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Create camps table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS camps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            max_donors INTEGER,
            peak_hours TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create simulations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camp_id INTEGER NOT NULL,
            num_servers INTEGER NOT NULL,
            num_screening_staff INTEGER NOT NULL,
            avg_screening_time REAL NOT NULL,
            avg_donation_time REAL NOT NULL,
            arrival_rate REAL NOT NULL,
            arrival_distribution TEXT DEFAULT 'Poisson',
            service_distribution TEXT DEFAULT 'Exponential',
            queue_discipline TEXT DEFAULT 'FCFS',
            allow_idle_servers INTEGER DEFAULT 1,
            total_donors_simulated INTEGER,
            donors_served INTEGER,
            donors_unserved INTEGER,
            avg_waiting_time REAL,
            max_waiting_time REAL,
            avg_queue_length REAL,
            avg_server_utilization REAL,
            simulation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (camp_id) REFERENCES camps (id)
        )
    ''')
    
    # Create donors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id INTEGER NOT NULL,
            donor_index INTEGER NOT NULL,
            arrival_time REAL NOT NULL,
            registration_start REAL,
            registration_end REAL,
            screening_start REAL,
            screening_end REAL,
            donation_start REAL,
            donation_end REAL,
            registration_wait REAL,
            screening_wait REAL,
            donation_wait REAL,
            total_wait_time REAL,
            total_time_in_system REAL,
            served INTEGER DEFAULT 0,
            FOREIGN KEY (simulation_id) REFERENCES simulations (id)
        )
    ''')
    
    # Create service_stations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_stations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id INTEGER NOT NULL,
            station_type TEXT NOT NULL,
            station_number INTEGER NOT NULL,
            utilization_rate REAL NOT NULL,
            total_service_time REAL NOT NULL,
            donors_served INTEGER NOT NULL,
            FOREIGN KEY (simulation_id) REFERENCES simulations (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at: {DATABASE_PATH}")
