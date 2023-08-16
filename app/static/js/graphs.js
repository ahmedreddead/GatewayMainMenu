
flatpickr("#start-time", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true
    });

flatpickr("#end-time", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    time_24hr: true
});

function mapStatusToValue(status) {
    switch (status) {
        case 'on':
            return 10;
        case 'off':
            return 1;
        case 'Motion Detected':
            return 10;
        case 'No Motion':
            return 1;
        case 'opened':
            return 10;
        case 'closed':
            return 1;
        case 'No Glass Break ':
            return 1;

        // Add more cases for other status values
        default:
            return 0 ; // Use black for unknown statuses
    }
}
function fetchAndDrawGraph() {
    var startTime = document.getElementById('start-time').value;
    var endTime = document.getElementById('end-time').value;

    $.ajax({
        url: `/api/all_data?start_time=${startTime}&end_time=${endTime}`,
        method: 'GET',
        dataType: 'json',
        success: function (allData) {
            document.getElementById('graph-container').innerHTML = ''; // Clear previous graphs

            allData.forEach(itemData => {
                if (itemData.data.length > 0) {
                    var graphContainer = document.createElement('div');
                    graphContainer.className = 'graph-container';
                    graphContainer.id = `graph-${itemData.item.itemId}`;
                    document.getElementById('graph-container').appendChild(graphContainer);

                    var graphData = [];

                    var currentStatus = -1; // Initialize to an invalid value
                    var startTime = null;
                    var endTime = null;
                    var statusLabel = ''; // Initialize status label

                    itemData.data.forEach(item => {
                        var timestamp = new Date(item[2]);
                        var statusValue = mapStatusToValue(item[1]);

                        if (statusValue !== currentStatus) {
                            if (currentStatus === 1) {
                                // End of an "on" interval
                                endTime = timestamp;
                            } else {
                                // Start of an "on" interval
                                startTime = timestamp;
                                statusLabel = getStatusLabel(itemData.item.type, statusValue); // Get status label based on sensor type
                            }

                            // Create a single bar for the interval
                            graphData.push({
                                x: [startTime, endTime],
                                y: [1, 1],
                                type: 'bar',
                                opacity: 0.6, // Adjust the opacity as needed
                                hoverinfo: 'none', // Disable hover info for clarity
                                name: statusLabel, // Display customized status label
                                showlegend: false, // Hide legend entry
                            });

                            currentStatus = statusValue;
                        }
                    });

                    var layout = {
                        title: `${itemData.item.type} - ${itemData.item.itemId}`,
                        xaxis: {title: 'Time'},
                        yaxis: {title: 'Status'},
                        barmode: 'overlay', // Overlay bars instead of stacking,
                        annotations: [] ,// Clear annotations
                        width: 600, // Adjust the width of the graph
                        height: 400, // Adjust the height of the graph
                    };

                    Plotly.newPlot(graphContainer.id, graphData, layout, {responsive: true, displayModeBar: false});
                }
            });
        },
        error: function (error) {
            console.log('Error fetching data:', error);
        }
    });

}

// Function to get status label based on sensor type
function getStatusLabel(sensorType, statusValue) {
    if (sensorType === 'door') {
        return statusValue === 1 ? 'Opened' : 'Closed';
    } else if (sensorType === 'motion') {
        return statusValue === 1 ? 'Motion Detected' : 'No Motion';
    }
    return ''; // Default label if sensor type is not recognized
}

// Call the fetchAndDrawGraph function on page load
fetchAndDrawGraph();
