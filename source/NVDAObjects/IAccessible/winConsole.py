#NVDAObjects/WinConsole.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import thread
import time
import ctypes
import difflib
import pythoncom
import globalVars
import debug
import queueHandler
import tones
from keyUtils import sendKey, key
import winKernel
import winUser
import speech
from . import IAccessible

class WinConsole(IAccessible):

	def __init__(self,*args,**vars):
		IAccessible.__init__(self,*args,**vars)
		self.consoleEventHookHandles=[] #Holds the handles for all the win events we register so we can remove them later

	def connectConsole(self):
		#Give a little time for the console to settle down
		time.sleep(0.1)
		pythoncom.PumpWaitingMessages()
		if not winUser.isWindow(self.windowHandle):
			return
		#Get the process ID of the console this NVDAObject is fore
		processID,threadID=self.windowProcessID
		#Attach NVDA to this console so we can access its text etc
		res=winKernel.attachConsole(processID)
		if not res:
			raise OSError("WinConsole: could not get console std handle") 
		#Try and get the handle for this console's standard out
		res=winKernel.getStdHandle(winKernel.STD_OUTPUT_HANDLE)
		if not res:
			raise OSError("consoleWindowClassClient: could not get console std handle") 
		self.consoleHandle=res
		self.cConsoleEventHook=ctypes.CFUNCTYPE(ctypes.c_voidp,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)(self.consoleEventHook)
		#Register this callback with all the win events we need, storing the given handles for removal later
		for eventID in [winUser.EVENT_CONSOLE_CARET,winUser.EVENT_CONSOLE_UPDATE_REGION,winUser.EVENT_CONSOLE_UPDATE_SIMPLE,winUser.EVENT_CONSOLE_UPDATE_SCROLL,winUser.EVENT_CONSOLE_LAYOUT]:
			handle=winUser.setWinEventHook(eventID,eventID,0,self.cConsoleEventHook,0,0,0)
			if handle:
				self.consoleEventHookHandles.append(handle)
			else:
				raise OSError('Could not register console event %s'%eventID)
		#Setup the monitoring thread which will watch a variable, and speak new text at the appropriate time
		#Each event doesn't individually speak its own text since speaking text is quite intensive due to the diff algorithms  
		self.keepMonitoring=True
		self.lastConsoleEvent=None
		text=self.consoleVisibleText
		self.textRepresentation=text
		lineLength=self.getConsoleHorizontalLength()
		self.textRepresentationLineLength=lineLength
		self.prevConsoleVisibleLines=[text[x:x+lineLength] for x in xrange(0,len(text),lineLength)]
		self.prevConsoleVisibleLines=[text[x:x+lineLength] for x in xrange(0,len(text),lineLength)]
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		self.reviewOffset=self.text_caretOffset-info.windowRect.top*info.consoleSize.x
		thread.start_new_thread(self.monitorThread,())
		pythoncom.PumpWaitingMessages()
		time.sleep(0.1)

	def disconnectConsole(self):
		#Unregister any win events we are using
		for handle in self.consoleEventHookHandles:
			winUser.unhookWinEvent(handle)
		self.consoleEventHookHandles=[]
		#Get ready to stop monitoring - give it a little time to finish
		self.keepMonitoring=False
		time.sleep(0.001)
		#Get rid of the console handle we were holding
		if hasattr(self,'consoleHandle'):
			del self.consoleHandle
		#Try freeing NVDA from this console
		try:
			winKernel.freeConsole()
		except:
			pass

	def isConsoleDead(self):
		#Every console should have at least one process associated with it
		#This console should have two if NVDA is also connected
		#if there is only one (it must be NVDA) so we free NVDA from it so it can close
		num=winKernel.getConsoleProcessList((ctypes.c_int*2)(),2)
		if num<2:
			return True
		else:
			return False

	def consoleEventHook(self,handle,eventID,window,objectID,childID,threadID,timestamp):
		#We don't want to do anything with the event if the event is not for the window this console is in
		if window!=self.windowHandle:
			return
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		#Update the review cursor position with the caret position
		if globalVars.caretMovesReviewCursor:
			self.reviewOffset=self.text_caretOffset-info.windowRect.top*info.consoleSize.x
		#For any events other than caret movement, we want to let the monitor thread know that there might be text to speak
		if eventID!=winUser.EVENT_CONSOLE_CARET:
			self.lastConsoleEvent=eventID
		if eventID==winUser.EVENT_CONSOLE_UPDATE_SIMPLE:
			x=winUser.LOWORD(objectID)
			y=winUser.HIWORD(objectID)
			if x<info.cursorPosition.x and (y==info.cursorPosition.y or y==info.cursorPosition.y+1):  
				queueHandler.queueFunction(queueHandler.eventQueue,speech.speakTypedCharacters,unichr(winUser.LOWORD(childID)))

	def monitorThread(self):
		try:
			consoleEvent=None
			# We want the first event to be handled immediately.
			timeSinceLast=5
			checkDead_timer=0
			#Keep the thread alive while keepMonitoring is true - disconnectConsole will make it false if the focus moves away 
			while self.keepMonitoring:
				#If there has been a console event lately, remember it and reset the notification to None
				if self.lastConsoleEvent:
					consoleEvent=self.lastConsoleEvent
					self.lastConsoleEvent=None
				if timeSinceLast<5:
					timeSinceLast+=1
				if consoleEvent and timeSinceLast==5:
					# There is a new event and there has been enough time since the last one was handled, so handle this.
					timeSinceLast=0
					if globalVars.reportDynamicContentChanges:
						text=self.consoleVisibleText
						self.textRepresentation=text
						lineLength=self.getConsoleHorizontalLength()
						newLines=[text[x:x+lineLength] for x in xrange(0,len(text),lineLength)]
						outLines=self.calculateNewText(newLines,self.prevConsoleVisibleLines)
						if consoleEvent != winUser.EVENT_CONSOLE_UPDATE_SIMPLE and not (len(outLines) == 1 and len(outLines[0]) <= 1):
							for line in outLines:
								queueHandler.queueFunction(queueHandler.eventQueue, speech.speakText, line)
						self.prevConsoleVisibleLines=newLines
					consoleEvent=None
				#Every 10 times we also make sure the console isn't dead, if so we need to stop the thread ourselves
				if checkDead_timer>=10:
					checkDead_timer=0
					if self.isConsoleDead():
						self.disconnectConsole()
				checkDead_timer+=1
				#Each round of the while loop we wait 10 milliseconds
				time.sleep(0.01)
		except:
			debug.writeException("console monitorThread")

	def getConsoleVerticalLength(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		return info.consoleSize.y

	def getConsoleHorizontalLength(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		return info.consoleSize.x

	def _get_text_reviewOffsetLimits(self):
		if not hasattr(self,"consoleHandle"):
			return (0,0) 
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		top=self.getOffsetFromConsoleCoord(0,info.windowRect.top)
		bottom=self.getOffsetFromConsoleCoord(self.getConsoleHorizontalLength(),info.windowRect.bottom)
		return (top,bottom)

	def _get_text_caretOffset(self):
		if not hasattr(self,"consoleHandle"):
			return 0
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		y=info.cursorPosition.y
		x=info.cursorPosition.x
		return self.getOffsetFromConsoleCoord(x,y)

	def getOffsetFromConsoleCoord(self,x,y):
		if not hasattr(self,"consoleHandle"):
			return 0
		return (y*self.getConsoleHorizontalLength())+x

	def getConsoleCoordFromOffset(self,offset):
		if not hasattr(self,"consoleHandle"):
			return (0,0)
		return (offset%self.getConsoleHorizontalLength(),offset/self.getConsoleHorizontalLength())

	def text_getLineOffsets(self,offset):
		if not hasattr(self,"consoleHandle"):
			return (0,0)
		start=offset-(offset%self.getConsoleHorizontalLength())
		end=start+self.getConsoleHorizontalLength()
		return (start,end)

	def text_getNextLineOffsets(self,offset):
		if not hasattr(self,"consoleHandle"):
			return (0,0)
		(x,y)=self.getConsoleCoordFromOffset(offset)
		x=0
		y+=1
		newOffset=self.getOffsetFromConsoleCoord(x,y)
		if newOffset<self.text_characterCount:
			return self.text_getLineOffsets(newOffset)
		else:
			return None

	def text_getPrevLineOffsets(self,offset):
		if not hasattr(self,"consoleHandle"):
			return (0,0)
		(x,y)=self.getConsoleCoordFromOffset(offset)
		x=0
		if y<=0:
			return None
		y-=1
		newOffset=self.getOffsetFromConsoleCoord(x,y)
		if newOffset>=0:
			return self.text_getLineOffsets(newOffset)
		else:
			return None

	def _get_text_characterCount(self):
		return self.getOffsetFromConsoleCoord(self.getConsoleHorizontalLength(),self.getConsoleVerticalLength()-1)

	def text_getText(self,start=None,end=None):
		if not hasattr(self,"consoleHandle"):
			return "\0"
		start=start if isinstance(start,int) else 0
		end=end if isinstance(end,int) else len(self.value)
		(x,y)=self.getConsoleCoordFromOffset(start)
		maxLen=end-start
		text=winKernel.readConsoleOutputCharacter(self.consoleHandle,maxLen,x,y)
		return text

	def _get_consoleVisibleText(self):
		if not hasattr(self,"consoleHandle"):
			return ""
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		topLine=info.windowRect.top
		bottomLine=info.windowRect.bottom
		lineLength=info.consoleSize.x
		return winKernel.readConsoleOutputCharacter(self.consoleHandle,((bottomLine-topLine)+1)*lineLength,0,topLine)

	def event_nameChange(self):
		pass

	def event_gainFocus(self):
		super(WinConsole,self).event_gainFocus()
		self.connectConsole()
		for line in self.prevConsoleVisibleLines:
			speech.speakText(line)

	def event_looseFocus(self):
		self.disconnectConsole()

	def calculateNewText(self,newLines,oldLines):
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
		if not foundChange and not outLines:
			# We know that something has changed, but there doesn't appear to be any new text.
			# Therefore, just speak the current line.
			start, end = self.text_getLineOffsets(self.text_caretOffset)
			#outLines.append(self.text_getText(start, end).strip())
		return outLines

	def script_protectConsoleKillKey(self,keyPress,nextScript):
		self.disconnectConsole()
		sendKey(keyPress)
		time.sleep(0.01)
		self.connectConsole()
		self.lastConsoleEvent=winUser.EVENT_CONSOLE_UPDATE_REGION

[WinConsole.bindKey(keyName,scriptName) for keyName,scriptName in [
	("control+c","protectConsoleKillKey"),
	("ExtendedUp","text_moveByLine"),
	("ExtendedDown","text_moveByLine"),
	("ExtendedLeft","text_moveByCharacter"),
	("ExtendedRight","text_moveByCharacter"),
	("Control+ExtendedLeft","text_moveByWord"),
	("Control+ExtendedRight","text_moveByWord"),
	("Shift+ExtendedRight","text_changeSelection"),
	("Shift+ExtendedLeft","text_changeSelection"),
	("Shift+ExtendedHome","text_changeSelection"),
	("Shift+ExtendedEnd","text_changeSelection"),
	("Shift+ExtendedUp","text_changeSelection"),
	("Shift+ExtendedDown","text_changeSelection"),
	("Control+Shift+ExtendedLeft","text_changeSelection"),
	("Control+Shift+ExtendedRight","text_changeSelection"),
	("ExtendedHome","text_moveByCharacter"),
	("ExtendedEnd","text_moveByCharacter"),
	("control+extendedHome","text_moveByLine"),
	("control+extendedEnd","text_moveByLine"),
	("control+shift+extendedHome","text_changeSelection"),
	("control+shift+extendedEnd","text_changeSelection"),
	("ExtendedDelete","text_delete"),
	("Back","text_backspace"),
]]
