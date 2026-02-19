/**
 * Compare Page JavaScript
 * Allows comparison of multiple simulations
 */

let allSimulations = [];
let selectedSimulations = [];

document.addEventListener('DOMContentLoaded', async function() {
    await loadSimulations();
    setupCompareButton();
});

async function loadSimulations() {
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const content = document.getElementById('compareContent');

    try {
        const response = await fetch('/api/simulations');
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Failed to load simulations');
        }

        allSimulations = data.simulations;
        displaySimulationCheckboxes(allSimulations);

        loading.style.display = 'none';
        content.style.display = 'block';

    } catch (err) {
        console.error('Error loading simulations:', err);
        loading.style.display = 'none';
        error.textContent = `Error: ${err.message}`;
        error.style.display = 'block';
    }
}

function displaySimulationCheckboxes(simulations) {
    const container = document.getElementById('simulationCheckboxes');

    if (simulations.length === 0) {
        container.innerHTML = '<p>No simulations available for comparison</p>';
        return;
    }

    container.innerHTML = simulations.map(sim => {
        const date = new Date(sim.simulation_date);
        const dateStr = date.toLocaleDateString();

        return `
            <div class="checkbox-item">
                <input type="checkbox" id="sim-${sim.id}" value="${sim.id}">
                <label for="sim-${sim.id}">
                    <strong>ID ${sim.id}:</strong> ${sim.camp_name} 
                    (${dateStr}, ${sim.num_servers} servers, ${sim.donors_served} served)
                </label>
            </div>
        `;
    }).join('');
}

function setupCompareButton() {
    const compareButton = document.getElementById('compareButton');
    compareButton.addEventListener('click', async function() {
        const checkboxes = document.querySelectorAll('#simulationCheckboxes input[type="checkbox"]:checked');
        const selectedIds = Array.from(checkboxes).map(cb => parseInt(cb.value));

        if (selectedIds.length < 2) {
            alert('Please select at least 2 simulations to compare');
            return;
        }

        if (selectedIds.length > 4) {
            alert('Please select maximum 4 simulations to compare');
            return;
        }

        await compareSimulations(selectedIds);
    });
}

async function compareSimulations(simulationIds) {
    try {
        const response = await fetch('/api/simulations/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ simulation_ids: simulationIds })
        });

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Failed to compare simulations');
        }

        selectedSimulations = data.comparisons;
        displayComparisonTable(selectedSimulations);
        createComparisonCharts(selectedSimulations);

        document.getElementById('comparisonResults').style.display = 'block';
        document.getElementById('comparisonResults').scrollIntoView({ behavior: 'smooth' });

    } catch (err) {
        console.error('Error comparing simulations:', err);
        alert(`Error: ${err.message}`);
    }
}

function displayComparisonTable(simulations) {
    const tbody = document.getElementById('comparisonTableBody');
    const table = document.getElementById('comparisonTable');
    const thead = table.querySelector('thead tr');

    // Update table headers
    thead.innerHTML = '<th>Metric</th>';
    simulations.forEach((sim, index) => {
        thead.innerHTML += `<th class="sim-col">Simulation ${sim.id}</th>`;
    });

    // Hide unused columns
    const allHeaders = thead.querySelectorAll('.sim-col');
    allHeaders.forEach((header, index) => {
        header.style.display = index < simulations.length ? 'table-cell' : 'none';
    });

    // Metrics to compare
    const metrics = [
        { label: 'Camp Name', key: 'camp_name' },
        { label: 'Number of Servers', key: 'num_servers' },
        { label: 'Screening Staff', key: 'num_screening_staff' },
        { label: 'Arrival Rate (per hour)', key: 'arrival_rate' },
        { label: 'Total Donors', key: 'total_donors_simulated' },
        { label: 'Donors Served', key: 'donors_served' },
        { label: 'Donors Unserved', key: 'donors_unserved' },
        { label: 'Avg Waiting Time (min)', key: 'avg_waiting_time', format: 'decimal' },
        { label: 'Max Waiting Time (min)', key: 'max_waiting_time', format: 'decimal' },
        { label: 'Avg Queue Length', key: 'avg_queue_length', format: 'decimal' },
        { label: 'Avg Server Utilization (%)', key: 'avg_server_utilization', format: 'decimal' }
    ];

    tbody.innerHTML = metrics.map(metric => {
        let row = `<tr><td><strong>${metric.label}</strong></td>`;
        
        simulations.forEach(sim => {
            let value = sim[metric.key];
            if (metric.format === 'decimal' && value !== null && value !== undefined) {
                value = value.toFixed(1);
            }
            row += `<td>${value ?? '-'}</td>`;
        });

        // Fill remaining columns
        for (let i = simulations.length; i < 4; i++) {
            row += '<td style="display: none;">-</td>';
        }

        row += '</tr>';
        return row;
    }).join('');
}

function createComparisonCharts(simulations) {
    createWaitTimeComparisonChart(simulations);
    createUtilizationComparisonChart(simulations);
    createDonorsComparisonChart(simulations);
}

function createWaitTimeComparisonChart(simulations) {
    const ctx = document.getElementById('waitTimeComparisonChart').getContext('2d');

    // Destroy existing chart if any
    if (window.waitTimeChart) {
        window.waitTimeChart.destroy();
    }

    window.waitTimeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: simulations.map(s => `Sim ${s.id}`),
            datasets: [
                {
                    label: 'Average Waiting Time',
                    data: simulations.map(s => s.avg_waiting_time),
                    backgroundColor: 'rgba(139,30,63,0.72)',
                    borderColor: '#8B1E3F',
                    borderWidth: 1,
                    borderRadius: 4
                },
                {
                    label: 'Max Waiting Time',
                    data: simulations.map(s => s.max_waiting_time),
                    backgroundColor: 'rgba(200,75,108,0.65)',
                    borderColor: '#C84B6C',
                    borderWidth: 1,
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Time (minutes)'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function createUtilizationComparisonChart(simulations) {
    const ctx = document.getElementById('utilizationComparisonChart').getContext('2d');

    if (window.utilizationChart) {
        window.utilizationChart.destroy();
    }

    window.utilizationChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: simulations.map(s => `Sim ${s.id}`),
            datasets: [{
                label: 'Average Server Utilization (%)',
                data: simulations.map(s => s.avg_server_utilization),
                backgroundColor: 'rgba(75,126,200,0.72)',
                borderColor: '#4B7EC8',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Utilization (%)'
                    },
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

function createDonorsComparisonChart(simulations) {
    const ctx = document.getElementById('donorsComparisonChart').getContext('2d');

    if (window.donorsChart) {
        window.donorsChart.destroy();
    }

    window.donorsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: simulations.map(s => `Sim ${s.id}`),
            datasets: [
                {
                    label: 'Donors Served',
                    data: simulations.map(s => s.donors_served),
                    backgroundColor: 'rgba(5,150,105,0.7)',
                    borderColor: '#059669',
                    borderWidth: 1,
                    borderRadius: 4
                },
                {
                    label: 'Donors Unserved',
                    data: simulations.map(s => s.donors_unserved),
                    backgroundColor: 'rgba(139,30,63,0.65)',
                    borderColor: '#8B1E3F',
                    borderWidth: 1,
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Number of Donors'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}
