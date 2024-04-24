from adafruit import *
from timer import *
import threading
import fsm
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
    "next-cycle": 1,
    "mixer1": 2,
    "mixer2": 2,
    "mixer3": 2,
    "selector": None,
    "pump-in": 2,
    "pump-out": 2,
    "active": 0,
}

sched_active = []

def data_callback(feed_id, payload):
    key = feed_id.replace("assignment.", "")
    if key in state:

        state[key] = payload
        print(f"Updated {key} to {state[key]}")
        
    else:
        print(f"No handler found for feed: {feed_id}")
        

adafruit_client = Adafruit_MQTT()
adafruit_client.setRecvCallBack(data_callback)

start_sched = fsm.FarmScheduler()

while True:
    # This is a placeholder for reading state updates, possibly from a serial or MQTT message
    # readSerial(mqtt_instance.client)
    print(state)
    if state["active"] == 1:
        sched_active.append(state.copy())
        print("Activated new schedule!")
        print(state)
        state["active"] = 0  # Reset the active flag


    for schedule in sched_active:
        start_sched.add_schedule(schedule)
        start_sched.run()
        sched_active.remove(schedule)

    time.sleep(1)
