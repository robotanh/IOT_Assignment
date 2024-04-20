from adafruit import *
import time
import random
import json

mixer1 = []
mixer2 = []
sched = {
    "cambien1": mixer1,
    "cambien2": mixer2,
}

def data_callback(feed_id, payload):
    print(f"Received data from {feed_id}: {payload}")
    if feed_id in sched:
        # Append the payload to the corresponding list
        sched[feed_id].append(payload)
    else:
        print("No handler found for feed:", feed_id)

adafruit_client = Adafruit_MQTT()
adafruit_client.setRecvCallBack(data_callback)

while True:
	# readSerial(mqtt_instance.client)
    print(sched)
    time.sleep(5)
