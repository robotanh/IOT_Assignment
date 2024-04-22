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
sched = {
    "assignment.nextcycle": nextcycle,
    "assignment.mixer1": mixer1,
    "assignment.mixer2": mixer2,
    "assignment.mixer3": mixer3,
    "assignment.area": area,
    "assignment.pumpin": pumpin,
    "assignment.pumpout": pumpout,
    "assignment.active": active,


}
sched_active = {}

def data_callback(feed_id, payload):
    print(f"Received data from {feed_id}: {payload}")
    if feed_id in sched:
        # Append the payload to the corresponding list
        sched[feed_id] = payload
        if sched["assignment.active"] == True:
            sched_active = sched
            sched["assignment.active"] = False
    else:
        print("No handler found for feed:", feed_id)

adafruit_client = Adafruit_MQTT()
adafruit_client.setRecvCallBack(data_callback)

while True:
	# readSerial(mqtt_instance.client)
    print(sched)
    time.sleep(5)
