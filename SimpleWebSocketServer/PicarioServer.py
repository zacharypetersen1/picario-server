import random

buckets = {}
location = {}
objects = {}
outGoingMsgs = {}
mapSize = pow(2,8) #hard coded in pico-carts
cellWidth = 64

def onStart():
	# Create empty buckets
	for i in range(0, int(mapSize/cellWidth)):
		for j in range(0, int(mapSize/cellWidth)):
			buckets[(i,j)] = []
			#buckets[(i,j)].append(int(random.random()*10))
	
	# Generate objects 1-255
	for i in range(1, 256):
		obj = {"id":i, "x":0, "y":0, "size": 1}
		setRndLoc(obj)
		buckets[getObjBucket(obj)].append(obj)
	#debugBuckets()

def onConnect(id):
	pass

def onDisconnect(id):
	pass

def getObjBucket(obj):
	return (getBucket(obj['x'], obj['y']))

def getBucket(x, y):
	return (int(x/cellWidth), int(y/cellWidth))

# Set obj to random location
def setRndLoc(obj):
	obj['x'] = int(random.random() * mapSize)
	obj['y'] = int(random.random() * mapSize)

def debugBuckets():
	for key in buckets:
		print(str(key) + " "+ str(buckets[key]))
