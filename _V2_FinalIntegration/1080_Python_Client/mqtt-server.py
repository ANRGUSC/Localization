import json
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
import random
import sys
sys.path.append('/usr/local/lib/python3.7/dist-packages')
import paho.mqtt.client as mqtt

# import server address, server port and keep alive from conf.py
SERVER_HOST = 'eclipse.usc.edu'
SERVER_PORT = 3883
KEEP_ALIVE = 180


# Procedure to initialize the GPU Engine client
PassTests = 0
FailedTests = 0
TotalTests = 0
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
def clientInit():
	# Nvidia IP -> 192.168.1.162 else connect to localHost in other modes
	IP_address = str('192.168.1.157') 
	Port = int('8190') 
	server.connect((IP_address, Port))

def serverInit():
	subprocess.Popen(["./server", "8194"])

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
					return message.split("$35V35 OUTPUT: OK; ")[1]
			else: 
				sys.stdout.flush()


# When the client receives a CONNACK message from the broker
# in response to the connect it generates an on_connect() callback.
def on_connect(mqttc, obj, flags, rc):
	print("connected! rc = "+str(rc))


def estimate_function(sendPayLoadData):

    print ("estimate start at GPU Engine") # debug info
    stime = time.time()

    result = blockSendToServer(sendPayLoadData)
    
    print(str(result)) # debug info
    print("time elapsed from GPU Engine: " + str(time.time() - stime))
    return str(result)


# When the mqtt client receives a message
def on_message(mqttc, obj, msg):
	# parse the payload to get observation vector, channel number and alg
	print ("estimate start on Msg Recieve") # debug info
	sendPayLoadData = {}
	payload = json.loads(msg.payload)
	print ("Payload Data: ", msg.payload.decode())
	channel = payload['channel']
	sendPayLoadData['observation'] = payload['observation']
	sendPayLoadData['alg'] = payload['ALG']
	sendPayLoadData['Tx'] = payload['Tx']
	sendPayLoadData['Ty'] = payload['Ty']
	stime = time.time()

	message = {}
	message['real_pos'] = payload['real_pos']
	message['msg_id'] = payload['msg_id']
	message['channel'] = channel
	# error handling
	if len(payload['observation']) is 3:
		# Calling the GPU engine
		result = estimate_function(sendPayLoadData)
		
		# Parsing the result
		result = result.rstrip('\x00')
		resultVec = []
		resultVec.append(int(result.split(',')[0].split('[')[1]))
		resultVec.append(int(result.split(',')[1].split(']')[0]))
		message['coordinate'] = resultVec
	
	else:
		return

	print("time elapsed Ready to publish: " + str(time.time() - stime))
	# publish the result coordinate

	# add timestamp when server is ready to publish
	timestamp = payload['timestamp']
	mid = time.mktime(datetime.datetime.now().timetuple())
	timestamp.append(mid.__str__())
	message['timestamp'] = timestamp
	mqttc.publish("localization/result/two", json.dumps(message), qos=0)

def on_publish(mqttc, obj, mid):
	print("server publish result: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))


# Enable this line if the GPU server is also present in
# the same machine. else assume that the server is already started
# serverInit()

clientInit()
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect(SERVER_HOST, SERVER_PORT, KEEP_ALIVE)
mqttc.subscribe("localization/observation/1", 0)

mqttc.loop_forever()