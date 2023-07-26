-- MariaDB dump 10.19  Distrib 10.5.19-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: grafanadb
-- ------------------------------------------------------
-- Server version	10.5.19-MariaDB-0+deb11u2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `action_siren`
--

DROP TABLE IF EXISTS `action_siren`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `action_siren` (
  `action_id` int(11) DEFAULT NULL,
  `siren_id` int(11) NOT NULL,
  `siren_status` varchar(20) NOT NULL,
  `order_number` int(11) NOT NULL,
  UNIQUE KEY `action_id` (`action_id`,`siren_id`,`order_number`),
  KEY `siren_id` (`siren_id`),
  CONSTRAINT `action_siren_ibfk_1` FOREIGN KEY (`siren_id`) REFERENCES `actuators` (`actuatorid`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`order_number` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `action_switch`
--

DROP TABLE IF EXISTS `action_switch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `action_switch` (
  `action_id` int(11) DEFAULT NULL,
  `switch_id` int(11) NOT NULL,
  `switch_status` varchar(20) NOT NULL,
  `order_number` int(11) NOT NULL,
  UNIQUE KEY `action_id` (`action_id`,`switch_id`,`order_number`),
  KEY `switch_id` (`switch_id`),
  CONSTRAINT `action_switch_ibfk_1` FOREIGN KEY (`switch_id`) REFERENCES `actuators` (`actuatorid`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`order_number` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `actuators`
--

DROP TABLE IF EXISTS `actuators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `actuators` (
  `actuatorid` int(11) NOT NULL,
  `cp` varchar(10) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`actuatorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER check_actuator_sensor_id
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
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `automation`
--

DROP TABLE IF EXISTS `automation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `automation` (
  `event_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `action_id` int(11) DEFAULT NULL,
  UNIQUE KEY `unique_event_action` (`event_id`,`action_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `automation_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dashboard_actuators`
--

DROP TABLE IF EXISTS `dashboard_actuators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard_actuators` (
  `dashboard_id` int(11) NOT NULL,
  `actuator_id` int(11) NOT NULL,
  UNIQUE KEY `unique_dashboard_actuator` (`dashboard_id`,`actuator_id`),
  KEY `actuator_id` (`actuator_id`),
  CONSTRAINT `dashboard_actuators_ibfk_1` FOREIGN KEY (`dashboard_id`) REFERENCES `dashboards` (`id`),
  CONSTRAINT `dashboard_actuators_ibfk_2` FOREIGN KEY (`actuator_id`) REFERENCES `actuators` (`actuatorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dashboard_items`
--

DROP TABLE IF EXISTS `dashboard_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dashboard_sensors`
--

DROP TABLE IF EXISTS `dashboard_sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard_sensors` (
  `dashboard_id` int(11) NOT NULL,
  `sensor_id` int(11) NOT NULL,
  UNIQUE KEY `unique_dashboard_sensor` (`dashboard_id`,`sensor_id`),
  KEY `sensor_id` (`sensor_id`),
  CONSTRAINT `dashboard_sensors_ibfk_1` FOREIGN KEY (`dashboard_id`) REFERENCES `dashboards` (`id`),
  CONSTRAINT `dashboard_sensors_ibfk_2` FOREIGN KEY (`sensor_id`) REFERENCES `sensors` (`sensorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dashboards`
--

DROP TABLE IF EXISTS `dashboards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboards` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `dashboards_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `delay`
--

DROP TABLE IF EXISTS `delay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `delay` (
  `action_id` int(11) NOT NULL,
  `duration` int(11) NOT NULL,
  `order_number` int(11) NOT NULL,
  UNIQUE KEY `action_id` (`action_id`,`order_number`),
  UNIQUE KEY `order_number` (`order_number`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`duration` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `door_sensor`
--

DROP TABLE IF EXISTS `door_sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `door_sensor` (
  `sensorid` int(11) NOT NULL,
  `door_status` varchar(20) NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `door_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER door_security
AFTER INSERT ON door_sensor
FOR EACH ROW
BEGIN
  DECLARE event_triggerr INT;
  DECLARE event_id_param INT;
  DECLARE action_id_param INT;
  DECLARE door_triggerr INT;
  DECLARE motion_triggerr INT;

  
  SET event_id_param = 35; 
  SET action_id_param = 66; 
  
  
  IF NEW.sensorid IN (
      SELECT door_sensor_id
      FROM event_door
      WHERE event_id = event_id_param AND door_sensor_id = NEW.sensorid AND door_sensor_status = NEW.door_status
    ) THEN
    
    UPDATE event_door
    SET triggerr = 1
    WHERE event_id = event_id_param AND door_sensor_id = NEW.sensorid;
  END IF;

  
  SET door_triggerr = (
    SELECT MIN(triggerr)
    FROM event_door
    WHERE event_id = event_id_param
    GROUP BY event_id
  );

  SET motion_triggerr = (
    SELECT MIN(triggerr)
    FROM event_motion
    WHERE event_id = event_id_param
    GROUP BY event_id
  );

  
  IF door_triggerr = 1 AND motion_triggerr = 1 THEN

      UPDATE event_door SET triggerr = 0 WHERE event_id = event_id_param;
      UPDATE event_motion SET triggerr = 0 WHERE event_id = event_id_param;

      INSERT INTO push_alert VALUES (event_id_param , action_id_param );
  

  END IF;
  
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `event_door`
--

DROP TABLE IF EXISTS `event_door`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_door` (
  `event_id` int(11) NOT NULL,
  `door_sensor_id` int(11) NOT NULL,
  `door_sensor_status` varchar(50) NOT NULL,
  `triggerr` int(11) NOT NULL,
  UNIQUE KEY `event_id` (`event_id`,`door_sensor_id`),
  KEY `door_sensor_id` (`door_sensor_id`),
  CONSTRAINT `event_door_ibfk_1` FOREIGN KEY (`door_sensor_id`) REFERENCES `door_sensor` (`sensorid`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`triggerr` in (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `event_motion`
--

DROP TABLE IF EXISTS `event_motion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_motion` (
  `event_id` int(11) NOT NULL,
  `motion_sensor_id` int(11) NOT NULL,
  `motion_sensor_status` varchar(50) NOT NULL,
  `triggerr` int(11) NOT NULL,
  UNIQUE KEY `event_id` (`event_id`,`motion_sensor_id`),
  KEY `motion_sensor_id` (`motion_sensor_id`),
  CONSTRAINT `event_motion_ibfk_1` FOREIGN KEY (`motion_sensor_id`) REFERENCES `motion_sensor` (`sensorid`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`triggerr` in (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `glass_sensor`
--

DROP TABLE IF EXISTS `glass_sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `glass_sensor` (
  `sensorid` int(11) NOT NULL,
  `glass_status` varchar(20) NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `glass_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `motion_sensor`
--

DROP TABLE IF EXISTS `motion_sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `motion_sensor` (
  `sensorid` int(11) NOT NULL,
  `motion_status` varchar(20) NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `motion_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER motion_security
AFTER INSERT ON motion_sensor
FOR EACH ROW
BEGIN
  DECLARE event_triggerr INT;
  DECLARE event_id_param INT;
  DECLARE action_id_param INT;
  DECLARE door_triggerr INT;
  DECLARE motion_triggerr INT;

  
  SET event_id_param = 35; 
  SET action_id_param = 66; 
  
  
  IF NEW.sensorid IN (
      SELECT motion_sensor_id
      FROM event_motion
      WHERE event_id = event_id_param AND motion_sensor_id = NEW.sensorid AND motion_sensor_status = NEW.motion_status
    ) THEN
    
    UPDATE event_motion
    SET triggerr = 1
    WHERE event_id = event_id_param AND motion_sensor_id = NEW.sensorid;
  END IF;

  
  SET door_triggerr = (
    SELECT MIN(triggerr)
    FROM event_door
    WHERE event_id = event_id_param
    GROUP BY event_id
  );

  SET motion_triggerr = (
    SELECT MIN(triggerr)
    FROM event_motion
    WHERE event_id = event_id_param
    GROUP BY event_id
  );

  
  IF door_triggerr = 1 AND motion_triggerr = 1 THEN

      UPDATE event_door SET triggerr = 0 WHERE event_id = event_id_param;
      UPDATE event_motion SET triggerr = 0 WHERE event_id = event_id_param;
      INSERT INTO push_alert VALUES (event_id_param , action_id_param );
  


  END IF;
  
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `polution_sensor`
--

DROP TABLE IF EXISTS `polution_sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `polution_sensor` (
  `sensorid` int(11) NOT NULL,
  `polution` float NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `polution_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `power`
--

DROP TABLE IF EXISTS `power`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `power` (
  `power` float NOT NULL,
  `date_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `push_alert`
--

DROP TABLE IF EXISTS `push_alert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `push_alert` (
  `event_id` int(11) NOT NULL,
  `action_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `relay_switch`
--

DROP TABLE IF EXISTS `relay_switch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relay_switch` (
  `actuatorid` int(11) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `actuatorid` (`actuatorid`),
  CONSTRAINT `relay_switch_ibfk_1` FOREIGN KEY (`actuatorid`) REFERENCES `actuators` (`actuatorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sensors`
--

DROP TABLE IF EXISTS `sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensors` (
  `sensorid` int(11) NOT NULL,
  `cp` varchar(10) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`sensorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER check_sensor_actuator_id
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
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `siren`
--

DROP TABLE IF EXISTS `siren`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `siren` (
  `actuatorid` int(11) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `actuatorid` (`actuatorid`),
  CONSTRAINT `siren_ibfk_1` FOREIGN KEY (`actuatorid`) REFERENCES `actuators` (`actuatorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `smoke_sensor`
--

DROP TABLE IF EXISTS `smoke_sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smoke_sensor` (
  `sensorid` int(11) NOT NULL,
  `fire_status` varchar(20) NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `smoke_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temperature_sensor`
--

DROP TABLE IF EXISTS `temperature_sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `temperature_sensor` (
  `sensorid` int(11) NOT NULL,
  `temperature` float NOT NULL,
  `humidty` float NOT NULL,
  `date_time` datetime DEFAULT NULL,
  KEY `sensorid` (`sensorid`),
  CONSTRAINT `temperature_sensor_ibfk_1` FOREIGN KEY (`sensorid`) REFERENCES `sensors` (`sensorid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-26 12:36:15
