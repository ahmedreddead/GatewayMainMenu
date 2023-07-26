CREATE DATABASE Gateway;

USE Gateway;

CREATE TABLE sensors (
    sensorid INT PRIMARY KEY NOT NULL,
    cp VARCHAR(10),
    name VARCHAR(50)
);

CREATE TABLE temperature_sensor (
    sensorid INT NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    date_time DATETIME,
    FOREIGN KEY (sensorid) REFERENCES sensors(sensorid)
);

CREATE TABLE door_sensor (
    sensorid INT NOT NULL,
    door_status VARCHAR(20) NOT NULL,
    date_time DATETIME,
    FOREIGN KEY (sensorid) REFERENCES sensors(sensorid)
);

CREATE TABLE smoke_sensor (
    sensorid INT NOT NULL,
    fire_status VARCHAR(20) NOT NULL,
    date_time DATETIME,
    FOREIGN KEY (sensorid) REFERENCES sensors(sensorid)
);

CREATE TABLE actuators (
    actuatorid INT PRIMARY KEY NOT NULL,
    cp VARCHAR(10),
    name VARCHAR(50)
);

CREATE TABLE relay_switch (
    actuatorid INT NOT NULL,
    status VARCHAR(20),
    date_time DATETIME,
    FOREIGN KEY (actuatorid) REFERENCES actuators(actuatorid)
);

CREATE TABLE siren (
    actuatorid INT NOT NULL,
    status VARCHAR(20),
    date_time DATETIME,
    FOREIGN KEY (actuatorid) REFERENCES actuators(actuatorid)
);

CREATE TABLE motion_sensor (
    sensorid INT NOT NULL,
    motion_status VARCHAR(20) NOT NULL,
    date_time DATETIME,
    FOREIGN KEY (sensorid) REFERENCES sensors(sensorid)
);

CREATE TABLE glass_sensor (
    sensorid INT NOT NULL,
    glass_status VARCHAR(20) NOT NULL,
    date_time DATETIME,
    FOREIGN KEY (sensorid) REFERENCES sensors(sensorid)
);

CREATE TABLE pollution_sensor (
    sensorid INT NOT NULL,
    pollution FLOAT NOT NULL,
    date_time DATETIME,
    FOREIGN KEY (sensorid) REFERENCES sensors(sensorid)
);

CREATE TABLE power (
    power FLOAT NOT NULL,
    date_time DATETIME
);

-- New table: users
CREATE TABLE users (
    id INT PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- New table: dashboards
CREATE TABLE dashboards (
    id INT PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- New table: dashboard_sensors
CREATE TABLE dashboard_sensors (
    dashboard_id INT NOT NULL,
    sensor_id INT NOT NULL,
    FOREIGN KEY (dashboard_id) REFERENCES dashboards (id),
    FOREIGN KEY (sensor_id) REFERENCES sensors (sensorid)
);

-- New table: dashboard_actuators
CREATE TABLE dashboard_actuators (
    dashboard_id INT NOT NULL,
    actuator_id INT NOT NULL,
    FOREIGN KEY (dashboard_id) REFERENCES dashboards (id),
    FOREIGN KEY (actuator_id) REFERENCES actuators (actuatorid)
);

-- Add unique constraint to dashboard_actuators table
ALTER TABLE dashboard_actuators
ADD CONSTRAINT unique_dashboard_actuator
UNIQUE (dashboard_id, actuator_id);

-- Add unique constraint to dashboard_sensors table
ALTER TABLE dashboard_sensors
ADD CONSTRAINT unique_dashboard_sensor
UNIQUE (dashboard_id, sensor_id);

CREATE TABLE dashboard_items (
    dashboard_id INT NOT NULL,
    item_id INT NOT NULL,
    partition_id VARCHAR(50) NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    PRIMARY KEY (dashboard_id, item_id),
    FOREIGN KEY (dashboard_id) REFERENCES dashboards (id),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create a trigger on sensors table
DELIMITER //
CREATE TRIGGER check_sensor_actuator_id
BEFORE INSERT ON sensors
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT *
        FROM actuators
        WHERE actuatorid = NEW.sensorid
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'sensorid and actuatorid cannot have the same value.';
    END IF;
END//
DELIMITER ;

-- Create a trigger on actuators table
DELIMITER //
CREATE TRIGGER check_actuator_sensor_id
BEFORE INSERT ON actuators
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT *
        FROM sensors
        WHERE sensorid = NEW.actuatorid
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'sensorid and actuatorid cannot have the same value.';
    END IF;
END//
DELIMITER ;

-- New table: automation
CREATE TABLE automation (
    event_id INT,
    user_id INT NOT NULL,
    action_id INT,
    UNIQUE KEY unique_event_action (event_id, action_id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE action_siren (
    action_id INT,
    siren_id INT NOT NULL,
    siren_status VARCHAR(20) NOT NULL,
    order_number INT NOT NULL,
    CHECK (order_number >= 0),
    UNIQUE (action_id, siren_id, order_number),
    FOREIGN KEY (siren_id) REFERENCES actuators (actuatorid)
);

CREATE TABLE action_switch (
    action_id INT,
    switch_id INT NOT NULL,
    switch_status VARCHAR(20) NOT NULL,
    order_number INT NOT NULL,
    CHECK (order_number >= 0),
    UNIQUE (action_id, switch_id, order_number),
    FOREIGN KEY (switch_id) REFERENCES actuators (actuatorid)
);

CREATE TABLE delay (
    action_id INT NOT NULL,
    duration INT NOT NULL,
    order_number INT NOT NULL,
    UNIQUE (action_id, order_number),
    CHECK (duration >= 0),
    UNIQUE (order_number)
);

CREATE TABLE push_alert (
    event_id INT NOT NULL,
    action_id INT NOT NULL,
    FOREIGN KEY (event_id, action_id) REFERENCES automation (event_id, action_id)
);

-- You can add more INSERT statements for testing or data initialization if needed.
