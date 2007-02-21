#NVDAObjects/winConsole.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import thread
import time
import ctypes
import difflib
import debug
import tones
from keyUtils import sendKey, key
import winKernel
import winUser
import audio
import IAccessible

class NVDAObject_winConsole(IAccessible.NVDAObject_IAccessible):

	def __init__(self,*args,**vars):
		IAccessible.NVDAObject_IAccessible.__init__(self,*args,**vars)
		self.consoleEventHookHandles=[]

	text_caretSayAllGenerator=None

	def connectConsole(self):
		processID=self.windowProcessID[0]
		try:
			winKernel.freeConsole()
		except:
			debug.writeException("freeConsole")
			pass
		winKernel.attachConsole(processID)
		res=winKernel.getStdHandle(winKernel.STD_OUTPUT_HANDLE)
		if not res:
			raise OSError("NVDAObject_consoleWindowClassClient: could not get console std handle") 
		self.consoleHandle=res
		self.cConsoleEventHook=ctypes.CFUNCTYPE(ctypes.c_voidp,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)(self.consoleEventHook)
		for eventID in [winUser.EVENT_CONSOLE_CARET,winUser.EVENT_CONSOLE_UPDATE_REGION,winUser.EVENT_CONSOLE_UPDATE_SIMPLE,winUser.EVENT_CONSOLE_UPDATE_SCROLL,winUser.EVENT_CONSOLE_LAYOUT]:
			handle=winUser.setWinEventHook(eventID,eventID,0,self.cConsoleEventHook,0,0,0)
			if handle:
				self.consoleEventHookHandles.append(handle)
			else:
				raise OSError('Could not register console event %s'%eventID)
		self.keepMonitoring=True
		self.lastConsoleEvent=None
		thread.start_new_thread(self.monitorThread,())

	def disconnectConsole(self):
		for handle in self.consoleEventHookHandles:
			winUser.unhookWinEvent(handle)
		self.consoleEventHookHandles=[]
		self.keepMonitoring=False
		time.sleep(0.001)
		if hasattr(self,'consoleHandle'):
			del self.consoleHandle
		try:
			winKernel.freeConsole()
		except:
			pass

	def isConsoleDead(self):
		num=winKernel.getConsoleProcessList((ctypes.c_int*2)(),2)
		if num<2:
			return True
		else:
			return False

	def consoleEventHook(self,handle,eventID,window,objectID,childID,threadID,timestamp):
		if window!=self.windowHandle:
			return
		self.text_reviewOffset=self.text_caretOffset
		if eventID!=winUser.EVENT_CONSOLE_CARET:
			self.lastConsoleEvent=eventID
		#audio.speakMessage("event %d"%eventID)

	def monitorThread(self):
		try:
			#tones.beep(440,200)
			update_timer=0
			checkDead_timer=0
			while self.keepMonitoring:
				if self.lastConsoleEvent:
					consoleEvent=self.lastConsoleEvent
					self.lastConsoleEvent=None
					update_timer=1
				if update_timer>0:
					update_timer+=1
				if update_timer>=4:
					update_timer=0
					newLines=self.consoleVisibleLines
					newText=self.calculateNewText(newLines,self.prevConsoleVisibleLines).strip()
					if len(newText)>0 and (not consoleEvent==winUser.EVENT_CONSOLE_UPDATE_SIMPLE or (self.lastConsoleEvent or len(newText)>1)):
						audio.speakText(newText)
					self.prevConsoleVisibleLines=newLines
				if checkDead_timer>=10:
					checkDead_timer=0
					if self.isConsoleDead():
						self.disconnectConsole()
				checkDead_timer+=1
				time.sleep(0.01)
			#tones.beep(880,200)
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

	def _get_consoleVisibleLines(self):
		if not hasattr(self,"consoleHandle"):
			return []
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		top=info.windowRect.top
		bottom=info.windowRect.bottom
		lines=[]
		consoleHorizontalLength=self.getConsoleHorizontalLength()
		consoleHandle=self.consoleHandle
		func=winKernel.readConsoleOutputCharacter
		return [func(consoleHandle,consoleHorizontalLength,0,lineNum) for lineNum in xrange(top,bottom+1)]

	def event_nameChange(self):
		pass

	def event_gainFocus(self):
		super(NVDAObject_winConsole,self).event_gainFocus()
		self.connectConsole()
		self.text_reviewOffset=self.text_caretOffset
		for line in (x for x in self.consoleVisibleLines if not x.isspace()):
			audio.speakText(line)
		self.prevConsoleVisibleLines=self.consoleVisibleLines

	def event_looseFocus(self):
		self.disconnectConsole()

	def calculateNewText(self,newLines,oldLines):
		newText=""
		diffLines=[x for x in list(difflib.ndiff(oldLines,newLines)) if (x[0] in ['+','-'])] 
		for lineNum in xrange(len(diffLines)):
			if diffLines[lineNum][0]=="+":
				text=diffLines[lineNum][2:]
				if not diffLines[lineNum][2:].isspace() and (lineNum>0) and (diffLines[lineNum-1][0]=="-"):
					start=0
					end=len(text)
					for pos in xrange(len(text)):
						if diffLines[lineNum][2:][pos]!=diffLines[lineNum-1][2:][pos]:
							start=pos
							break
					for pos in xrange(len(text)-1,0,-1):
						if diffLines[lineNum][2:][pos]!=diffLines[lineNum-1][2:][pos]:
							end=pos+1
							break
					text=text[start:end]
				if len(text)>0 and not text.isspace():
					newText=" ".join([newText,text])
			#time.sleep(0.001)
		return newText

	def script_protectConsoleKillKey(self,keyPress,nextScript):
		self.disconnectConsole()
		sendKey(keyPress)
		time.sleep(0.01)
		self.connectConsole()
		self.lastConsoleEvent=winUser.EVENT_CONSOLE_UPDATE_REGION

[NVDAObject_winConsole.bindKey(keyName,scriptName) for keyName,scriptName in [
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
