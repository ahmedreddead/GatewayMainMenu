
function toggleActivation(button, actionId) {
    // Here you can implement the JavaScript logic to toggle activation status.
    // You may use AJAX to send a request to the server to update the activation status for the given actionId.

    // For demonstration purposes, we'll simply toggle the text on the button.
    if (button.textContent.trim() === 'Deactivate') {
        button.textContent = 'Activate';
    } else {
        button.textContent = 'Deactivate';
    }
}

function deleteAction(actionId) {
    // Here you can implement the JavaScript logic to handle the delete action.
    // You may use AJAX to send a request to the server to delete the action with the given actionId.

    // For demonstration purposes, we'll just show an alert.
    alert('Action with ID ' + actionId + ' will be deleted.');
}

// Function to create a new table row and cells for each item in the data array
function createTableRow(item) {
    var newRow = document.createElement('tr');
    var idCell = document.createElement('td');
    var statusCell = document.createElement('td');

    idCell.textContent = item.id;
    statusCell.textContent = item.status;

    newRow.appendChild(idCell);
    newRow.appendChild(statusCell);

    return newRow;
}
function createTableRow_actions(item) {
    var newRow = document.createElement('tr');

    var orderCell = document.createElement('td');
    var typeCell = document.createElement('td');
    var idCell = document.createElement('td');
    var statusCell = document.createElement('td');

    orderCell.textContent = item.order;
    typeCell.textContent = item.type;
    idCell.textContent = item.id;
    statusCell.textContent = item.status;

    newRow.appendChild(orderCell);
    newRow.appendChild(typeCell);
    newRow.appendChild(idCell);
    newRow.appendChild(statusCell);

    return newRow;
}

// Get the table body element
var tableBody = document.getElementById('tableDoorEvent');

// Loop through the data array and append each item to the table
eventDoor.forEach(function(item) {
    var newRow = createTableRow(item);
    tableBody.appendChild(newRow);
});

var tableBody = document.getElementById('tableMotionEvent');

eventMotion.forEach(function(item) {
    var newRow = createTableRow(item);
    tableBody.appendChild(newRow);
});


var tableBody = document.getElementById('actionsdata');

actions_data.forEach(function(item) {
    var newRow = createTableRow_actions(item);
    tableBody.appendChild(newRow);
});
