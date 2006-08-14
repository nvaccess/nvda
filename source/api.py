#api.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import struct
import pyAA
import win32api
import win32con
import win32com.client
import win32gui
import debug
import globalVars
import dictionaries
from stateUtils import *

# Initialise WMI; required for getProcessName.
_wmi = win32com.client.GetObject('winmgmts:')

#User functions

def quit():
	globalVars.stayAlive=False

def getSpeakableKeyList(keyList):
	keyName=""
	for key in keyList:
		keyName="%s %s"%(keyName,key)
	return keyName

def getRoleName(role):
	if dictionaries.roleNames.has_key(role) is True:
		return dictionaries.roleNames[role]
	else:
		return role

def getStateNames(states,opposite=False):
	str=""
	for state in createStateList(states):
		str="%s %s"%(str,getStateName(state,opposite=opposite))
	return str

def getStateName(state,opposite=False):
	if dictionaries.stateNames.has_key(state):
		name=dictionaries.stateNames[state]
	else:
		name=state
	if opposite is True:
		name="not %s"%name
	return name

def getObjectName(accObject):
	try:
		res=accObject.GetName()
	except:
		debug.writeError("api.getObjectName: failed to get name from object %s, but trying to get window name instead"%accObject)
		res=None
	if res is None:
		try:
			window=accObject.Window
		except:
			debug.writeError("api.getObjectName: failed to get window from object %s"%accObject)
			return None
		res=win32gui.GetWindowText(window)
	return res

def getObjectValue(accObject):
	try:
		return accObject.GetValue()
	except:
		debug.writeError("api.getObjectValue: failed to get value from object %s"%accObject)
		return None

def getObjectRole(accObject):
	try:
		return accObject.GetRole()
	except:
		debug.writeError("api.getObjectRole: failed to get role from object %s"%accObject)
		return None

def getObjectRoleText(accObject):
	try:
		return accObject.GetRoleText()
	except:
		debug.writeError("api.getObjectRoleText: failed to get role text from object %s"%accObject)
		return None

def getObjectStates(accObject):
	try:
		return accObject.GetState()
	except:
		debug.writeError("api.getObjectStates: failed to get states from object %s"%accObject)
		return None

def getObjectStateText(accObject):
	try:
		text=accObject.GetStateText()
	except:
		debug.writeError("api.getObjectStateText: failed to get state text for object %s"%accObject)
		return None
	return text

def getObjectDescription(accObject):
	try:
		return accObject.GetDescription()
	except:
		debug.writeError("api.getObjectDescription: failed to get description from object %s"%accObject)
		return None

def getObjectHelp(accObject):
	try:
		return accObject.GetHelp()
	except:
		debug.writeError("api.getObjectHelp: failed to get help from object %s"%accObject)
		return None

def getObjectKeyboardShortcut(accObject):
	try:
		return accObject.GetKeyboardShortcut()
	except:
		debug.writeError("api.getObjectKeyboardShortcut: failed to get keyboard shortcut from object %s"%accObject)
		return None

def getObjectProcessID(accObject):
	try:
		return accObject.ProcessID
	except:
		debug.writeError("api.getObjectProcessID: failed to get process ID from object %s"%accObject)
		return None

def getObjectPath(accObject):
	try:
		return accObject.GetPath()
	except:
		debug.writeError("api.getObjectPath: failed to get path from object %s"%accObject)
		return None

def getObjectLocation(accObject):
	try:
		return accObject.GetLocation()
	except:
		debug.writeError("api.getObjectLocation: failed to get location from object %s"%accObject)
		return None

def getObjectPositionInGroup(accObject):
	try:
		index=accObject.GetChildID()
	except:
		debug.writeError("api.getObjectPositionInGroup: failed to get child ID from object %s"%accObject)
		return None
	try:
		count=accObject.GetParent().GetChildCount()
	except:
		debug.writeError("api.getObjectPositionInGroup: failed to get parent's child count from object %s"%accObject)
		return None
	if index>0:
		return "%d of %d" % (index,count)

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

def getObjectClass(accObject):
	try:
		return accObject.GetClassName()
	except:
		debug.writeError("api.getObjectClass: failed to get class from object %s"%accObject)
		return None

def getObjectFromPoint(position):
	try:
		return pyAA.AccessibleObjectFromPoint(position)
	except:
		debug.writeException("api.getObjectFromPoint")
		return None

def objectHasFocus(accObject):
	try:
		states=accObject.GetState()
	except:
		debug.writeError("api.objectHasFocus: failed to get states for object %s"%accObject)
		return False
	if states&pyAA.Constants.STATE_SYSTEM_FOCUSED:
		return True
	else:
		return False

def getFocusWindow():
	return win32gui.GetFocus()

def getForegroundWindow():
	return win32gui.GetForegroundWindow()

def getObjectActiveChild(accObject):
	try:
		return accObject.GetFocus()
	except:
		debug.writeError("api.getObjectActiveChild: failed to get active child object from object %s"%accObject)
		return None

def getObjectFromEvent(window,objectID,childID):
	try:
		accObject=pyAA.AccessibleObjectFromEvent(window,objectID,childID)
	except:
		debug.writeError("api.getObjectFromEvent: failed to get object with window %d, object ID %d, and child ID %d"%(window,objectID,childID))
		return None
	return accObject

def getWindowFromObject(accObject):
	try:
		return accObject.Window
	except:
		debug.writeError("api.getWindowFromObject: failed to get window from object %s"%accObject)
		return None

def getObjectChildCount(accObject):
	try:
		return accObject.GetChildCount()
	except:
		debug.writeError("api.getObjectChildCount: failed to get child count from object %s"%accObject) 
		return None

def getObjectChildID(accObject):
	try:
		return accObject.GetChildID()
	except:
		debug.writeError("api.getObjectChildID: failed to get child ID from object %s"%accObject) 
		return None

def getObjectChildren(accObject):
	children=[]
	try:
		for child in accObject.GetChildren():
			if getObjectRole(child)==ROLE_SYSTEM_WINDOW:
				child=getObjectFromEvent(getWindowFromObject(child),-4,0)
			if child is not None:
				children.append(child)
	except:
		debug.writeError("api.getObjectChildren: exception in accObject.GetChildren()")
		return None
	if len(children)>0:
		return children
	else:
		return None

def getObjectSelectedChildren(accObject):
	try:
		return accObject.GetSelection()
	except:
		debug.writeError("api.getObjectSelectedChildren: failed to get selected items from object %s"%accObject) 
		return None

def getObjectParent(accObject):
	try:
		accObject=accObject.GetParent()
	except:
		debug.writeError("api.getObjectParent: failed to get parent object") 
		return None
	try:
		role=accObject.GetRole()
	except:
		debug.writeError("api.getObjectParent: failed to get role of object %s"%accObject)
		return None
	if role==pyAA.Constants.ROLE_SYSTEM_WINDOW:
		try:
			accObject=accObject.GetParent()
			accObject=pyAA.AccessibleObjectFromEvent(accObject.Window,pyAA.Constants.OBJID_CLIENT,0)
		except:
			debug.writeError("api.getObjectParent: failed to get client object of parent window")
			return None
	try:
		role=accObject.GetRole()
	except:
		debug.writeError("api.getObjectNext: failed to get role for next object")
		role=None
	if (role is not None) and (role>=0):
		return accObject
	else:
		return None

def getObjectNext(accObject):
	try:
		parentRole=accObject.GetParent().GetRole()
	except:
		parentRole=None
	if parentRole==pyAA.Constants.ROLE_SYSTEM_WINDOW:
		try:
			accObject=pyAA.AccessibleObjectFromEvent(accObject.GetParent().Navigate(pyAA.Constants.NAVDIR_NEXT).Window,pyAA.Constants.OBJID_CLIENT,0)
		except:
			debug.writeError("api.getObjectNext: failed to get next client object via parent window object")
			return None
	else:
		try:
			accObject=accObject.Navigate(pyAA.Constants.NAVDIR_NEXT)
		except:
			debug.writeError("api.getObjectNext: failed to get next object")
			return None
	try:
		role=accObject.GetRole()
	except:
		debug.writeError("api.getObjectNext: failed to get role for next object")
		role=None
	if (role is not None) and (role>=0):
		return accObject
	else:
		return None

def getObjectPrevious(accObject):
	try:
		parentRole=accObject.GetParent().GetRole()
	except:
		parentRole=None
	if parentRole==pyAA.Constants.ROLE_SYSTEM_WINDOW:
		try:
			accObject=pyAA.AccessibleObjectFromEvent(accObject.GetParent().Navigate(pyAA.Constants.NAVDIR_PREVIOUS).Window,pyAA.Constants.OBJID_CLIENT,0)
		except:
			debug.writeError("api.getObjectPrevious: failed to get previous client object via parent window object")
			return None
	else:
		try:
			accObject=accObject.Navigate(pyAA.Constants.NAVDIR_PREVIOUS)
		except:
			debug.writeError("api.getObjectPrevious: failed to get previous object")
			return None
	try:
		role=accObject.GetRole()
	except:
		debug.writeError("api.getObjectNext: failed to get role for next object")
		role=None
	if (role is not None) and (role>=0):
		return accObject
	else:
		return None

def getObjectFirstChild(accObject):
	o=None
	childID=getObjectChildID(accObject)
	if childID is None:
		debug.writeError("api.getObjectFirstChild: failed to get a child ID from object %s"%accObject)
		return None
	if childID>0:
		try:
			o=accObject.GetChild(childID)
		except:
			debug.writeError("api.getObjectFirstChild: failed to get a real object from child ID %d of object %s"%(childID,accObject))
			return None
	else:
		try:
			o=accObject.Navigate(pyAA.Constants.NAVDIR_FIRSTCHILD)
		except:
			debug.writeError("api.getObjectFirstChild: failed to get child object")
			return None
		role=getObjectRole(o)
		if role is None:
			debug.writeError("api.getObjectFirstChild: failed to get role from object %s"%accObject)
			return None
		if role==pyAA.Constants.ROLE_SYSTEM_WINDOW:
			try:
				o=pyAA.AccessibleObjectFromWindow(o.Window,pyAA.Constants.OBJID_CLIENT)
			except:
				debug.writeError("api.getObjectFirstChild: failed to get client object from window object")
				return None
	try:
		role=o.GetRole()
	except:
		debug.writeError("api.getObjectNext: failed to get role for next object")
		role=None
	if (role is not None) and (role>=0):
		return o
	else:
		return None

def getObjectLeft(accObject):
	try:
		accObject=accObject.Navigate(pyAA.Constants.NAVDIR_RIGHT)
	except:
		debug.writeError("api.getObjectRight: failed to get left object")
		return None


def getObjectRight(accObject):
	try:
		accObject=accObject.Navigate(pyAA.Constants.NAVDIR_RIGHT)
	except:
		debug.writeError("api.getObjectRight: failed to get right object")
		return None

def getObjectUp(accObject):
	try:
		accObject=accObject.Navigate(pyAA.Constants.NAVDIR_UP)
	except:
		debug.writeError("api.getObjectUp: failed to get upobject")
		return None

def getObjectDown(accObject):
	try:
		accObject=accObject.Navigate(pyAA.Constants.NAVDIR_DOWN)
	except:
		debug.writeError("api.getObjectDown: failed to get down object")
		return None

def doObjectDefaultAction(accObject):
	try:
		accObject.DoDefaultAction()
	except:
		debug.writeError("DoObjectDefaultAction: failed to do default action of object %s"%accObject) 
		return None

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

def getCharacter():
	(window,objectID,childID)=globalVars.focus_locator
	point=getWindowInsertionPoint(window)
	character=getWindowCharacter(window,point)
	return character

def getLine():
	(window,objectID,childID)=globalVars.focus_locator
	point=getWindowInsertionPoint(window)
	lineNum=getWindowLineNumber(window,point)
	line=getWindowLine(window,lineNum)
	return line

def getCaretIndex():
	(window,objectID,childID)=globalVars.focus_locator
	point=getWindowInsertionPoint(window)
	return point

def key(name):
	l = name.split("+")
	if len(l) >= 2:
		modifiers = frozenset(l[0:-1])
	else:
		modifiers = None
	return (modifiers, l[-1])
