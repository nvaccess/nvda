
threadList=[]

def newThread(generator):
		threadList.append(generator)

def pump():
	delList=[]
	for num in range(len(threadList)):
		try:
			threadList[num].next()
		except StopIteration:
			delList.append(num)
	for num in delList:
		del threadList[num]

