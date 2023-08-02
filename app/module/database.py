import mysql.connector
from mysql.connector import Error

"""
host='localhost',
database='gateway',
user='root',
password='0000',
port='9999'
"""


class Database :

    def __init__(self,host,port,username,password,database_name):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database_name = database_name
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                 database=self.database_name,
                                                 user=self.username,
                                                 password=self.password,
                                                 port=self.port
                                                 )
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                #print("Connected to MySQL Server version ", db_Info)


        except Error as e:
            print("Error while connecting to MySQL", e)
    def is_connected (self) :
        return self.connection.is_connected()

    def disconnect(self):

            if self.connection.is_connected():

                self.connection.close()
                #print("MySQL connection is closed")
    def ckeck_connection (self):

            if self.connection.is_connected():
                return True
            else:
                return False

    def insert_new_sensor(self,sensorid,cp,name):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO sensors(sensorid,cp,name) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,cp,name)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_new_actuator(self,actuatorid ,cp,name):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO actuators(actuatorid ,cp,name) VALUES (%s,%s,%s)"""
            records_to_insert = (actuatorid ,cp,name)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_temperature_sensor_reading(self,sensorid,temp,hum,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO temperature_sensor(sensorid,temperature,humidty,date_time) VALUES (%s,%s,%s,%s)"""
            records_to_insert = (sensorid,temp,hum,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_door_sensor_reading(self,sensorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO door_sensor(sensorid,door_status,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_smoke_sensor_reading(self,sensorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO smoke_sensor(sensorid,fire_status,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_glass_sensor_reading(self,sensorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO glass_sensor(sensorid,glass_status,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_motion_sensor_reading(self,sensorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO motion_sensor(sensorid,motion_status,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_polution_sensor_reading(self,sensorid,polution,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO polution_sensor(sensorid,polution,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,polution,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_power_reading(self,power,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO power(power,date_time) VALUES (%s,%s)"""
            records_to_insert = (power,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_relay_switch_reading(self,actuatorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO relay_switch(actuatorid,status,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (actuatorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_siren_reading(self,actuatorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO siren(actuatorid,status,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (actuatorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def check_sensorid(self,sensorid):
        try:
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            check_query = "SELECT * FROM sensors WHERE sensorid = %s"
            cursor.execute(check_query, (sensorid,))
            result = cursor.fetchone()
            #self.connection.commit()
            return result
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def check_actuatorid(self,actuatorid):
        try:
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            check_query = "SELECT * FROM actuators WHERE actuatorid = %s"
            cursor.execute(check_query, (actuatorid,))
            result = cursor.fetchone()
            #self.connection.commit()
            return result
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_sensor_to_dashboard (self,dashboard_id , sensor_id):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO dashboard_sensors (dashboard_id,sensor_id) VALUES (%s,%s)"""
            records_to_insert = (int(dashboard_id),int(sensor_id))
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_actuators_to_dashboard (self,dashboard_id , actuators_id):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO dashboard_actuators (dashboard_id,actuator_id) VALUES (%s,%s)"""
            records_to_insert = (int(dashboard_id),int(actuators_id))
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def get_sensors_by_user(self,user_id):
        try:
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            query = """
                SELECT id, name
                FROM (
                  SELECT s.sensorid AS id, s.name
                  FROM sensors s
                  JOIN dashboard_sensors ds ON s.sensorid = ds.sensor_id
                  JOIN dashboards d ON ds.dashboard_id = d.id
                  WHERE d.user_id = {user_id}
                ) AS sensor_result
                UNION
                SELECT id, name
                FROM (
                  SELECT a.actuatorid AS id, a.name
                  FROM actuators a
                  JOIN dashboard_actuators da ON a.actuatorid = da.actuator_id
                  JOIN dashboards d ON da.dashboard_id = d.id
                  WHERE d.user_id = {user_id}
                ) AS actuator_result;
                """.format(user_id=user_id)
            # Execute the query and fetch the results
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_positions_into_dashboard (self,positions , dashboard_id , user_id ):
        try:
            cursor = self.connection.cursor()
            for item in positions :
                item_id = item['itemId']
                partition_id = item['partitionId']
                item_type = item['type']

                insert_query = """
                    INSERT INTO dashboard_items (dashboard_id, item_id, partition_id, item_type,user_id)
                    VALUES (%s, %s, %s, %s,%s)
                    ON DUPLICATE KEY UPDATE partition_id = VALUES(partition_id)
                """

                insert_data = (dashboard_id, item_id, partition_id, item_type,user_id)  # Using dashboard ID 1
                cursor.execute(insert_query, insert_data)

            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def get_positions(self,user_id, dashboard_id):
        try:
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            select_query = """
                SELECT item_id, partition_id, item_type
                FROM dashboard_items
                WHERE user_id = %s AND dashboard_id = %s
            """            # Execute the query and fetch the results
            cursor.execute(select_query, (user_id, dashboard_id))
            result = cursor.fetchall()
            data = []
            # Iterate over the rows and extract the required values
            for row in result:
                item_id, partition_id, item_type = row
                data.append({
                    'itemId': item_id,
                    'partitionId': partition_id,
                    'type': item_type
                })
            return data
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def delete_sensor(self, sensorid, type):
        try:
            cursor = self.connection.cursor()
            print(sensorid)
            print(type)
            sensorid = str(sensorid)
            if type == 'glass_break' :
                type = "glass_sensor"

            if type == 'temperature' :
                type = "temperature_sensor"

            # Delete from dashboard_items
            command = """DELETE FROM dashboard_items WHERE item_id = %s"""
            cursor.execute(command, (sensorid,))

            # Delete from dashboard_sensors
            command = """DELETE FROM dashboard_sensors WHERE sensor_id = %s"""
            cursor.execute(command, (sensorid,))

            # Delete from sensor data table
            command = f"DELETE FROM {type} WHERE sensorid = %s"
            cursor.execute(command, (sensorid,))

            # Delete from sensors table
            command = """DELETE FROM sensors WHERE sensorid = %s"""
            cursor.execute(command, (sensorid,))

            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to delete from MySQL table: {}".format(error))
            return error

    def delete_actuator(self, actuatorid, type):
        try:
            cursor = self.connection.cursor()
            print(actuatorid)
            print(type)
            actuatorid = str(actuatorid)

            # Delete from dashboard_items
            command = """DELETE FROM dashboard_items WHERE item_id = %s"""
            cursor.execute(command, (actuatorid,))

            # Delete from dashboard_actuators
            command = """DELETE FROM dashboard_actuators WHERE actuator_id = %s"""
            cursor.execute(command, (actuatorid,))

            # Delete from sensor data table
            command = f"DELETE FROM {type} WHERE actuatorid = %s"
            cursor.execute(command, (actuatorid,))

            # Delete from sensors table
            command = """DELETE FROM actuators WHERE actuatorid = %s"""
            cursor.execute(command, (actuatorid,))

            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to delete from MySQL table: {}".format(error))
            return error

    def get_actions(self , action_id ):
        try:
            result = {}
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            select_query = """
                SELECT siren_id, siren_status, order_number
                FROM action_siren
                WHERE action_id = %s 
            """            # Execute the query and fetch the results
            cursor.execute(select_query, (action_id,))
            result['siren'] = cursor.fetchall()

            select_query = """
                SELECT switch_id, switch_status, order_number
                FROM action_switch
                WHERE action_id = %s 
            """            # Execute the query and fetch the results
            cursor.execute(select_query, (action_id,))
            result['switch'] = cursor.fetchall()

            select_query = """
                SELECT duration , order_number
                FROM delay 
                WHERE action_id = %s 
            """            # Execute the query and fetch the results
            cursor.execute(select_query, (action_id,))
            result['time']  = cursor.fetchall()

            return result


        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def get_push_alert(self, ):
        try:
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            check_query = "SELECT event_id, action_id FROM push_alert"
            cursor.execute(check_query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def delete_push_alert(self, action_id):
        try:
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            cursor.execute("DELETE FROM push_alert WHERE action_id = %s", (action_id,))
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def get_events_by_user(self , userid):
        try:
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            check_query = """SELECT a.`event_id`,
                            GROUP_CONCAT(DISTINCT CONCAT( '[' , d.`door_sensor_id`, ',', d.`door_sensor_status`, ']'  )) AS event_door,
                            GROUP_CONCAT(DISTINCT CONCAT( '[', m.`motion_sensor_id`, ',', m.`motion_sensor_status` , ']' )) AS event_motion
                            FROM
                                `automation` a
                            JOIN
                                `event_door` d ON a.`event_id` = d.`event_id`
                            JOIN
                                `event_motion` m ON a.`event_id` = m.`event_id`
                            WHERE
                                a.`user_id` = %s
                                AND a.`event_id` IN (SELECT `event_id` FROM `automation` WHERE `user_id` = %s )
                            GROUP BY
                                a.`event_id`;
                            """
            cursor.execute(check_query , [str(userid), str (userid)],)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def get_actions_by_user(self , userid):
        try:
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            check_query = """SELECT
                                    a.`action_id`,
                                    GROUP_CONCAT(DISTINCT CONCAT( '[',s.`siren_id`, ',', s.`siren_status`, ',', s.`order_number` , ']')) AS action_siren,
                                    GROUP_CONCAT(DISTINCT CONCAT('[', sw.`switch_id`, ',', sw.`switch_status`, ',', sw.`order_number`, ']')) AS action_switch,
                                    GROUP_CONCAT(DISTINCT CONCAT('[' , d.`duration`, ',', d.`order_number`, ']')) AS delay
                                FROM
                                    `automation` a
                                LEFT JOIN
                                    `action_siren` s ON a.`action_id` = s.`action_id`
                                LEFT JOIN
                                    `action_switch` sw ON a.`action_id` = sw.`action_id`
                                LEFT JOIN
                                    `delay` d ON a.`action_id` = d.`action_id`
                                WHERE
                                    a.`user_id` = %s
                                    AND a.`action_id` IN (SELECT `action_id` FROM `automation` WHERE `user_id` = %s )
                                GROUP BY
                                    a.`action_id`;
                                """
            cursor.execute(check_query , [str(userid), str (userid)] )
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def check_insert_event_id(self, event_id , user_id):
        try:
            cursor = self.connection.cursor()
            check_query = "SELECT event_id FROM automation WHERE user_id = %s"
            cursor.execute(check_query, (user_id,))
            result = cursor.fetchone()
            if event_id in result :
                return False
            else:
                return True

        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error
    def check_insert_action_id(self, action_id , user_id):
        try:
            cursor = self.connection.cursor()
            check_query = "SELECT action_id FROM automation WHERE user_id = %s"
            cursor.execute(check_query, (user_id,))
            result = cursor.fetchone()
            if action_id in result :
                return False
            else:
                return True

        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error



    def insert_new_automation(self , event_id , action_id , user_id ):
        try:
            cursor = self.connection.cursor()
            insert_query = "INSERT INTO automation (event_id, user_id, action_id) VALUES (%s, %s, %s)"
            # Data to be inserted
            data = (event_id, user_id, action_id)
            cursor.execute(insert_query, data)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_door_event(self , event_id , door_sensor_id , door_status ):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO event_door (  event_id , door_sensor_id , door_sensor_status , triggerr ) VALUES (%s,%s,%s, %s) """
            records_to_insert = ( event_id , door_sensor_id , door_status , 0 )
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_motion_event(self , event_id , motion_sensor_id , motion_status ):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO event_door (  event_id , door_sensor_id , door_sensor_status , triggerr ) VALUES (%s,%s,%s, %s) """
            records_to_insert = ( event_id , motion_sensor_id , motion_status , 0 )
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def get_events_and_action_by_user(self, userid):
        try:
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            check_query = """
        SELECT
            a.`event_id`,
            GROUP_CONCAT(DISTINCT CONCAT('[', d.`door_sensor_id`, ',', d.`door_sensor_status`, ']')) AS event_door,
            GROUP_CONCAT(DISTINCT CONCAT('[', m.`motion_sensor_id`, ',', m.`motion_sensor_status`, ']')) AS event_motion,
            a.`action_id`,
            GROUP_CONCAT(DISTINCT CONCAT('[', s.`siren_id`, ',', s.`siren_status`, ',', s.`order_number`, ']')) AS action_siren,
            GROUP_CONCAT(DISTINCT CONCAT('[', sw.`switch_id`, ',', sw.`switch_status`, ',', sw.`order_number`, ']')) AS action_switch,
            GROUP_CONCAT(DISTINCT CONCAT('[', dl.`duration`, ',', dl.`order_number`, ']')) AS delay
        FROM
            `automation` a
        LEFT JOIN
            `event_door` d ON a.`event_id` = d.`event_id`
        LEFT JOIN
            `event_motion` m ON a.`event_id` = m.`event_id`
        LEFT JOIN
            `action_siren` s ON a.`action_id` = s.`action_id`
        LEFT JOIN
            `action_switch` sw ON a.`action_id` = sw.`action_id`
        LEFT JOIN
            `delay` dl ON a.`action_id` = dl.`action_id`
        WHERE
            a.`user_id` = %s
            AND a.`event_id` IN (SELECT `event_id` FROM `automation` WHERE `user_id` = %s)
        GROUP BY
            a.`event_id`, a.`action_id`
    """
            cursor.execute(check_query ,(userid, userid))
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error


    def get_sensor_id_by_type(self, type):
        try:
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            check_query = "SELECT sensorid FROM sensors WHERE name =%s"
            cursor.execute(check_query , [type])
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def get_actuator_id_by_type(self, type):
        try:
            cursor = self.connection.cursor()
            # Check if the sensor ID already exists in the sensors table
            check_query = "SELECT actuatorid FROM actuators WHERE name = %s"
            cursor.execute(check_query , [type])
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error



