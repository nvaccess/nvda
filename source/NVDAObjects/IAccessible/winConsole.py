#NVDAObjects/WinConsole.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import threading
import time
import ctypes
import difflib
import pythoncom
import api
import globalVars
from logHandler import log
import queueHandler
import textHandler
import tones
from keyUtils import sendKey, key
import winKernel
import winUser
import speech
from . import IAccessible
from .. import NVDAObjectTextInfo
import controlTypes
import braille

class WinConsole(IAccessible):

	def __init__(self,*args,**vars):
		IAccessible.__init__(self,*args,**vars)
		self.consoleEventHookHandles=[] #Holds the handles for all the win events we register so we can remove them later

	def connectConsole(self):
		if hasattr(self,'consoleHandle'):
			return
		#Give a little time for the console to settle down
		time.sleep(0.1)
		pythoncom.PumpWaitingMessages()
		if not winUser.isWindow(self.windowHandle):
			return
		#Get the process ID of the console this NVDAObject is fore
		processID=self.windowProcessID
		if processID<=0:
			log.debugWarning("Could not get valid processID from window "%self.windowHandle)
			return
		#Attach NVDA to this console so we can access its text etc
		if winKernel.kernel32.GetConsoleWindow():
			log.debug("Already attached to a console, need to free first")
			if winKernel.freeConsole()==0:
				raise OSError("Could not free console")
		if winKernel.attachConsole(processID)==0:
			raise OSError("WinConsole: could not attach console") 
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
		self.basicText=self.consoleVisibleText
		lineLength=self.getConsoleHorizontalLength()
		if lineLength<=0:
			raise RuntimeError("console line length is not valid")
		self.basicTextLineLength=lineLength
		self.prevConsoleVisibleLines=[self.basicText[x:x+lineLength] for x in xrange(0,len(self.basicText),lineLength)]
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		if globalVars.caretMovesReviewCursor and self==api.getReviewPosition().obj:
			api.setReviewPosition(self.makeTextInfo(textHandler.POSITION_CARET))
		self.monitorThread=threading.Thread(target=self.monitorThreadFunc)
		self.monitorThread.start()
		pythoncom.PumpWaitingMessages()
		time.sleep(0.1)

	def disconnectConsole(self):
		if not hasattr(self,'consoleHandle'):
			return
		#Unregister any win events we are using
		for handle in self.consoleEventHookHandles:
			winUser.unhookWinEvent(handle)
		self.consoleEventHookHandles=[]
		#Get ready to stop monitoring - give it a little time to finish
		self.keepMonitoring=False
		self.monitorThread.join()
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
		#Notify the monitor thread that an event has occurred
		self.lastConsoleEvent=eventID
		if eventID==winUser.EVENT_CONSOLE_UPDATE_SIMPLE:
			x=winUser.LOWORD(objectID)
			y=winUser.HIWORD(objectID)
			if x<info.cursorPosition.x and (y==info.cursorPosition.y or y==info.cursorPosition.y+1):  
				queueHandler.queueFunction(queueHandler.eventQueue,speech.speakTypedCharacters,unichr(winUser.LOWORD(childID)))

	def monitorThreadFunc(self):
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
					#Update the review cursor position with the caret position
					if globalVars.caretMovesReviewCursor and self==api.getReviewPosition().obj:
						queueHandler.queueFunction(queueHandler.eventQueue, api.setReviewPosition, self.makeTextInfo(textHandler.POSITION_CARET))
					queueHandler.queueFunction(queueHandler.eventQueue, braille.handler.handleCaretMove, self)
					if globalVars.reportDynamicContentChanges:
						text=self.consoleVisibleText
						self.basicText=text
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
						self.keepMonitoring=False
						queueHandler.queueFunction(queueHandler.eventQueue,self.disconnectConsole)
				checkDead_timer+=1
				#Each round of the while loop we wait 10 milliseconds
				time.sleep(0.01)
		except:
			log.error("console monitorThread", exc_info=True)

	def getConsoleVerticalLength(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		return max(info.consoleSize.y,25)

	def getConsoleHorizontalLength(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		return max(info.consoleSize.x,80)

	def _get_basicCaretOffset(self):
		if not hasattr(self,"consoleHandle"):
			offset=0 
		else:
			info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
			y=info.cursorPosition.y
			x=info.cursorPosition.x
			offset=self.getOffsetFromConsoleCoord(x,y)
		return offset

	def _get_basicSelectionOffsets(self):
		offset=self.basicCaretOffset
		return (offset,offset)

	def _get_basicTextLineLength(self):
		if hasattr(self,'consoleHandle'):
			return self.getConsoleHorizontalLength()
		else:
			return super(WinConsole,self)._get_basicTextLineLength()

	def getOffsetFromConsoleCoord(self,x,y):
		if not hasattr(self,"consoleHandle"):
			return 0
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		return ((y*self.getConsoleHorizontalLength())+x)-(info.windowRect.top*info.consoleSize.x)

	def getConsoleCoordFromOffset(self,offset):
		if not hasattr(self,"consoleHandle"):
			return (0,0)
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		offset+=(info.windowRect.top*info.consoleSize.x)
		return (offset%self.getConsoleHorizontalLength(),offset/self.getConsoleHorizontalLength())

	def _get_consoleVisibleText(self):
		if not hasattr(self,"consoleHandle"):
			return ""
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		topLine=info.windowRect.top
		lineCount=(info.windowRect.bottom-topLine)+1
		lineLength=info.consoleSize.x
		return winKernel.readConsoleOutputCharacter(self.consoleHandle,lineCount*lineLength,0,topLine)

	def event_nameChange(self):
		pass

	def event_foreground(self):
		self.event_gainFocus()

	def event_gainFocus(self):
		self.connectConsole()
		super(WinConsole,self).event_gainFocus()
		for line in self.prevConsoleVisibleLines:
			if not line.isspace() and len(line)>0: 
				speech.speakText(line)

	def event_loseFocus(self):
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
		return outLines

	def script_protectConsoleKillKey(self,keyPress):
		self.disconnectConsole()
		sendKey(keyPress)
		time.sleep(0.01)
		self.connectConsole()
		self.lastConsoleEvent=winUser.EVENT_CONSOLE_UPDATE_REGION

	def _get_role(self):
		return controlTypes.ROLE_TERMINAL

[WinConsole.bindKey(keyName,scriptName) for keyName,scriptName in [
	("control+c","protectConsoleKillKey"),
	("ExtendedUp","moveByLine"),
	("ExtendedDown","moveByLine"),
	("ExtendedLeft","moveByCharacter"),
	("ExtendedRight","moveByCharacter"),
	("Control+ExtendedLeft","moveByWord"),
	("Control+ExtendedRight","moveByWord"),
	("Shift+ExtendedRight","changeSelection"),
	("Shift+ExtendedLeft","changeSelection"),
	("Shift+ExtendedHome","changeSelection"),
	("Shift+ExtendedEnd","changeSelection"),
	("Shift+ExtendedUp","changeSelection"),
	("Shift+ExtendedDown","changeSelection"),
	("Control+Shift+ExtendedLeft","changeSelection"),
	("Control+Shift+ExtendedRight","changeSelection"),
	("ExtendedHome","moveByCharacter"),
	("ExtendedEnd","moveByCharacter"),
	("control+extendedHome","moveByLine"),
	("control+extendedEnd","moveByLine"),
	("control+shift+extendedHome","changeSelection"),
	("control+shift+extendedEnd","changeSelection"),
	("ExtendedDelete","delete"),
	("Back","backspace"),
]]
