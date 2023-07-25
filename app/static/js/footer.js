function additem() {
  // Display the loading message
  document.getElementById("loading-div").style.display = "block";
  var successMessage = document.getElementById("success-message");

  
  // Simulate a delay (replace this with your actual request logic)
  
  // Get the values of the sensor attributes
  var type = document.getElementById('item-type').value;
  var id = document.getElementById('item-id').value;
  var protocol = document.getElementById('item-protocol').value;

  // Create a JSON object with the sensor data
  var sensorData = {
    type: type,
    id: id,
    protocol: protocol
  };

  // Send an AJAX POST request to the Flask API
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/add-item', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      // Hide the loading message
      
      // Check the response status
      if (xhr.status === 200) {
        // Item added successfully
        document.getElementById("loading-div").style.display = "none";
        successMessage.style.display = "block";
        var response = JSON.parse(xhr.responseText);
        console.log(response);
        var addItemModal = document.getElementById('add-item-modal');
        setTimeout(function() {
        successMessage.style.display = "none";
        addItemModal.style.display = 'none';
        }, 3000);

        
        setTimeout(function() {
        location.reload();
        }, 5000);
          
      } else {
        // Item not added successfully
        document.getElementById("loading-div").style.display = "none";
        var errorMessage = document.getElementById("error-message");
        errorMessage.style.display = "block";

        console.log('Item not added successfully');
        var addItemModal = document.getElementById('add-item-modal');
        setTimeout(function() {
        errorMessage.style.display = "none";
        addItemModal.style.display = 'none';
        }, 5000);
        
      }
    }
  };
  xhr.send(JSON.stringify(sensorData));

  // Close the modal dialog after adding the item
  var addItemModal = document.getElementById('add-item-modal');
  addItemModal.style.display = 'block';

}


  // Add an event listener to the "Add Item" button
var addItemButton = document.getElementById('add-item-button');
addItemButton.addEventListener('click', function () {
var addItemModal = document.getElementById('add-item-modal');
addItemModal.style.display = 'block';
// Add an event listener to the close button in the modal dialog
var closeBtn = document.getElementsByClassName('close')[0];
closeBtn.addEventListener('click', function () {
var addItemModal = document.getElementById('add-item-modal');
addItemModal.style.display = 'none';
});

});

// Add an event listener to the "Add" button in the modal dialog
var addConfirmButton = document.getElementById('add-item-confirm');
addConfirmButton.addEventListener('click', additem);


      
        
        
function displayItemList(itemLocations) {
  const itemList = document.getElementById("item-list");
  itemList.innerHTML = ""; // Clear previous options

  itemLocations.forEach((item) => {
    const option = document.createElement("option");
    option.value = [item.itemId ,item.type  ] ;
    option.textContent = item.type +"   "+ item.itemId;
    itemList.appendChild(option);
  });
}

// Function to handle item deletion
function deleteItem() {
  const selectedItem = document.getElementById("item-list").value;
    
    
  document.getElementById("loading-div").style.display = "block";
  var successMessage = document.getElementById("success-delete");

  
  // Simulate a delay (replace this with your actual request logic)
  
  // Get the values of the sensor attributes
  var type = document.getElementById('item-type').value;
  var id = document.getElementById('item-id').value;
  var protocol = document.getElementById('item-protocol').value;
  if (!selectedItem) {
    alert("Please select an item to delete");
    return;
  }

  // Make an AJAX request to the server to delete the item
  const deleteItemURL = "/delete-item"; // Replace with the actual URL endpoint for deleting an item in your Flask application
  const xhr = new XMLHttpRequest();
  xhr.open("POST", deleteItemURL);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onload = function () {
    if (xhr.status === 200) {
      // Item deleted successfully
      //alert("Item deleted successfully");
      displayItemList(itemLocations); // Refresh the item list
        
        document.getElementById("loading-div").style.display = "none";
        successMessage.style.display = "block";
        var response = JSON.parse(xhr.responseText);
        console.log(response);
        var addItemModal = document.getElementById('add-item-modal');
        setTimeout(function() {
        successMessage.style.display = "none";
        addItemModal.style.display = 'none';
        }, 3000);

        
        setTimeout(function() {
        location.reload();
        }, 5000);
    } else {
        // Item not added successfully
        document.getElementById("loading-div").style.display = "none";
        var errorMessage = document.getElementById("error-delete");
        errorMessage.style.display = "block";

        console.log('Item not added successfully');
        var addItemModal = document.getElementById('add-item-modal');
        setTimeout(function() {
        errorMessage.style.display = "none";
        addItemModal.style.display = 'none';
        }, 5000);
        
      }
  };
  xhr.send(JSON.stringify({ deletedItem: selectedItem }));
}

// Add click event listener to the delete button
const deleteButton = document.getElementById("delete-item");
deleteButton.addEventListener("click", deleteItem);
        
        
displayItemList(itemLocations);
        