
threadList=[]

def newThread(generator):
	"""Adds this generator object to the main thread list which will be iterated in the main core loop""" 
	threadList.append(generator)

def makeGeneratorFunction(func,*args,**vars):
	"""Makes a generator function out of a simple function that does not yield itself. Do not use functions that process for a long time"""
	func(*args,**vars)
	yield None

def pump():
	delList=[]
	for num in range(len(threadList)):
		try:
			threadList[num].next()
		except StopIteration:
			delList.append(num)
	for num in delList:
		del threadList[num]

