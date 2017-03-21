import random

buckets = {}
location = {}
objects = {}
outGoingMsgs = {}
mapSize = pow(2,8) #hard coded in pico-carts
cellWidth = 64
cellMax = int(mapSize / cellWidth)

def onStart():
	# Create empty buckets
	for i in range(0, cellMax):
		for j in range(0, cellMax):
			buckets[(i,j)] = []
			#buckets[(i,j)].append(int(random.random()*10))
	
	# Generate objects 1-255
	for i in range(1, 256):
		obj = {"id":i, "x":0, "y":0, "size": 1}
		setRndLoc(obj)
		buckets[getObjBucket(obj)].append(obj)
		objects[i] = obj
	#debugBuckets()

def onConnect(myId):
	outGoingMsgs[myId] = []
	objects[myId]['size'] = 3
	outGoingMsgs[myId].append(objects[myId])
	#debugOutGoingMessages(myId)
	thisCell = getObjBucket(objects[myId])
	for cell in getSelfAndNeighbors(thisCell):
		for obj in buckets[cell]:
			outGoingMsgs[myId].append(obj)

	#debugOutGoingMessages(myId)
	#updateObject(objects[myId])
	

def onDisconnect(myId):
	debugActivePlayers()
	objects[myId]['size'] = 1
	del outGoingMsgs[myId]
	debugActivePlayers()
	#updateObject(objects[myId])

def getSelfAndNeighbors(cell):
	"""Find neighboring cell

	Parameters
	----------
	c : tuple
	(i,j) of cell space.

	>>> getSelfAndNeighbors((1,1)) # doctest: +ELLIPSIS
	[(0, 0), ..., (2, 2)]
	>>> len(getSelfAndNeighbors((0,0)))
	4
	"""
	i,j = cell
	cellList = []
	for y in range(j-1, j+2):
		for x in range(i-1, i+2):
			if(x >= 0 and x < cellMax and y >= 0 and y < cellMax):
				cellList.append((x, y))
	return cellList


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

def debugOutGoingMessages(myId):
	print('onConnect@3')
	print("Outgoing for " + str(myId) +" " + str(outGoingMsgs[myId]))

def debugActivePlayers():
	if len(outGoingMsgs) == 0:
		print('No active players')
	for ids in outGoingMsgs:
		print("Player id: "+str(ids))