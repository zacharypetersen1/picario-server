import random

cells = {}
objects = {}
outGoingMsgs = {}
mapSize = pow(2,8) #hard coded in pico-carts
cellWidth = 64
cellMax = int(mapSize / cellWidth)

def onStart():
	# Create empty cells
	for i in range(0, cellMax):
		for j in range(0, cellMax):
			cells[(i,j)] = []
			#cells[(i,j)].append(int(random.random()*10))
	
	# Generate objects 1-255
	for i in range(1, 256):
		obj = {"type":"obj", "id":i, "x":0, "y":0, "size": 1}
		setRndLoc(obj)
		cells[objGetCellIndex(obj)].append(obj)
		objects[i] = obj
	#debugCells()

def onConnect(myId):
	outGoingMsgs[myId] = []
	objects[myId]['size'] = 3
	outGoingMsgs[myId].append(objects[myId])
	#debugOutGoingMessages(myId)
	thisCell = objGetCellIndex(objects[myId])
	for cell in getSelfAndNeighbors(thisCell):
		for obj in cells[cell]:
			outGoingMsgs[myId].append(obj)

	#debugOutGoingMessages(myId)
	#updateObject(objects[myId])
	
def onMessage(myId, objectToUpdate):
	
	# gather info about cells
	leavingCell = objGetCellIndex(objects[objectToUpdate["id"]])	# object's cell location currently stored in memory
	arrivingCell = objGetCellIndex(objectToUpdate)					# object's cell location given new position
	leavingCells = getSelfAndNeighbors(leavingCell)					# all neighboring cells near where object was
	arrivingCells = getSelfAndNeighbors(arrivingCell)				# all neigboring cells near where object is now
	destroyCells = treatAsDestroy(leavingCells, arrivingCells)		# cells that object was near and is no longer near
	createCells = treatAsCreate(leavingCells, arrivingCells)		# cells that object was not near and is now near
	
	# if this object is a player then update that player
	if(isPlayer(objectToUpdate["id"]) and (leavingCell != arrivingCell)):
		for cellIndex in destroyCells:
			for obj in cells[cellIndex]:
				destroyMsg = obj.copy()
				destroyMsg["size"] = 0
				outGoingMsgs[objectToUpdate["id"]].append(destroyMsg)
		for cellIndex in createCells:
			for obj in cells[cellIndex]:
				outGoingMsgs[objectToUpdate["id"]].append(obj)

	if(leavingCell != arrivingCell):
		destroyInTheseCells(destroyCells, objectToUpdate)
		# destroy self in "cells"
	
	updateInTheseCells(arrivingCells, objectToUpdate)

	# add/update self in "cells"

	return outGoingMsgs

def destroyInTheseCells(destroyCells, message):
	destroyMsg = message.copy()
	destroyMsg["size"] = 0
	for cellIndex in destroyCells:
		for playerID in getPlayerIDsInCell(cellIndex):
			outGoingMsgs[playerID].append(destroyMsg)

def updateInTheseCells(updateCells, message):
	for cellIndex in updateCells:
		for playerID in getPlayerIDsInCell(cellIndex):
			outGoingMsgs[playerID].append(message)

def treatAsDestroy(leaving, arriving):
	"""
	Finds all the cells that need to remove an object

	>>> treatAsDestroy([(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)], [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)])
	[(0, 0), (1, 0), (2, 0), (0, 1), (0, 2)]

	>>> treatAsDestroy([(0,0),(1,1),(0,1), (1,0)], [(0,0),(1,1),(0,1), (1,0)])
	[]

	"""
	tmp = []
	for elem in leaving:
		if elem not in arriving:
			tmp.append(elem)
	return tmp

def treatAsCreate(leaving, arriving):
	tmp = []
	for elem in arriving:
		if elem not in leaving:
			tmp.append(elem)
	return tmp

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

def isPlayer(playerID):
	return playerID in outGoingMsgs

def getPlayerIDsInCell(cellIndex):
	playerIDs = []
	for obj in cells[cellIndex]:
		if isPlayer(obj[id]):
			playerIDs.append(obj[id])
	return playerIDs

def objGetCellIndex(obj):
	return (getCellIndex(obj['x'], obj['y']))

def getCellIndex(x, y):
	return (int(x/cellWidth), int(y/cellWidth))

# Set obj to random location
def setRndLoc(obj):
	obj['x'] = int(random.random() * mapSize)
	obj['y'] = int(random.random() * mapSize)

def debugCells():
	for key in cells:
		print(str(key) + " "+ str(cells[key]))

def debugOutGoingMessages(myId):
	print('onConnect@3')
	print("Outgoing for " + str(myId) +" " + str(outGoingMsgs[myId]))

def debugActivePlayers():
	if len(outGoingMsgs) == 0:
		print('No active players')
	for ids in outGoingMsgs:
		print("Player id: "+str(ids))