import json
import sys
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
    # print(msg)
    payload = json.loads(msg.payload)
    print(payload)
    mqttc.publish("localization/observation/2", 'bye')

def on_subscribe(mqttc, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_publish(mqttc, obj, mid):
	print("server publish result: "+str(mid))


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect(SERVER_HOST, SERVER_PORT, KEEP_ALIVE)
mqttc.subscribe("localization/observation/1", 0)

mqttc.loop_forever()