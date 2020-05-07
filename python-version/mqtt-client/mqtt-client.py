#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# qos is a parameter available on each publish call. It is one of three levels:
# 0 – at most once. This means that the system will make a best effort to deliver the message, 
# 1 – at least once. This means that the system will use storage and handshaking to ensure that the message is delivered. 
# However, in doing so it may send the same message multiple times, resulting in duplicates.
# This example shows how you can use the MQTT client in a class.
import argparse
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime
import sensor
import sys
sys.path.insert(0, '../common')
import conf

SERVER_HOST = conf.host
SERVER_PORT = conf.port
KEEP_ALIVE = conf.keep_alive
RETRY_LIMIT = conf.RETRY_LIMIT

def on_connect(mqttc, obj, flags, rc):
    print("Connected to %s:%s" % (mqttc._host, mqttc._port))

def on_publish(mqttc, obj, mid):
    print("client publish obs: "+str(mid))

def on_log(mqttc, obj, level, string):
    print(string)

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_log = on_log

def mqttClient(ALG):
    rc = mqttc.connect(SERVER_HOST, SERVER_PORT, KEEP_ALIVE)
    msg_id = 0
    while rc == 0:
        # r, obs = sensor.read_static()
        channel = "one"
	# r, obs = sensor.read_btmgmt(msg_id)
        # r, obs = sensor.read_dynamic(msg_id)
        r, obs, Tx, Ty = sensor.read_cell_measurement(msg_id)
        msg_id = msg_id+1
        timestamp = []
        # convert to seconds
        timestamp.append(time.mktime(datetime.now().timetuple()))
        payload = {}
        payload['real_pos'] = r
        payload['msg_id'] = msg_id
        payload['observation'] = obs
        payload['Tx'] = Tx
        payload['Ty'] = Ty
        payload['channel'] = channel
        payload['timestamp'] = timestamp
        payload['ALG'] = ALG
	print payload
        mqttc.publish("localization/observation", json.dumps(payload), qos=0)
        time.sleep(45)
    mqttc.disconnect()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ALG')
    args = parser.parse_args()
    mqttClient(args.ALG)

if __name__ == '__main__':
    main()
