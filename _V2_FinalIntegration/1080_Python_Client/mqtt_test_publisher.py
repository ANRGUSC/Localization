import sys
import json
sys.path.append('/usr/local/lib/python3.7/dist-packages')
import paho.mqtt.client as mqtt


# import server address, server port and keep alive from conf.py
SERVER_HOST = 'eclipse.usc.edu'
SERVER_PORT = 3883
KEEP_ALIVE = 180


def on_connect(mqttc, obj, flags, rc):
	print("connected! rc = "+str(rc))

def on_message(mqttc, obj, msg):
	# parse the payload to get observation vector, channel number and alg
    # payload = json.loads(msg.payload)
    print(msg.payload)

def on_subscribe(mqttc, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_publish(mqttc, obj, mid):
	print("server publish result: "+str(mid))


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

payload = {'observation': [-120.40999999999991, -126.28899999999972, -125.26200000000017], 'Tx': [1, 2, 3], 'Ty': [5, 5, 5], 'timestamp': [1563815078.0], 'msg_id': 1, 'real_pos': (1, 5), 'ALG': 'MESE', 'channel': 'one'}

mqttc.connect(SERVER_HOST, SERVER_PORT, KEEP_ALIVE)
mqttc.publish("localization/observation/1", json.dumps(payload))
mqttc.subscribe("localization/observation/2", 0)

mqttc.loop_forever()