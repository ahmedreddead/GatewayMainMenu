var isEditMode = false; // Variable to track if the dashboard is in edit mode
var itemLocations ;
$(document).ready(function() {
    $(".dashboard-item").draggable({
        revert: "invalid",
        zIndex: 100,
        cursor: "move",
        disabled: true // Disable dragging initially
    });

    $(".dashboard-partition").droppable({
    accept: ".dashboard-item",
    drop: function(event, ui) {
        var draggable = ui.draggable;
        var droppable = $(this);
        var droppableItem = droppable.children(".dashboard-item");

        if (droppableItem.length > 0) {
            var draggableParent = draggable.parent();
            var droppableParent = droppableItem.parent();

            draggable.detach().appendTo(droppableParent);
            droppableItem.detach().appendTo(draggableParent);
        } else {
            if (!draggable.parent().is(droppable)) {
                draggable.detach().appendTo(droppable);
            }
        }

        draggable.css({ top: 0, left: 0 });
    },
    disabled: true // Disable dropping initially
    });

    // Edit button click event
    $("#editButton").click(function() {
    if (!isEditMode) {
        $(".dashboard-item").draggable("enable"); // Enable dragging
        $(".dashboard-partition").droppable("enable"); // Enable dropping
        $("#okButton").show(); // Show the OK button
        isEditMode = true;
    }
    });

    // OK button click event
    $("#okButton").click(function() {
    if (isEditMode) {
        $(".dashboard-item").draggable("disable"); // Disable dragging
        $(".dashboard-partition").droppable("disable"); // Disable dropping
        $("#okButton").hide(); // Hide the OK button
        isEditMode = false;
                
        itemLocations = [];
        $(".dashboard-partition").each(function(index) {
            var partition = $(this);
            var partitionId = partition.attr("id");
            partition.find(".dashboard-item").each(function() {
                var itemId = $(this).attr("id");               
                var type = null;
                for (var i = 0; i < items.length; i++) {
                if (items[i].itemId == itemId) {
                    type = items[i].type; // Assign the type if a match is found
                    break;
                }
            }
                                        
                itemLocations.push({
                    itemId: itemId,
                    partitionId: partitionId ,
                    type: type       
                });
            });
        });

                // Send itemLocations to Flask
        $.ajax({
            type: "POST",
            url: "/process_locations",
            data: JSON.stringify(itemLocations),
            contentType: "application/json",
            success: function(response) {
                console.log("Locations sent to Flask successfully");
            },
            error: function(error) {
                console.error("Error sending locations to Flask:", error);
            }
            });
            
            }
                     });






});



// Create the dashboard partitions dynamically
var dashboardContainer = $("#dashboardContainer");
var partitionIndex = 0 ;
for (var i = 0; i < numItems; i++) {
    var row = $('<div class="dashboard-row"></div>');
    for (var j = 0; j < numPerRow; j++) {
        var partition = $('<div class="dashboard-partition"></div>');
        partition.attr('id', 'partition-' + partitionIndex);
        row.append(partition);
        partitionIndex++;
    }
    dashboardContainer.append(row);
}


itemLocations.forEach(function(location) {
    var icon;
    var item;
    if (location.type === 'siren' || location.type === 'switch') {
        icon = getActuatorIcon(location.type, 'off');
    } else if (location.type === 'door_sensor')
    {
        icon = getSensorIcon(location.type, 'opened');
    }
    else if (location.type === 'motion_sensor')
    {
        icon = getSensorIcon(location.type, 'No Motion');
    }
    else {
        icon = getSensorIcon(location.type, 'No Motion');
    }

    if (location.type == 'siren' || location.type == 'switch') {
        console.log(location.type , location.itemId)
        item = $('<div class="actuator dashboard-item">' + icon + location.type + ' ' + location.itemId + '</div>').click(function() {
            toggleActuator(location.type, location.itemId);
        });
        socket.on(`${location.type}_data`, function (data) {
            let actuatorData = JSON.parse(data);
            updateActuatorData(location.type, actuatorData);
        });

    } else {
        item = $('<div class="sensor dashboard-item">' + icon + location.type + ' ' + location.itemId + '</div>');
        socket.on(`${location.type}_data`, function (data) {
            let sensorData = JSON.parse(data);
            updateSensorData(location.type, sensorData);
        });

    }
    item.attr('id', location.itemId);
    var partition = $('#' + location.partitionId);
    partition.append(item);



});



