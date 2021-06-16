# MQTT heartbeat script

The point of this script is to send status every previously defined period. 
It is used it for state indication of PC on local Home Assistant setup, but 
it can be used for anything.

## Installation

First open *config.json* setup your broker address, your PC name, name of
 your log file and notification period. 

After that you should edit your current user's cron entries and add 
*heartbeat* cron job to start *mqtt_heartbeat.py* script on every boot.

```
crontab -e
// add "@reboot cd /full/path/to/repo/ && ./mqtt_heartbeat.py"
```