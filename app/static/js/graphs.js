
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
            return 0;
        case 'Motion Detected':
            return 10;
        case 'No Motion':
            return 0;
        case 'opened':
            return 10;
        case 'closed':
            return 0;
        case 'No Glass Break ':
            return 0;

        // Add more cases for other status values
        default:
            return 0; // Use black for unknown statuses
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
                    var startTime1 = null;
                    var endTime1 = null;
                    var color = null;

                    itemData.data.forEach((item, index) => {
                        var timestamp = new Date(item[2]);
                        var statusValue = mapStatusToValue(item[1]);

                        if (statusValue === currentStatus) {
                            endTime1 = timestamp; // Extend the interval
                        } else {
                            if (currentStatus !== -1) {
                                // Create a single bar for the interval with color based on status value
                                graphData.push({
                                    x: [startTime1, endTime1],
                                    y: [1, 1],
                                    type: 'bar',
                                    opacity: 0.6,
                                    hoverinfo: 'none',
                                    showlegend: false,
                                    marker: {
                                        color: color
                                    }
                                });
                            }

                            // Start a new interval
                            currentStatus = statusValue;
                            startTime1 = timestamp;
                            endTime1 = timestamp;
                            color = currentStatus === 10 ? '#ff0000' : '#0073e6'; // Red or blue shade
                        }

                        // Check if this is the last data point
                        if (index === itemData.data.length - 1) {
                            // Create a bar from the last data point to the current time
                            var currentTime = new Date();
                            graphData.push({
                                x: [timestamp, currentTime],
                                y: [1, 1],
                                type: 'bar',
                                opacity: 0.6,
                                hoverinfo: 'none',
                                showlegend: false,
                                marker: {
                                    color: color
                                }
                            });
                        }
                    });

                    var layout = {
                        title: `${itemData.item.type} - ${itemData.item.itemId}`,
                        xaxis: {title: 'Time'},
                        yaxis: {title: 'Status'},
                        barmode: 'overlay',
                        annotations: [],
                        width: 600,
                        height: 400
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
    if (sensorType === 'door_sensor') {
        return statusValue === 1 ? 'opened' : 'closed';
    } else if (sensorType === 'motion_sensor') {
        return statusValue === 1 ? 'Motion Detected' : 'No Motion';
    }
    return ''; // Default label if sensor type is not recognized
}

// Call the fetchAndDrawGraph function on page load
fetchAndDrawGraph();
