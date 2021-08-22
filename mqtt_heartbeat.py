#!/bin/python3

import sys
import time
from datetime import datetime
import json
import paho.mqtt.client as mqtt
from pathlib import Path
import os

def log_write(text):
    global log_file
    log = open(log_file, "a")
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y [%H:%M:%S]")
    log.write(current_time + " > " + text + "\n")

def on_connect(client, userdata, flags, rc):
    print("user:", userdata)
    print("flags:", flags)
    if rc == 0:
        client.connected_flag = True
        log_write('Connection OK, result:' + str(rc))
        print('Connection OK, result:', str(rc))
    else:
        log_write('Bad connection, result:' + str(rc))
        print('Bad connection, result:', str(rc))

def on_socket_open(client, userdata, sock):
    print("socket opened")

def on_socket_close(client, userdata, sock):
    print("socket close")

def on_disconnect(client, userdata, rc):
    print("disconnect")
    log_write("disconnect")

if len(sys.argv) != 2:
    print("Must provide cfg file absolute path")
    sys.exit()

# import configuration
cfg_file = open(sys.argv[1], "r")
cfg_str = cfg_file.read()
cfg_file.close()
cfg_json = json.loads(cfg_str)

log_file = cfg_json["log_file"]

print("log file size: ", Path(log_file).stat().st_size)
if Path(log_file).stat().st_size > 8192:
    print("log file to big. Deleting log file")
    os.remove(log_file)

name = cfg_json["name"]
broker = cfg_json["broker"]
period = cfg_json["period"]

client = mqtt.Client()
client.connected_flag = False
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_socket_close = on_socket_close
client.on_socket_open = on_socket_open

log_write("Started...")

while True:
    try:
        client.connect(broker, 1883, 5)
    except Exception as ex:
        print(ex)
        log_write(str(ex))
        time.sleep(3)
    else:
        log_write("Connected to broker")
        break

client.loop_start()

while True:
    try:
        client.publish(name + "/status",  "ON")
    except Exception as error:
        log_write(error)

    time.sleep(period)
