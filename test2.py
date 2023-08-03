
import json
from test import  *

actions_str = ('[33,off,3],[33,on,1]', None, '[10,2]')






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
        list_of_Actions.append([ int(t[1]) ,'time', t[0]+ ' sec' ,None ])


    actions_dict = {item[0]: {"type": item[1], "id": item[3], "status": item[2]} for item in list_of_Actions}

    # Sort the dictionary by keys (the order)
    sorted_actions = sorted(actions_dict.items())

    # Convert the sorted dictionary back to a list of dictionaries
    sorted_data = [{"order": order, **values} for order, values in sorted_actions]

    # Convert the sorted data to JSON format
    json_data = json.dumps(sorted_data, indent=2)

    # Print the JSON data
    return json_data




print( actions_to_json(actions_str[0],actions_str[1],actions_str[2]) )

Events = [
         {'type': 'motion_sensor', 'id': '6', 'status': 'motion_detected'},
         {'type': 'door_sensor', 'id': '2298', 'status': 'opened'},
         {'type': 'door_sensor', 'id': '9987', 'status': 'closed'}
         ]

Actions = [
    {'type': 'siren', 'id': '9', 'status': 'on', 'delay': ''}
    ,{'type': 'delay', 'id': None, 'status': '', 'delay': '5'},
    {'type': 'siren', 'id': '9', 'status': 'off', 'delay': ''}
]


for dic in Events :
    if dic['type'] == 'motion_sensor' :
        object.insert_door_event(event_id,dic['id'],dic['status'])
    elif dic['type'] == 'door_sensor' :
        object.insert_motion_event(event_id , dic['id'],dic['status'] )

for index , dic in enumerate(Actions) :
    if dic['type'] == 'siren' :
        object.insert_action_siren(index ,action_id,dic['id'],dic['status'])
    elif dic['type'] == 'switch' :
        object.insert_action_switch(index, action_id , dic['id'],dic['status'] )
    elif dic['type'] == 'delay' :
        object.insert_action_switch(index, action_id , dic['delay'] )
