#default.py
#The default app module for NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winsound
import pythoncom
from constants import *
import keyEventHandler
import globalVars
from api import *
import audio
from config import conf
import gui

lastFocusStates=None
lastMouseLocator=()
menuActive=False


speakBySound={
OBJECT_STATE:{STATE_SYSTEM_CHECKED:r"c:\windows\media\ding.wav"},
OBJECT_STATE_OFF:{STATE_SYSTEM_CHECKED:r"c:\windows\media\chord.wav"},
TEXT_LINE:{"":r"waves\line_blank.wav"}
}

def speakObject(accObject):
	global lastFocusStates
	window=getWindowFromObject(accObject)
	name=getObjectName(accObject)
	role=getObjectRole(accObject)
	if conf["presentation"]["reportClassOfAllObjects"] or (conf["presentation"]["reportClassOfClientObjects"] and (role==ROLE_SYSTEM_CLIENT)):
		className=getObjectClass(accObject)
	else:
		className=None
	roleName=getRoleName(role)
	states=getObjectStates(accObject)
	stateNames=""
	if states is not None:
		states=filterStates(states)
		stateNames=""
		for state in createStateList(states):
			stateNames="%s %s"%(stateNames,getStateName(state))
	if role==ROLE_SYSTEM_TEXT:
		selectionPoints=getWindowSelectionPoints(window)
		if selectionPoints is not None:
			value="selected %s"%getWindowCharacters(window,selectionPoints[0],selectionPoints[1])
		elif getWindowLineCount(window)>0:
			point=getWindowInsertionPoint(window)
			lineNum=getWindowLineNumber(window,point)
			value=getWindowLine(window,lineNum)
		elif getWindowTextLength(window)>0:
			value=getWindowText(window)
		else:
			value=""
	else:
		value=getObjectValue(accObject)
	description=getObjectDescription(accObject)
	if description==name:
		description=None
	help=getObjectHelp(accObject)
	if conf["presentation"]["reportKeyboardShortcuts"]:
		keyboardShortcut=getObjectKeyboardShortcut(accObject)
	else:
		keyboardShortcut=None
	position=getObjectPositionInGroup(accObject)
	if role!=ROLE_SYSTEM_GROUPING:
		groupName=getObjectGroupName(accObject)
	else:
		groupName=None
	audio.speakObjectProperties(groupName=groupName,name=name,className=className,roleName=roleName,stateNames=stateNames,value=value,description=description,help=help,keyboardShortcut=keyboardShortcut,position=position)

def sayLine():
	line=getLine()
	debug.writeMessage("line: \"%s\""%line)
	audio.speakText(line)

def sayCharacter():
	character=getCharacter()
	audio.speakSymbol(character)

def sayWord():
	(window,objectID,childID)=globalVars.focus_locator
	point=getWindowInsertionPoint(window)
	word=getWindowWord(window,point)
	audio.speakText(word)

def readDialogObjects(accObject):
	for o in accObject.GetChildren():
		if getObjectRole(o)==ROLE_SYSTEM_WINDOW:
			o=getObjectFromEvent(o.Window,-4,0)
		state=getObjectStates(o)
		if (not state&STATE_SYSTEM_OFFSCREEN) and (not state&STATE_SYSTEM_INVISIBLE):
			speakObject(o)
		if getObjectRole(o)==ROLE_SYSTEM_PROPERTYPAGE:
			readDialogObjects(o)

def event_moduleStart():
	pass

def event_mouseMove(position):
	global lastMouseLocator
	if conf["mouse"]["reportObjectUnderMouse"] is False:
		return 
	accObject=getObjectFromPoint(position)
	if accObject is None:
		return 
	window=getWindowFromObject(accObject)
	childID=getObjectChildID(accObject)
	if (window,childID)!=lastMouseLocator:
		audio.cancel()
		speakObject(accObject)
	lastMouseLocator=(window,childID)

def event_objectLocationChange(window,objectID,childID):
	if objectID==OBJID_CARET:
		event_caretChange(window,objectID,childID)

def event_caretChange(window,objectID,childID):
	setNavigatorPosition(getWindowInsertionPoint(window))

def event_foreground(window,objectID,childID):
	className=getWindowClass(window)
	if className=="Progman":
		return
	if className=="Shell_TrayWnd":
		return
	accObject=getObjectFromEvent(window,objectID,childID)
	setNavigatorObject(accObject)
	speakObject(accObject)
	if getObjectRole(accObject)==ROLE_SYSTEM_DIALOG:
		readDialogObjects(accObject)
	globalVars.focus_locator=(window,objectID,childID)

def event_menuStart(window,objectID,childID):
	global menuActive
	audio.cancel()
	if not menuActive:
		accObject=getObjectFromEvent(window,objectID,childID)
		role=getObjectRole(accObject)
		if (role!=ROLE_SYSTEM_MENUBAR) and (role!=ROLE_SYSTEM_MENUITEM) and (role!=ROLE_SYSTEM_MENUPOPUP):
			return
		menuActive=True
		event_focusObject(window,objectID,childID)
		accObject=getObjectFromEvent(window,objectID,childID)
		speakObject(getObjectFirstChild(accObject))

def event_menuEnd(window,objectID,childID):
	pass

def endMenu():
	global menuActive
	menuActive=False
	audio.cancel()
	audio.speakMessage("Leaving menus")

def event_maximize(window,objectID,childID):
	accObject=getObjectFromEvent(window,objectID,childID)
	audio.speakMessage("maximized")
	speakObject(accObject)

def event_minimize(window,objectID,childID):
	accObject=getObjectFromEvent(window,objectID,childID)
	audio.speakMessage("minimized")
	speakObject(accObject)

def event_switchStart(window,objectID,childID):
	audio.speakMessage("Task switcher")

def event_switchEnd(window,objectID,childID):
	pass

def event_createObject(window,objectID,childID):
	pass
def event_destroyObject(window,objectID,childID):
	pass

def event_focusObject(window,objectID,childID):
	global lastFocusStates, menuActive
	if (window,objectID,childID)==globalVars.focus_locator:
		return
	if (window==globalVars.focus_locator[0]) and (childID==0) and (globalVars.focus_locator[2]>0):
		return
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if menuActive and ((role!=ROLE_SYSTEM_MENUITEM) and (role!=ROLE_SYSTEM_MENUBAR) and (role!=ROLE_SYSTEM_MENUPOPUP)):
		endMenu()
	if (not menuActive) and ((role==ROLE_SYSTEM_MENUBAR) or (role==ROLE_SYSTEM_MENUITEM) or (role==ROLE_SYSTEM_MENUPOPUP)):
		return
	if not objectHasFocus(accObject):
		return
	speakObject(accObject)
	globalVars.focus_locator=(window,objectID,childID)
	lastFocusStates=getObjectStates(accObject)
	setNavigatorObject(accObject)
	point=getWindowInsertionPoint(window)
	if point is None:
		point=0
	setNavigatorPosition(point)

def event_hideObject(window,objectID,childID):
	pass

def event_showObject(window,objectID,childID):
	if objectID==-4:
		accObject=getObjectFromEvent(window,objectID,childID)
		if (conf["presentation"]["reportTooltips"] is True) and getObjectRole(accObject)==ROLE_SYSTEM_TOOLTIP:
			audio.speakObjectProperties(roleName=getRoleName(ROLE_SYSTEM_TOOLTIP),value=getObjectName(accObject))

def event_objectAcceleratorChange(window,objectID,childID):
	accObject=getObjectFromEvent(window,objectID,childID)
	if objectHasFocus(accObject) is True:
		audio.speakMessage("object accelerator changed")
		audio.speakObjectProperties(keyboardShortcut=getObjectKeyboardShortcut(accObject))

def event_objectDefactionChange(window,objectID,childID):
	accObject=getObjectFromEvent(window,objectID,childID)
	if objectHasFocus(accObject) is True:
		audio.speakMessage("Defaction changed")

def event_objectDescriptionChange(window,objectID,childID):
	accObject=getObjectFromEvent(window,objectID,childID)
	if objectHasFocus(accObject) is True:
		audio.speakObjectProperties(description=getObjectDescription(accObject))

def event_objectHelpChange(window,objectID,childID):
	accObject=getObjectFromEvent(window,objectID,childID)
	if objectHasFocus(accObject) is True:
		audio.speakObjectProperties(help=getObjectHelp(accObject))

def event_objectNameChange(window,objectID,childID):
	accObject=getObjectFromEvent(window,objectID,childID)
	if objectHasFocus(accObject) is True:
		audio.speakObjectProperties(name=getObjectName(accObject))
	elif (conf["mouse"]["reportMouseShapeChanges"] is True) and objectID==OBJID_CURSOR:
		audio.speakObjectProperties(name=getObjectName(accObject))

def event_objectParentChange(window,objectID,childID):
	pass

def event_objectReorder(window,objectID,childID):
	pass

def event_objectStateChange(window,objectID,childID):
	global lastFocusStates
	if (window,objectID,childID)!=globalVars.focus_locator:
		return
	accObject=getObjectFromEvent(window,objectID,childID)
	states=getObjectStates(accObject)
	if states is None:
		return None
	if not states&STATE_SYSTEM_FOCUSED:
		return 
	states_on=states-(states&lastFocusStates)
	states_on=filterStates(states_on)
	audio.speakObjectProperties(stateNames=getStateNames(states_on))
	states_off=lastFocusStates-(states&lastFocusStates)
	states_off=filterStates(states_off)
	audio.speakObjectProperties(stateNames=getStateNames(states_off,opposite=True))
	lastFocusStates=states

def event_objectSelection(window,objectID,childID):
	event_objectStateChange(window,objectID,childID)

def event_objectSelectionAdd(window,objectID,childID):
	event_objectStateChange(window,objectID,childID)

def event_objectSelectionRemove(window,objectID,childID):
	event_objectStateChange(window,objectID,childID)

def event_objectSelectionWithIn(window,objectID,childID):
	event_objectStateChange(window,objectID,childID)

def event_objectValueChange(window,objectID,childID):
	accObject=getObjectFromEvent(window,objectID,childID)
	value=getObjectValue(accObject)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_PROGRESSBAR:
		percentage=int(value[0:-1])
		winsound.Beep((300+(percentage*3)),30)
	if value is None:
		return
	if objectHasFocus(accObject) is False:
		return
	if role==ROLE_SYSTEM_TEXT:
		event_caretChange(window,objectID,childID)
	else:
		audio.speakObjectProperties(value=value)

def script_navigator_object_current(keyPress):
	curObject=getNavigatorObject()
	speakObject(curObject)
	return False

def script_navigator_object_recursive(keyPress,obj=None):
	if obj is None:
		curObject=getNavigatorObject()
		if getObjectChildID(curObject)>0:
			audio.speakMessage("No children")
			return
		speakObject(curObject)
		if getObjectRole(curObject)!=ROLE_SYSTEM_LINK:
			childObject=getObjectFirstChild(curObject)
			script_navigator_object_recursive(keyPress,obj=childObject)
	else:
		speakObject(obj)
		if getObjectRole(obj)!=ROLE_SYSTEM_LINK:
			childObject=getObjectFirstChild(obj)
			if (childObject is not None) and (getObjectLocation(getObjectParent(childObject))==getObjectLocation(obj)):
				script_navigator_object_recursive(keyPress,obj=childObject)
		nextObject=getObjectNext(obj)
		if (nextObject is not None) and (getObjectLocation(getObjectPrevious(nextObject))==getObjectLocation(obj)):
			script_navigator_object_recursive(keyPress,obj=nextObject)

def script_navigator_object_parent(keyPress):
	curObject=getNavigatorObject()
	curObject=getObjectParent(curObject)
	if curObject is not None:
		setNavigatorObject(curObject)
		speakObject(curObject)
	else:
		audio.speakMessage("No parent")
	return False

def script_navigator_object_next(keyPress):
	curObject=getObjectNext(globalVars.navigatorObject)
	if curObject is not None:
		globalVars.navigatorObject=curObject
		speakObject(curObject)
	else:
		audio.speakMessage("No next")
	return False

def script_navigator_object_previous(keyPress):
	curObject=getObjectPrevious(globalVars.navigatorObject)
	if curObject is not None:
		globalVars.navigatorObject=curObject
		speakObject(curObject)
	else:
		audio.speakMessage("No previous")
	return False

def script_navigator_object_firstChild(keyPress):
	curObject=getObjectFirstChild(globalVars.navigatorObject)
	if curObject is not None:
		globalVars.navigatorObject=curObject
		speakObject(curObject)
	else:
		audio.speakMessage("No children")
	return False

def script_navigator_object_doDefaultAction(keyPress):
	doObjectDefaultAction(globalVars.navigatorObject)
	return False

def script_navigator_object_where(keyPress):
	curObject=getNavigatorObject()
	while curObject is not None:
		speakObject(curObject)
		curObject=getObjectParent(curObject)
	return False

def script_navigator_object_left(keyPress):
	curObject=getObjectLeft(globalVars.navigatorObject)
	if curObject is not None:
		globalVars.navigatorObject=curObject
		speakObject(curObject)
	else:
		audio.speakMessage("No left")
	return False

def script_navigator_object_right(keyPress):
	curObject=getObjectRight(globalVars.navigatorObject)
	if curObject is not None:
		globalVars.navigatorObject=curObject
		speakObject(curObject)
	else:
		audio.speakMessage("No right")
	return False

def script_navigator_object_up(keyPress):
	curObject=getObjectUp(globalVars.navigatorObject)
	if curObject is not None:
		globalVars.navigatorObject=curObject
		speakObject(curObject)
	else:
		audio.speakMessage("No up")
	return False

def script_navigator_object_down(keyPress):
	curObject=getObjectLeft(globalVars.navigatorObject)
	if curObject is not None:
		globalVars.navigatorObject=curObject
		speakObject(curObject)
	else:
		audio.speakMessage("No down")
	return False

def script_navigator_line_current(keyPress):
	curObject=getNavigatorObject()
	window=getWindowFromObject(curObject)
	lineCount=getWindowLineCount(window)
	if (lineCount is None) or (lineCount==0):
		audio.speakMessage("No lines")
		return None
	curPosition=getNavigatorPosition()
	if curPosition is not None:
		lineNum=getWindowLineNumber(window,curPosition)
		line=getWindowLine(window,lineNum)
		audio.speakText(line)

def script_navigator_line_next(keyPress):
	curObject=getNavigatorObject()
	window=getWindowFromObject(curObject)
	lineCount=getWindowLineCount(window)
	if (lineCount is None) or (lineCount==0):
		audio.speakMessage("No lines")
		return None
	curPosition=getNavigatorPosition()
	curLineNum=getWindowLineNumber(window,curPosition)
	curLineCount=getWindowLineCount(window)
	nextLineNum=curLineNum+1
	if (nextLineNum+1)>curLineCount:
		curLine=getWindowLine(window,curLineNum)
		audio.speakMessage("Bottom")
		audio.speakText(curLine)
	else:
		nextLine=getWindowLine(window,nextLineNum)
		audio.speakText(nextLine)
		nextPosition=getWindowLinePosition(window,nextLineNum)
		setNavigatorPosition(nextPosition)
	return False

def script_navigator_line_previous(keyPress):
	curObject=getNavigatorObject()
	window=getWindowFromObject(curObject)
	lineCount=getWindowLineCount(window)
	if (lineCount is None) or (lineCount==0):
		audio.speakMessage("No lines")
		return None
	curPosition=getNavigatorPosition()
	curLineNum=getWindowLineNumber(window,curPosition)
	curLineCount=getWindowLineCount(window)
	prevLineNum=curLineNum-1
	if prevLineNum<0:
		curLine=getWindowLine(window,curLineNum)
		audio.speakMessage("Top")
		audio.speakText(curLine)
	else:
		prevLine=getWindowLine(window,prevLineNum)
		audio.speakText(prevLine)
		prevPosition=getWindowLinePosition(window,prevLineNum)
		setNavigatorPosition(prevPosition)
	return False

def script_navigator_character_current(keyPress):
	curObject=getNavigatorObject()
	window=getWindowFromObject(curObject)
	textLength=getWindowTextLength(window)
	if (textLength is None) or (textLength==0):
		audio.speakMessage("No text")
		return None
	curPosition=getNavigatorPosition()
	if curPosition is None:
		curPosition=0
	curCharacter=getWindowCharacter(window,curPosition)
	if curCharacter is not None:
		audio.speakSymbol(curCharacter)
	return False

def script_navigator_character_next(keyPress):
	curObject=getNavigatorObject()
	window=getWindowFromObject(curObject)
	textLength=getWindowTextLength(window)
	if (textLength is None) or (textLength==0):
		audio.speakMessage("No text")
		return None
	curPosition=getNavigatorPosition()
	if curPosition is None:
		curPosition=0
	nextPosition=curPosition+1
	textLength=getWindowTextLength(window)
	if nextPosition>=textLength:
		audio.speakMessage("right")
		curCharacter=getWindowCharacter(window,curPosition)
		audio.speakSymbol(curCharacter)
	else:
		nextCharacter=getWindowCharacter(window,nextPosition)
		audio.speakSymbol(nextCharacter)
		setNavigatorPosition(nextPosition)
	return False

def script_navigator_character_previous(keyPress):
	curObject=getNavigatorObject()
	window=getWindowFromObject(curObject)
	textLength=getWindowTextLength(window)
	if (textLength is None) or (textLength==0):
		audio.speakMessage("No text")
		return None
	curPosition=getNavigatorPosition()
	if curPosition is None:
		curPosition=0
	prevPosition=curPosition-1
	textLength=getWindowTextLength(window)
	if prevPosition<0:
		audio.speakMessage("Left")
		curCharacter=getWindowCharacter(window,curPosition)
		audio.speakSymbol(curCharacter)
	else:
		prevCharacter=getWindowCharacter(window,prevPosition)
		audio.speakSymbol(prevCharacter)
		setNavigatorPosition(prevPosition)
	return False

def script_quit(keyPress):
	quit()

def script_upArrow(keyPress):
	keyEventHandler.sendKey(keyPress)
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		sayLine()

def script_downArrow(keyPress):
	keyEventHandler.sendKey(keyPress)
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		sayLine()

def script_rightArrow(keyPress):
	keyEventHandler.sendKey(keyPress)
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		sayCharacter()

def script_leftArrow(keyPress):
	keyEventHandler.sendKey(keyPress)
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		sayCharacter()

def script_controlLeftArrow(keyPress):
	keyEventHandler.sendKey(keyPress)
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		sayWord()

def script_controlRightArrow(keyPress):
	keyEventHandler.sendKey(keyPress)
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		sayWord()

def script_shiftRightArrow(keyPress):
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		selectionPoints=getWindowSelectionPoints(window)
		keyEventHandler.sendKey(keyPress)
		newSelectionPoints=getWindowSelectionPoints(window)
		if (selectionPoints is None) and (newSelectionPoints is not None):
			audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],newSelectionPoints[1]))
		elif newSelectionPoints is None:
			audio.speakSymbol(getWindowCharacter(window,getWindowInsertionPoint(window)))
		elif (newSelectionPoints is not None) and (selectionPoints is not None):
			if newSelectionPoints[1]>selectionPoints[1]:
				audio.speakText("selected %s"%getWindowCharacters(window,selectionPoints[1],newSelectionPoints[1]))
			elif newSelectionPoints[0]>selectionPoints[0]:
				audio.speakText("unselected %s"%getWindowCharacters(window,selectionPoints[0],newSelectionPoints[0]))
	else:
		keyEventHandler.sendKey(keyPress)

def script_shiftLeftArrow(keyPress):
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		selectionPoints=getWindowSelectionPoints(window)
		keyEventHandler.sendKey(keyPress)
		newSelectionPoints=getWindowSelectionPoints(window)
		if (selectionPoints is None) and (newSelectionPoints is not None):
			audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],newSelectionPoints[1]))
		elif newSelectionPoints is None:
			audio.speakSymbol(getWindowCharacter(window,getWindowInsertionPoint(window)))
		elif (newSelectionPoints is not None) and (selectionPoints is not None):
			if newSelectionPoints[1]<selectionPoints[1]:
				audio.speakText("unselected %s"%getWindowCharacters(window,newSelectionPoints[1],selectionPoints[1]))
			elif newSelectionPoints[0]<selectionPoints[0]:
				audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],selectionPoints[0]))
	else:
		keyEventHandler.sendKey(keyPress)

def script_shiftEnd(keyPress):
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		selectionPoints=getWindowSelectionPoints(window)
		keyEventHandler.sendKey(keyPress)
		newSelectionPoints=getWindowSelectionPoints(window)
		if (selectionPoints is None) and (newSelectionPoints is not None):
			audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],newSelectionPoints[1]))
		elif newSelectionPoints is None:
			audio.speakSymbol(getWindowCharacter(window,getWindowInsertionPoint(window)))
		elif (newSelectionPoints is not None) and (selectionPoints is not None):
			if newSelectionPoints[1]>selectionPoints[1]:
				audio.speakText("selected %s"%getWindowCharacters(window,selectionPoints[1],newSelectionPoints[1]))
			elif newSelectionPoints[0]>selectionPoints[0]:
				audio.speakText("unselected %s"%getWindowCharacters(window,selectionPoints[0],newSelectionPoints[0]))
	else:
		keyEventHandler.sendKey(keyPress)

def script_shiftHome(keyPress):
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		selectionPoints=getWindowSelectionPoints(window)
		keyEventHandler.sendKey(keyPress)
		newSelectionPoints=getWindowSelectionPoints(window)
		if (selectionPoints is None) and (newSelectionPoints is not None):
			audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],newSelectionPoints[1]))
		elif newSelectionPoints is None:
			audio.speakSymbol(getWindowCharacter(window,getWindowInsertionPoint(window)))
		elif (newSelectionPoints is not None) and (selectionPoints is not None):
			if newSelectionPoints[1]<selectionPoints[1]:
				audio.speakText("unselected %s"%getWindowCharacters(window,newSelectionPoints[1],selectionPoints[1]))
			elif newSelectionPoints[0]<selectionPoints[0]:
				audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],selectionPoints[0]))
	else:
		keyEventHandler.sendKey(keyPress)

def script_shiftDownArrow(keyPress):
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		selectionPoints=getWindowSelectionPoints(window)
		keyEventHandler.sendKey(keyPress)
		newSelectionPoints=getWindowSelectionPoints(window)
		if (selectionPoints is None) and (newSelectionPoints is not None):
			audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],newSelectionPoints[1]))
		elif newSelectionPoints is None:
			audio.speakSymbol(getWindowCharacter(window,getWindowInsertionPoint(window)))
		elif (newSelectionPoints is not None) and (selectionPoints is not None):
			if newSelectionPoints[1]>selectionPoints[1]:
				audio.speakText("selected %s"%getWindowCharacters(window,selectionPoints[1],newSelectionPoints[1]))
			elif newSelectionPoints[0]>selectionPoints[0]:
				audio.speakText("unselected %s"%getWindowCharacters(window,selectionPoints[0],newSelectionPoints[0]))
	else:
		keyEventHandler.sendKey(keyPress)

def script_shiftUpArrow(keyPress):
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		selectionPoints=getWindowSelectionPoints(window)
		keyEventHandler.sendKey(keyPress)
		newSelectionPoints=getWindowSelectionPoints(window)
		if (selectionPoints is None) and (newSelectionPoints is not None):
			audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],newSelectionPoints[1]))
		elif newSelectionPoints is None:
			audio.speakSymbol(getWindowCharacter(window,getWindowInsertionPoint(window)))
		elif (newSelectionPoints is not None) and (selectionPoints is not None):
			if newSelectionPoints[1]<selectionPoints[1]:
				audio.speakText("unselected %s"%getWindowCharacters(window,newSelectionPoints[1],selectionPoints[1]))
			elif newSelectionPoints[0]<selectionPoints[0]:
				audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],selectionPoints[0]))
	else:
		keyEventHandler.sendKey(keyPress)

def script_controlShiftRightArrow(keyPress):
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		selectionPoints=getWindowSelectionPoints(window)
		keyEventHandler.sendKey(keyPress)
		newSelectionPoints=getWindowSelectionPoints(window)
		if (selectionPoints is None) and (newSelectionPoints is not None):
			audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],newSelectionPoints[1]))
		elif newSelectionPoints is None:
			audio.speakSymbol(getWindowCharacter(window,getWindowInsertionPoint(window)))
		elif (newSelectionPoints is not None) and (selectionPoints is not None):
			if newSelectionPoints[1]>selectionPoints[1]:
				audio.speakText("selected %s"%getWindowCharacters(window,selectionPoints[1],newSelectionPoints[1]))
			elif newSelectionPoints[0]>selectionPoints[0]:
				audio.speakText("unselected %s"%getWindowCharacters(window,selectionPoints[0],newSelectionPoints[0]))
	else:
		keyEventHandler.sendKey(keyPress)

def script_controlShiftLeftArrow(keyPress):
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		selectionPoints=getWindowSelectionPoints(window)
		keyEventHandler.sendKey(keyPress)
		newSelectionPoints=getWindowSelectionPoints(window)
		if (selectionPoints is None) and (newSelectionPoints is not None):
			audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],newSelectionPoints[1]))
		elif newSelectionPoints is None:
			audio.speakSymbol(getWindowCharacter(window,getWindowInsertionPoint(window)))
		elif (newSelectionPoints is not None) and (selectionPoints is not None):
			if newSelectionPoints[1]<selectionPoints[1]:
				audio.speakText("unselected %s"%getWindowCharacters(window,newSelectionPoints[1],selectionPoints[1]))
			elif newSelectionPoints[0]<selectionPoints[0]:
				audio.speakText("selected %s"%getWindowCharacters(window,newSelectionPoints[0],selectionPoints[0]))
	else:
		keyEventHandler.sendKey(keyPress)
 
def script_home(keyPress):
	keyEventHandler.sendKey(keyPress)
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		sayCharacter()

def script_end(keyPress):
	keyEventHandler.sendKey(keyPress)
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		sayCharacter()

def script_delete(keyPress):
	keyEventHandler.sendKey(keyPress)
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		sayCharacter()

def script_backspace(keyPress):
	(window,objectID,childID)=globalVars.focus_locator
	accObject=getObjectFromEvent(window,objectID,childID)
	role=getObjectRole(accObject)
	if role==ROLE_SYSTEM_TEXT:
		point=getWindowInsertionPoint(window)
		if point>0:
			delChar=getWindowCharacter(window,point-1)
			keyEventHandler.sendKey(keyPress)
			newPoint=getWindowInsertionPoint(window)
			if newPoint<point:
				audio.speakSymbol(delChar)
	else:
		keyEventHandler.sendKey(keyPress)



def getNavigatorObject():
	curObject=globalVars.navigatorObject
	return curObject

def setNavigatorObject(curObject):
	globalVars.navigatorObject=curObject

def getNavigatorPosition():
	return globalVars.navigatorPosition

def setNavigatorPosition(position):
	globalVars.navigatorPosition=position

def script_showGui(key):
	gui.showGui()

keyMap={
key("Insert+Q"):script_quit,
key("Up"):script_navigator_line_current,
key("Home"):script_navigator_line_previous,
key("Prior"):script_navigator_line_next,
key("Down"):script_navigator_character_current,
key("End"):script_navigator_character_previous,
key("Next"):script_navigator_character_next,
key("Insert+Clear"):script_navigator_object_current,
key("Insert+Up"):script_navigator_object_parent,
key("Insert+Down"):script_navigator_object_firstChild,
key("Insert+Left"):script_navigator_object_previous,
key("Insert+Right"):script_navigator_object_next,
key("Insert+Shift+Left"):script_navigator_object_left,
key("Insert+Shift+Right"):script_navigator_object_right,
key("Insert+Shift+Up"):script_navigator_object_up,
key("Insert+Shift+Down"):script_navigator_object_down,
key("Insert+ExtendedReturn"):script_navigator_object_doDefaultAction,
key("Insert+Add"):script_navigator_object_recursive,
key("Insert+Shift+Add"):script_navigator_object_where,
key("ExtendedUp"):script_upArrow,
key("ExtendedDown"):script_downArrow,
key("ExtendedLeft"):script_leftArrow,
key("ExtendedRight"):script_rightArrow,
key("Control+ExtendedLeft"):script_controlLeftArrow,
key("Control+ExtendedRight"):script_controlRightArrow,
key("Shift+ExtendedRight"):script_shiftRightArrow,
key("Shift+ExtendedLeft"):script_shiftLeftArrow,
key("Shift+ExtendedHome"):script_shiftHome,
key("Shift+ExtendedEnd"):script_shiftEnd,
key("Shift+ExtendedUp"):script_shiftUpArrow,
key("Shift+ExtendedDown"):script_shiftDownArrow,
key("Control+Shift+ExtendedLeft"):script_controlShiftLeftArrow,
key("Control+Shift+ExtendedRight"):script_controlShiftRightArrow,
key("ExtendedHome"):script_home,
key("ExtendedEnd"):script_end,
key("ExtendedDelete"):script_delete,
key("Back"):script_backspace,
key("Insert+N"): script_showGui,
}

default=globals().copy()
