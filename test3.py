from app.module.controller import *
import random

object = create_database_object()
#object.insert_trigger('111', '222')
end_time = datetime.datetime.now()
start_time = end_time - timedelta(hours=24)
print(object.get_actuator_data_by_time("relay_switch",'33',start_time,end_time))