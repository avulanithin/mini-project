"""
Service Station model for tracking server utilization
"""
from .database import get_db, close_db


class ServiceStation:
    """Represents a service station (server) in the simulation"""
    
    def __init__(self, id=None, simulation_id=None, station_type=None, station_number=None,
                 utilization_rate=None, total_service_time=None, donors_served=None):
        self.id = id
        self.simulation_id = simulation_id
        self.station_type = station_type
        self.station_number = station_number
        self.utilization_rate = utilization_rate
        self.total_service_time = total_service_time
        self.donors_served = donors_served
    
    @staticmethod
    def create(simulation_id, station_type, station_number, utilization_rate,
               total_service_time, donors_served):
        """Create a new service station record"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO service_stations (
                simulation_id, station_type, station_number, utilization_rate,
                total_service_time, donors_served
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (simulation_id, station_type, station_number, utilization_rate,
              total_service_time, donors_served))
        conn.commit()
        station_id = cursor.lastrowid
        close_db(conn)
        return station_id
    
    @staticmethod
    def bulk_create(stations_data):
        """Bulk insert service stations"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO service_stations (
                simulation_id, station_type, station_number, utilization_rate,
                total_service_time, donors_served
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', stations_data)
        conn.commit()
        close_db(conn)
    
    @staticmethod
    def get_by_simulation_id(simulation_id):
        """Get all service stations for a simulation"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM service_stations 
            WHERE simulation_id = ? 
            ORDER BY station_type, station_number
        ''', (simulation_id,))
        rows = cursor.fetchall()
        close_db(conn)
        
        stations = [ServiceStation(**dict(row)) for row in rows]
        return stations
    
    def to_dict(self):
        """Convert service station to dictionary"""
        return {
            'id': self.id,
            'simulation_id': self.simulation_id,
            'station_type': self.station_type,
            'station_number': self.station_number,
            'utilization_rate': self.utilization_rate,
            'total_service_time': self.total_service_time,
            'donors_served': self.donors_served
        }
