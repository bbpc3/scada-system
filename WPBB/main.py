import json
import sys
import time

import config
import decoder
import log
import paho.mqtt.client as mqtt
import serial
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

logger = log.get_module_logger(__name__)

#import RPi.GPIO as GPIO
failbuffer = json.loads('{"E01": 0, "A01": 0, "E02": 0, "A02": 0, "E03": 0, "A03": 0, "E04": 0, "A04": 0, "E05": 0, "A05": 0, "E06": 0, "A06": 0, "E07": 0, "A07": 0, "E08": 0, "A08": 0, "E09": 0, "A09": 0, "E10": 0, "A10": 0, "E11": 0, "A11": 0, "A12": 0, "A13": 0, "A14": 0, "A15": 0, "A16": 0}')
lastrun = time.time()
#GPIO.cleanup()
#GPIO.setmode(GPIO.BCM)

#GPIO.setup(3, GPIO.OUT)

#GPIO.output(3, GPIO.HIGH)

#print( GPIO.gpio_function(3))

#ser = serial.Serial("/dev/ttyS0", 9600, 8, "N", 1, timeout=None) #, rtscts=True)
#ser = serial.Serial("/dev/ttyAMA1", 9600, rtscts=True)

client = mqtt.Client(client_id="wpClient",
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

ser = serial.Serial(
        port="/dev/ttyAMA1", #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        timeout=None, 
        rtscts=False
)

def getdata(command : bytes):
    #logger.debug("Getting data...")
    temp = b""
    ser.read_all()
    ser.write(command + b"\r\n")
    time.sleep(0.1)
    while ser.in_waiting > 0:
        data = ser.read_all()
        if b"\f" in data:
            logger.warn("Fail!! Sending A...")
            return None
        temp += data
        time.sleep(0.1)
    return temp

while True:
        # try:
    ser.read_all()
    buf = b""
    buf1 = getdata(b"M")
    time.sleep(1)
    buf2 = getdata(b"O")
    time.sleep(1)
    buf3 = getdata(b"I")
    time.sleep(1)
    
    if buf1 != None and buf2 != None and buf3 != None:
        buf = buf1 + buf2 + buf3
        try:
            decoded = decoder.decode(decoder.getSection(buf))
            if decoded == failbuffer:
                logger.warn("Failbuffer...skipping")
                continue
            payload = json.dumps(decoded, indent=2)
            client.publish(config.dataTopic, payload.encode())
            client.publish(config.debugTopic, buf)
            #logger.info(f"Successfully published payload...")
        except:
            pass
    else:
        ser.write(b"A\r\n")
        
    time.sleep(10)

    
        