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
});
