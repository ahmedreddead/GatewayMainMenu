var automationButton  = document.getElementById('automationButton');
var homeButton  = document.getElementById('homeButton');
var automationTable = document.getElementById('automationTable');
var dashboardContainer = document.getElementById('dashboardContainer');


var addItem = document.getElementById('add-item-button');
var EditItem = document.getElementById('editButton');
var OkItem = document.getElementById('okButton');
var addAutomationBtn = document.getElementById('addAutomationBtn');

automationButton.addEventListener('click', function () {
    // Toggle the visibility of the automation table
    automationTable.style.display = 'block';
    dashboardContainer.style.display = 'none';
    addItem.style.display = 'none';
    EditItem.style.display = 'none';
    OkItem.style.display = 'none';
    addAutomationBtn.style.display = 'block';

});
homeButton.addEventListener('click', function () {
    // Toggle the visibility of the automation table
    automationTable.style.display = 'none';
    dashboardContainer.style.display = 'block';
    EditItem.style.display = 'block';
    addItem.style.display = 'flex';
    addAutomationBtn.style.display = 'none';



});
        // Function to create a table row for an item
function createTableRow(item) {
    var row = document.createElement('tr');
    row.innerHTML = `
                <td>${item.event_id}</td>
                <td>${item.event_name}</td>
                <td>${item.description}</td>
                <td>
                    <button class="deleteBtn" data-id="${item.event_id}">Delete</button>
                    <button class="activateBtn" data-id="${item.event_id}">Activate</button>
                    <button class="deactivateBtn" data-id="${item.event_id}">Deactivate</button>
                </td>
            `;
            return row;
        }

        // Function to populate the table with items from Flask
function populateAutomationTable(items) {
    var tableBody = document.getElementById('automationTableBody');
    tableBody.innerHTML = '';

    items.forEach(function (item) {
        var row = createTableRow(item);
        tableBody.appendChild(row);
    });
}

        // AJAX calls for each option (delete, activate, deactivate)
$(document).on('click', '.deleteBtn', function () {
    var itemId = $(this).data('id');
            // Perform AJAX call to Flask API to delete the item with itemId
            // Example AJAX call:
            // $.ajax({
            //     type: 'DELETE',
            //     url: '/api/delete_item/' + itemId,
            //     success: function (response) {
            //         // Handle success response
            //     },
            //     error: function (error) {
            //         // Handle error response
            //     }
            // });
});

$(document).on('click', '.activateBtn', function () {
            var itemId = $(this).data('id');
            // Perform AJAX call to Flask API to activate the item with itemId
            // Example AJAX call:
            // $.ajax({
            //     type: 'POST',
            //     url: '/api/activate_item/' + itemId,
            //     success: function (response) {
            //         // Handle success response
            //     },
            //     error: function (error) {
            //         // Handle error response
            //     }
            // });
});

$(document).on('click', '.deactivateBtn', function () {
            var itemId = $(this).data('id');
            // Perform AJAX call to Flask API to deactivate the item with itemId
            // Example AJAX call:
            // $.ajax({
            //     type: 'POST',
            //     url: '/api/deactivate_item/' + itemId,
            //     success: function (response) {
            //         // Handle success response
            //     },
            //     error: function (error) {
            //         // Handle error response
            //     }
            // });
});

        // Assuming you have a function to get items from Flask and pass them here
var itemsFromFlask = []; // Replace this with the actual items from Flask
populateAutomationTable(itemsFromFlask);