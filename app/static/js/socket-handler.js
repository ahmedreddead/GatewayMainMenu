var socket;
var retryCount = 0;
var maxRetryAttempts = 20;

function connectSocket() {

        socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', handleSocketConnect);
        socket.on('disconnect', handleSocketDisconnect);
        return socket
    }
function handleSocketConnect() {
            console.log('Socket connected');
  // Perform necessary operations after successful socket connection
        }

function handleSocketDisconnect() {
    console.log('Socket disconnected');
    retrySocketConnection();
}

function retrySocketConnection() {
    if (retryCount < maxRetryAttempts) {
        retryCount++;
        console.log('Retrying socket connection... (attempt ' + retryCount + ')');
        setTimeout(connectSocket, 5000); // Retry after 2 seconds (adjust as needed)
    } else {
        console.log('Max retry attempts reached. Socket connection failed.');
    }
}

socket = connectSocket();



   //var socket = io.connect('http://' + document.domain + ':' + location.port);
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
   if (this.readyState == 4) {
       if (this.status == 200) {
           var data = JSON.parse(this.responseText);
           console.log(data)
           for (let deviceType in data) {
               if (deviceType == 'switch' || deviceType == 'siren') {
                   updateActuatorData(deviceType, data[deviceType]);
               } else {
                   updateSensorData(deviceType, data[deviceType]);
               }
           }
       } else {
           console.error('Error retrieving data:', this.status, this.statusText);
       }
   }
};
xhr.onerror = function() {
   console.error('Request failed.');
};
xhr.open('GET', '/data', true);
xhr.send();

