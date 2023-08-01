from app.module.controller import *
import random


def get_events_details():
    # { [ eventid : 556 , name : secure , description : [{sirenid : 5564 , status : on } , {delay : 5 } , {sirenid : 545 , status : off}] ,..... }


    object = create_database_object()
    result = object.get_events_by_user(1)

    print(result)


def get_actions_details() :
    object = create_database_object()
    result = object.get_actions_by_user(1)
    print(result)



def create_new_automation (object) :
    insert_event_flag = 0
    insert_action_flag = 0
    event_id = 0
    action_id = 0
    #user_id = session['user_id']
    user_id = 1

    while not insert_event_flag :
        object = create_database_object()
        event_id_new = random.randint(1, 9999)
        #object.check_insert_event_id( event_id, user_id)
        if object.check_insert_event_id(event_id_new, 1) :
            event_id = event_id_new
            insert_event_flag = 1

    while not insert_action_flag:
        object = create_database_object()
        action_id_new = random.randint(1, 9999)
        # object.check_insert_event_id( event_id, user_id)
        if object.check_insert_action_id(action_id_new, 1):
            action_id = action_id_new
            insert_action_flag = 1
    object = create_database_object()

    object.insert_new_automation(event_id,action_id,user_id)


    return (event_id,action_id)

def add_door_event (event_id ,sensor_id ,sensor_status ):

    object = create_database_object()
    object.insert_door_event(event_id,sensor_id,sensor_status)
    object.disconnect()

def add_motion_event  (event_id ,sensor_id ,sensor_status ):

    object = create_database_object()
    object.insert_motion_event(event_id, sensor_id, sensor_status)
    object.disconnect()



object =create_database_object()

#(9987, 'door_sensor') opened
#(3361, 'door_sensor') closed
#(215987, 'motion_sensor')

#sensors = object.get_sensors_by_user(1)
#for sensor in sensors :
#    print(sensor)


(event_id , action_id) = create_new_automation(object)

print(event_id , action_id )

#object.insert_new_automation(57 , 99 , 1)
#  |     2304      |       1       |      7751    |


'''
add_door_event(event_id,9987,'opened')
add_door_event(event_id,3361,'closed')
add_motion_event(event_id,215987,'motion_sensor')
get_events_details()
'''

get_events_details()
get_actions_details()


import mysql.connector

def execute_combined_query(user_id):
    # Replace the placeholders with your actual database credentials
    db_config = {
        "host": "10.20.0.169",
        "user": "grafana",
        "password": "pwd123",
        "database": "grafanadb"
    }

    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Prepare the SQL query
    combined_query = """
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

    try:
        # Execute the query with the provided user_id as a parameter
        cursor.execute(combined_query, (user_id, user_id))

        # Fetch all the results
        results = cursor.fetchall()

        # Print the results
        for row in results:
            event_id, event_door, event_motion, action_id, action_siren, action_switch, delay = row
            print(f"Event ID: {event_id}")
            print(f"Event Door: {event_door}")
            print(f"Event Motion: {event_motion}")
            print(f"Action ID: {action_id}")
            print(f"Action Siren: {action_siren}")
            print(f"Action Switch: {action_switch}")
            print(f"Delay: {delay}")
            print("-----------------------")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Usage example: Execute the combined query for a specific user_id (e.g., user_id = 1)
execute_combined_query(user_id=1)


