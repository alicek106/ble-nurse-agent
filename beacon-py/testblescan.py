# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys

import time
import datetime

import json
import pymongo

import bluetooth._bluetooth as bluez

dbparam = sys.argv[1]
dbaddr = "mongodb://" + dbparam +"/"
print "connect to " + dbaddr + "..."

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

connection = pymongo.MongoClient(dbaddr)
dbname = sys.argv[2]
db = connection[dbname]
print "DB Connection Successful"

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

while True:
	time.sleep(3)
	returnedList = blescan.parse_events(sock, 5)
	for beacon in returnedList:
		blelist = beacon.split(",")
		
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		print st

		distance = calcDistance(blelist[4], blelist[5])

		blestr = "{\"time\":\""
		blestr += st
		blestr += "\""

		blestr += ", \"distance\":\""
                blestr += str(distance)
                blestr += "\""

		blestr += ", \"mac\":\""
		blestr += blelist[0]
		blestr += "\""
	
		blestr += ", \"id\":\""
		blestr += blelist[1]
		blestr += "\""

		blestr += ", \"major\":"
		blestr += blelist[2]

		blestr += ", \"minor\":"
		blestr += blelist[3]

		blestr += ", \"power\":"
		blestr += blelist[4]

		blestr += ", \"rssi\":"
		blestr += blelist[5]

		blestr += "}"

		coll = blelist[0][0] + blelist[0][1] + blelist[0][3] + blelist[0][4]
		collection = db[coll]

		blejson = json.loads(blestr)

		collection.insert(blejson)
		
		print blestr
