import datetime
import json
import threading
import time
import random

from flask import render_template, request, jsonify
from app import app,socketio

from flask_mqtt import Mqtt
from app.module import database
from flask import session

from flask import redirect, url_for
from datetime import timedelta


app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Set session duration (e.g., 7 days)
mqtt = Mqtt(app)
sensor_data = {}
sensor_types = [ 'temperature', 'humidity', 'motion_sensor', 'door_sensor', 'glass_break' ,'switch', 'siren']
sensor_counts = {}
is_first_load = True
page_loaded = False


host = '10.20.0.197'


@app.after_request
def add_cache_control(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


@app.route('/delete_automation', methods=['POST'])
def delete_automation():
    data = request.get_json()
    object = create_database_object()
    object.delete_automation(data['event_id'], data['action_id'])
    object.delete_trigger(data['event_id'])
    return jsonify({'message': 'Data received successfully.'})

def create_new_automation (Actions , Events) :
    insert_event_flag = 0
    insert_action_flag = 0
    event_id = 0
    action_id = 0
    user_id = session['user_id']

    try:
        while not insert_event_flag :
            object = create_database_object()
            event_id_new = random.randint(1, 9999)
            if object.check_insert_event_id(event_id_new,user_id) :
                event_id = event_id_new
                insert_event_flag = 1

        while not insert_action_flag:
            object = create_database_object()
            action_id_new = random.randint(1, 9999)
            if object.check_insert_action_id(action_id_new, user_id):
                action_id = action_id_new
                insert_action_flag = 1

        object = create_database_object()

        object.insert_new_automation(event_id,action_id,user_id)

        for dic in Events:
            if dic['type'] == 'motion_sensor':
                status = 'Motion Detected'
                object.insert_motion_event(event_id, dic['id'], status)
            elif dic['type'] == 'door_sensor':
                object.insert_door_event(event_id, dic['id'], dic['status'])

        for index, dic in enumerate(Actions):
            if dic['type'] == 'siren':
                object.insert_action_siren(index+1, action_id, dic['id'], dic['status'])
            elif dic['type'] == 'switch':
                object.insert_action_switch(index+1, action_id, dic['id'], dic['status'])
            elif dic['type'] == 'delay':
                object.insert_action_delay(index+1, action_id, dic['delay'])

        object.insert_trigger(event_id,action_id)


    except Exception as e :
        print("error" , e)

    return 200


@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()
    events = data.get('events')
    actions = data.get('actions')

    # Process the events and actions data as needed
    # For demonstration purposes, we'll just print the data
    print("Events:", events)
    print("Actions:", actions)
    response =create_new_automation(actions,events)

    if response == 200 :
        return jsonify({'message': 'Data received successfully.'})
    else:
        return jsonify({'message': 'Data received unsuccessfully.'})


@app.route('/get_ids', methods=['POST'])
def get_ids():
    selected_type = request.form['type']
    object = create_database_object()

    # Mock data to simulate Flask response with IDs
    if selected_type == "motion_sensor":
        ids = object.get_sensor_id_by_type(selected_type)
    elif selected_type == "door_sensor":
        ids = object.get_sensor_id_by_type(selected_type)
    elif selected_type == 'switch':
        ids = object.get_actuator_id_by_type(selected_type)
    elif selected_type == 'siren':
        ids = object.get_actuator_id_by_type(selected_type)
    else:
        ids = []

    return jsonify({'ids': ids})

@app.route('/save_event', methods=['POST'])
def save_event():
    event_data = request.get_json()
    # Save the event_data to your database or process it as required
    return jsonify({'status': 'success'})

@app.route('/save_action', methods=['POST'])
def save_action():
    event_data = request.get_json()
    # Save the event_data to your database or process it as required
    return jsonify({'status': 'success'})

def insert_reading(sensorType , sensorId , status) :
    object = create_database_object()
    time = datetime.datetime.now()
    if sensorType == 'door_sensor' :
        object.insert_door_sensor_reading(sensorId,status , time)
    elif sensorType == 'motion_sensor' :
        object.insert_motion_sensor_reading(sensorId,status ,time)
    elif sensorType == 'temperature' :
        object.insert_temperature_sensor_reading(sensorId,status,status,time)
    elif sensorType == 'polution' :
        object.insert_polution_sensor_reading(sensorId,status,time)
    elif sensorType == 'switch' :
        object.insert_relay_switch_reading(sensorId,status,time)
    elif sensorType == 'siren' :
        object.insert_siren_reading(sensorId ,status ,time)
    elif sensorType == 'smoke' :
        object.insert_smoke_sensor_reading(sensorId ,status ,time)

    object.disconnect()

def actions_to_json(siren, switch, time):
    list_of_Actions = []
    siren = str(siren).split('],[')
    siren = [ x.replace('[','').replace(']','') for x in siren]
    siren = [x.split(',') for x in siren ]

    switch = str(switch).split('],[')
    switch = [x.replace('[', '').replace(']', '') for x in switch]
    switch = [x.split(',') for x in switch]


    time = str(time).split('],[')
    time = [x.replace('[', '').replace(']', '') for x in time]
    time = [x.split(',') for x in time]


    for sirenAcrion in siren :
        if sirenAcrion[0] =='None' :
            break
        list_of_Actions.append([ int(sirenAcrion[2]) , 'siren',sirenAcrion[1], int(sirenAcrion[0])   ])
    for switchAcrion in switch :
        if switchAcrion[0] == 'None' :
            break
        list_of_Actions.append([ int(switchAcrion[2]) ,'switch' ,switchAcrion[1] , int(switchAcrion[0]) ])
    for t in time :
        if t[0] == 'None' :
            break
        list_of_Actions.append([ int(t[1]) ,'delay', t[0]+ ' sec' ,None ])


    actions_dict = {item[0]: {"type": item[1], "id": item[3], "status": item[2]} for item in list_of_Actions}

    # Sort the dictionary by keys (the order)
    sorted_actions = sorted(actions_dict.items())

    # Convert the sorted dictionary back to a list of dictionaries
    sorted_data = [{"order": order, **values} for order, values in sorted_actions]

    # Convert the sorted data to JSON format
    json_data = json.dumps(sorted_data, indent=2)

    # Print the JSON data
    return json_data

def data_to_json(data_string) :
    import json
    if data_string == "None" or not data_string:
        data_json = json.dumps([], indent=2)
        return data_json
    data_list = []
    print(data_string)
    if '],[' in str(data_string) :
        for item in data_string.split('],['):
            id, status = item.strip('[]').split(',')
            data_list.append({'id': int(id), 'status': status})
    elif ']' in data_string :
        id, status = str(data_string).replace('[', '').replace(']','').split(',')
        data_list.append({'id': int(id), 'status': status})


    # Now data_list contains the list of dictionaries with ID and Status
    data_json = json.dumps(data_list, indent=2)
    return data_json
def create_database_object () :
    object = database.Database(host, 3306, "grafana", "pwd123", "grafanadb")
    object.connect()
    return  object

@app.route('/process_locations', methods=['POST'])
def process_locations():
    item_locations = request.get_json()
    # Process the item locations as needed
    # Here, we simply print the item locations and return them as JSON response
    session['item_locations'] = item_locations
    object = create_database_object()
    update_process_location(item_locations,object)
    object.disconnect()

    return jsonify(item_locations)

def update_process_location (item_locations,object) :
    object.insert_positions_into_dashboard(item_locations,session['dashboard_id'],session.get('user_id'))

@app.route('/add-item', methods=['POST'])
def add_item():
    global sensor_counts
    object = database.Database(host, 3306, "grafana", "pwd123", "grafanadb")
    object.connect()
    user_id = session.get('user_id')
    dashboard_id = 0
    sensor_data = request.json
    cursor = object.connection.cursor()
    Error_Flag = False
    #{'type': 'motion_sensor', 'id': '98553', 'protocol': 'wifi'}
    print(sensor_data)
    typeOfSensor = 'sensors'
    # Perform the necessary actions to add the sensor to the database
    if sensor_data['type'] in ["switch","siren"] :
        typeOfSensor = "actuators"

    # Execute the SQL query to retrieve the ID of the first dashboard
    cursor.execute("SELECT id FROM dashboards WHERE user_id = %s LIMIT 1", (user_id,))
    result = cursor.fetchone()
    print(result)
    if result is not None:
        dashboard_id = result[0]
    else:
        print("No dashboard found for user ID:", user_id)
        object.connection.close()
        exit()

    print(type (dashboard_id))
    print(type (sensor_data['id']))

    if typeOfSensor == "sensors" :
    # insert data base sensor
        if not object.check_sensorid(sensor_data['id']) :
            if object.insert_new_sensor(sensor_data['id'],sensor_data['protocol'],sensor_data['type']) :
                Error_Flag = True
    # insert dashboard new sensor
        if object.insert_sensor_to_dashboard(dashboard_id,sensor_data['id']) :
            Error_Flag = True

    if typeOfSensor == "actuators" :
    # insert data base actuators
        if not object.check_actuatorid(sensor_data['id']):
            if object.insert_new_actuator(sensor_data['id'], sensor_data['protocol'], sensor_data['type']) :
                Error_Flag = True
    # insert dashboard actuators
        if object.insert_actuators_to_dashboard(dashboard_id, sensor_data['id']) :
            Error_Flag = True




    # Return a JSON response

    print(sensor_data['type'],sensor_data['id'])
    #print(session["sensor_counts"])

    object.disconnect()


    if Error_Flag == False :
        response = {'message': 'item added successfully'}

        sensor_counts = session["sensor_counts"]
        if sensor_data['type'] not in sensor_counts.keys():
            sensor_counts[sensor_data['type']] = []
        if int(sensor_data['id']) not in sensor_counts[sensor_data['type']] :
            sensor_counts[sensor_data['type']].append(int(sensor_data['id']))

        session['sensor_counts'] = sensor_counts

        return jsonify(response), 200
    else:
        response = {'message': 'item Failed to add '}
        return jsonify(response), 404

@app.route('/delete-item',methods =['POST'])
def delete_item () :
    item_data = request.json
    print(type(item_data))
    print(item_data)
    deleted_item_id , deleted_item_type = str (item_data['deletedItem']).split(',')
    object= create_database_object()

    if deleted_item_type == 'siren' or deleted_item_type == 'switch' :
        if deleted_item_type == 'switch' :
            deleted_item_type = ' relay_switch'
        status = object.delete_actuator(deleted_item_id,deleted_item_type)
    else:
        status = object.delete_sensor(deleted_item_id,deleted_item_type)

    if status :
        response = {'message': 'item not added '}
        return jsonify(response), 404
    else:
        response = {'message': 'item added '}
        return jsonify(response), 200

@app.before_request
def check_first_load():
    pass

def get_data_database ():
    global  sensor_counts
    object = create_database_object()
    sensor_counts = {key: [] for key in sensor_types}

    cursor = object.connection.cursor()
    check_query = "SELECT * FROM sensors"
    cursor.execute(check_query)
    result = cursor.fetchall()
    for row in result:
        if row[2] in sensor_types:
            sensor_counts[row[2]].append(row[0])
    check_query = "SELECT * FROM actuators"
    cursor.execute(check_query)
    result = cursor.fetchall()
    for row in result:
        if row[2] in sensor_types:
            sensor_counts[row[2]].append(row[0])
    cursor.close()
    object.connection.close()
    sensor_counts = {key: value for key, value in sensor_counts.items() if value}

    return sensor_counts

def get_data_From_dashboard(object):
    user_id = session.get('user_id') # Assuming user ID is 1, replace with the actual user ID retrieval logic
    sensor_counts = {key: [] for key in sensor_types}
    # Query to retrieve sensor and actuator data from the first dashboard
    result = object.get_sensors_by_user(user_id)
    # Format the results as a list of dictionaries
    data = [{'id': row[0], 'name': row[1]} for row in result]
    for row in data:
        if row['name'] != 'temp' :
            sensor_counts[row['name']].append(row['id'])
    sensor_counts = {key: value for key, value in sensor_counts.items() if value}
    print(sensor_counts)
    session["sensor_counts"] = sensor_counts
    return sensor_counts

def validate_credentials(username, password):
    object = create_database_object()

    cursor = object.connection.cursor()
    check_query = "SELECT id FROM users WHERE name = %s AND password = %s"
    cursor.execute(check_query, (username, password))
    result = cursor.fetchone()
    user_id = result[0] if result else None
    cursor.close()
    object.connection.close()

    return user_id

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate the username and password against the database
        # Check if the credentials are correct and exist in the database
        user_id = validate_credentials(username, password)
        if user_id:
            # Save the username in the session
            session['username'] = username
            session['user_id'] = user_id
            session['dashboard_id'] = 1
            session.permanent = True  # Enable permanent session
            #return redirect(url_for('index'))
            return index()
        else:
            error_message = "Invalid username or password"
    else:
        error_message = ""

    return render_template('login.html', error=error_message)

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))


def check_session_parameters() :
    # Access session in the WebSocket connection
    if 'first_load' not in session:  # Check if it's the first client connection
        session['first_load'] = False
    if 'user_id' not in session or 'dashboard_id' not in session:
        return redirect(url_for('login'))


    object = create_database_object()
    session['sensor_counts'] = get_data_From_dashboard(object)
    session['item_locations'] = get_items_locations(object)
    if not session['item_locations'] :
            counter = 0
            items = []
            for x in session['sensor_counts'].keys():
                for n in session['sensor_counts'][x]:
                    items.append({'itemId': n, 'partitionId': 'partition-' + str(counter), 'type': str(x)})
                    counter +=1
            session['item_locations'] = items
            update_process_location(session['item_locations'],object)

    session['count'] = len(session['item_locations'])


    max_partition = max(int(d['partitionId'].split('-')[1]) for d in session['item_locations'])
    sensor_counts = session['sensor_counts']
    item_locations = session['item_locations']
    list_of_ids = []
    list_of_typeids = []
    for dic in item_locations :
        list_of_ids.append(dic['itemId'])
        list_of_typeids.append(dic['type'])
    #and list_of_typeids[list_of_ids.index(id)] == type
    for type in sensor_counts.keys():
        for id in sensor_counts[type]:
            if id not in list_of_ids  :
                max_partition += 1
                session['item_locations'].append({'itemId': id, 'partitionId': 'partition-' + str(max_partition), 'type': str(type)})
                update_process_location(session['item_locations'],object)
                session['count'] +=1


    session['events_and_actions'] = object.get_events_and_action_by_user(session.get('user_id'))

    object.disconnect()

def get_items_locations (object) :
    result = object.get_positions(session.get('user_id'),session.get('dashboard_id'))
    result = sorted(result, key=lambda x: int(x['partitionId'].split('-')[1]))
    return result

@app.route('/')
def index():
    check_session_parameters()
    if 'username' not in session:
        return redirect(url_for('login'))
    count = session.get('count')
    partition_width  = 200
    partition_height = 200
    padding = 50
    numPerRow = 4
    numItems = ( count // numPerRow )+ 1
    len_items = count  # Replace with the actual number of items
    print(session['events_and_actions'] )
    door_event_data = []
    motion_event_data = []
    actions_data = []
    for i in range(len(session['events_and_actions'])) :
        door_event_data.append (data_to_json( (session['events_and_actions'][i] )[1]))
        motion_event_data.append(data_to_json((session['events_and_actions'][i])[2]) )
        actions_data.append(actions_to_json( (session['events_and_actions'][i])[4] ,(session['events_and_actions'][i])[5] , (session['events_and_actions'][i])[6] ) )
    '''
   for i in range(len(session['events_and_actions'])) :
        door_event_data.append(data_to_json( (session['events_and_actions'][i] )[1] )   )

    for i in range(len(session['events_and_actions'])):
        motion_event_data.append(data_to_json((session['events_and_actions'][i])[2]))

    for i in range(len(session['events_and_actions'])):
        actions_data.append(actions_to_json( (session['events_and_actions'][i])[4] ,(session['events_and_actions'][i])[5] , (session['events_and_actions'][i])[6]) )'''

    actions_data_parsed = [json.loads(action) for action in actions_data]
    door_data_parsed = [json.loads(door) for door in door_event_data]
    motion_data_parsed = [json.loads(motion) for motion in motion_event_data]
    print(actions_data_parsed)

    if 'username' in session:
        # User is already logged in, render the user page
        return render_template('index.html',actions_data= actions_data_parsed , door_event_data=door_data_parsed , motion_event_data=motion_data_parsed , data = session['events_and_actions'] , item_locations=session['item_locations'],len_items=len_items, num_items=numItems, items_flask=session['item_locations'], username=session['username'], partition_width=partition_width,partition_height=partition_height,padding=padding , num_per_row =numPerRow )
    else:
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))

@app.route('/data')
def data():
    return jsonify(sensor_data)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    try:
        mqtt.subscribe('#')
    except :
        print("aaaaaaaaaaaaaaaaaaaaaa")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    try:
        data = dict(
        topic=message.topic,
        payload=message.payload.decode()
        )
    #print(data)
        topic_parts = data['topic'].split('/')
        sensor_type = topic_parts[1]
        sensor_id = topic_parts[2]
        if sensor_type not in sensor_data:
            sensor_data[sensor_type] = {}
        sensor_data[sensor_type][sensor_id] = data['payload']
        socketio.emit(f'{sensor_type}_data', json.dumps(sensor_data[sensor_type]))
        insert_reading(sensor_type, sensor_id, data['payload'])
    except :
        print("error")

    #t = threading.Thread(target=insert_reading, args=(sensor_type, sensor_id, data['payload']))
    #t.start()

@socketio.on('actuator_command')
def handle_actuator_command(data):
    try:
        actuator_type = data['type']
        actuator_id = data['id']
        actuator_value = data['value']
        mqtt.publish(f'micropolis/{actuator_type}/{actuator_id}', actuator_value)
    except :
        print("error")

def do_action (action_id, object ) :
    actons = object.get_actions(action_id)
    list_of_actions = []
    for i in actons.keys() :
        for value in actons[i] :
            if i =='time' :
                sec , order = value
                list_of_actions.insert(order-1,(i , sec))
            else:
                id , status , order = value
                list_of_actions.insert(order-1 ,(i , id, status) )

    for tuple in list_of_actions :
        if tuple[0] == 'siren' or tuple[0] == 'switch' :
            data = { 'type' : tuple[0] , 'id' : tuple[1] , 'value' : tuple[2]}
            handle_actuator_command(data)
        else:
            time.sleep(int (tuple[1]) )

def do_action_thread(action_id):
    # Perform the necessary action
    try:
        do_action(action_id, create_database_object())
    except :
        pass
# Function to check for new rows periodically
def check_push_alerts():
    while True:
        try:
            object = create_database_object()
            rows = object.get_push_alert()
            if rows :
                for row in rows:
                    event_id, action_id = row
                    t = threading.Thread(target=do_action_thread, args=(action_id,))
                    t.start()
                    object.delete_push_alert(action_id)
            object.disconnect()
            time.sleep(1)

        except Exception as e:
            print("Error in push alerts:", e)
            object = create_database_object()






