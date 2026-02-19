"""
Donor model for tracking individual donor journey through the system
"""
from .database import get_db, close_db


class Donor:
    """Represents a donor in the simulation"""
    
    def __init__(self, id=None, simulation_id=None, donor_index=None, arrival_time=None,
                 registration_start=None, registration_end=None, screening_start=None,
                 screening_end=None, donation_start=None, donation_end=None,
                 registration_wait=None, screening_wait=None, donation_wait=None,
                 total_wait_time=None, total_time_in_system=None, served=None):
        self.id = id
        self.simulation_id = simulation_id
        self.donor_index = donor_index
        self.arrival_time = arrival_time
        self.registration_start = registration_start
        self.registration_end = registration_end
        self.screening_start = screening_start
        self.screening_end = screening_end
        self.donation_start = donation_start
        self.donation_end = donation_end
        self.registration_wait = registration_wait
        self.screening_wait = screening_wait
        self.donation_wait = donation_wait
        self.total_wait_time = total_wait_time
        self.total_time_in_system = total_time_in_system
        self.served = served
    
    @staticmethod
    def create(simulation_id, donor_index, arrival_time, registration_start=None,
               registration_end=None, screening_start=None, screening_end=None,
               donation_start=None, donation_end=None, registration_wait=None,
               screening_wait=None, donation_wait=None, total_wait_time=None,
               total_time_in_system=None, served=0):
        """Create a new donor record"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO donors (
                simulation_id, donor_index, arrival_time, registration_start, registration_end,
                screening_start, screening_end, donation_start, donation_end,
                registration_wait, screening_wait, donation_wait, total_wait_time,
                total_time_in_system, served
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (simulation_id, donor_index, arrival_time, registration_start, registration_end,
              screening_start, screening_end, donation_start, donation_end,
              registration_wait, screening_wait, donation_wait, total_wait_time,
              total_time_in_system, served))
        conn.commit()
        donor_id = cursor.lastrowid
        close_db(conn)
        return donor_id
    
    @staticmethod
    def bulk_create(donors_data):
        """Bulk insert donors for better performance"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO donors (
                simulation_id, donor_index, arrival_time, registration_start, registration_end,
                screening_start, screening_end, donation_start, donation_end,
                registration_wait, screening_wait, donation_wait, total_wait_time,
                total_time_in_system, served
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', donors_data)
        conn.commit()
        close_db(conn)
    
    @staticmethod
    def get_by_simulation_id(simulation_id):
        """Get all donors for a simulation"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM donors WHERE simulation_id = ? ORDER BY donor_index', (simulation_id,))
        rows = cursor.fetchall()
        close_db(conn)
        
        donors = [Donor(**dict(row)) for row in rows]
        return donors
    
    def to_dict(self):
        """Convert donor to dictionary"""
        return {
            'id': self.id,
            'simulation_id': self.simulation_id,
            'donor_index': self.donor_index,
            'arrival_time': self.arrival_time,
            'registration_start': self.registration_start,
            'registration_end': self.registration_end,
            'screening_start': self.screening_start,
            'screening_end': self.screening_end,
            'donation_start': self.donation_start,
            'donation_end': self.donation_end,
            'registration_wait': self.registration_wait,
            'screening_wait': self.screening_wait,
            'donation_wait': self.donation_wait,
            'total_wait_time': self.total_wait_time,
            'total_time_in_system': self.total_time_in_system,
            'served': self.served
        }
