import random

buckets = {}
location = {}
objects = {}
outGoingMsgs = {}
mapSize = pow(2,8) #hard coded in pico-carts
cellWidth = 64

def onStart():
	for i in range(0, int(mapSize/cellWidth)):
		for j in range(0, int(mapSize/cellWidth)):
			buckets[(i,j)] = []
			buckets[(i,j)].append(int(random.random()*10))
	debugBuckets()

def onConnect(id):
	pass

def onDisconnect(id):
	pass

def debugBuckets():
	for key in buckets:
		print(str(key) + " "+ str(buckets[key]))
