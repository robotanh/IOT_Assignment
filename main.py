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
    "mixer2": 4,
    "mixer3": 3,
    "selector": None,
    "pump-in": 2,
    "pump-out": 3,
    "active": 0,
}

sched_active = {}

def data_callback(feed_id, payload):
    key = feed_id.replace("assignment.", "")
    if key in state:

        state[key] = payload
        print(f"Updated {key} to {state[key]}")
        
        # # Activate or deactivate schedule
        # if key == "active" and state[key] == 1:
        #     global sched_active
        #     sched_active = state.copy()
        #     state["active"] = 0
        #     print("Activated new schedule!")
    else:
        print(f"No handler found for feed: {feed_id}")
        
# def run_timers():
#     while True:
#         timerRun()
#         time.sleep(1)  # Run timer every second
    
# timer_thread = threading.Thread(target=run_timers)
# timer_thread.start()

adafruit_client = Adafruit_MQTT()
adafruit_client.setRecvCallBack(data_callback)

start_sched = fsm.FarmScheduler()
# data = '{"mixer1": 3, "mixer2": 3, "mixer3": 3, "pump-in": 3, "pump-out": 3,  "next-cycle"=1,"active"=1}'
while True:
	# readSerial(mqtt_instance.client)
    print(state)
    if state["active"] == 1:
      sched_active = state.copy()
      start_sched.add_schedule(sched_active)
      start_sched.run()
      state["active"] = 0
      print("Activated new schedule!")
      print(sched_active)
    time.sleep(1)
