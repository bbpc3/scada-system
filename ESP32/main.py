# Complete project details at https://RandomNerdTutorials.com
import json

import decoder
import interval
from machine import UART, Pin

cts = 17
rts = 16
rx = 0
tx = 15

# ,cts=cts, rts=rts, flow=UART.CTS | UART.RTS
#u = UART(1, baudrate=9600, rts=rts, cts=cts, flow=UART.RTS | UART.CTS)
u = UART(1, baudrate=9600)

u.init(rx=rx, tx=tx)

       

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == interval_topic:
        print('ESP new Interval command')
        try:
            global message_interval
            newInterval = float(msg)
            newInterval = int(newInterval)
            if newInterval < 1:
                print('Interval needs to be greater than 0')
            else:
                message_interval = newInterval
                interval.storeInterval(message_interval)
        except: 
            print('Error parsing interval')



def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub, interval_topic
    client = MQTTClient(client_id, mqtt_server, user="admin", password="scada!123")
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(interval_topic, qos=2)
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (mqtt_server, interval_topic))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

def update(client):
    global state_topic
    if u.any():
        data = u.read()
        decoded = decoder.decode(data)
        print(decoded)
        client.publish(state_topic, json.dumps(decoded).encode("ascii"))
        print("Published update...")
        


try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            update(client)
            last_message = time.time()
    except OSError as e:
        print(e)
        restart_and_reconnect()
