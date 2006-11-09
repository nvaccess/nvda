generators={}
lastGeneratorValues={}
lastID=0

def newID():
	global lastID
	lastID+=1
	return lastID

def addGenerator(generator):
	"""Adds this generator object to the main thread list which will be iterated in the main core loop""" 
	ID=newID()
	generators[ID]=generator
	return ID

def removeGenerator(ID):
	del generators[ID]

def generatorExists(ID):
	return generators.has_key(ID)

def getLastGeneratorValue(ID):
	if lastGeneratorValues.has_key(ID):
		val=lastGeneratorValues[ID]
		if not generatorExists(ID):
			del lastGeneratorValues[ID]
		return val
	else:
		return None

def executeFunction(func,*args,**vars):
	g=makeGeneratorFunction(func,*args,**vars)
	ID=addGenerator(g)
	while generatorExists(ID):
		time.sleep(0.001)
	return getLastGeneratorValue(ID)


def makeGeneratorFunction(func,*args,**vars):
	"""Makes a generator function out of a simple function that does not yield itself. Do not use functions that process for a long time"""
	res=func(*args,**vars)
	yield res

def pump():
	delList=[]
	for ID in generators.keys():
		try:
			lastGeneratorValues[ID]=generators[ID].next()
		except StopIteration:
			delList.append(ID)
	for ID in delList:
		del generators[ID]
