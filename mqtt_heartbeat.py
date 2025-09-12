#!/bin/python3

import sys
import time
from datetime import datetime
import json
import paho.mqtt.client as mqtt
from pathlib import Path
import os
import config as cfg

# Research Home Assistant MQTT Discovery (https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery) before using this code

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo

print("Heartbeat started...")

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(
    host=cfg.broker.host,
    port=cfg.broker.port,
    client_name=cfg.unique_id
)

print("MQTT settings:", mqtt_settings)

# Information about the status entity
sensor_info = BinarySensorInfo(
    name="PC state",
    unique_id=cfg.unique_id,
    device_class="connectivity",
    expire_after=cfg.period * 2,
    device={
        "identifiers": [cfg.unique_id + "_device"],
        "manufacturer": cfg.manufacturer,
        "model": cfg.model,
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
        print(str(error))

    try:
        time.sleep(cfg.period)
    except KeyboardInterrupt:
        pc_status.off()
        pc_status.mqtt_client.publish("availability", "offline")
        print("Stopped by user")
        sys.exit(0)

