// Function to map status values to colors
// Initialize Flatpickr
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
            return 1;
        case 'off':
            return 0;
        case 'Motion Detected':
            return 1;
        case 'No Motion':
            return 0;
        case 'opened':
            return 1;
        case 'closed':
            return 0;
        // Add more cases for other status values
        default:
            return 0 ; // Use black for unknown statuses
    }
}

// Function to fetch data using jQuery AJAX and draw graphs
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
                    graphContainer.id = `graph-${itemData.item.itemId}`;
                    document.getElementById('graph-container').appendChild(graphContainer);

                    var graphData = {
                        x: itemData.data.map(item => new Date(item[2])),
                        y: itemData.data.map(item => mapStatusToValue(item[1])),
                        type: 'bar'
                    };
                    var layout = {
                        title: `${itemData.item.type} - ${itemData.item.itemId}`,
                        xaxis: {title: 'Time'},
                        yaxis: {title: 'Status'}
                    };
                    Plotly.newPlot(graphContainer.id, [graphData], layout);
                }
            });
        },
        error: function (error) {
            console.log('Error fetching data:', error);
        }
    });

}

// Call the fetchAndDrawGraph function on page load
fetchAndDrawGraph();