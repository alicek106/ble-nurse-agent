# Dependencies Import

import blescan
import sys
import time
import datetime
import json
import bluetooth._bluetooth as bluez
from collections import OrderedDict
import paho.mqtt.client as mqtt


# Global value initialize
MQTT_SERVER = sys.argv[1]
DEVICE_NAME = sys.argv[2]
SLEEP_TIME = float(sys.argv[3])

# BLE Initialize

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print "ble thread started"

except:
    print "error accessing bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

# MQTT Initialize
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print("Connected to  %s" % MQTT_SERVER)
# The callback for when a PUBLISH message is received from the server.

client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_SERVER, 1883, 60)




# Distance Calculate Function from Rssi strength

def calcDistance(txPower, rssi):
    if(rssi == 0):
        return -1.0
    try:
        ratio = float(rssi) / float(txPower)
    except ZeroDivisionError:
        ratio = 0
    if(ratio < 1.0):
        return pow(ratio, 10)
    else:
        accuracy = (0.89976)*pow(ratio, 7.7095) + 0.111
        return accuracy



# Start collecting beacon sensor data

while True:
    time.sleep(SLEEP_TIME)
    returnedList = blescan.parse_events(sock, 5)

    arr = []
    for beacon in returnedList:
        blelist = beacon.split(",")

        data = OrderedDict()
        now = time.time()
        timestamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
        distance = calcDistance(blelist[4], blelist[5])

        data["time"] = timestamp
        data["distance"] = str(distance)
        data["mac"] = blelist[0]
        data["id"] = blelist[1]
        data["major"] = blelist[2]
        data["minor"] = blelist[3]
        data["power"] = blelist[4]
        data["rssi"] = blelist[5]
        data["uid"] = blelist[0][0] + blelist[0][1] + blelist[0][3] + blelist[0][4]
        # For example, fac4, 1dac ...
        arr.append(data)
    client.publish("ble/" + DEVICE_NAME, json.dumps([pn for pn in arr]))
