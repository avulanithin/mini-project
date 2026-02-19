/**
 * Setup Page JavaScript
 * Handles camp configuration form and simulation execution
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('campSetupForm');
    const startTimeInput = document.getElementById('startTime');
    const endTimeInput = document.getElementById('endTime');
    const durationInput = document.getElementById('durationMinutes');
    const notification = document.getElementById('notification');

    // Calculate duration when time inputs change
    function calculateDuration() {
        const startTime = startTimeInput.value;
        const endTime = endTimeInput.value;

        if (startTime && endTime) {
            const [startHour, startMin] = startTime.split(':').map(Number);
            const [endHour, endMin] = endTime.split(':').map(Number);

            const startMinutes = startHour * 60 + startMin;
            const endMinutes = endHour * 60 + endMin;

            let duration = endMinutes - startMinutes;
            if (duration < 0) {
                duration += 24 * 60; // Handle overnight camps
            }

            durationInput.value = duration;
        }
    }

    startTimeInput.addEventListener('change', calculateDuration);
    endTimeInput.addEventListener('change', calculateDuration);

    // Initial calculation
    calculateDuration();

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Running Simulation...';
        submitButton.disabled = true;

        // Collect form data
        const formData = {
            name: document.getElementById('campName').value,
            start_time: document.getElementById('startTime').value,
            end_time: document.getElementById('endTime').value,
            duration_minutes: parseInt(document.getElementById('durationMinutes').value),
            max_donors: document.getElementById('maxDonors').value ? parseInt(document.getElementById('maxDonors').value) : null,
            peak_hours: document.getElementById('peakHours').value
        };

        try {
            // Step 1: Create camp
            const campResponse = await fetch('/api/camps', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const campResult = await campResponse.json();

            if (!campResult.success) {
                throw new Error(campResult.error || 'Failed to create camp');
            }

            const campId = campResult.camp_id;

            // Step 2: Run simulation
            const simulationData = {
                camp_id: campId,
                num_servers: parseInt(document.getElementById('numServers').value),
                num_screening_staff: parseInt(document.getElementById('numScreeningStaff').value),
                avg_screening_time: parseFloat(document.getElementById('avgScreeningTime').value),
                avg_donation_time: parseFloat(document.getElementById('avgDonationTime').value),
                arrival_rate: parseFloat(document.getElementById('arrivalRate').value),
                arrival_distribution: document.getElementById('arrivalDistribution').value,
                service_distribution: document.getElementById('serviceDistribution').value,
                queue_discipline: document.getElementById('queueDiscipline').value,
                allow_idle_servers: parseInt(document.getElementById('allowIdleServers').value)
            };

            const simResponse = await fetch('/api/simulations/run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(simulationData)
            });

            const simResult = await simResponse.json();

            if (!simResult.success) {
                throw new Error(simResult.error || 'Failed to run simulation');
            }

            // Success - redirect to results page
            showNotification('success', 'Simulation completed successfully! Redirecting...');
            setTimeout(() => {
                window.location.href = `/results/${simResult.simulation_id}`;
            }, 1500);

        } catch (error) {
            console.error('Error:', error);
            showNotification('error', `Error: ${error.message}`);
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }
    });

    function showNotification(type, message) {
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.display = 'block';

        if (type === 'success') {
            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }
    }
});
