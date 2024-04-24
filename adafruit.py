import serial.tools.list_ports

import sys

import time

import random
import json
from Adafruit_IO import MQTTClient

#from simple_ai import image_detector

#from port import *

from rs485 import *

#from adafruit import *

class Adafruit_MQTT:
    # AIO_FEED_IDs = ["cambien1", "cambien2"]
    # AIO_USERNAME = "robotanh"
    # AIO_KEY = ""
    AIO_FEED_IDs = [
                        "assignment.mixer1", 
                        "assignment.mixer2", 
                        "assignment.mixer3",
                        "assignment.next-cycle",
                        "assignment.selector", 
                        "assignment.pump-in", 
                        "assignment.pump-out",
                        "assignment.active"
                    ]
    AIO_USERNAME = "huytran1305"
    AIO_KEY = ""
    recvCallBack = None

    def connected(self, client):
        print("Connected ...")
        for feed in self.AIO_FEED_IDs:
            client.subscribe(feed)

    def subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed...")

    def disconnected(self, client):
        print("Disconnected... Trying to reconnect.")
        self.client.reconnect()

    def message(self, client, feed_id, payload):
        try:
            # Assuming payload is a JSON string, parse it
            data = json.loads(payload)
            if self.recvCallBack:
                self.recvCallBack(feed_id, data)
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from payload: {payload}")

    def setRecvCallBack(self, func):
        self.recvCallBack = func

    def __init__(self):
        self.client = MQTTClient(self.AIO_USERNAME, self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()






# Create an instance of Adafruit_MQTT

# mqtt_instance = Adafruit_MQTT()


# while True:
# 	# readSerial(mqtt_instance.client)
# 	time.sleep(2)

