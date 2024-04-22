from adafruit import *
import time
import random
import json

mixer1 = None
mixer2 = None
mixer3 = None
nextcycle = None
area = None
pumpin = None
pumpout = None
active = False

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
    "nextcycle": None,
    "mixer1": None,
    "mixer2": None,
    "mixer3": None,
    "area": None,
    "pumpin": None,
    "pumpout": None,
    "active": False,
}

sched_active = {}

def data_callback(feed_id, payload):
    key = feed_id.replace("assignment.", "")
    if key in state:

        state[key] = payload
        print(f"Updated {key} to {state[key]}")
        
        # Activate or deactivate schedule
        if key == "active" and state[key] is True:
            global sched_active
            sched_active = state.copy()
            state["active"] = False
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
