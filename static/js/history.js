/**
 * History Page JavaScript
 * Displays list of past simulations
 */

let allSimulations = [];

document.addEventListener('DOMContentLoaded', async function() {
    await loadSimulations();
    setupSearch();
});

async function loadSimulations() {
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const content = document.getElementById('historyContent');

    try {
        const response = await fetch('/api/simulations');
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Failed to load simulations');
        }

        allSimulations = data.simulations;
        displaySimulations(allSimulations);

        loading.style.display = 'none';
        content.style.display = 'block';

    } catch (err) {
        console.error('Error loading simulations:', err);
        loading.style.display = 'none';
        error.textContent = `Error: ${err.message}`;
        error.style.display = 'block';
    }
}

function displaySimulations(simulations) {
    const tbody = document.getElementById('simulationsTableBody');

    if (simulations.length === 0) {
        tbody.innerHTML = '<tr><td colspan="11" style="text-align: center;">No simulations found</td></tr>';
        return;
    }

    tbody.innerHTML = simulations.map(sim => {
        const date = new Date(sim.simulation_date);
        const dateStr = date.toLocaleString();

        return `
            <tr>
                <td>${sim.id}</td>
                <td>${sim.camp_name}</td>
                <td>${dateStr}</td>
                <td>${sim.num_servers}</td>
                <td>${sim.num_screening_staff}</td>
                <td>${sim.arrival_rate}/hr</td>
                <td>${sim.total_donors_simulated || 0}</td>
                <td>${sim.donors_served || 0}</td>
                <td>${sim.avg_waiting_time ? sim.avg_waiting_time.toFixed(1) : '-'} min</td>
                <td>${sim.avg_server_utilization ? sim.avg_server_utilization.toFixed(1) : '-'}%</td>
                <td>
                    <a href="/results/${sim.id}" class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">
                        View
                    </a>
                </td>
            </tr>
        `;
    }).join('');
}

function setupSearch() {
    const searchInput = document.getElementById('searchSimulations');
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        
        const filtered = allSimulations.filter(sim => 
            sim.camp_name.toLowerCase().includes(searchTerm) ||
            sim.id.toString().includes(searchTerm)
        );

        displaySimulations(filtered);
    });
}
