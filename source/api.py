#api.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import pyAA
import difflib
import win32gui
import win32com.client
import debug
import globalVars
import dictionaries
import audio
from config import conf
import appModules
import gui
import NVDAObjects
import virtualBuffer

# Initialise WMI; required for getProcessName.
_wmi = win32com.client.GetObject('winmgmts:')

#User functions

def quit():
	globalVars.stayAlive=False

def showGui():
	gui.showGui()

def getCurrentAppModule():
	return appModules.current

def getNVDAObjectByLocator(window,objectID,childID):
	accObject=getMSAAObjectFromEvent(window,objectID,childID)
	if not accObject:
		return None
	obj=NVDAObjects.NVDAObject(accObject)
	if not obj:
		return None
	return obj

def getNVDAObjectByPoint(point):
	accObject=getMSAAObjectFromPoint(point)
	if not accObject:
		return None
	obj=NVDAObjects.NVDAObject(accObject)
	if not obj:
		return None
	return obj

def getFocusObject():
	return globalVars.focusObject

def getFocusLocator():
	return globalVars.focus_locator

def setFocusObjectByLocator(window,objectID,childID):
	if (window,objectID,childID)==getFocusLocator():
		return False
	focusObject=getNVDAObjectByLocator(window,objectID,childID)
	if not focusObject:
		return False
	globalVars.focus_locator=(window,objectID,childID)
	globalVars.focusObject=focusObject
	if globalVars.navigatorTracksFocus:
		setNavigatorObject(focusObject)
	return True

def getVirtualBuffer():
	return globalVars.virtualBuffer

def setVirtualBuffer(window):
	v=virtualBuffer.virtualBuffer(window)
	globalVars.virtualBuffer=v
	globalVars.virtualBufferCursor=v.getCaretIndex()

def getVirtualBufferCursor():
	return globalVars.virtualBufferCursor


def setVirtualBufferCursor(index):
	globalVars.virtualBufferCursor=index


def isDecendantWindow(parent,child):
	if (parent==child) or win32gui.IsChild(parent,child):
		return True
	else:
		return False


def getNavigatorObject():
	return globalVars.navigatorObject

def setNavigatorObject(obj):
	globalVars.navigatorObject=obj
def keyHasScript(keyPress):
	if getCurrentAppModule().keyMap.has_key(keyPress):
		return True
	if getFocusObject().keyMap.has_key(keyPress):
		return True
	return False

def executeScript(keyPress):
	script=getCurrentAppModule().keyMap.get(keyPress,None)
	if not script:
		script=getFocusObject().keyMap.get(keyPress,None)
	if script:
		try:
			script(keyPress)
			return True
		except:
			audio.speakMessage("Error executing script %s bound to key %s"%(script.__name__,str(keyPress)))
			debug.writeException("Error executing script %s bound to key %s"%(script.__name__,str(keyPress)))
			return False

def eventExists(name,locator):
	if getCurrentAppModule().__dict__.has_key("event_%s"%name):
		return True
	focusLocator=getFocusLocator()
	focusObject=getFocusObject()
	if (locator==focusLocator) and hasattr(focusObject,"event_%s"%name):
		return True
	return False

def executeEvent(name,locator):
	if (name=="caret") and (locator[0]!=getFocusLocator()[0]):
		setFocusObjectByLocator(locator[0],locator[1],locator[2])
	event=getCurrentAppModule().__dict__.get("event_%s"%name,None)
	if event:
		try:
			apply(event,locator)
			return True
		except:
			audio.speakMessage("Error executing event %s from appModule"%event.__name__)
			debug.writeException("Error executing event %s from appModule"%event.__name__)
			return False
	thisObj=getNVDAObjectByLocator(locator[0],locator[1],locator[2])
	focusLocator=getFocusLocator()
	focusObject=getFocusObject()
	if locator==focusLocator and hasattr(focusObject,"event_%s"%name): 
		event=getattr(focusObject,"event_%s"%name)
		try:
			event()
			return True
		except:
			audio.speakMessage("Error executing event %s from focusObject"%event.__name__)
			debug.writeException("Error executing event %s from focusObject"%event.__name__)
			return False
	elif thisObj and hasattr(thisObj,"event_%s"%name):
		event=getattr(thisObj,"event_%s"%name)
		try:
			event()
			return True
		except:
			audio.speakMessage("Error executing event %s from object"%event.__name__)
			debug.writeException("Error executing event %s from object"%event.__name__)
			return False

def getObjectGroupName(accObject):
	try:
		(objectLeft,objectTop,objectRight,objectBottom)=accObject.GetLocation()
	except:
		debug.writeError("api.getObjectGrouping: fialed to get location of object %s"%accObject)
		return None
	try:
		while (accObject is not None) and (accObject.GetRole()!=pyAA.Constants.ROLE_SYSTEM_GROUPING):
			accObject=getObjectPrevious(accObject)
			if accObject is None:
				debug.writeError("api.getObjectGroupName: no more previous objects")
				return None
		if accObject.GetRole()==pyAA.Constants.ROLE_SYSTEM_GROUPING:
			(groupLeft,groupTop,groupRight,groupBottom)=accObject.GetLocation()
			if (objectLeft>=groupLeft) and (objectTop>=groupTop) and (objectRight<=groupRight) and (objectBottom<=groupBottom):
				return accObject.GetName()
			else:
				debug.writeError("api.getObjectGroupName: object is not with in bounds of cloest grouping")
				return None
		debug.writeError("api.getObjectGroupName: could not find a grouping on this level")
		return None
	except:
		debug.writeError("api.getObjectGroupName: error finding group name")
		return None

def getMSAAObjectFromPoint(position):
	try:
		return pyAA.AccessibleObjectFromPoint(position)
	except:
		debug.writeException("api.getObjectFromPoint")
		return None

def getForegroundWindow():
	return win32gui.GetForegroundWindow()

def getMSAAObjectFromEvent(window,objectID,childID):
	try:
		accObject=pyAA.AccessibleObjectFromEvent(window,objectID,childID)
	except:
		debug.writeError("api.getObjectFromEvent: failed to get object with window %d, object ID %d, and child ID %d"%(window,objectID,childID))
		return None
	return accObject

def getWindowLocation(window):
	return win32gui.GetClientRect(window)

def getWindowControlID(window):
	return win32gui.GetWindowLong(window)

def getWindowClass(window):
	return win32gui.GetClassName(window)

def getWindowTextLength(window):
	textLength=win32gui.SendMessage(window,win32con.WM_GETTEXTLENGTH,0,0)
	if (textLength is None) or (textLength<0):
		debug.writeError("api.getWindowTextLength: failed to get text length from window")
		return None
	return textLength

def getWindowText(window):
	textLength=getWindowTextLength(window)
	if textLength is None:
		debug.writeError("api.getWindowText: No text because text length is None")
		return None
	if textLength==0:
		return ""
	textBuf=win32gui.PyMakeBuffer(textLength)
	win32gui.SendMessage(window,win32con.WM_GETTEXT,textLength+1,textBuf)
	(bufAddr,bufLen)=win32gui.PyGetBufferAddressAndLen(textBuf)
	text=win32gui.PyGetString(bufAddr,bufLen)
	if len(text)!=textLength:
		debug.writeError("text is not predicted length (\"%s\")"%text)
		return None
	return text

def getWindowLineCount(window):
	lineCount=win32gui.SendMessage(window,win32con.EM_GETLINECOUNT,0,0)
	if (lineCount is None) or (lineCount<0):
		debug.writeError("api.getWindowLineCount: failed to get line count")
		return None
	return lineCount

def getWindowLinePosition(window,lineNum):
	lineCount=getWindowLineCount(window)
	if (lineCount is None) or ((lineNum+1)>lineCount):
		debug.writeError("api.getWindowLinePosition: line number is not in range of windows line count")
		return None
	curPos=win32gui.SendMessage(window,win32con.EM_LINEINDEX,lineNum,0)
	if (curPos is None) or (curPos<0):
		debug.writeError("api.getWindowLinePosition: failed to get position from line number %d, window %d"%(lineNum,window))
		return None
	return curPos

def getWindowLineLength(window,lineNum):
	lineCount=getWindowLineCount(window)
	if (lineCount is None) or ((lineNum+1)>lineCount):
		debug.writeError("api.getWindowLineLength: lineNum %d is not in range of lineCount %d"%((lineNum+1),lineCount))
		return None
	curPos=getWindowLinePosition(window,lineNum)
	if (curPos is None) or (curPos<0):
		debug.writeError("api.getWindowLine: failed to get position of line")
		return None
	lineLength=win32gui.SendMessage(window,win32con.EM_LINELENGTH,curPos,0)
	if (lineLength is None) or (lineLength<0):
		debug.writeError("api.getWindowLine: line length invalid or negative (line number %d, line position %d"%(lineNum,curPos))
		return None
	return lineLength

def getWindowLine(window,lineNum):
	if lineNum is None:
		return None
	lineCount=getWindowLineCount(window)
	if (lineCount is None) or ((lineNum+1)>lineCount):
		debug.writeError("api.getWindowLine: line number is not in range of windows line count")
		return None
	lineLength=getWindowLineLength(window,lineNum)
	if lineLength is None:
		debug.writeError("api.getWindowLine: line length is not valid")
		return None
	if lineLength==0:
		return None
	lineBuf=struct.pack('i',lineLength+1)
	lineBuf=lineBuf+"".ljust(lineLength-2)
	res=win32gui.SendMessage(window,win32con.EM_GETLINE,lineNum,lineBuf)
	#if res<lineLength:
	#	debug.writeError("api.getWindowLine: could not receive text of line")
	#	return None
	line="%s"%lineBuf[0:lineLength]
	return line

def getWindowLineNumber(window,curPosition):
	textLength=getWindowTextLength(window)
	if (textLength is None) or (textLength==0):
		debug.writeError("api.getWindowLineNumber: invalid text length")
		return None
	if curPosition>textLength:
		debug.writeError("api.getWindowLineNumber: curPosition %d is greater than textLength %d"%(curPosition,textLength))
		return None
	lineNum=win32gui.SendMessage(window,win32con.EM_LINEFROMCHAR,curPosition,0)
	if (lineNum is None) or (lineNum<0):
		debug.writeError("api.getWindowLineNumber: failed to get line number from window")
		return None
	return lineNum

def getWindowCharacter(window,position):
	lineCount=getWindowLineCount(window)
	if (lineCount is not None) and (lineCount>0): 
		lineNum=getWindowLineNumber(window,position)
		if lineNum is None:
			debug.writeError("api.getWindowCharacter: could not get line number from position")
			return None
		line=getWindowLine(window,lineNum)
		if line is None:
			debug.writeError("api.getWindowCharacter: could not get text of line")
			return None
		linePosition=getWindowLinePosition(window,lineNum)
		if linePosition is None:
			debug.writeError("api.getWindowCharacter: failed to get line position")
			return None
		relativePosition=position-linePosition
		if (relativePosition<0) or (relativePosition>=len(line)):
			debug.writeError("api.getWindowCharacter: relativePosition %d is wrong (linePosition %d, position %d)"%(relativePosition,linePosition,position))
			return None
		return line[relativePosition]
	else:
		textLength=getWindowTextLength(window)
		if (textLength is None) or (textLength==0):
			debug.writeError("api.getWindowCharacter: invalid text length")
			return None
		if position>=textLength:
			debug.writeError("api.getWindowCharacter: position %d is greater than textLength %d"%(position,textLength))
			return None
		text=getWindowText(window)
		if text is None:
			debug.writeError("api.getWindowCharacter: text is invalid")
			return None
		return text[position]

def getWindowCharacters(window,start,end):
	textLength=getWindowTextLength(window)
	if (textLength is None) or (textLength==0):
		debug.writeError("api.getWindowCharacters: text length is 0 or invalid")
		return None
	if (start is None) or (end is None) or (start==end)or (start>textLength) or (end>textLength):
		debug.writeError("api.getWindowCharacters: start or end is invalid (start %d, end %d, text length %d)"%(start,end,textLength))
		return None
	text=getWindowText(window)
	if text is None:
		debug.writeError("api.getWindowCharacters: invalid text")
		return None
	return text[start:end]

def getWindowWord(window,position):
	whitespace=['\n','\r','\t',' ','\0']
	lineCount=getWindowLineCount(window)
	if (lineCount is not None) and (lineCount>0): 
		lineNum=getWindowLineNumber(window,position)
		if lineNum is None:
			debug.writeError("api.getWindowWord: could not get line number from position")
			return None
		line=getWindowLine(window,lineNum)
		if line is None:
			debug.writeError("api.getWindowWord: could not get text of line")
			return None
		linePosition=getWindowLinePosition(window,lineNum)
		if linePosition is None:
			debug.writeError("api.getWindowWord: failed to get line position")
			return None
		relativePosition=position-linePosition
		if (relativePosition<0) or (relativePosition>len(line)):
			debug.writeError("api.getWindowWord: relativePosition %d is wrong (linePosition %d, position %d)"%(relativePosition,linePosition,position))
			return None
		wordEnd=relativePosition
		while (wordEnd<len(line)) and (line[wordEnd] not in whitespace):
			wordEnd+=1
		debug.writeMessage("line: %s"%line)
		debug.writeMessage("word: %s"%line[relativePosition:(wordEnd+1)])
		return line[relativePosition:(wordEnd+1)]
	else:
		textLength=getWindowTextLength(window)
		if (textLength is None) or (textLength==0):
			debug.writeError("api.getWindowWord: invalid text length")
			return None
		if position>=textLength:
			debug.writeError("api.getWindowWord: position %d is greater than textLength %d"%(position,textLength))
			return None
		text=getWindowText(window)
		if text is None:
			debug.writeError("api.getWindowWord: text is invalid")
			return None
		wordEnd=position
		while (wordEnd<len(text)) and (text[wordEnd] not in whitespace):
			wordEnd+=1
		return text[position:(wordEnd+1)]

def getWindowSelectionPoints(window):
	textLength=getWindowTextLength(window)
	if textLength is None:
		debug.writeError("api.getWindowSelectionPoints: invalid text length")
		return None
	word=win32gui.SendMessage(window,win32con.EM_GETSEL,0,0)
	if word<0:
		debug.writeError("api.getWindowSelectionPoints: got invalid selection word from window")
		return None
	a=win32api.HIWORD(word)
	b=win32api.LOWORD(word)
	start=min(a,b)
	end=max(a,b)
	if start==end:
		debug.writeError("api.getWindowSelectionPoints: no selection because start and end are the same")
		return None
	return (start,end)

def getWindowInsertionPoint(window):
	textLength=getWindowTextLength(window)
	if textLength is None:
		debug.writeError("api.getWindowInsertionPoint: invalid text length")
		return None
	word=win32gui.SendMessage(window,win32con.EM_GETSEL,0,0)
	if word<0:
		debug.writeError("api.getWindowInsertionPoint: got invalid selection word from window")
		return None
	point=win32api.HIWORD(word)
	return point

def getStringDifference(newSTR,oldSTR,checkLength=False):
	if oldSTR is None:
		oldSTR="\0"
	if newSTR is None:
		newSTR="\0"
	oldSTR_length=len(oldSTR)
	newSTR_length=len(newSTR)
	newChar=None
	oldChar=None
	diff_start=None
	diff_end=None
	for index in range(newSTR_length):
		newChar=newSTR[index]
		if index<oldSTR_length:
			oldChar=oldSTR[index]
		else:
			oldChar="\0"
		if newChar!=oldChar:
			diff_start=index
			break
	for index in range(newSTR_length):
		backIndex=(index+1)*-1
		newChar=newSTR[backIndex]
		if index<oldSTR_length:
			oldChar=oldSTR[backIndex]
		else:
			oldChar="\0"
		if newChar!=oldChar:
			diff_end=newSTR_length-index
			break
	if (diff_start is not None) and (diff_end is not None):
		return newSTR[diff_start:diff_end]
	else:
		return ""

def makeStateList(stateText):
	stateList=stateText.split("+")
	return stateList

def getProcessName(processID):
	result  =  _wmi.ExecQuery("select * from Win32_Process where ProcessId=%d" % processID[0])
	if len(result) > 0:
		return result[0].Properties_('Name').Value
	else:
		return ""

def strNewText(a,b):
	gen=difflib.ndiff(a,b)
	newText=""
	block=""
	for line in gen:
		if line[0]=="+":
			block+=line[2]
		elif block:
			newText+="%s "%block
			block=""
	return newText



