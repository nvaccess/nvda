import datetime
from keyEventHandler import key
from constants import *
from api import *
import audio
import NVDAObjects


def event_moduleStart():
	pass

def event_moduleEnd():
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

def script_virtualBuffer_moveToCaret(keyPress):
	buf=getVirtualBuffer()
	pos=	buf.getCaretPosition()
	setVirtualBufferCursor(pos)
	audio.speakText(buf.getLine(buf.getLineNumber(pos)))

def script_virtualBuffer_line_current(keyPress):
	buf=getVirtualBuffer()
	curPos=getVirtualBufferCursor()
	curLineNum=buf.getLineNumber(curPos)
	audio.speakText(buf.getLine(curLineNum))

def script_virtualBuffer_line_next(keyPress):
	buf=getVirtualBuffer()
	curPos=getVirtualBufferCursor()
	curLineNum=buf.getLineNumber(curPos)
	if curLineNum<buf.getLineCount()-1:
		nextLineNum=curLineNum+1
	else:
		nextLineNum=None
	if nextLineNum:
		audio.speakText(buf.getLine(nextLineNum))
		setVirtualBufferCursor(buf.getLineStart(nextLineNum))
	else:
		audio.speakMessage("bottom")
		audio.speakText(buf.getLine(curLineNum))

def script_virtualBuffer_line_previous(keyPress):
	buf=getVirtualBuffer()
	curPos=getVirtualBufferCursor()
	curLineNum=buf.getLineNumber(curPos)
	if curLineNum>0:
		prevLineNum=curLineNum-1
		audio.speakText(buf.getLine(prevLineNum))
		setVirtualBufferCursor(buf.getLineStart(prevLineNum))
	else:
		audio.speakMessage("top")
		audio.speakText(buf.getLine(curLineNum))

def script_virtualBuffer_character_current(keyPress):
	buf=getVirtualBuffer()
	curPos=getVirtualBufferCursor()
	audio.speakText(buf.getCharacter(curPos))

def script_virtualBuffer_character_next(keyPress):
	buf=getVirtualBuffer()
	curPos=getVirtualBufferCursor()
	nextPos=buf.nextCharacter(curPos)
	if nextPos and (buf.getLineNumber(curPos)==buf.getLineNumber(nextPos)):
		audio.speakText(buf.getCharacter(nextPos))
		setVirtualBufferCursor(nextPos)
	else:
		audio.speakMessage("right")
		audio.speakText(buf.getCharacter(curPos))

def script_virtualBuffer_character_previous(keyPress):
	buf=getVirtualBuffer()
	curPos=getVirtualBufferCursor()
	prevPos=buf.previousCharacter(curPos)
	if (prevPos is not None) and (buf.getLineNumber(curPos)==buf.getLineNumber(prevPos)):
		audio.speakText(buf.getCharacter(prevPos))
		setVirtualBufferCursor(prevPos)
	else:
		audio.speakMessage("left")
		audio.speakText(buf.getCharacter(curPos))

def script_virtualBuffer_word_current(keyPress):
	buf=getVirtualBuffer()
	curPos=getVirtualBufferCursor()
	audio.speakText(buf.getWord(curPos))

def script_virtualBuffer_word_next(keyPress):
	buf=getVirtualBuffer()
	curPos=getVirtualBufferCursor()
	nextPos=buf.nextWord(curPos)
	if nextPos:
		audio.speakText(buf.getWord(nextPos))
		setVirtualBufferCursor(nextPos)
	else:
		audio.speakMessage("bottom")
		audio.speakText(buf.getWord(curPos))

def script_virtualBuffer_word_previous(keyPress):
	buf=getVirtualBuffer()
	curPos=getVirtualBufferCursor()
	prevPos=buf.previousWord(curPos)
	if prevPos:
		audio.speakText(buf.getWord(prevPos))
		setVirtualBufferCursor(prevPos)
	else:
		audio.speakMessage("top")
		audio.speakText(buf.getWord(curPos))

def script_virtualBuffer_activateObject(keyPress):
	buf=getVirtualBuffer()
	curPos=getVirtualBufferCursor()
	buf.activatePosition(curPos)

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
