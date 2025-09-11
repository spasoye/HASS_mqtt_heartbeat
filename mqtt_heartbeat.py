#!/bin/python3

import sys
import time
from datetime import datetime
import json
import paho.mqtt.client as mqtt
from pathlib import Path
import os
import config as cfg
import ha_mqtt_discoverable as had

def log_write(text):
    log = open(cfg.log_file, "a")
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y [%H:%M:%S]")
    log.write(current_time + " > " + text + "\n")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    print(f"user {userdata}")
    print(f"flags {flags}")

    if reason_code == 0:
        client.connected_flag = True
        log_write('Connection OK, result:' + str(reason_code))
        print('Connection OK, result:', str(reason_code))
    else:
        log_write('Bad connection, result:' + str(reason_code))
        print('Bad connection, result:', str(reason_code))

def on_socket_open(client, userdata, sock):
    print("socket opened")

def on_socket_close(client, userdata, sock):
    print("socket close")

def on_disconnect(client, userdata, rc):
    print("disconnect")
    log_write("disconnect")

try:
    print("log file size: ", Path(cfg.log_file).stat().st_size)
except:
    print("No log file")
else:
    if Path(cfg.log_file).stat().st_size > 8192:
        print("log file to big. Deleting log file")
        os.remove(cfg.log_file)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connected_flag = False
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_socket_close = on_socket_close
client.on_socket_open = on_socket_open

log_write("Started...")

while True:
    try:
        client.connect(cfg.broker, 1883, 5)
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
        client.publish(cfg.name + "/status",  "ON")
    except Exception as error:
        log_write(error)

    time.sleep(cfg.period)
