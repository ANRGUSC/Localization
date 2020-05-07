# This piece of code declare all static variable as well as prior distribution

# MQTT broker info
host = "127.0.0.1"
port = 1883
keep_alive = 180
RETRY_LIMIT = 5

# Floor Plan Model
l = 15                     # length of the grid.(x-dimension) 53
w = 100                     # breadth of the grid.(y-dimension) 94
total_area = 109

mode = "simple_path_loss"    # mode could be simple_path_loss or fingerprinting

sigm = 16.16               # S.D of the log normal R.V divided by 10
eta = 3.93                 # Path loss factor

rad1 = 0.1                   # d1 in P(d1) in units of gran
rad2 = 1.6                   # d2 in P(d2) in units of gran

# Position of the transmitters.
# Tx = [5,7,9]
# Ty = [20,16,18]

# Define Office Area in Grid
# Remove impossible positions to save computation
# def isValid(x, y):
# 	return True 

def isValid(x, y):
	return True

def isValid_old(x, y):
	if 0 <= x < 6 and y in range(48, 54):
		return True
	if 6 <= x < 10 and y in range(0, 54):
		return True
	if 10 <= x < 15 and (y in range(6, 11) or y in range(48, 54)):
		return True
	if 15 <= x < 22 and (y in range(6, 11) or y in range(48, 54) or y in range(90, 95)):
		return True
	if 22 <= x < 29 and y in range(6, 95):
		return True
	if 29 <= x < 53 and y in range(6, 10):
		return True
	return False

# Calculate Prior prob
# Equal Likely in Hallway Area
Prob = {}
for i in range(0, l):
	for j in range(0, w):
		r = (i, j)
		if isValid(i,j):
			Prob[r] = 1.0/total_area
		else:
			Prob[r] = 0.0
