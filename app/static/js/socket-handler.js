var socket;
var retryCount = 0;
var maxRetryAttempts = 3;

function connectSocket() {
        socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', handleSocketConnect);
        socket.on('disconnect', handleSocketDisconnect);
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
        setTimeout(connectSocket, 2000); // Retry after 2 seconds (adjust as needed)
    } else {
        console.log('Max retry attempts reached. Socket connection failed.');
    }
}

connectSocket();
        
        
    //var socket = io.connect('http://' + document.domain + ':' + location.port);
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var data = JSON.parse(this.responseText);
        for (let deviceType in data) {
            if (deviceType == 'switch'  ) {
                updateActuatorData(deviceType, data[deviceType]);
            } else {
                if (deviceType == 'siren' ) {
                    updateActuatorData(deviceType, data[deviceType]);
            }   else {
                    updateSensorData(deviceType, data[deviceType]);
                }
            }

                }
            }
};
xhr.open('GET', '/data', true);
xhr.send();