import math
import numpy as np
import sys
sys.path.insert(0, '../common')
import conf
import fingerprinting

if conf.mode == "fingerprinting":
	f = fingerprinting.Fingerprinting()

def gaussian(x, mu, sig):
	return (1./np.sqrt(2*np.pi)*sig)*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def estimate(obs, alg, Tx, Ty):
	cost = sys.maxint
	ans = []
	# loop through every element in grid
	for i in range(0, conf.l):
		for j in range(0, conf.w):
			if conf.isValid(i,j):
				r_hat = (i, j)
				temp = expected_cost(r_hat, obs, alg, Tx, Ty)
				if temp < cost:
					cost = temp
					ans = r_hat
	return ans

# E(C(r_hat, obs)) = sum C(r, r_hat, obs)) through every r in grid
# method isValid remove points with 0 probability to reduce computation complexity
def expected_cost(r_hat, obs, alg, Tx, Ty):
	expect = 0
	for i in range(0, conf.l):
		for j in range(0, conf.w):
			if conf.isValid(i,j):
				r = (i, j)
				prob = conf.Prob[r]
				if alg == "MEDE":
					expect = expect+prob*likelihood(r,obs,Tx,Ty)*cost_MEDE(r, r_hat, obs)
				elif alg == "MMSE":
					expect = expect+prob*likelihood(r,obs,Tx,Ty)*cost_MMSE(r, r_hat, obs)
				else:
					expect = expect+prob*likelihood(r,obs,Tx,Ty)*cost_MLE(r, r_hat, obs)
	return expect

# correspond to fo(O|R=r) simple path loss model
def likelihood(r, obs, Tx, Ty):
	if conf.mode == "fingerprinting":
		return f.likelihood(obs, r)
	obs_r = []
	for x, y in zip(Tx, Ty):
		distance = math.sqrt((x-r[0])**2 + (y-r[1])**2)
		if distance == 0: continue
		obs_r.append(-10 * conf.eta * np.log(distance))  
	likelihood = 1
	for i in range(len(obs_r)):
		likelihood = likelihood*gaussian(obs[i], obs_r[i], conf.sigm)
	return likelihood

def cost_MLE(r, r_hat, obs):
	if abs(r[0]-r_hat[0]) < conf.rad1 and abs(r[1]-r_hat[1]) < conf.rad1:
		return -1
	return 0

def cost_MEDE(r, r_hat, obs):
	return math.sqrt((r_hat[0]-r[0])**2 + (r_hat[1]-r[1])**2)

def cost_MMSE(r, r_hat, obs):
	return (r_hat[0]-r[0])**2 + (r_hat[1]-r[1])**2


# obs = [-79, -84, -83, -84, -68,-77, -73, -85, -63, -62] #real position (26, 94)
# print estimate(obs,'MLE') # estimate position (26, 93)
