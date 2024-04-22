from adafruit import *
import time
import random
import json


"""
    [
  {
    "cycle": 5,
    "flow1": 20,
    "flow2": 10,
    "flow3": 20,
    "isActive": true,
    "schedulerName": "LỊCH TƯỚI 1",
    "startTime": "18:30",
    "stopTime": "18:40"
  }
]

"""
state = {
    "cycle": None,
    "mixer1": None,
    "mixer2": None,
    "mixer3": None,
    "selector": None,
    "pump-in": False,
    "pump-out": False,
    "active": False,
}

sched_active = {}

def data_callback(feed_id, payload):
    key = feed_id.replace("assignment.", "")
    if key in state:

        state[key] = payload
        print(f"Updated {key} to {state[key]}")
        
        # Activate or deactivate schedule
        if key == "active" and state[key] == 1:
            global sched_active
            sched_active = state.copy()
            state["active"] = 0
            print("Activated new schedule!")
    else:
        print(f"No handler found for feed: {feed_id}")

adafruit_client = Adafruit_MQTT()
adafruit_client.setRecvCallBack(data_callback)

while True:
	# readSerial(mqtt_instance.client)
    print(state)
    print (sched_active)
    time.sleep(5)
