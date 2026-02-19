"""
Camp model for managing blood donation camp information
"""
from .database import get_db, close_db


class Camp:
    """Represents a blood donation camp"""
    
    def __init__(self, id=None, name=None, start_time=None, end_time=None, 
                 duration_minutes=None, max_donors=None, peak_hours=None, created_at=None):
        self.id = id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.duration_minutes = duration_minutes
        self.max_donors = max_donors
        self.peak_hours = peak_hours
        self.created_at = created_at
    
    @staticmethod
    def create(name, start_time, end_time, duration_minutes, max_donors=None, peak_hours=None):
        """Create a new camp"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO camps (name, start_time, end_time, duration_minutes, max_donors, peak_hours)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, start_time, end_time, duration_minutes, max_donors, peak_hours))
        conn.commit()
        camp_id = cursor.lastrowid
        close_db(conn)
        return camp_id
    
    @staticmethod
    def get_by_id(camp_id):
        """Get camp by ID"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM camps WHERE id = ?', (camp_id,))
        row = cursor.fetchone()
        close_db(conn)
        
        if row:
            return Camp(
                id=row['id'],
                name=row['name'],
                start_time=row['start_time'],
                end_time=row['end_time'],
                duration_minutes=row['duration_minutes'],
                max_donors=row['max_donors'],
                peak_hours=row['peak_hours'],
                created_at=row['created_at']
            )
        return None
    
    @staticmethod
    def get_all():
        """Get all camps"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM camps ORDER BY created_at DESC')
        rows = cursor.fetchall()
        close_db(conn)
        
        camps = []
        for row in rows:
            camps.append(Camp(
                id=row['id'],
                name=row['name'],
                start_time=row['start_time'],
                end_time=row['end_time'],
                duration_minutes=row['duration_minutes'],
                max_donors=row['max_donors'],
                peak_hours=row['peak_hours'],
                created_at=row['created_at']
            ))
        return camps
    
    def to_dict(self):
        """Convert camp to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration_minutes': self.duration_minutes,
            'max_donors': self.max_donors,
            'peak_hours': self.peak_hours,
            'created_at': self.created_at
        }
