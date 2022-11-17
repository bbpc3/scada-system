import json
import logging
import socket
import subprocess
import time

import config
import datadecoder
import interval
import log
import paho.mqtt.client as mqtt
import sshclient
from encoder import NpEncoder
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

logger = log.get_module_logger("mainmodule")
# SETUP
client = mqtt.Client(client_id="solarclient",
                         transport=config.transport,
                         protocol=mqtt.MQTTv5
                         )
client.username_pw_set("admin", "scada!123")

properties=Properties(PacketTypes.CONNECT)
properties.SessionExpiryInterval=30*60 # in seconds
client.connect(config.broker,
                port=config.myport,
                clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                properties=properties,
                keepalive=60)


client.loop_start()

logger.info("loop starting")

# Main Loop
while True:
    if not client.is_connected:
        result = client.reconnect()
    
    data = sshclient.getData()
    if data is not None:
        decoded = datadecoder.decode(data)
        payload = json.dumps(decoded, cls=NpEncoder).encode("utf-8")
        client.publish(config.dataTopic, payload)
        logger.info("Data published successfully")
    time.sleep(interval.readInterval())

logger.info("loop stopped")


# Cleanup
client.disconnect()
client.loop_stop()
