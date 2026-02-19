/**
 * Results Page JavaScript
 * Displays simulation results with charts and tables
 */

let donorsData = [];
let queueChart, waitingChart, utilizationChart;

document.addEventListener('DOMContentLoaded', async function() {
    await loadSimulationResults();
    setupTableFilters();
});

async function loadSimulationResults() {
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const content = document.getElementById('resultsContent');

    try {
        // Fetch simulation summary
        const simResponse = await fetch(`/api/simulations/${SIMULATION_ID}`);
        const simData = await simResponse.json();

        if (!simData.success) {
            throw new Error(simData.error || 'Failed to load simulation');
        }

        const simulation = simData.simulation;
        const camp = simData.camp;

        // Fetch donors data
        const donorsResponse = await fetch(`/api/simulations/${SIMULATION_ID}/donors`);
        const donorsResult = await donorsResponse.json();

        if (!donorsResult.success) {
            throw new Error('Failed to load donors data');
        }

        donorsData = donorsResult.donors;

        // Fetch stations data
        const stationsResponse = await fetch(`/api/simulations/${SIMULATION_ID}/stations`);
        const stationsResult = await stationsResponse.json();

        if (!stationsResult.success) {
            throw new Error('Failed to load stations data');
        }

        const stations = stationsResult.stations;

        // Fetch queue statistics
        const queueResponse = await fetch(`/api/simulations/${SIMULATION_ID}/queue-stats`);
        const queueResult = await queueResponse.json();

        if (!queueResult.success) {
            throw new Error('Failed to load queue statistics');
        }

        const queueData = queueResult.queue_data;

        // Display all data
        displayCampInfo(camp);
        displaySimulationParams(simulation);
        displayKPIs(simulation);
        displayDonorsTable(donorsData);
        displayStationsTable(stations);
        
        // Create charts
        createQueueLengthChart(queueData);
        createWaitingTimeChart(donorsData);
        createUtilizationChart(stations);

        loading.style.display = 'none';
        content.style.display = 'block';

    } catch (err) {
        console.error('Error loading results:', err);
        loading.style.display = 'none';
        error.textContent = `Error: ${err.message}`;
        error.style.display = 'block';
    }
}

function infoItem(label, value) {
    return `<div class="info-item"><div class="info-item-label">${label}</div><strong>${value}</strong></div>`;
}

function displayCampInfo(camp) {
    const container = document.getElementById('campInfo');
    container.innerHTML = [
        infoItem('Camp Name', camp.name),
        infoItem('Start Time', camp.start_time),
        infoItem('End Time', camp.end_time),
        infoItem('Duration', camp.duration_minutes + ' min'),
        infoItem('Max Donors', camp.max_donors || 'Unlimited'),
    ].join('');
}

function displaySimulationParams(sim) {
    const container = document.getElementById('simParams');
    container.innerHTML = [
        infoItem('Donation Counters', sim.num_servers),
        infoItem('Screening Staff', sim.num_screening_staff),
        infoItem('Avg Screening Time', sim.avg_screening_time + ' min'),
        infoItem('Avg Donation Time', sim.avg_donation_time + ' min'),
        infoItem('Arrival Rate λ', sim.arrival_rate + ' / hr'),
        infoItem('Service Distribution', sim.service_distribution),
    ].join('');
}

function displayKPIs(sim) {
    const container = document.getElementById('kpiGrid');
    const serveRate = sim.total_donors_simulated > 0 
        ? ((sim.donors_served / sim.total_donors_simulated) * 100).toFixed(1)
        : 0;

    const kpis = [
        { icon: '👥', value: sim.total_donors_simulated, label: 'Total Donors Simulated' },
        { icon: '✅', value: sim.donors_served, label: 'Donors Served' },
        { icon: '⛔', value: sim.donors_unserved, label: 'Donors Unserved' },
        { icon: '📈', value: serveRate + '%', label: 'Service Rate' },
        { icon: '⏱', value: sim.avg_waiting_time.toFixed(1) + ' min', label: 'Avg Wait Time' },
        { icon: '🔺', value: sim.max_waiting_time.toFixed(1) + ' min', label: 'Max Wait Time' },
        { icon: '🔢', value: sim.avg_queue_length.toFixed(1), label: 'Avg Queue Length' },
        { icon: '⚡', value: sim.avg_server_utilization.toFixed(1) + '%', label: 'Avg Server Utilization' },
    ];
    container.innerHTML = kpis.map(k => `
        <div class="kpi-card">
            <span class="kpi-icon">${k.icon}</span>
            <div class="kpi-value">${k.value}</div>
            <div class="kpi-label">${k.label}</div>
        </div>
    `).join('');
}

function displayDonorsTable(donors) {
    const tbody = document.getElementById('donorsTableBody');
    tbody.innerHTML = donors.map(donor => `
        <tr>
            <td>${donor.donor_index}</td>
            <td>${donor.arrival_time.toFixed(1)}</td>
            <td>${donor.registration_start ? donor.registration_start.toFixed(1) : '-'}</td>
            <td>${donor.registration_end ? donor.registration_end.toFixed(1) : '-'}</td>
            <td>${donor.screening_start ? donor.screening_start.toFixed(1) : '-'}</td>
            <td>${donor.screening_end ? donor.screening_end.toFixed(1) : '-'}</td>
            <td>${donor.donation_start ? donor.donation_start.toFixed(1) : '-'}</td>
            <td>${donor.donation_end ? donor.donation_end.toFixed(1) : '-'}</td>
            <td>${donor.total_wait_time.toFixed(1)}</td>
            <td>${donor.total_time_in_system.toFixed(1)}</td>
            <td>
                <span class="status-badge ${donor.served ? 'status-served' : 'status-unserved'}">
                    ${donor.served ? 'Served' : 'Unserved'}
                </span>
            </td>
        </tr>
    `).join('');
}

function displayStationsTable(stations) {
    const tbody = document.getElementById('stationsTableBody');
    tbody.innerHTML = stations.map(station => `
        <tr>
            <td>${station.station_type}</td>
            <td>${station.station_number}</td>
            <td>${station.utilization_rate.toFixed(1)}%</td>
            <td>${station.total_service_time.toFixed(1)} min</td>
            <td>${station.donors_served}</td>
        </tr>
    `).join('');
}

function createQueueLengthChart(queueData) {
    const ctx = document.getElementById('queueLengthChart').getContext('2d');
    
    queueChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: queueData.map(d => d.time),
            datasets: [
                {
                    label: 'Registration Queue',
                    data: queueData.map(d => d.registration),
                    borderColor: '#8B1E3F',
                    backgroundColor: 'rgba(139,30,63,0.08)',
                    tension: 0.4,
                    borderWidth: 2
                },
                {
                    label: 'Screening Queue',
                    data: queueData.map(d => d.screening),
                    borderColor: '#C84B6C',
                    backgroundColor: 'rgba(200,75,108,0.08)',
                    tension: 0.4,
                    borderWidth: 2
                },
                {
                    label: 'Donation Queue',
                    data: queueData.map(d => d.donation),
                    borderColor: '#4B7EC8',
                    backgroundColor: 'rgba(75,126,200,0.08)',
                    tension: 0.4,
                    borderWidth: 2
                },
                {
                    label: 'Total Queue',
                    data: queueData.map(d => d.total),
                    borderColor: '#1F2937',
                    backgroundColor: 'rgba(31,41,55,0.06)',
                    tension: 0.4,
                    borderWidth: 2.5,
                    borderDash: [5, 3]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top'
                },
                title: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time (minutes)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Queue Length (donors)'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function createWaitingTimeChart(donors) {
    const ctx = document.getElementById('waitingTimeChart').getContext('2d');
    
    const servedDonors = donors.filter(d => d.served);
    
    waitingChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Total Waiting Time',
                data: servedDonors.map(d => ({
                    x: d.donor_index,
                    y: d.total_wait_time
                })),
                backgroundColor: 'rgba(139,30,63,0.55)',
                borderColor: '#8B1E3F',
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Donor Index'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Waiting Time (minutes)'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function createUtilizationChart(stations) {
    const ctx = document.getElementById('utilizationChart').getContext('2d');
    
    const labels = stations.map(s => `${s.station_type.charAt(0).toUpperCase() + s.station_type.slice(1)} ${s.station_number}`);
    const data = stations.map(s => s.utilization_rate);
    const colors = stations.map(s => {
        if (s.station_type === 'registration') return 'rgba(139,30,63,0.75)';
        if (s.station_type === 'screening') return 'rgba(200,75,108,0.75)';
        return 'rgba(75,126,200,0.75)';
    });
    
    utilizationChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Utilization %',
                data: data,
                backgroundColor: colors,
                borderColor: colors.map(c => c.replace('0.7', '1')),
                borderWidth: 1
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
                },
                x: {
                    title: {
                        display: true,
                        text: 'Service Station'
                    }
                }
            }
        }
    });
}

function setupTableFilters() {
    const searchInput = document.getElementById('searchDonors');
    const filterSelect = document.getElementById('filterServed');

    searchInput.addEventListener('input', filterTable);
    filterSelect.addEventListener('change', filterTable);
}

function filterTable() {
    const searchTerm = document.getElementById('searchDonors').value.toLowerCase();
    const filterValue = document.getElementById('filterServed').value;

    let filtered = donorsData;

    // Apply served filter
    if (filterValue === 'served') {
        filtered = filtered.filter(d => d.served);
    } else if (filterValue === 'unserved') {
        filtered = filtered.filter(d => !d.served);
    }

    // Apply search filter (on donor index)
    if (searchTerm) {
        filtered = filtered.filter(d => 
            d.donor_index.toString().includes(searchTerm)
        );
    }

    displayDonorsTable(filtered);
}
