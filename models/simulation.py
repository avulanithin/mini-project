"""
Simulation model for storing simulation run data
"""
from .database import get_db, close_db


class Simulation:
    """Represents a simulation run"""
    
    def __init__(self, id=None, camp_id=None, num_servers=None, num_screening_staff=None,
                 avg_screening_time=None, avg_donation_time=None, arrival_rate=None,
                 arrival_distribution=None, service_distribution=None, queue_discipline=None,
                 allow_idle_servers=None, total_donors_simulated=None, donors_served=None,
                 donors_unserved=None, avg_waiting_time=None, max_waiting_time=None,
                 avg_queue_length=None, avg_server_utilization=None, simulation_date=None):
        self.id = id
        self.camp_id = camp_id
        self.num_servers = num_servers
        self.num_screening_staff = num_screening_staff
        self.avg_screening_time = avg_screening_time
        self.avg_donation_time = avg_donation_time
        self.arrival_rate = arrival_rate
        self.arrival_distribution = arrival_distribution
        self.service_distribution = service_distribution
        self.queue_discipline = queue_discipline
        self.allow_idle_servers = allow_idle_servers
        self.total_donors_simulated = total_donors_simulated
        self.donors_served = donors_served
        self.donors_unserved = donors_unserved
        self.avg_waiting_time = avg_waiting_time
        self.max_waiting_time = max_waiting_time
        self.avg_queue_length = avg_queue_length
        self.avg_server_utilization = avg_server_utilization
        self.simulation_date = simulation_date
    
    @staticmethod
    def create(camp_id, num_servers, num_screening_staff, avg_screening_time, avg_donation_time,
               arrival_rate, arrival_distribution='Poisson', service_distribution='Exponential',
               queue_discipline='FCFS', allow_idle_servers=1):
        """Create a new simulation record"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO simulations (
                camp_id, num_servers, num_screening_staff, avg_screening_time, 
                avg_donation_time, arrival_rate, arrival_distribution, service_distribution,
                queue_discipline, allow_idle_servers
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (camp_id, num_servers, num_screening_staff, avg_screening_time, avg_donation_time,
              arrival_rate, arrival_distribution, service_distribution, queue_discipline, allow_idle_servers))
        conn.commit()
        simulation_id = cursor.lastrowid
        close_db(conn)
        return simulation_id
    
    @staticmethod
    def update_results(simulation_id, total_donors, donors_served, donors_unserved,
                       avg_wait, max_wait, avg_queue_len, avg_util):
        """Update simulation with results"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE simulations SET
                total_donors_simulated = ?,
                donors_served = ?,
                donors_unserved = ?,
                avg_waiting_time = ?,
                max_waiting_time = ?,
                avg_queue_length = ?,
                avg_server_utilization = ?
            WHERE id = ?
        ''', (total_donors, donors_served, donors_unserved, avg_wait, max_wait, 
              avg_queue_len, avg_util, simulation_id))
        conn.commit()
        close_db(conn)
    
    @staticmethod
    def get_by_id(simulation_id):
        """Get simulation by ID"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM simulations WHERE id = ?', (simulation_id,))
        row = cursor.fetchone()
        close_db(conn)
        
        if row:
            return Simulation(**dict(row))
        return None
    
    @staticmethod
    def get_by_camp_id(camp_id):
        """Get all simulations for a camp"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM simulations WHERE camp_id = ? ORDER BY simulation_date DESC', (camp_id,))
        rows = cursor.fetchall()
        close_db(conn)
        
        simulations = [Simulation(**dict(row)) for row in rows]
        return simulations
    
    @staticmethod
    def get_all():
        """Get all simulations"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM simulations ORDER BY simulation_date DESC')
        rows = cursor.fetchall()
        close_db(conn)
        
        simulations = [Simulation(**dict(row)) for row in rows]
        return simulations
    
    def to_dict(self):
        """Convert simulation to dictionary"""
        return {
            'id': self.id,
            'camp_id': self.camp_id,
            'num_servers': self.num_servers,
            'num_screening_staff': self.num_screening_staff,
            'avg_screening_time': self.avg_screening_time,
            'avg_donation_time': self.avg_donation_time,
            'arrival_rate': self.arrival_rate,
            'arrival_distribution': self.arrival_distribution,
            'service_distribution': self.service_distribution,
            'queue_discipline': self.queue_discipline,
            'allow_idle_servers': self.allow_idle_servers,
            'total_donors_simulated': self.total_donors_simulated,
            'donors_served': self.donors_served,
            'donors_unserved': self.donors_unserved,
            'avg_waiting_time': self.avg_waiting_time,
            'max_waiting_time': self.max_waiting_time,
            'avg_queue_length': self.avg_queue_length,
            'avg_server_utilization': self.avg_server_utilization,
            'simulation_date': self.simulation_date
        }
