# this file generate fake RSS data using simple path loss model and feed to mqtt-client
# constant variable is defined in "../common/conf.py"

import math
import numpy as np
import sys
sys.path.insert(0, '../common')
import conf
import subprocess
import random
import sys

# static localization
def read_static():
	obs_raw = []
	r = (15,50)
	for x, y in zip(conf.Tx, conf.Ty):
		distance = math.sqrt((x-r[0])**2 + (y-r[1])**2)
		obs_raw.append(-10 * conf.eta * np.log(distance))
	obs = [x + y for x, y in zip(obs_raw, np.random.rand(3))]
	return r, obs

def read_dynamic(next):
	positions = [(8,10),(8,30),(8,50),(15,50),(26,50),(26,70)]
	r = positions[next%len(positions)]
	obs_raw = []
	for x, y in zip(conf.Tx, conf.Ty):
		distance = math.sqrt((x-r[0])**2 + (y-r[1])**2)
		obs_raw.append(-10 * conf.eta * np.log(distance))
	obs = [x + y for x, y in zip(obs_raw, np.random.rand(3))]
	return r, obs

def read_dynamic_transmitters(next):
	Tx = [5,7,9]
	Ty = [20+next,16+next,18+next]
	positions = zip(Tx, Ty)
	r = positions[next%len(positions)]
	obs_raw = []
	for x, y in zip(Tx, Ty):
		distance = math.sqrt((x-r[0])**2 + (y-r[1])**2)
		obs_raw.append(-1.0*(random.random()*(55.0-10.0) + 10.0))
		# obs_raw.append(-10 * conf.eta * np.log(distance))
	obs = [x + y for x, y in zip(obs_raw, np.random.rand(3))]
	return r, obs, Tx, Ty

def read_cell_measurement(next):
	Tx = [5,6,7]
	Ty = [5,5,5]
	positions = zip(Tx, Ty)
	r = positions[next%len(positions)]
	obs1 = []
	obs2 = []
	obs3 = []
	cmd1 = ['sudo /home/anrg/srsLTE/build/lib/examples/cell_measurement -a serial=3134664 -f 2685000000']
	cmd2 = ['sudo /home/anrg/srsLTE/build/lib/examples/cell_measurement -a serial=3133B49 -f 2685000000']
	cmd3 = ['sudo /home/anrg/srsLTE/build/lib/examples/cell_measurement -a serial=3133B4A -f 2685000000']
		
	sys.stdout.write("Please wait...")
	p1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, bufsize=1)
	for line in iter(p1.stdout.readline, b''):
		try:
			value = line.split(' ')
			if (value[value.index("RSSI:")+1] != ""):
				obs1.append(float(value[value.index("RSSI:")+1]))
				if (len(obs1) == 100): break
		except:
			sys.stdout.write(".")
			continue
	p1.kill()

	p2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, bufsize=1)
	for line in iter(p2.stdout.readline, b''):
		try:
			value = line.split(' ')
			if (value[value.index("RSSI:")+1] != ""):
				obs2.append(float(value[value.index("RSSI:")+1]))
				if (len(obs2) == 100): break
		except:
			sys.stdout.write(".")
			continue
	p2.kill()

	p3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE, bufsize=1)
	for line in iter(p3.stdout.readline, b''):
		try:
			value = line.split(' ')
			if (value[value.index("RSSI:")+1] != ""):
				obs3.append(float(value[value.index("RSSI:")+1]))
				if (len(obs3) == 100): break
		except:
			sys.stdout.write(".")
			continue
	p3.kill()
	print ""

	obs = [sum(obs1)/100.0, sum(obs2)/100.0, sum(obs3)/100.0]
	obs_final = []
	Tx_final = []
	Ty_final = []

	for i in range(len(obs)):
		if (obs[i] != 0.0):
			Tx_final.append(Tx[i])
			Ty_final.append(Ty[i])
			obs_final.append(obs[i])

	return r, obs_final, Tx_final, Ty_final

def read_btmgmt(next):
	positions = [(3,10),(3,15),(3,20),(3,25),(3,30)]
	r = positions[next%len(positions)]
	obs = []
	cmd = ["/usr/bin/btmgmt find | grep 'C6:61:8D:06:53:9C'"]

	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1)
	for line in iter(p.stdout.readline, b''):
		obs.append(int(line.split(' ')[7]))
		if (len(obs) != 0):
			break
		else:
			print "No reading found"
	p.stdout.close()
	p.wait()
	return r, obs

