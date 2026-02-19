"""
Main routes for serving web pages
"""
from flask import render_template
from . import main_bp


@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@main_bp.route('/setup')
def setup():
    """Camp setup configuration page"""
    return render_template('setup.html')


@main_bp.route('/results/<int:simulation_id>')
def results(simulation_id):
    """Simulation results dashboard"""
    return render_template('results.html', simulation_id=simulation_id)


@main_bp.route('/history')
def history():
    """Historical simulations page"""
    return render_template('history.html')


@main_bp.route('/compare')
def compare():
    """Compare multiple simulations"""
    return render_template('compare.html')
