from keyEventHandler import key
from api import *
import audio
import datetime


def event_moduleStart():
	pass

def event_switchStart(window,objectID,childID):
	audio.speakMessage("task switcher")

def event_switchEnd(window,objectID,childID):
	audio.cancel()

def script_dateTime(keyPress):
	text=datetime.datetime.today().strftime("%I:%M %p on %A %B %d, %Y")
	if text[0]=='0':
		text=text[1:]
	audio.speakMessage(text)

def script_navigator_object_current(keyPress):
	curObject=getNavigatorObject()
	curObject.speakObject()
	return False

def script_navigator_object_recursive(keyPress,obj=None):
	if obj is None:
		curObject=getNavigatorObject()
		if curObject.getChildID()>0:
			audio.speakMessage("No children")
			return
		curObject.speakObject()
		childObject=curObject.getFirstChild()
		script_navigator_object_recursive(keyPress,obj=childObject)
	else:
		obj.speakObject()
		if obj.getRole()!=ROLE_SYSTEM_LINK:
			childObject=obj.getFirstChild()
			if (childObject is not None) and (childObject.getParent().getLocation()==obj.getLocation()):
				script_navigator_object_recursive(keyPress,obj=childObject)
		nextObject=obj.getNext()
		if (nextObject is not None) and (nextObject.getPrevious().getLocation()==obj.getLocation()):
			script_navigator_object_recursive(keyPress,obj=nextObject)

def script_navigator_object_parent(keyPress):
	curObject=getNavigatorObject()
	curObject=curObject.getParent()
	if curObject is not None:
		setNavigatorObject(curObject)
		curObject.speakObject()
	else:
		audio.speakMessage("No parent")

def script_navigator_object_next(keyPress):
	curObject=getNavigatorObject()
	curObject=curObject.getNext()
	if curObject is not None:
		setNavigatorObject(curObject)
		curObject.speakObject()
	else:
		audio.speakMessage("No next")

def script_navigator_object_previous(keyPress):
	curObject=getNavigatorObject()
	curObject=curObject.getPrevious()
	if curObject is not None:
		setNavigatorObject(curObject)
		curObject.speakObject()
	else:
		audio.speakMessage("No previous")

def script_navigator_object_firstChild(keyPress):
	curObject=getNavigatorObject()
	curObject=curObject.getFirstChild()
	if curObject is not None:
		setNavigatorObject(curObject)
		curObject.speakObject()
	else:
		audio.speakMessage("No children")

def script_navigator_object_doDefaultAction(keyPress):
	curObject=getNavigatorObject()
	curObject.doDefaultAction()

def script_navigator_object_where(keyPress):
	curObject=getNavigatorObject()
	while curObject is not None:
		curObject.speakObject()
		curObject=curObject.getParent()

def script_navigator_line_current(keyPress):
	curObject=getNavigatorObject()
	curIndex=getNavigatorIndex()
	audio.speakText(curObject.getLine(index=curIndex))

def script_navigator_line_next(keyPress):
	curObject=getNavigatorObject()
	curIndex=getNavigatorIndex()
	nextIndex=curObject.getNextLineIndex(curIndex)
	if nextIndex:
		audio.speakText(curObject.getLine(index=nextIndex))
		setNavigatorIndex(nextIndex)
	else:
		audio.speakMessage("bottom")
		audio.speakText(curObject.getLine(index=curIndex))

def script_navigator_line_previous(keyPress):
	curObject=getNavigatorObject()
	curIndex=getNavigatorIndex()
	prevIndex=curObject.getPreviousLineIndex(curIndex)
	if prevIndex:
		audio.speakText(curObject.getLine(index=prevIndex))
		setNavigatorIndex(prevIndex)
	else:
		audio.speakMessage("top")
		audio.speakText(curObject.getLine(index=curIndex))

def script_navigator_character_current(keyPress):
	curObject=getNavigatorObject()
	curIndex=getNavigatorIndex()
	audio.speakText(curObject.getCharacter(index=curIndex))

def script_navigator_character_next(keyPress):
	curObject=getNavigatorObject()
	curIndex=getNavigatorIndex()
	nextIndex=curObject.getNextCharacterIndex(curIndex,crossLines=False)
	if nextIndex:
		audio.speakText(curObject.getCharacter(index=nextIndex))
		setNavigatorIndex(nextIndex)
	else:
		audio.speakMessage("right")
		audio.speakText(curObject.getCharacter(index=curIndex))

def script_navigator_character_previous(keyPress):
	curObject=getNavigatorObject()
	curIndex=getNavigatorIndex()
	prevIndex=curObject.getPreviousCharacterIndex(curIndex,crossLines=False)
	if prevIndex:
		audio.speakText(curObject.getCharacter(index=prevIndex))
		setNavigatorIndex(prevIndex)
	else:
		audio.speakMessage("left")
		audio.speakText(curObject.getCharacter(index=curIndex))

def script_navigator_character_activate(keyPress):
	curObject=getNavigatorObject()
	curIndex=getNavigatorIndex()
	curObject.activateAtIndex(curIndex)

def script_quit(keyPress):
	audio.speakMessage("Exiting NVDA",wait=True)
	quit()

def script_showGui(keyPress):
	showGui()

keyMap={
key("insert+q"):script_quit,
key("insert+n"):script_showGui,
key("insert+F12"):script_dateTime,
key("Up"):script_navigator_line_current,
key("Home"):script_navigator_line_previous,
key("Prior"):script_navigator_line_next,
key("Down"):script_navigator_character_current,
key("End"):script_navigator_character_previous,
key("Next"):script_navigator_character_next,
key("ExtendedReturn"):script_navigator_character_activate,
key("Insert+Clear"):script_navigator_object_current,
key("Insert+Up"):script_navigator_object_parent,
key("Insert+Down"):script_navigator_object_firstChild,
key("Insert+Left"):script_navigator_object_previous,
key("Insert+Right"):script_navigator_object_next,
key("Insert+ExtendedReturn"):script_navigator_object_doDefaultAction,
key("Insert+Add"):script_navigator_object_recursive,
key("Insert+Shift+Add"):script_navigator_object_where,
}

default=globals().copy()
