import json
#import paho.mqtt.client as mqtt
# import estimate
import datetime
import time
import sys
sys.path.insert(0, '../common')
# import conf
import socket 
import select 
import sys 
import os
import subprocess

# import server address, server port and keep alive from conf.py
# SERVER_HOST = conf.host
# SERVER_PORT = conf.port
# KEEP_ALIVE = conf.keep_alive


# Procedure to initialize the GPU Engine client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
def clientInit():
	IP_address = str('127.0.0.1') 
	Port = int('8192') 
	server.connect((IP_address, Port))

def serverInit():
	subprocess.Popen(["./server", "8192"])

# Procedure to block send to Server

def blockSendToServer(payload): 

	payload['authentication'] =  "(l!=N| REQ: "
	message = str(payload) 
	server.send(message.encode())
	# maintains a list of possible input streams
	while True: 
		sockets_list = [sys.stdin, server] 
		read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
		for socks in read_sockets: 
			if socks == server: 
				message = socks.recv(2048)
				message = message.decode("ascii", "backslashreplace") 
				if "$35V35 OUTPUT: OK; " in message:
					return message
			else: 
				sys.stdout.flush()


# When the client receives a CONNACK message from the broker
# in response to the connect it generates an on_connect() callback.
def on_connect(mqttc, obj, flags, rc):
	print("connected! rc = "+str(rc))


def estimate_function():
    payload={'observation': [-120.40999999999991, -126.28899999999972, -125.26200000000017], 'Tx': [1, 2, 3], 'Ty': [5, 5, 5], 'timestamp': [1563815078.0], 'msg_id': 1, 'real_pos': (1, 5), 'ALG': 'MESE', 'channel': 'one'}
    #payload = json.loads(payload)
    channel = payload['channel']
    obs = payload['observation']
    alg = payload['ALG']
    Tx = payload['Tx']
    Ty = payload['Ty']
    # print ("estimate start") # debug info
    stime = time.time()

    result = blockSendToServer(payload)
    
    print(result) # debug info
    # print("time elapsed: " + str(time.time() - stime))
    # print(str(time.time() - stime))


# When the mqtt client receives a message
def on_message(mqttc, obj, msg):
	# parse the payload to get observation vector, channel number and alg
	payload = json.loads(msg.payload)
	channel = payload['channel']
	obs = payload['observation']
	alg = payload['ALG']
	Tx = payload['Tx']
	Ty = payload['Ty']
	print ("estimate start") # debug info
	stime = time.time()
	result = estimate.estimate(obs, alg, Tx, Ty)
	print(list(result)) # debug info
	print("time elapsed: " + str(time.time() - stime))
	# publish the result coordinate
	message = {}
	message['real_pos'] = payload['real_pos']
	message['msg_id'] = payload['msg_id']
	message['channel'] = channel
	message['coordinate'] = result
	# add timestamp when server is ready to publish
	timestamp = payload['timestamp']
	mid = time.mktime(datetime.datetime.now().timetuple())
	timestamp.append(mid.__str__())
	message['timestamp'] = timestamp
	mqttc.publish("localization/result/"+channel, json.dumps(message), qos=0)

def on_publish(mqttc, obj, mid):
	print("server publish result: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))


#mqttc = mqtt.Client()
#mqttc.on_connect = on_connect
#mqttc.on_message = on_message
#mqttc.on_publish = on_publish
#mqttc.on_subscribe = on_subscribe

#mqttc.connect(SERVER_HOST, SERVER_PORT, KEEP_ALIVE)
#mqttc.subscribe("localization/observation/#", 0)

#mqttc.loop_forever()

serverInit()
time.sleep(0.002)
clientInit()

count = 1
for _ in range(50):
	print ("##################Test #", count, "##################\n")
	estimate_function()
	print ("##################End of Test########################\n")
	count = count + 1

# estimate_function()
server.close()
