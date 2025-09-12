#!/bin/python3

import sys
import time
from datetime import datetime
import json
import paho.mqtt.client as mqtt
from pathlib import Path
import os
import config as cfg
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo

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

log_write("Started...")

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(
    host=cfg.broker,
    port=1883,
    client_id=cfg.unique_id
)

# Information about the status entity
sensor_info = BinarySensorInfo(
    name="PC state",
    unique_id=cfg.unique_id,
    device_class="connectivity",
    expire_after=cfg.period * 2,
    device={
        "identifiers": [cfg.unique_id + "_device"],
        "manufacturer": "Spas Tech",
        "model": "Heartbeat v1",
        "name": cfg.name
    },
)

settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

# Create the switch entity
pc_status = BinarySensor(settings)
pc_status.on()  # Set initial state to ON

while True:
    try:
        pc_status.on()  # Update the state to ON
    except Exception as error:
        log_write(str(error))

    try:
        time.sleep(cfg.period)
    except KeyboardInterrupt:
        pc_status.off()
        log_write("Stopped by user")
        sys.exit(0)

