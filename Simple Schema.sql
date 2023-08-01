CREATE TABLE `action_siren` (
  `action_id` int(11) DEFAULT NULL,
  `siren_id` int(11) NOT NULL,
  `siren_status` varchar(20) NOT NULL,
  `order_number` int(11) NOT NULL,
  UNIQUE KEY `action_id` (`action_id`,`siren_id`,`order_number`),
  KEY `siren_id` (`siren_id`),
  CONSTRAINT `action_siren_ibfk_1` FOREIGN KEY (`siren_id`) REFERENCES `actuators` (`actuatorid`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`order_number` >= 0)
);

CREATE TABLE `action_switch` (
  `action_id` int(11) DEFAULT NULL,
  `switch_id` int(11) NOT NULL,
  `switch_status` varchar(20) NOT NULL,
  `order_number` int(11) NOT NULL,
  UNIQUE KEY `action_id` (`action_id`,`switch_id`,`order_number`),
  KEY `switch_id` (`switch_id`),
  CONSTRAINT `action_switch_ibfk_1` FOREIGN KEY (`switch_id`) REFERENCES `actuators` (`actuatorid`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`order_number` >= 0)
);

CREATE TABLE `actuators` (
  `actuatorid` int(11) NOT NULL,
  `cp` varchar(10) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`actuatorid`)
);


CREATE TABLE `automation` (
  `event_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `action_id` int(11) DEFAULT NULL,
  UNIQUE KEY `unique_event_action` (`event_id`,`action_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `automation_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);

CREATE TABLE `dashboard_actuators` (
  `dashboard_id` int(11) NOT NULL,
  `actuator_id` int(11) NOT NULL,
  UNIQUE KEY `unique_dashboard_actuator` (`dashboard_id`,`actuator_id`),
  KEY `actuator_id` (`actuator_id`),
  CONSTRAINT `dashboard_actuators_ibfk_1` FOREIGN KEY (`dashboard_id`) REFERENCES `dashboards` (`id`),
  CONSTRAINT `dashboard_actuators_ibfk_2` FOREIGN KEY (`actuator_id`) REFERENCES `actuators` (`actuatorid`)
) ;

CREATE TABLE `dashboard_items` (
  `dashboard_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `partition_id` varchar(50) NOT NULL,
  `item_type` varchar(50) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`dashboard_id`,`item_id`),
  KEY `fk_user_id` (`user_id`),
  CONSTRAINT `dashboard_items_ibfk_1` FOREIGN KEY (`dashboard_id`) REFERENCES `dashboards` (`id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);

CREATE TABLE `dashboard_sensors` (
  `dashboard_id` int(11) NOT NULL,
  `sensor_id` int(11) NOT NULL,
  UNIQUE KEY `unique_dashboard_sensor` (`dashboard_id`,`sensor_id`),
  KEY `sensor_id` (`sensor_id`),
  CONSTRAINT `dashboard_sensors_ibfk_1` FOREIGN KEY (`dashboard_id`) REFERENCES `dashboards` (`id`),
  CONSTRAINT `dashboard_sensors_ibfk_2` FOREIGN KEY (`sensor_id`) REFERENCES `sensors` (`sensorid`)
);

CREATE TABLE `dashboards` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `dashboards_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);

CREATE TABLE `delay` (
  `action_id` int(11) NOT NULL,
  `duration` int(11) NOT NULL,
  `order_number` int(11) NOT NULL,
  UNIQUE KEY `action_id` (`action_id`,`order_number`),
  UNIQUE KEY `order_number` (`order_number`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`duration` >= 0)
) ;

CREATE TABLE `door_sensor` (
  `sensorid` int(11) NOT NULL,
  `door_status` varchar(20) NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `door_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
);



CREATE TABLE `event_door` (
  `event_id` int(11) NOT NULL,
  `door_sensor_id` int(11) NOT NULL,
  `door_sensor_status` varchar(50) NOT NULL,
  `triggerr` int(11) NOT NULL,
  UNIQUE KEY `event_id` (`event_id`,`door_sensor_id`),
  KEY `door_sensor_id` (`door_sensor_id`),
  CONSTRAINT `event_door_ibfk_1` FOREIGN KEY (`door_sensor_id`) REFERENCES `sensors` (`sensorid`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`triggerr` in (0,1))
);

//


ALTER TABLE event_door
DROP FOREIGN KEY event_door_ibfk_1;

ALTER TABLE event_door
ADD CONSTRAINT event_door_ibfk_1 FOREIGN KEY (door_sensor_id) REFERENCES sensors (sensorid);

//


CREATE TABLE `event_motion` (
  `event_id` int(11) NOT NULL,
  `motion_sensor_id` int(11) NOT NULL,
  `motion_sensor_status` varchar(50) NOT NULL,
  `triggerr` int(11) NOT NULL,
  UNIQUE KEY `event_id` (`event_id`,`motion_sensor_id`),
  KEY `motion_sensor_id` (`motion_sensor_id`),
  CONSTRAINT `event_motion_ibfk_1` FOREIGN KEY (`motion_sensor_id`) REFERENCES `motion_sensor` (`sensorid`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`triggerr` in (0,1))
);


CREATE TABLE `glass_sensor` (
  `sensorid` int(11) NOT NULL,
  `glass_status` varchar(20) NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `glass_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
);

CREATE TABLE `motion_sensor` (
  `sensorid` int(11) NOT NULL,
  `motion_status` varchar(20) NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `motion_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
)
;
CREATE TABLE `polution_sensor` (
  `sensorid` int(11) NOT NULL,
  `polution` float NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `polution_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
)
;

CREATE TABLE `power` (
  `power` float NOT NULL,
  `date_time` datetime DEFAULT NULL
)
;
CREATE TABLE `push_alert` (
  `event_id` int(11) NOT NULL,
  `action_id` int(11) NOT NULL
)
;

CREATE TABLE `relay_switch` (
  `actuatorid` int(11) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `actuatorid` (`actuatorid`),
  CONSTRAINT `relay_switch_ibfk_1` FOREIGN KEY (`actuatorid`) REFERENCES `actuators` (`actuatorid`)
);
CREATE TABLE `sensors` (
  `sensorid` int(11) NOT NULL,
  `cp` varchar(10) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`sensorid`)
) ;

CREATE TABLE `siren` (
  `actuatorid` int(11) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `actuatorid` (`actuatorid`),
  CONSTRAINT `siren_ibfk_1` FOREIGN KEY (`actuatorid`) REFERENCES `actuators` (`actuatorid`)
);

CREATE TABLE `smoke_sensor` (
  `sensorid` int(11) NOT NULL,
  `fire_status` varchar(20) NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `smoke_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
) ;

CREATE TABLE `temperature_sensor` (
  `sensorid` int(11) NOT NULL,
  `temperature` float NOT NULL,
  `humidty` float NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `temperature_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
);

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ;
















