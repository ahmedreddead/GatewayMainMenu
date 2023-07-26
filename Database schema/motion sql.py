DELIMITER //

CREATE TRIGGER motion_security
AFTER INSERT ON motion_sensor
FOR EACH ROW
BEGIN
  DECLARE event_triggerr INT;
  DECLARE event_id_param INT;
  DECLARE action_id_param INT;
  DECLARE door_triggerr INT;
  DECLARE motion_triggerr INT;

  -- Get the event_id and action_id parameters
  SET event_id_param = 35; -- Replace <event_id_value> with the actual event ID parameter
  SET action_id_param = 66; -- Replace <action_id_value> with the actual action ID parameter
  
  -- Check if the inserted row is a motion sensor
  IF NEW.sensorid IN (
      SELECT motion_sensor_id
      FROM event_motion
      WHERE event_id = event_id_param AND motion_sensor_id = NEW.sensorid AND motion_sensor_status = NEW.motion_status
    ) THEN
    -- Update the trigger value for the corresponding event and action
    UPDATE event_motion
    SET triggerr = 1
    WHERE event_id = event_id_param AND motion_sensor_id = NEW.sensorid;
  END IF;

  -- Check if all triggers (door, motion, and switch) are set to 1 for the given event and action
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

  -- If all triggers are set to 1, execute the Python script
  IF door_triggerr = 1 AND motion_triggerr = 1 THEN

      UPDATE event_door SET triggerr = 0 WHERE event_id = event_id_param;
      UPDATE event_motion SET triggerr = 0 WHERE event_id = event_id_param;
      INSERT INTO push_alert VALUES (event_id_param , action_id_param );
  	


  END IF;
  
END//

DELIMITER ;
