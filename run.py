import threading

from app import app,socketio,check_push_alerts


#app.run(debug=True, host='127.0.0.1', port=2000)


try:
    t = threading.Thread(target=check_push_alerts)
    t.start()
except :
    print("error in alarms")

socketio.run(app, debug=True, host='0.0.0.0', port=5555,allow_unsafe_werkzeug=True)