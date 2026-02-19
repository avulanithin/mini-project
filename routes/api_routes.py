"""
API routes for REST endpoints
"""
from flask import request, jsonify
from . import api_bp
from models import Camp, Simulation, Donor, ServiceStation
from services import SimulationEngine


@api_bp.route('/camps', methods=['GET'])
def get_camps():
    """Get all camps"""
    try:
        camps = Camp.get_all()
        return jsonify({
            'success': True,
            'camps': [camp.to_dict() for camp in camps]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/camps', methods=['POST'])
def create_camp():
    """Create a new camp"""
    try:
        data = request.json
        
        # Validate required fields
        required = ['name', 'start_time', 'end_time', 'duration_minutes']
        for field in required:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        camp_id = Camp.create(
            name=data['name'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            duration_minutes=int(data['duration_minutes']),
            max_donors=int(data.get('max_donors')) if data.get('max_donors') else None,
            peak_hours=data.get('peak_hours', '')
        )
        
        return jsonify({
            'success': True,
            'camp_id': camp_id,
            'message': 'Camp created successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/camps/<int:camp_id>', methods=['GET'])
def get_camp(camp_id):
    """Get camp by ID"""
    try:
        camp = Camp.get_by_id(camp_id)
        if camp:
            return jsonify({
                'success': True,
                'camp': camp.to_dict()
            })
        else:
            return jsonify({'success': False, 'error': 'Camp not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/simulations/run', methods=['POST'])
def run_simulation():
    """Run a new simulation"""
    try:
        data = request.json
        
        # Validate required fields
        required = ['camp_id', 'num_servers', 'num_screening_staff', 
                   'avg_screening_time', 'avg_donation_time', 'arrival_rate']
        for field in required:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        # Get camp details
        camp = Camp.get_by_id(data['camp_id'])
        if not camp:
            return jsonify({'success': False, 'error': 'Camp not found'}), 404
        
        # Create simulation record
        simulation_id = Simulation.create(
            camp_id=camp.id,
            num_servers=int(data['num_servers']),
            num_screening_staff=int(data['num_screening_staff']),
            avg_screening_time=float(data['avg_screening_time']),
            avg_donation_time=float(data['avg_donation_time']),
            arrival_rate=float(data['arrival_rate']),
            arrival_distribution=data.get('arrival_distribution', 'Poisson'),
            service_distribution=data.get('service_distribution', 'Exponential'),
            queue_discipline=data.get('queue_discipline', 'FCFS'),
            allow_idle_servers=int(data.get('allow_idle_servers', 1))
        )
        
        # Run simulation
        engine = SimulationEngine(
            duration_minutes=camp.duration_minutes,
            num_servers=int(data['num_servers']),
            num_screening_staff=int(data['num_screening_staff']),
            avg_screening_time=float(data['avg_screening_time']),
            avg_donation_time=float(data['avg_donation_time']),
            arrival_rate=float(data['arrival_rate']),
            arrival_distribution=data.get('arrival_distribution', 'Poisson'),
            service_distribution=data.get('service_distribution', 'Exponential'),
            max_donors=camp.max_donors,
            allow_idle_servers=bool(int(data.get('allow_idle_servers', 1)))
        )
        
        results = engine.run()
        
        # Update simulation with results
        Simulation.update_results(
            simulation_id=simulation_id,
            total_donors=results['summary']['total_donors_simulated'],
            donors_served=results['summary']['donors_served'],
            donors_unserved=results['summary']['donors_unserved'],
            avg_wait=results['summary']['avg_waiting_time'],
            max_wait=results['summary']['max_waiting_time'],
            avg_queue_len=results['summary']['avg_queue_length'],
            avg_util=results['summary']['avg_server_utilization']
        )
        
        # Save donor data
        donors_data = []
        for donor in results['donors']:
            donors_data.append((
                simulation_id,
                donor['donor_index'],
                donor['arrival_time'],
                donor['registration_start'],
                donor['registration_end'],
                donor['screening_start'],
                donor['screening_end'],
                donor['donation_start'],
                donor['donation_end'],
                donor['registration_wait'],
                donor['screening_wait'],
                donor['donation_wait'],
                donor['total_wait_time'],
                donor['total_time_in_system'],
                donor['served']
            ))
        
        if donors_data:
            Donor.bulk_create(donors_data)
        
        # Save service station data
        stations_data = []
        for station in results['service_stations']:
            stations_data.append((
                simulation_id,
                station['station_type'],
                station['station_number'],
                station['utilization_rate'],
                station['total_service_time'],
                station['donors_served']
            ))
        
        if stations_data:
            ServiceStation.bulk_create(stations_data)
        
        return jsonify({
            'success': True,
            'simulation_id': simulation_id,
            'summary': results['summary'],
            'message': 'Simulation completed successfully'
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/simulations/<int:simulation_id>', methods=['GET'])
def get_simulation(simulation_id):
    """Get simulation summary"""
    try:
        simulation = Simulation.get_by_id(simulation_id)
        if not simulation:
            return jsonify({'success': False, 'error': 'Simulation not found'}), 404
        
        camp = Camp.get_by_id(simulation.camp_id)
        
        return jsonify({
            'success': True,
            'simulation': simulation.to_dict(),
            'camp': camp.to_dict() if camp else None
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/simulations/<int:simulation_id>/donors', methods=['GET'])
def get_simulation_donors(simulation_id):
    """Get all donors for a simulation"""
    try:
        donors = Donor.get_by_simulation_id(simulation_id)
        return jsonify({
            'success': True,
            'donors': [donor.to_dict() for donor in donors]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/simulations/<int:simulation_id>/stations', methods=['GET'])
def get_simulation_stations(simulation_id):
    """Get all service stations for a simulation"""
    try:
        stations = ServiceStation.get_by_simulation_id(simulation_id)
        return jsonify({
            'success': True,
            'stations': [station.to_dict() for station in stations]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/simulations/<int:simulation_id>/queue-stats', methods=['GET'])
def get_queue_stats(simulation_id):
    """Get queue statistics over time"""
    try:
        # Get donors and compute queue lengths over time
        donors = Donor.get_by_simulation_id(simulation_id)
        simulation = Simulation.get_by_id(simulation_id)
        
        if not simulation:
            return jsonify({'success': False, 'error': 'Simulation not found'}), 404
        
        # Reconstruct queue lengths over time (simplified version)
        # In production, this would be stored during simulation
        camp = Camp.get_by_id(simulation.camp_id)
        time_points = list(range(0, camp.duration_minutes + 1, 5))  # Every 5 minutes
        
        queue_data = []
        for t in time_points:
            # Count donors in each stage at time t
            registration_count = 0
            screening_count = 0
            donation_count = 0
            
            for donor in donors:
                donor_dict = donor.to_dict()
                # Check if donor is in registration queue at time t
                if donor_dict['arrival_time'] <= t and (donor_dict['registration_start'] is None or donor_dict['registration_start'] > t):
                    registration_count += 1
                # Check if donor is in screening queue at time t
                elif donor_dict['registration_end'] and donor_dict['registration_end'] <= t and \
                     (donor_dict['screening_start'] is None or donor_dict['screening_start'] > t):
                    screening_count += 1
                # Check if donor is in donation queue at time t
                elif donor_dict['screening_end'] and donor_dict['screening_end'] <= t and \
                     (donor_dict['donation_start'] is None or donor_dict['donation_start'] > t):
                    donation_count += 1
            
            queue_data.append({
                'time': t,
                'registration': registration_count,
                'screening': screening_count,
                'donation': donation_count,
                'total': registration_count + screening_count + donation_count
            })
        
        return jsonify({
            'success': True,
            'queue_data': queue_data
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/simulations', methods=['GET'])
def get_all_simulations():
    """Get all simulations"""
    try:
        simulations = Simulation.get_all()
        result = []
        
        for sim in simulations:
            camp = Camp.get_by_id(sim.camp_id)
            sim_dict = sim.to_dict()
            sim_dict['camp_name'] = camp.name if camp else 'Unknown'
            result.append(sim_dict)
        
        return jsonify({
            'success': True,
            'simulations': result
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/simulations/compare', methods=['POST'])
def compare_simulations():
    """Compare multiple simulations"""
    try:
        data = request.json
        simulation_ids = data.get('simulation_ids', [])
        
        if not simulation_ids:
            return jsonify({'success': False, 'error': 'No simulation IDs provided'}), 400
        
        comparisons = []
        for sim_id in simulation_ids:
            simulation = Simulation.get_by_id(sim_id)
            if simulation:
                camp = Camp.get_by_id(simulation.camp_id)
                sim_dict = simulation.to_dict()
                sim_dict['camp_name'] = camp.name if camp else 'Unknown'
                comparisons.append(sim_dict)
        
        return jsonify({
            'success': True,
            'comparisons': comparisons
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
