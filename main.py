from adafruit import *
import time
import random
import json


def received_feed(feed_id, payload):
    data_dict = json.loads(payload)
    print(data_dict)

mqtt_instance = Adafruit_MQTT()
mqtt_instance.setRecvCallBack(received_feed)

while True:
	# readSerial(mqtt_instance.client)
	time.sleep(2)
