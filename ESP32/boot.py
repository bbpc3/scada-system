# Complete project details at https://RandomNerdTutorials.com

import gc
import os
import sys
import time

import esp
import interval
import machine
import micropython
import network
import ubinascii
from mqtt import MQTTClient

gc.collect()
ssid = 'FRITZ!Box 5590 KY'
password = 'shalAcficip7'
mqtt_server = 'raspberrypi'
client_id = 'ESP8266WP'


# EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'

base_topic = b'/home/wp'
interval_topic = base_topic + b'/interval'
state_topic = base_topic + b'/state'

last_message = 0
message_interval = interval.readInterval()
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

wifi_counter = 0

while station.isconnected() == False:
    counter += 1
    if counter > 20:
        machine.reset()
    time.sleep(1)
    pass

print('Connection successful')
print(station.ifconfig())

