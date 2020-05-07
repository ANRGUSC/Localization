import sys
sys.path.insert(0, '../common')
import conf
import operator

class Fingerprinting:

	# private variable
	# 1. top 10 access point
	# 2. table of likelihood: unique identified by mac address+coordinate

	def __init__(self):
		self.table = self.parseRSSLocation()
		self.top = self.getTop10()

	# get top 10 access point from file "RSS_Location"
	def getTop10(self):
		f = open('RSS_Location')
		AP_freq = {}
		for line in f:
			tmp = line.split(" ")
			mac = tmp[0]
			if mac not in AP_freq:
				AP_freq[mac] = 1
			else:
				AP_freq[mac] = AP_freq[mac]+1
		f.close()
		top = []
		# sort according to access point frequency
		sorted_AP = sorted(AP_freq.items(), key=operator.itemgetter(1), reverse=True)
		# return top10 access point
		for i in range(10):
			top.append(sorted_AP[i][0])
		# print top
		return top

	# get table of likelihood
	def parseRSSLocation(self):
		table = {}
		f = open('RSS_Location')
		for line in f:
			tmp = line.split(" ")
			mac = tmp[0]
			range = self.getRange(int(tmp[1]))
			coordinate = "(" + str(tmp[2][1:-1]) +", "+ str(tmp[3][:-1])
			if coordinate not in table:
				table[coordinate] = {}
			if mac not in table[coordinate]:
				table[coordinate][mac] = {}
			if range not in table[coordinate][mac]:
				table[coordinate][mac][range] = 1
			else:
				table[coordinate][mac][range] = table[coordinate][mac][range]+1
		f.close()
		return table

	def getRange(self, rss):
		base = rss/5
		return str(base*5)+"-"+str(base*5+5)

	def fingerprintingCalculation(self, real, mac, rss):
		# print str(real) +" "+ mac + " " + rss
		if not conf.isValid(real[0], real[1]):
			# print "invalid real location"
			return 0
		real = real.__str__()
		# TODO: Bug need to be fixed, every real coordinate should included expect invalid range
		if real not in self.table:
			# print "real location not in table"
			return 0
		if mac not in self.table[real]:
			# print "mac address not in table of real location"
			return 0
		if rss not in self.table[real][mac]:
			return 0
		return  self.table[real][mac][rss]

	def likelihood(self, obs, r):
		likelihood = 1
		for i in range(len(obs)):
			likelihood = likelihood*self.fingerprintingCalculation(r, self.top[i], self.getRange(obs[i]))
		return likelihood
