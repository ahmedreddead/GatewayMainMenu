function getSensorIcon(sensorType,sensorStatus) {
            switch (sensorType) {
                case 'temperature':
                    return '<i class="fa fa-thermometer-half sensor-icon"></i>';
                case 'humidity':
                    return '<i class="fa fa-tint sensor-icon"></i>';
                case 'glass_break':
                    return '<img src="static/photo/broken-window.png" class="sensor-icon"  width="140" height="140">';
                case 'motion_sensor':
                    if (sensorStatus === 'No Motion') {
                        return '<img src="static/photo/motionno.png" class="sensor-icon"  width="140" height="140">';
                    } else if (sensorStatus === 'Motion Detected') {
                        return '<img src="static/photo/motiond.png" class="sensor-icon"  width="140" height="140">';
                    }else {
                        return '';
                    }                
                case 'door_sensor':
                    if (sensorStatus === 'opened') {
                        return '<img src="static/photo/door.png" class="sensor-icon"  width="140" height="140">';
                    } else if (sensorStatus === 'closed') {
                        return '<img src="static/photo/doorclosed.png" class="sensor-icon"  width="140" height="140">';
                    }
                default:
                    return '';
                }
}

function getActuatorIcon(actuatorType, actuatorValue) {
            let actuatorIconClass = actuatorValue === 'on' ? 'actuator-icon-on' : 'actuator-icon-off';
            switch (actuatorType) {
                case 'switch':
                    return `<img src="static/photo/light${actuatorValue === 'on' ? 'on' : 'off'}.png" class="actuator-icon"  width="170" height="170">`;                // add more actuator types and icons here
                case 'siren':
                    return `<img src="static/photo/siren${actuatorValue === 'on' ? 'on' : 'off'}.png" class="actuator-icon"  width="170" height="170">`;                // add more actuator types and icons here
                default:
                    return '';
            }
}

function updateSensorData(sensorType, sensorData) {
            for (let sensorId in sensorData) {
                let sensorElementId = sensorId;
                let sensorElement = document.getElementById(sensorElementId);
                if (sensorElement) {
                    let sensorValue = sensorData[sensorId];
                    let lastUpdated = new Date().toLocaleTimeString();
                    sensorElement.innerHTML = `
                        <div class="sensor">
                            ${getSensorIcon(sensorType,sensorValue )}
                            <div class="sensor-name">${sensorType} ${sensorId}</div>
                            <div class="sensor-value">${sensorValue || 'Unknown'}</div>
                            <div class="last-updated">Last updated: ${lastUpdated}</div>
                        </div>
                    `;
                }
            }
}
        
function updateActuatorData(actuatorType, actuatorData) {
            for (let actuatorId in actuatorData) {
                let actuatorElementId = actuatorId;
                let actuatorElement = document.getElementById(actuatorElementId);
                if (actuatorElement !== null) {
                    console.log("Element found:", actuatorElement.innerHTML);
                } else {
                    console.log("Element not found.");
                }
                if (actuatorElement) {
                    let actuatorValue = actuatorData[actuatorId];
                    let lastUpdated = new Date().toLocaleTimeString();
                    actuatorElement.innerHTML = `
                        <div class="actuator">
                            ${getActuatorIcon(actuatorType, actuatorValue)}
                            <div class="actuator-name">${actuatorType} ${actuatorId}</div>
                            <div class="actuator-value">${actuatorValue || 'Unknown'}</div>
                            <div class="last-updated">Last updated: ${lastUpdated}</div>
                        </div>
                    `;
                    actuatorElement.setAttribute('data-value', actuatorValue);
                }
            }
}

function toggleActuator(actuatorType, actuatorId) {
            let actuatorElementId = actuatorId;
            let actuatorElement = document.getElementById(actuatorElementId);
            let actuatorValue = actuatorElement.getAttribute('data-value');
            let newActuatorValue;
            if (actuatorValue === 'off') {
                newActuatorValue = 'on';
                actuatorElement.setAttribute('data-value', newActuatorValue);
            } else {
                newActuatorValue = 'off';
                actuatorElement.setAttribute('data-value', newActuatorValue);
            }
            /*
    console.log(newActuatorValue);
    actuatorElement.innerHTML = `
                        <div class="actuator">
                            ${getActuatorIcon(actuatorType, newActuatorValue)}
                            <div class="actuator-name">${actuatorType} ${actuatorId}</div>
                            <div class="actuator-value">${newActuatorValue || 'Unknown'}</div>
                        </div>
                    `;
*/
    socket.emit('actuator_command', {
                type: actuatorType,
                id: actuatorId,
                value: newActuatorValue
            });
}
        