#winConsoleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2018 NV Access Limited, Babbage B.V.

import gui
import winUser
import winKernel
import wincon
from colors import RGB
import eventHandler
from logHandler import log
import speech
import textInfos
import api
import config
import locationHelper
from typing import (
	Optional,
	Dict,
)

"""
Handler for NVDA's legacy Windows Console support,
used in situations where UIA isn't available.
"""

#: How often to check whether the console is dead (in ms).
CHECK_DEAD_INTERVAL = 100

consoleObject=None #:The console window that is currently in the foreground.
consoleWinEventHookHandles=[] #:a list of currently registered console win events.
consoleOutputHandle=None
checkDeadTimer=None

CONSOLE_COLORS_TO_RGB=( #http://en.wikipedia.org/wiki/Color_Graphics_Adapter
	RGB(0x00,0x00,0x00), #black
	RGB(0x00,0x00,0xAA), #blue
	RGB(0x00,0xAA,0x00), #green
	RGB(0x00,0xAA,0xAA), #cyan
	RGB(0xAA,0x00,0x00), #red
	RGB(0xAA,0x00,0xAA), #magenta
	RGB(0xAA,0x55, 0x00), #brown
	RGB(0xAA,0xAA,0xAA), #white
	RGB(0x55,0x55,0x55), #gray
	RGB(0x55,0x55,0xFF), #light blue
	RGB(0x55,0xFF,0x55), #light green
	RGB(0x55,0xFF,0xFF), #light cyan
	RGB(0xFF,0x55,0x55), #light red
	RGB(0xFF,0x55,0xFF), #light magenta
	RGB(0xFF,0xFF,0x55), #yellow
	RGB(0xFF,0xFF,0xFF), #white (high intensity)
)

COMMON_LVB_UNDERSCORE=0x8000



@wincon.PHANDLER_ROUTINE
def _consoleCtrlHandler(event):
	if event in (wincon.CTRL_C_EVENT,wincon.CTRL_BREAK_EVENT):
		return True
	return False

def connectConsole(obj):
	global consoleObject, consoleOutputHandle, checkDeadTimer
	#Get the process ID of the console this NVDAObject is fore
	processID,threadID=winUser.getWindowThreadProcessID(obj.windowHandle)
	#Attach NVDA to this console so we can access its text etc
	try:
		wincon.AttachConsole(processID)
	except WindowsError as e:
		log.debugWarning("Could not attach console: %r"%e)
		return False
	wincon.SetConsoleCtrlHandler(_consoleCtrlHandler,True)
	consoleOutputHandle=winKernel.CreateFile(u"CONOUT$",winKernel.GENERIC_READ|winKernel.GENERIC_WRITE,winKernel.FILE_SHARE_READ|winKernel.FILE_SHARE_WRITE,None,winKernel.OPEN_EXISTING,0,None)                                                     
	#Register this callback with all the win events we need, storing the given handles for removal later
	for eventID in (winUser.EVENT_CONSOLE_CARET,winUser.EVENT_CONSOLE_UPDATE_REGION,winUser.EVENT_CONSOLE_UPDATE_SIMPLE,winUser.EVENT_CONSOLE_UPDATE_SCROLL,winUser.EVENT_CONSOLE_LAYOUT):
		handle=winUser.setWinEventHook(eventID,eventID,0,consoleWinEventHook,0,0,0)
		if not handle:
			raise OSError("could not register eventID %s"%eventID)
		consoleWinEventHookHandles.append(handle)
	consoleObject=obj
	checkDeadTimer=gui.NonReEntrantTimer(_checkDead)
	checkDeadTimer.Start(CHECK_DEAD_INTERVAL)
	return True

def disconnectConsole():
	global consoleObject, consoleOutputHandle, consoleWinEventHookHandles, checkDeadTimer
	if not consoleObject:
		log.debugWarning("console was not connected")
		return False
	checkDeadTimer.Stop()
	checkDeadTimer=None
	#Unregister any win events we are using
	for handle in consoleWinEventHookHandles:
		winUser.unhookWinEvent(handle)
	consoleEventHookHandles=[]
	consoleObject.stopMonitoring()
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
	# Every console should have at least one process associated with it.
	# This console should have two if NVDA is also connected.
	# If there is only one, it must be NVDA alone, so it is dead.
	processList=wincon.GetConsoleProcessList(2)
	return len(processList) < 2

def _checkDead():
	try:
		if isConsoleDead():
			# We must disconnect NVDA from this console so it can close.
			disconnectConsole()
	except:
		log.exception()

def getConsoleVisibleLines():
	consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
	topLine=consoleScreenBufferInfo.srWindow.Top
	lineCount=(consoleScreenBufferInfo.srWindow.Bottom-topLine)+1
	lineLength=consoleScreenBufferInfo.dwSize.x
	text=wincon.ReadConsoleOutputCharacter(consoleOutputHandle,lineCount*lineLength,0,topLine)
	newLines=[text[x:x+lineLength] for x in range(0,len(text),lineLength)]
	return newLines

@winUser.WINEVENTPROC
def consoleWinEventHook(handle,eventID,window,objectID,childID,threadID,timestamp):
	from NVDAObjects.behaviors import KeyboardHandlerBasedTypedCharSupport
	#We don't want to do anything with the event if the event is not for the window this console is in
	if window!=consoleObject.windowHandle:
		return
	if eventID==winUser.EVENT_CONSOLE_CARET and not eventHandler.isPendingEvents("caret",consoleObject):
		eventHandler.queueEvent("caret",consoleObject)
	# It is safe to call this event from this callback.
	# This avoids an extra core cycle.
	consoleObject.event_textChange()
	if eventID==winUser.EVENT_CONSOLE_UPDATE_SIMPLE:
		x=winUser.GET_X_LPARAM(objectID)
		y=winUser.GET_Y_LPARAM(objectID)
		consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
		if (
			not isinstance(consoleObject, KeyboardHandlerBasedTypedCharSupport)
			and x < consoleScreenBufferInfo.dwCursorPosition.x
			and (
				y == consoleScreenBufferInfo.dwCursorPosition.y
				or y == consoleScreenBufferInfo.dwCursorPosition.y+1
			)
		):
			eventHandler.queueEvent("typedCharacter",consoleObject,ch=chr(winUser.LOWORD(childID)))

def initialize():
	pass

def terminate():
	if consoleObject:
		disconnectConsole()

class WinConsoleTextInfo(textInfos.offsets.OffsetsTextInfo):

	_cache_consoleScreenBufferInfo=True
	def _get_consoleScreenBufferInfo(self):
		return wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)

	def _offsetFromConsoleCoord(self,x,y):
		consoleScreenBufferInfo=self.consoleScreenBufferInfo
		val=y-consoleScreenBufferInfo.srWindow.Top
		val*=consoleScreenBufferInfo.dwSize.x
		val+=x
		return val

	def _consoleCoordFromOffset(self,offset):
		consoleScreenBufferInfo=self.consoleScreenBufferInfo
		x=offset%consoleScreenBufferInfo.dwSize.x
		y=offset-x
		# #9641: add another slash because this is an integer, otherwise int/float conflict is seen and backspacing fails.
		y//=consoleScreenBufferInfo.dwSize.x
		y+=consoleScreenBufferInfo.srWindow.Top
		return x,y

	def _getOffsetFromPoint(self,x,y):
		consoleScreenBufferInfo = self.consoleScreenBufferInfo
		screenLeft, screenTop, screenWidth, screenHeight = self.obj.location
		relativeX = x - screenLeft
		relativeY = y - screenTop
		lineLength = (consoleScreenBufferInfo.srWindow.Right + 1) - consoleScreenBufferInfo.srWindow.Left
		numLines = (consoleScreenBufferInfo.srWindow.Bottom + 1) - consoleScreenBufferInfo.srWindow.Top
		characterWidth = screenWidth // lineLength
		characterHeight = screenHeight // numLines
		characterX = (relativeX // characterWidth) + consoleScreenBufferInfo.srWindow.Left
		characterY = (relativeY // characterHeight) + consoleScreenBufferInfo.srWindow.Top
		return self._offsetFromConsoleCoord(characterX,characterY)

	def _getPointFromOffset(self,offset):
		consoleScreenBufferInfo = self.consoleScreenBufferInfo
		characterX, characterY = self._consoleCoordFromOffset(offset)
		screenLeft, screenTop, screenWidth, screenHeight = self.obj.location
		lineLength = (consoleScreenBufferInfo.srWindow.Right + 1)- consoleScreenBufferInfo.srWindow.Left
		numLines = (consoleScreenBufferInfo.srWindow.Bottom + 1) - consoleScreenBufferInfo.srWindow.Top
		characterWidth = screenWidth // lineLength
		characterHeight = screenHeight // numLines
		relativeX = (characterX - consoleScreenBufferInfo.srWindow.Left) * characterWidth
		relativeY = (characterY - consoleScreenBufferInfo.srWindow.Top) * characterHeight
		x = relativeX + screenLeft
		y = relativeY + screenTop
		return locationHelper.Point(x,y)

	def _getCaretOffset(self):
		consoleScreenBufferInfo=self.consoleScreenBufferInfo
		return self._offsetFromConsoleCoord(consoleScreenBufferInfo.dwCursorPosition.x,consoleScreenBufferInfo.dwCursorPosition.y)

	def _getSelectionOffsets(self):
		selInfo=wincon.GetConsoleSelectionInfo()
		if selInfo.dwFlags&wincon.CONSOLE_SELECTION_NOT_EMPTY:
			start=self._offsetFromConsoleCoord(selInfo.srSelection.Left,selInfo.srSelection.Top)
			end=self._offsetFromConsoleCoord(selInfo.srSelection.Right,selInfo.srSelection.Bottom)
		else:
			start=end=self._getCaretOffset()
		return start,end

	def getTextWithFields(self, formatConfig: Optional[Dict] = None) -> textInfos.TextInfo.TextWithFieldsT:
		commands=[]
		if self.isCollapsed:
			return commands
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		left,top=self._consoleCoordFromOffset(self._startOffset)
		right,bottom=self._consoleCoordFromOffset(self._endOffset-1)
		rect=wincon.SMALL_RECT(left,top,right,bottom)
		if bottom-top>0: #offsets span multiple lines
			rect.Left=0
			rect.Right=self.consoleScreenBufferInfo.dwSize.x-1
			length=self.consoleScreenBufferInfo.dwSize.x*(bottom-top+1)
		else:
			length=self._endOffset-self._startOffset
		buf=wincon.ReadConsoleOutput(consoleOutputHandle, length, rect)
		if bottom-top>0:
			buf=buf[left:len(buf)-(self.consoleScreenBufferInfo.dwSize.x-right)+1]
		lastAttr=None
		lastText=[]
		boundEnd=self._startOffset
		for i,c in enumerate(buf):
			if self._startOffset+i==boundEnd:
				field,(boundStart,boundEnd)=self._getFormatFieldAndOffsets(boundEnd,formatConfig)
				if lastText:
					commands.append("".join(lastText))
					lastText=[]
				commands.append(textInfos.FieldCommand("formatChange",field))
			if not c.Attributes==lastAttr:
				formatField=textInfos.FormatField()
				if formatConfig['reportColor']:
					formatField["color"]=CONSOLE_COLORS_TO_RGB[c.Attributes&0x0f]
					formatField["background-color"]=CONSOLE_COLORS_TO_RGB[(c.Attributes>>4)&0x0f]
				if formatConfig['reportFontAttributes'] and c.Attributes&COMMON_LVB_UNDERSCORE:
					formatField['underline']=True
				if formatField:
					if lastText:
						commands.append("".join(lastText))
						lastText=[]
					command=textInfos.FieldCommand("formatChange", formatField)
					commands.append(command)
				lastAttr=c.Attributes
			lastText.append(c.Char)
		commands.append("".join(lastText))
		return commands

	def _getTextRange(self,start,end):
		startX,startY=self._consoleCoordFromOffset(start)
		return wincon.ReadConsoleOutputCharacter(consoleOutputHandle,end-start,startX,startY)

	def _getLineOffsets(self,offset):
		consoleScreenBufferInfo=self.consoleScreenBufferInfo
		x,y=self._consoleCoordFromOffset(offset)
		x=0
		start=self._offsetFromConsoleCoord(x,y)
		end=start+consoleScreenBufferInfo.dwSize.x
		return start,end

	def _getLineNumFromOffset(self,offset):
		consoleScreenBufferInfo=self.consoleScreenBufferInfo
		x,y=self._consoleCoordFromOffset(offset)
		return y-consoleScreenBufferInfo.srWindow.Top

	def _getStoryLength(self):
		consoleScreenBufferInfo=self.consoleScreenBufferInfo
		return consoleScreenBufferInfo.dwSize.x*((consoleScreenBufferInfo.srWindow.Bottom+1)-consoleScreenBufferInfo.srWindow.Top)

	def _get_clipboardText(self):
		return "\r\n".join(block.rstrip() for block in self.getTextInChunks(textInfos.UNIT_LINE))
