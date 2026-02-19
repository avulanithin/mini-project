"""
Discrete-Event Simulation Engine for Blood Donation Camp
Simulates donor arrivals, multi-stage queuing, and service processes
"""
import numpy as np
from collections import deque
import heapq


class Event:
    """Represents a simulation event"""
    def __init__(self, time, event_type, donor_id, data=None):
        self.time = time
        self.event_type = event_type  # 'arrival', 'registration_end', 'screening_end', 'donation_end'
        self.donor_id = donor_id
        self.data = data or {}
    
    def __lt__(self, other):
        return self.time < other.time


class DonorEntity:
    """Represents a donor entity in the simulation"""
    def __init__(self, donor_id, arrival_time):
        self.donor_id = donor_id
        self.arrival_time = arrival_time
        self.registration_start = None
        self.registration_end = None
        self.screening_start = None
        self.screening_end = None
        self.donation_start = None
        self.donation_end = None
        self.served = False


class Server:
    """Represents a service server"""
    def __init__(self, server_id, server_type):
        self.server_id = server_id
        self.server_type = server_type  # 'registration', 'screening', 'donation'
        self.busy = False
        self.current_donor = None
        self.busy_until = 0
        self.total_service_time = 0
        self.donors_served = 0


class SimulationEngine:
    """
    Discrete-event simulation engine for blood donation camp
    Implements multi-stage queuing with:
    - Poisson arrivals
    - Three service stages: Registration, Screening, Donation
    - Multiple parallel servers
    - FCFS queue discipline
    """
    
    def __init__(self, duration_minutes, num_servers, num_screening_staff,
                 avg_screening_time, avg_donation_time, arrival_rate,
                 arrival_distribution='Poisson', service_distribution='Exponential',
                 max_donors=None, allow_idle_servers=True):
        """
        Initialize simulation parameters
        
        Args:
            duration_minutes: Total camp duration in minutes
            num_servers: Number of donation service counters
            num_screening_staff: Number of screening staff
            avg_screening_time: Average screening time in minutes
            avg_donation_time: Average donation time in minutes
            arrival_rate: Donor arrival rate (donors per hour)
            arrival_distribution: Distribution for arrivals ('Poisson')
            service_distribution: Distribution for service times ('Exponential' or 'Uniform')
            max_donors: Maximum donors allowed (optional)
            allow_idle_servers: Whether to allow idle servers
        """
        self.duration_minutes = duration_minutes
        self.num_servers = num_servers
        self.num_screening_staff = num_screening_staff
        self.avg_screening_time = avg_screening_time
        self.avg_donation_time = avg_donation_time
        self.arrival_rate = arrival_rate  # donors per hour
        self.arrival_distribution = arrival_distribution
        self.service_distribution = service_distribution
        self.max_donors = max_donors
        self.allow_idle_servers = allow_idle_servers
        
        # Simulation state
        self.current_time = 0
        self.event_queue = []  # Priority queue of events
        self.donors = {}  # donor_id -> DonorEntity
        self.donor_counter = 0
        
        # Queues for each stage
        self.registration_queue = deque()
        self.screening_queue = deque()
        self.donation_queue = deque()
        
        # Servers for each stage (assuming 1 registration desk)
        self.registration_servers = [Server(1, 'registration')]
        self.screening_servers = [Server(i+1, 'screening') for i in range(num_screening_staff)]
        self.donation_servers = [Server(i+1, 'donation') for i in range(num_servers)]
        
        # Statistics tracking
        self.queue_length_samples = []  # (time, registration_q, screening_q, donation_q)
        self.time_points = []
        self.completed_donors = []
        
    def generate_interarrival_time(self):
        """Generate time between arrivals using Poisson process (exponential distribution)"""
        lambd = self.arrival_rate / 60.0  # Convert to arrivals per minute
        return np.random.exponential(1.0 / lambd)
    
    def generate_service_time(self, avg_time):
        """Generate service time based on configured distribution"""
        if self.service_distribution == 'Exponential':
            return np.random.exponential(avg_time)
        elif self.service_distribution == 'Uniform':
            # Uniform distribution around the average (±30%)
            return np.random.uniform(avg_time * 0.7, avg_time * 1.3)
        else:
            return avg_time
    
    def schedule_event(self, event):
        """Add event to priority queue"""
        heapq.heappush(self.event_queue, event)
    
    def get_next_event(self):
        """Get next event from priority queue"""
        if self.event_queue:
            return heapq.heappop(self.event_queue)
        return None
    
    def find_free_server(self, servers):
        """Find a free server from the list"""
        for server in servers:
            if not server.busy:
                return server
        return None
    
    def start_service(self, donor, servers, queue, stage_name, avg_service_time):
        """Start service for a donor at a specific stage"""
        server = self.find_free_server(servers)
        
        if server:
            # Start service
            server.busy = True
            server.current_donor = donor.donor_id
            service_time = self.generate_service_time(avg_service_time)
            end_time = self.current_time + service_time
            server.busy_until = end_time
            server.total_service_time += service_time
            server.donors_served += 1
            
            # Update donor record
            if stage_name == 'registration':
                donor.registration_start = self.current_time
                donor.registration_end = end_time
                event_type = 'registration_end'
            elif stage_name == 'screening':
                donor.screening_start = self.current_time
                donor.screening_end = end_time
                event_type = 'screening_end'
            else:  # donation
                donor.donation_start = self.current_time
                donor.donation_end = end_time
                event_type = 'donation_end'
            
            # Schedule completion event
            self.schedule_event(Event(end_time, event_type, donor.donor_id, {'server_id': server.server_id}))
            return True
        else:
            # Add to queue
            queue.append(donor.donor_id)
            return False
    
    def handle_arrival(self, event):
        """Handle donor arrival event"""
        donor_id = event.donor_id
        donor = self.donors[donor_id]
        
        # Try to start registration immediately
        if not self.start_service(donor, self.registration_servers, self.registration_queue, 'registration', 3):
            # Added to queue, nothing more to do
            pass
        
        # Schedule next arrival if within camp duration
        if self.max_donors is None or self.donor_counter < self.max_donors:
            next_arrival_time = self.current_time + self.generate_interarrival_time()
            if next_arrival_time < self.duration_minutes:
                self.donor_counter += 1
                new_donor = DonorEntity(self.donor_counter, next_arrival_time)
                self.donors[new_donor.donor_id] = new_donor
                self.schedule_event(Event(next_arrival_time, 'arrival', new_donor.donor_id))
    
    def handle_registration_end(self, event):
        """Handle registration completion"""
        donor = self.donors[event.donor_id]
        
        # Free the server
        for server in self.registration_servers:
            if server.current_donor == donor.donor_id:
                server.busy = False
                server.current_donor = None
                break
        
        # Try to start screening
        self.start_service(donor, self.screening_servers, self.screening_queue, 'screening', self.avg_screening_time)
        
        # Process registration queue
        if self.registration_queue:
            next_donor_id = self.registration_queue.popleft()
            next_donor = self.donors[next_donor_id]
            self.start_service(next_donor, self.registration_servers, self.registration_queue, 'registration', 3)
    
    def handle_screening_end(self, event):
        """Handle screening completion"""
        donor = self.donors[event.donor_id]
        
        # Free the server
        for server in self.screening_servers:
            if server.current_donor == donor.donor_id:
                server.busy = False
                server.current_donor = None
                break
        
        # Try to start donation
        self.start_service(donor, self.donation_servers, self.donation_queue, 'donation', self.avg_donation_time)
        
        # Process screening queue
        if self.screening_queue:
            next_donor_id = self.screening_queue.popleft()
            next_donor = self.donors[next_donor_id]
            self.start_service(next_donor, self.screening_servers, self.screening_queue, 'screening', self.avg_screening_time)
    
    def handle_donation_end(self, event):
        """Handle donation completion"""
        donor = self.donors[event.donor_id]
        donor.served = True
        self.completed_donors.append(donor)
        
        # Free the server
        for server in self.donation_servers:
            if server.current_donor == donor.donor_id:
                server.busy = False
                server.current_donor = None
                break
        
        # Process donation queue
        if self.donation_queue:
            next_donor_id = self.donation_queue.popleft()
            next_donor = self.donors[next_donor_id]
            self.start_service(next_donor, self.donation_servers, self.donation_queue, 'donation', self.avg_donation_time)
    
    def record_queue_lengths(self):
        """Record current queue lengths for statistics"""
        self.queue_length_samples.append({
            'time': self.current_time,
            'registration': len(self.registration_queue),
            'screening': len(self.screening_queue),
            'donation': len(self.donation_queue),
            'total': len(self.registration_queue) + len(self.screening_queue) + len(self.donation_queue)
        })
    
    def run(self):
        """Run the simulation"""
        # Initialize first arrival
        self.donor_counter = 1
        first_arrival_time = self.generate_interarrival_time()
        first_donor = DonorEntity(self.donor_counter, first_arrival_time)
        self.donors[first_donor.donor_id] = first_donor
        self.schedule_event(Event(first_arrival_time, 'arrival', first_donor.donor_id))
        
        # Process events
        while self.event_queue:
            event = self.get_next_event()
            
            # Stop if event is beyond camp duration
            if event.time > self.duration_minutes:
                break
            
            self.current_time = event.time
            
            # Record queue lengths periodically
            if len(self.queue_length_samples) == 0 or self.current_time - self.queue_length_samples[-1]['time'] >= 1:
                self.record_queue_lengths()
            
            # Handle event based on type
            if event.event_type == 'arrival':
                self.handle_arrival(event)
            elif event.event_type == 'registration_end':
                self.handle_registration_end(event)
            elif event.event_type == 'screening_end':
                self.handle_screening_end(event)
            elif event.event_type == 'donation_end':
                self.handle_donation_end(event)
        
        # Final queue length recording
        self.current_time = self.duration_minutes
        self.record_queue_lengths()
        
        return self.compute_results()
    
    def compute_results(self):
        """Compute simulation results and statistics"""
        results = {
            'donors': [],
            'service_stations': [],
            'summary': {}
        }
        
        # Process each donor
        total_donors = len(self.donors)
        donors_served = 0
        donors_unserved = 0
        total_wait_times = []
        max_wait_time = 0
        
        for donor_id, donor in self.donors.items():
            # Calculate waiting times
            registration_wait = (donor.registration_start - donor.arrival_time) if donor.registration_start else 0
            screening_wait = (donor.screening_start - donor.registration_end) if donor.screening_start and donor.registration_end else 0
            donation_wait = (donor.donation_start - donor.screening_end) if donor.donation_start and donor.screening_end else 0
            
            total_wait = registration_wait + screening_wait + donation_wait
            total_time_in_system = (donor.donation_end - donor.arrival_time) if donor.donation_end else 0
            
            if donor.served:
                donors_served += 1
                total_wait_times.append(total_wait)
                max_wait_time = max(max_wait_time, total_wait)
            else:
                donors_unserved += 1
            
            results['donors'].append({
                'donor_index': donor.donor_id,
                'arrival_time': round(donor.arrival_time, 2),
                'registration_start': round(donor.registration_start, 2) if donor.registration_start else None,
                'registration_end': round(donor.registration_end, 2) if donor.registration_end else None,
                'screening_start': round(donor.screening_start, 2) if donor.screening_start else None,
                'screening_end': round(donor.screening_end, 2) if donor.screening_end else None,
                'donation_start': round(donor.donation_start, 2) if donor.donation_start else None,
                'donation_end': round(donor.donation_end, 2) if donor.donation_end else None,
                'registration_wait': round(registration_wait, 2),
                'screening_wait': round(screening_wait, 2),
                'donation_wait': round(donation_wait, 2),
                'total_wait_time': round(total_wait, 2),
                'total_time_in_system': round(total_time_in_system, 2),
                'served': 1 if donor.served else 0
            })
        
        # Calculate average waiting time
        avg_wait = sum(total_wait_times) / len(total_wait_times) if total_wait_times else 0
        
        # Calculate average queue length
        avg_queue_length = sum(s['total'] for s in self.queue_length_samples) / len(self.queue_length_samples) if self.queue_length_samples else 0
        
        # Calculate server utilization
        all_servers = self.registration_servers + self.screening_servers + self.donation_servers
        total_utilization = 0
        
        for server in all_servers:
            utilization = (server.total_service_time / self.duration_minutes) * 100 if self.duration_minutes > 0 else 0
            results['service_stations'].append({
                'station_type': server.server_type,
                'station_number': server.server_id,
                'utilization_rate': round(utilization, 2),
                'total_service_time': round(server.total_service_time, 2),
                'donors_served': server.donors_served
            })
            total_utilization += utilization
        
        avg_utilization = total_utilization / len(all_servers) if all_servers else 0
        
        # Summary statistics
        results['summary'] = {
            'total_donors_simulated': total_donors,
            'donors_served': donors_served,
            'donors_unserved': donors_unserved,
            'avg_waiting_time': round(avg_wait, 2),
            'max_waiting_time': round(max_wait_time, 2),
            'avg_queue_length': round(avg_queue_length, 2),
            'avg_server_utilization': round(avg_utilization, 2),
            'queue_samples': self.queue_length_samples
        }
        
        return results
