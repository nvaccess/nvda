#winConsoleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

import winUser
import winKernel
import wincon
import eventHandler
from logHandler import log
import speech
import queueHandler
import textInfos
import api

consoleObject=None #:The console window that is currently in the foreground.
consoleWinEventHookHandles=[] #:a list of currently registered console win events.
consoleOutputHandle=None

@wincon.PHANDLER_ROUTINE
def _consoleCtrlHandler(event):
	if event in (wincon.CTRL_C_EVENT,wincon.CTRL_BREAK_EVENT):
		return True
	return False

def connectConsole(obj):
	global consoleObject, consoleOutputHandle
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
	#Register this callback with all the win events we need, storing the given handles for removal later
	for eventID in (winUser.EVENT_CONSOLE_CARET,winUser.EVENT_CONSOLE_UPDATE_REGION,winUser.EVENT_CONSOLE_UPDATE_SIMPLE,winUser.EVENT_CONSOLE_UPDATE_SCROLL,winUser.EVENT_CONSOLE_LAYOUT):
		handle=winUser.setWinEventHook(eventID,eventID,0,consoleWinEventHook,0,0,0)
		if not handle:
			raise OSError("could not register eventID %s"%eventID)
		consoleWinEventHookHandles.append(handle)
	consoleObject=obj
	return True

def disconnectConsole():
	global consoleObject, consoleOutputHandle, consoleWinEventHookHandles
	if not consoleObject:
		log.debugWarning("console was not connected")
		return False
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
	#We don't want to do anything with the event if the event is not for the window this console is in
	if window!=consoleObject.windowHandle:
		return
	if eventID==winUser.EVENT_CONSOLE_CARET:
		eventHandler.queueEvent("caret",consoleObject)
	consoleScreenBufferInfo=wincon.GetConsoleScreenBufferInfo(consoleOutputHandle)
	# It is safe to call this event from this RPC thread.
	# This avoids an extra core cycle.
	consoleObject.event_textChange()
	if eventID==winUser.EVENT_CONSOLE_UPDATE_SIMPLE:
		x=winUser.LOWORD(objectID)
		y=winUser.HIWORD(objectID)
		if x<consoleScreenBufferInfo.dwCursorPosition.x and (y==consoleScreenBufferInfo.dwCursorPosition.y or y==consoleScreenBufferInfo.dwCursorPosition.y+1):  
			queueHandler.queueFunction(queueHandler.eventQueue,speech.speakTypedCharacters,unichr(winUser.LOWORD(childID)))

def initialize():
	pass

def terminate():
	if consoleObject:
		disconnectConsole()

class WinConsoleTextInfo(textInfos.offsets.OffsetsTextInfo):

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

	def _get_clipboardText(self):
		return "\r\n".join(block.rstrip() for block in self.getTextInChunks(textInfos.UNIT_LINE))
