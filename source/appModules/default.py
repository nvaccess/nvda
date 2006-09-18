from keyEventHandler import key
from constants import *
from api import *
import audio
import datetime


def event_moduleStart():
	pass

def event_switchStart(window,objectID,childID):
	audio.speakMessage("task switcher")

def event_switchEnd(window,objectID,childID):
	audio.cancel()

def event_menuStart(window,objectID,childID):
	if not getMenuMode():
		obj=getNVDAObjectByLocator(window,objectID,childID)
		if obj and (obj.getRole() in [ROLE_SYSTEM_MENUBAR,ROLE_SYSTEM_MENUPOPUP,ROLE_SYSTEM_MENUITEM]):
			setMenuMode(True)
			audio.cancel()
			obj.speakObject()
			for child in obj.getChildren():
				if child.hasFocus():
					child.speakObject()
					break


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

def script_navigator_object_toFocus(keyPress):
	obj=getFocusObject()
	setNavigatorObject(obj)
	audio.speakMessage("Moved to focus")
	obj.speakObject()

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

def script_virtualBuffer_line_current(keyPress):
	buf=getVirtualBuffer()
	curIndex=getVirtualBufferCursor()
	audio.speakText(buf.getLine(index=curIndex))

def script_virtualBuffer_line_next(keyPress):
	buf=getVirtualBuffer()
	curIndex=getVirtualBufferCursor()
	nextIndex=buf.getNextLineIndex(curIndex)
	if nextIndex:
		audio.speakText(buf.getLine(index=nextIndex))
		setVirtualBufferCursor(nextIndex)
	else:
		audio.speakMessage("bottom")
		audio.speakText(buf.getLine(index=curIndex))

def script_virtualBuffer_line_previous(keyPress):
	buf=getVirtualBuffer()
	curIndex=getVirtualBufferCursor()
	prevIndex=buf.getPreviousLineIndex(curIndex)
	if prevIndex:
		audio.speakText(buf.getLine(index=prevIndex))
		setVirtualBufferCursor(prevIndex)
	else:
		audio.speakMessage("top")
		audio.speakText(buf.getLine(index=curIndex))

def script_virtualBuffer_character_current(keyPress):
	buf=getVirtualBuffer()
	curIndex=getVirtualBufferCursor()
	audio.speakText(buf.getCharacter(index=curIndex))

def script_virtualBuffer_moveToCaret(keyPress):
	buf=getVirtualBuffer()
	index=buf.getCaretIndex()
	setVirtualBufferCursor(index)
	audio.speakText(buf.getLine())

def script_virtualBuffer_character_next(keyPress):
	buf=getVirtualBuffer()
	curIndex=getVirtualBufferCursor()
	nextIndex=buf.getNextCharacterIndex(curIndex,crossLines=False)
	if nextIndex:
		audio.speakText(buf.getCharacter(index=nextIndex))
		setVirtualBufferCursor(nextIndex)
	else:
		audio.speakMessage("right")
		audio.speakText(buf.getCharacter(index=curIndex))

def script_virtualBuffer_character_previous(keyPress):
	buf=getVirtualBuffer()
	curIndex=getVirtualBufferCursor()
	prevIndex=buf.getPreviousCharacterIndex(curIndex,crossLines=False)
	if prevIndex:
		audio.speakText(buf.getCharacter(index=prevIndex))
		setVirtualBufferCursor(prevIndex)
	else:
		audio.speakMessage("left")
		audio.speakText(buf.getCharacter(index=curIndex))

def script_virtualBuffer_word_current(keyPress):
	buf=getVirtualBuffer()
	curIndex=getVirtualBufferCursor()
	audio.speakText(buf.getWord(index=curIndex))

def script_virtualBuffer_word_next(keyPress):
	buf=getVirtualBuffer()
	curIndex=getVirtualBufferCursor()
	nextIndex=buf.getNextCharacterIndex(buf.getWordEndIndex(curIndex),crossLines=False)
	if nextIndex:
		audio.speakText(buf.getWord(index=nextIndex))
		setVirtualBufferCursor(nextIndex)
	else:
		audio.speakMessage("right")
		audio.speakText(buf.getWord(index=curIndex))

def script_virtualBuffer_word_previous(keyPress):
	buf=getVirtualBuffer()
	curIndex=getVirtualBufferCursor()
	prevIndex=buf.getPreviousWordIndex(curIndex)
	if prevIndex:
		audio.speakText(buf.getWord(index=prevIndex))
		setVirtualBufferCursor(prevIndex)
	else:
		audio.speakMessage("left")
		audio.speakText(buf.getWord(index=curIndex))

def script_virtualBuffer_activateObject(keyPress):
	buf=getVirtualBuffer()
	curIndex=getVirtualBufferCursor()
	buf.activateIndex(curIndex)

def script_quit(keyPress):
	audio.speakMessage("Exiting NVDA",wait=True)
	quit()

def script_showGui(keyPress):
	showGui()

keyMap={
key("insert+q"):script_quit,
key("insert+n"):script_showGui,
key("insert+F12"):script_dateTime,
key("Up"):script_virtualBuffer_line_current,
key("Home"):script_virtualBuffer_line_previous,
key("Prior"):script_virtualBuffer_line_next,
key("Down"):script_virtualBuffer_character_current,
key("End"):script_virtualBuffer_character_previous,
key("Next"):script_virtualBuffer_character_next,
key("Clear"):script_virtualBuffer_word_current,
key("Left"):script_virtualBuffer_word_previous,
key("Right"):script_virtualBuffer_word_next,
key("ExtendedReturn"):script_virtualBuffer_activateObject,
key("Subtract"):script_virtualBuffer_moveToCaret,
key("Insert+Clear"):script_navigator_object_current,
key("insert+Subtract"):script_navigator_object_toFocus,
key("Insert+Up"):script_navigator_object_parent,
key("Insert+Down"):script_navigator_object_firstChild,
key("Insert+Left"):script_navigator_object_previous,
key("Insert+Right"):script_navigator_object_next,
key("Insert+ExtendedReturn"):script_navigator_object_doDefaultAction,
key("Insert+Add"):script_navigator_object_recursive,
key("Insert+Shift+Add"):script_navigator_object_where,
}

default=globals().copy()
