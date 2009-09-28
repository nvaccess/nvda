#winConsoleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import threading
import difflib
import winUser
import winKernel
import wincon
import eventHandler
from logHandler import log
import globalVars
import speech
import queueHandler
import textInfos
from NVDAObjects import NVDAObjectTextInfo
import api

consoleObject=None #:The console window that is currently in the foreground.
consoleWinEventHookHandles=[] #:a list of currently registered console win events.
keepAliveMonitorThread=False #:While true, the monitor thread should continue to run
monitorThread=None
consoleOutputHandle=None
lastConsoleWinEvent=None
lastConsoleVisibleLines=[] #:The most recent lines in the console (to work out a diff for announcing updates)

@wincon.PHANDLER_ROUTINE
def _consoleCtrlHandler(event):
	if event in (wincon.CTRL_C_EVENT,wincon.CTRL_BREAK_EVENT):
		return True
	return False

def connectConsole(obj):
	global consoleObject, consoleOutputHandle, lastConsoleWinEvent, keepAliveMonitorThread, monitorThread, lastConsoleVisibleLines
	#Get the process ID of the console this NVDAObject is fore
	processID,threadID=winUser.getWindowThreadProcessID(obj.windowHandle)
	#Attach NVDA to this console so we can access its text etc
	try:
		wincon.AttachConsole(processID)
	except WindowsError as e:
		log.debugWarning("Could not attach console: %s"%e)
		return False
	wincon.SetConsoleCtrlHandler(_consoleCtrlHandler,True)
	consoleOutputHandle=winKernel.CreateFile(u"CONOUT$",winKernel.GENERIC_READ|winKernel.GENERIC_WRITE,winKernel.FILE_SHARE_READ|winKernel.FILE_SHARE_WRITE,None,winKernel.OPEN_EXISTING,0,None)                                                     
	lastConsoleVisibleLines=getConsoleVisibleLines()
	#Register this callback with all the win events we need, storing the given handles for removal later
	for eventID in [winUser.EVENT_CONSOLE_CARET,winUser.EVENT_CONSOLE_UPDATE_REGION,winUser.EVENT_CONSOLE_UPDATE_SIMPLE,winUser.EVENT_CONSOLE_UPDATE_SCROLL,winUser.EVENT_CONSOLE_LAYOUT]:
		handle=winUser.setWinEventHook(eventID,eventID,0,consoleWinEventHook,0,0,0)
		if not handle:
			raise OSError("could not register eventID %s"%eventID)
		consoleWinEventHookHandles.append(handle)
	#Setup the monitoring thread which will watch a variable, and speak new text at the appropriate time
	#Each event doesn't individually speak its own text since speaking text is quite intensive due to the diff algorithms  
	keepAliveMonitorThread=True
	lastConsoleWinEvent=None
	consoleObject=obj
	monitorThread=threading.Thread(target=monitorThreadFunc)
	monitorThread.start()
	return True

def disconnectConsole():
	global consoleObject, consoleOutputHandle, consoleWinEventHookHandles, keepAliveMonitorThread
	if not consoleObject:
		log.debugWarning("console was not connected")
		return False
	#Unregister any win events we are using
	for handle in consoleWinEventHookHandles:
		winUser.unhookWinEvent(handle)
	consoleEventHookHandles=[]
	#Get ready to stop monitoring - give it a little time to finish
	keepAliveMonitorThread=False
	monitorThread.join()
	winKernel.closeHandle(consoleOutputHandle)
	consoleOutputHandle=None
	consoleObject=None
	try:
		wincon.SetConsoleCtrlHandler(_consoleCtrlHandler,False)
	except WindowsError:
		pass
	#Try freeing NVDA from this console
	try:
		wincon.FreeConsole()
	except WindowsError:
		pass
	return True

def isConsoleDead():
	#Every console should have at least one process associated with it
	#This console should have two if NVDA is also connected
	#if there is only one (it must be NVDA) so we free NVDA from it so it can close
	processList=wincon.GetConsoleProcessList(2)
	if len(processList)<2:
		return True
	else:
		return False

def getConsoleVisibleLines():
	consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
	topLine=consoleScreenBufferInfo.srWindow.Top
	lineCount=(consoleScreenBufferInfo.srWindow.Bottom-topLine)+1
	lineLength=consoleScreenBufferInfo.dwSize.x
	text=wincon.ReadConsoleOutputCharacter(consoleOutputHandle,lineCount*lineLength,0,topLine)
	newLines=[text[x:x+lineLength] for x in xrange(0,len(text),lineLength)]
	return newLines

@winUser.WINEVENTPROC
def consoleWinEventHook(handle,eventID,window,objectID,childID,threadID,timestamp):
	global lastConsoleWinEvent
	#We don't want to do anything with the event if the event is not for the window this console is in
	if window!=consoleObject.windowHandle:
		return
	if eventID==winUser.EVENT_CONSOLE_CARET:
		eventHandler.queueEvent("caret",consoleObject)
	consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
	#Notify the monitor thread that an event has occurred
	lastConsoleWinEvent=eventID
	if eventID==winUser.EVENT_CONSOLE_UPDATE_SIMPLE:
		x=winUser.LOWORD(objectID)
		y=winUser.HIWORD(objectID)
		if x<consoleScreenBufferInfo.dwCursorPosition.x and (y==consoleScreenBufferInfo.dwCursorPosition.y or y==consoleScreenBufferInfo.dwCursorPosition.y+1):  
			queueHandler.queueFunction(queueHandler.eventQueue,speech.speakTypedCharacters,unichr(winUser.LOWORD(childID)))

def monitorThreadFunc():
	global lastConsoleWinEvent, lastConsoleVisibleLines, keepAliveMonitorThread
	try:
		consoleEvent=None
		# We want the first event to be handled immediately.
		timeSinceLast=5
		checkDead_timer=0
		#Keep the thread alive while keepMonitoring is true - disconnectConsole will make it false if the focus moves away 
		while keepAliveMonitorThread:
			#If there has been a console event lately, remember it and reset the notification to None
			if lastConsoleWinEvent:
				consoleEvent=lastConsoleWinEvent
				lastConsoleWinEvent=None
			if timeSinceLast<5:
				timeSinceLast+=1
			if consoleEvent and timeSinceLast==5:
				# There is a new event and there has been enough time since the last one was handled, so handle this.
				timeSinceLast=0
				if globalVars.reportDynamicContentChanges:
					newLines=getConsoleVisibleLines()
					outLines=calculateNewText(newLines,lastConsoleVisibleLines)
					if not (len(outLines) == 1 and len(outLines[0]) <= 1):
						for line in outLines:
							queueHandler.queueFunction(queueHandler.eventQueue, speech.speakText, line)
					lastConsoleVisibleLines=newLines
				consoleEvent=None
			#Every 10 times we also make sure the console isn't dead, if so we need to stop the thread ourselves
			if checkDead_timer>=10:
				checkDead_timer=0
				if isConsoleDead():
					keepAliveMonitorThread=False
					queueHandler.queueFunction(queueHandler.eventQueue,disconnectConsole)
			checkDead_timer+=1
			#Each round of the while loop we wait 10 milliseconds
			time.sleep(0.01)
	except:
		log.error("console monitorThread", exc_info=True)

def initialize():
	pass

def terminate():
	if consoleObject:
		disconnectConsole()

def calculateNewText(newLines,oldLines):
	foundChange=False
	outLines=[]
	diffLines=[x for x in difflib.ndiff(oldLines,newLines) if (x[0] in ['+','-'])] 
	for lineNum in xrange(len(diffLines)):
		if diffLines[lineNum][0]=="+":
			text=diffLines[lineNum][2:]
			if not text.isspace() and (lineNum>0) and (diffLines[lineNum-1][0]=="-"):
				start=0
				end=len(text)
				for pos in xrange(len(text)):
					if text[pos]!=diffLines[lineNum-1][2:][pos]:
						start=pos
						break
				for pos in xrange(len(text)-1,0,-1):
					if text[pos]!=diffLines[lineNum-1][2:][pos]:
						end=pos+1
						break
				if end - start < 15:
					# Less than 15 characters have changed, so only speak the changed chunk.
					text=text[start:end]
					foundChange=True
			if len(text)>0 and not text.isspace():
				outLines.append(text)
	return outLines

class WinConsoleTextInfo(NVDAObjectTextInfo):

	def _offsetFromConsoleCoord(self,x,y):
		consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
		val=y-consoleScreenBufferInfo.srWindow.Top
		val*=consoleScreenBufferInfo.dwSize.x
		val+=x
		return val

	def _consoleCoordFromOffset(self,offset):
		consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
		x=offset%consoleScreenBufferInfo.dwSize.x
		y=offset-x
		y/=consoleScreenBufferInfo.dwSize.x
		y+=consoleScreenBufferInfo.srWindow.Top
		return x,y

	def _getOffsetFromPoint(self,x,y):
		consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
		screenLeft,screenTop,screenWidth,screenHeight=self.obj.location
		relativeX=x-screenLeft
		relativeY=y-screenTop
		lineLength=(consoleScreenBufferInfo.srWindow.Right+1)-consoleScreenBufferInfo.srWindow.Left
		numLines=(consoleScreenBufferInfo.srWindow.Bottom+1)-consoleScreenBufferInfo.srWindow.Top
		characterWidth=screenWidth/lineLength
		characterHeight=screenHeight/numLines
		characterX=(relativeX/characterWidth)+consoleScreenBufferInfo.srWindow.Left
		characterY=(relativeY/characterHeight)+consoleScreenBufferInfo.srWindow.Top
		offset=self._offsetFromConsoleCoord(characterX,characterY)
		return offset

	def _getPointFromOffset(self,offset):
		consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
		characterX,characterY=self._consoleCoordFromOffset(offset)
		screenLeft,screenTop,screenWidth,screenHeight=self.obj.location
		lineLength=(consoleScreenBufferInfo.srWindow.Right+1)-consoleScreenBufferInfo.srWindow.Left
		numLines=(consoleScreenBufferInfo.srWindow.Bottom+1)-consoleScreenBufferInfo.srWindow.Top
		characterWidth=screenWidth/lineLength
		characterHeight=screenHeight/numLines
		relativeX=(characterX-consoleScreenBufferInfo.srWindow.Left)*characterWidth
		relativeY=(characterY-consoleScreenBufferInfo.srWindow.Top)*characterHeight
		x=relativeX+screenLeft
		y=relativeY+screenTop
		return textInfos.Point(x,y)

	def _getCaretOffset(self):
		consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
		return self._offsetFromConsoleCoord(consoleScreenBufferInfo.dwCursorPosition.x,consoleScreenBufferInfo.dwCursorPosition.y)

	def _getSelectionOffsets(self):
		selInfo=wincon.GetConsoleSelectionInfo()
		if selInfo.dwFlags&wincon.CONSOLE_SELECTION_NOT_EMPTY:
			start=self._offsetFromConsoleCoord(selInfo.srSelection.Left,selInfo.srSelection.Top)
			end=self._offsetFromConsoleCoord(selInfo.srSelection.Right,selInfo.srSelection.Bottom)
		else:
			start=end=self._getCaretOffset()
		return start,end

	def _getTextRange(self,start,end):
		startX,startY=self._consoleCoordFromOffset(start)
		return wincon.ReadConsoleOutputCharacter(consoleOutputHandle,end-start,startX,startY)

	def _getLineOffsets(self,offset):
		consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
		x,y=self._consoleCoordFromOffset(offset)
		x=0
		start=self._offsetFromConsoleCoord(x,y)
		end=start+consoleScreenBufferInfo.dwSize.x
		return start,end

	def _getLineNumFromOffset(self,offset):
		consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
		x,y=self._consoleCoordFromOffset(offset)
		return y-consoleScreenBufferInfo.srWindow.top

	def _getStoryLength(self):
		consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
		return consoleScreenBufferInfo.dwSize.x*((consoleScreenBufferInfo.srWindow.Bottom+1)-consoleScreenBufferInfo.srWindow.Top)

	def copyToClipboard(self):
		blocks = (block.rstrip() for block in self.getTextInChunks(textInfos.UNIT_LINE))
		return api.copyToClip("\r\n".join(blocks))
