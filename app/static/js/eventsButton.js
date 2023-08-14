$(document).ready(function () {


    // Add Automation button click event
    $("#addAutomationBtn").click(function () {
        $("#overlay").show();
        $("#automationWindow").show();
    });
    // Done button click event
    $("#doneBtn").click(function () {
        // Collect data from user selections and send it to Flask using AJAX
        let eventsData = {}; // Collect events data
        let actionsData = {}; // Collect actions data

        $.ajax({
            type: "POST",
            url: "/save_data", // Your Flask route to save the data
            data: { eventsData, actionsData },
            success: function (response) {
                // Handle success (e.g., show a success message)
                $("#overlay").hide();
                $("#automationWindow").hide();
            },
            error: function (xhr, status, error) {
                // Handle error (e.g., show an error message)
                console.error(error);
            }
        });
    });
    // Handle adding events and actions dynamically (using event delegation)
    $("#automationWindow").on("click", ".add-event-btn", function () {
        // Add a new event option to the events section
        // Implement logic to fetch IDs based on the selected type
    });
    $("#automationWindow").on("click", ".add-action-btn", function () {
        // Add a new action option to the actions section
        // Implement logic to fetch IDs based on the selected type
    });
    $("#closeAutomationBtn").click(function () {
        $("#overlay").hide();
        $("#automationWindow").hide();
    });
// Add Event button click event
    $("#automationWindow").on("click", ".add-event-btn", function () {
        $("#eventOptions").show();
        $("#eventType").val(""); // Reset the type selection when adding a new event
        $("#eventId, #eventStatus, #addEventBtn").hide();
    });
    // Event type selection change event
    $("#automationWindow").on("change", "#eventType", function () {
        const selectedType = $(this).val();
        if (selectedType === "") {
            $("#eventId, #eventStatus, #addEventBtn").hide();
        } else {
            // Update status options based on the selected type
            const statusOptions = selectedType === "motion_sensor"
                ? [{ value: "motion_detected", text: "Motion Detected" }]
                : [{ value: "opened", text: "Opened" }, { value: "closed", text: "Closed" }];

            $("#eventStatus").empty();
            statusOptions.forEach((option) => {
                $("#eventStatus").append(`<option value="${option.value}">${option.text}</option>`);
            });

            $.ajax({
                type: "POST",
                url: "/get_ids", // Your Flask route to get IDs based on the selected type
                data: { type: selectedType },
                success: function (response) {
                    const ids = response.ids;
                    $("#eventId").empty();
                    ids.forEach((id) => {
                        $("#eventId").append(`<option value="${id}">${id}</option>`);
                    });
                    $("#eventId, #eventStatus, #addEventBtn").show();
                },
                error: function (xhr, status, error) {
                    console.error(error);
                }
            });
        }
    });
    const events = [];
    function updateEventsTable() {
        const tbody = $("#eventsTable tbody");
        tbody.empty();

        events.forEach((event, index) => {
            const row = `
                <tr>
                    <td>${event.type}</td>
                    <td>${event.id}</td>
                    <td>${event.status}</td>
                    <td><button class="remove-event-btn" data-index="${index}">Delete</button></td>
                </tr>
            `;
            tbody.append(row);
        });

        if (events.length === 0) {
            $("#eventsTable").hide();
        } else {
            $("#eventsTable").show();
        }
    }
    function addEventToBackend(event) {
        $.ajax({
            type: "POST",
            url: "/save_event", // Your Flask route to save the event data
            contentType: "application/json",
            data: JSON.stringify(event),
            success: function (response) {
                console.log("Event saved successfully:", response);
            },
            error: function (xhr, status, error) {
                console.error("Error saving event:", error);
            }
        });
    }
    function showError(message) {
        $("#errorMessage").text(message).show();
        setTimeout(function () {
            $("#errorMessage").fadeOut();
        }, 3000); // Hide the message after 3 seconds
    }
    // Add Event button click event
    $("#addEventBtn").click(function () {
        const selectedType = $("#eventType").val();
        const selectedId = $("#eventId").val();
        const selectedStatus = $("#eventStatus").val();

        if (selectedType && selectedId && selectedStatus) {
            // Check if the selected sensor ID already exists in the events array
            const isDuplicateId = events.some(event => event.id === selectedId);

            if (!isDuplicateId) {
                const event = {
                    type: selectedType,
                    id: selectedId,
                    status: selectedStatus
                };
                events.push(event);
                addEventToBackend(event); // Send event data to the backend
                updateEventsTable();
            } else {
                // Display an error message or take appropriate action for duplicate ID
                showError("Error: Duplicate sensor ID. Please choose a different ID.");
            }
        }

        $("#eventOptions").hide();
        $("#eventType, #eventId, #eventStatus").val("");
        $("#addEventBtn").hide();
    });
    // Remove Event button click event
    $("#eventsTable").on("click", ".remove-event-btn", function () {
        const index = $(this).data("index");
        events.splice(index, 1);
        updateEventsTable();
    });



    const actions = [];

    function updateActionsTable() {
        const tbody = $("#actionsTable tbody");
        tbody.empty();

        actions.forEach((action, index) => {
            const row = `
                <tr>
                    <td>${action.type}</td>
                    <td>${action.id}</td>
                    <td>${action.status || action.delay}</td>
                    <td><button class="remove-action-btn" data-index="${index}">Delete</button></td>
                </tr>
            `;
            tbody.append(row);
        });

        if (actions.length === 0) {
            $("#actionsTable").hide();
        } else {
            $("#actionsTable").show();
        }
    }

    function addActionToBackend(action) {
        // ... (previously defined code) ...
        $.ajax({
            type: "POST",
            url: "/save_action", // Your Flask route to save the event data
            contentType: "application/json",
            data: JSON.stringify(action),
            success: function (response) {
                console.log("Event saved successfully:", response);
            },
            error: function (xhr, status, error) {
                console.error("Error saving event:", error);
            }
        });
    }

    // Function to show an error message


    // Add Action button click event
    $("#automationWindow").on("click", ".add-action-btn", function () {
        $("#actionOptions").show();
        $("#actionType").val("");
        $("#actionId, #actionStatus, #delayTime, #addActionBtn").hide();
    });

    // ActionType selection change event
    $("#automationWindow").on("change", "#actionType", function () {
        const selectedType = $(this).val();
        if (selectedType === "switch" || selectedType === "siren") {
            $.ajax({
                type: "POST",
                url: "/get_ids", // Your Flask route to get IDs based on the selected type
                data: { type: selectedType },
                success: function (response) {
                    const ids = response.ids;
                    $("#actionId").empty();
                    ids.forEach((id) => {
                        $("#actionId").append(`<option value="${id}">${id}</option>`);
                    });
                    $("#actionId, #actionStatus, #addActionBtn").show();
                    $("#delayTime").hide();
                },
                error: function (xhr, status, error) {
                    console.error(error);
                }
            });
        } else if (selectedType === "delay") {
            $("#delayTime, #addActionBtn").show();
            $("#actionId, #actionStatus").hide();
        } else {
            $("#actionId, #actionStatus, #delayTime, #addActionBtn").hide();
        }
    });

    // AddActionBtn click event (specifically)
    $("#addActionBtn").click(function () {
        const selectedType = $("#actionType").val();
        const selectedId = $("#actionId").val();
        const selectedStatus = $("#actionStatus").val();
        const delayTime = $("#delayTime").val();

        if (selectedType && ((selectedId && selectedStatus) || (selectedType === "delay" && delayTime))) {
            const action = {
                type: selectedType,
                id: selectedId,
                status: selectedStatus,
                delay: delayTime
            };
            actions.push(action);
            addActionToBackend(action); // Send action data to the backend
            updateActionsTable();
        } else {
            showError("Please fill in all required fields.");
        }

        $("#actionOptions").hide();
        $("#actionType, #actionId, #actionStatus, #delayTime").val("");
    });

    // Remove Action button click event
    $("#actionsTable").on("click", ".remove-action-btn", function () {
        const index = $(this).data("index");
        actions.splice(index, 1);
        updateActionsTable();
    });


    // Function to send events and actions data to Flask
    function sendEventDataToFlask() {
        const eventData = {
            events: events,
            actions: actions
        };

        $.ajax({
            type: "POST",
            url: "/save_data", // Your Flask route to handle the data
            data: JSON.stringify(eventData),
            contentType: "application/json",
            success: function (response) {
                console.log("Data sent successfully:", response);
                // Add any success message or redirect as needed
                location.reload();
            },
            error: function (xhr, status, error) {
                console.error("Error sending data:", error);
                // Handle error and show an error message if needed
            }
        });
    }


    // Done button click event
    $("#doneBtn").click(function () {
        sendEventDataToFlask();
        // Add any other actions to perform when the "Done" button is clicked
    });

});
