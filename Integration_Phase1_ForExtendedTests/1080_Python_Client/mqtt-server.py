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
import random

# import server address, server port and keep alive from conf.py
# SERVER_HOST = conf.host
# SERVER_PORT = conf.port
# KEEP_ALIVE = conf.keep_alive


# Procedure to initialize the GPU Engine client
PassTests = 0
FailedTests = 0
TotalTests = 0
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
def clientInit():
	# Nvidia IP -> 192.168.1.162 else connect to localHost in other modes
	IP_address = str('68.181.32.115') 
	Port = int('8190') 
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

    global PassTests
    global FailedTests

	# Test Vectors
    test_vectors = ['0,28', '0,29', '0,29', '0,28']
    payload = []
    #Test1  # Output : 0, 28
    payload.append({'observation': [-120.40999999999991, -126.28899999999972, -125.26200000000017], 'Tx': [1, 2, 3], 'Ty': [5, 5, 5], 'timestamp': [1563815078.0], 'msg_id': 1, 'real_pos': (1, 5), 'ALG': 'MESE', 'channel': 'one'})
	#Test 2 # Output : 0, 29
    payload.append({'observation': [-121.60799999999993, -125.79600000000006, -127.02800000000018], 'Tx': [1, 2, 3], 'Ty': [5, 5, 5], 'timestamp': [1563815148.0], 'msg_id': 2, 'real_pos': (2, 5), 'ALG': 'MEDE', 'channel': 'one'})

	#Test 3 # Output : 0, 29
    payload.append({'observation': [-122.14600000000014, -124.94000000000023, -126.59299999999993], 'Tx': [1, 2, 3], 'Ty': [5, 5, 5], 'timestamp': [1563815220.0], 'msg_id': 3, 'real_pos': (3, 5), 'ALG': 'MEDE', 'channel': 'one'})

    #Test 4 # Output : 0, 28
    payload.append({'observation': [-118.77300000000014, -123.085, -125.84500000000017], 'Tx': [1, 2, 3], 'Ty': [5, 5, 5], 'timestamp': [1563817132.0], 'msg_id': 30, 'real_pos': (3, 5), 'ALG': 'MEDE', 'channel': 'one'})

    curTest = random.randrange(0, 4)
    print ("estimate start") # debug info
    stime = time.time()

    result = blockSendToServer(payload[curTest])
    
    print(result) # debug info
    print("time elapsed: " + str(time.time() - stime))

	# Final Test
    output = str(result.split('; [')[1].split(']')[0])
    output = str(output.strip())
    test_vectors[curTest] = str(test_vectors[curTest].strip())
    print("Expected:", test_vectors[curTest])
    print("Recieved:", output)
    if output == test_vectors[curTest]:
        print("Passed Known Answer Test")
        PassTests = PassTests + 1
    else:
        print("Failed Known Answer Test")
        FailedTests = FailedTests + 1


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

# serverInit()
# time.sleep(0.002)
clientInit()

count = 1
for _ in range(50):
	print ("##################Test #", count, "##################\n")
	TotalTests = TotalTests + 1
	estimate_function()
	print ("##################End of Test########################\n")
	count = count + 1

print ("****************************FINAL_STATISTICS****************************\n")
print ("Total Tests in this round: ", TotalTests)
print ("Number of Test Cases Passed: ", PassTests)
print ("Number of Test Cases Failed: ", FailedTests)
print ("****************************END_OF_REPORT****************************\n")

# estimate_function()
server.close()
