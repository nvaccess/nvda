import datetime
from keyboardHandler import key
from constants import *
from api import *
import audio
import NVDAObjects

class appModule(object):

	def __init__(self):
		self.keyMap={
key("insert+q"):self.script_quit,
key("insert+s"):self.script_speech_toggleMute,
key("insert+n"):self.script_showGui,
key("insert+F12"):self.script_dateTime,
key("Up"):self.script_virtualBuffer_line_current,
key("Home"):self.script_virtualBuffer_line_previous,
key("Prior"):self.script_virtualBuffer_line_next,
key("Down"):self.script_virtualBuffer_character_current,
key("End"):self.script_virtualBuffer_character_previous,
key("Next"):self.script_virtualBuffer_character_next,
key("Clear"):self.script_virtualBuffer_word_current,
key("Left"):self.script_virtualBuffer_word_previous,
key("Right"):self.script_virtualBuffer_word_next,
key("ExtendedReturn"):self.script_virtualBuffer_activateObject,
key("Subtract"):self.script_virtualBuffer_moveToCaret,
key("Insert+Clear"):self.script_navigator_object_current,
key("insert+Subtract"):self.script_navigator_object_toFocus,
key("Insert+Up"):self.script_navigator_object_parent,
key("Insert+Down"):self.script_navigator_object_firstChild,
key("Insert+Left"):self.script_navigator_object_previous,
key("Insert+Right"):self.script_navigator_object_next,
key("Insert+ExtendedReturn"):self.script_navigator_object_doDefaultAction,
key("Insert+Add"):self.script_navigator_object_recursive,
key("Insert+Shift+Add"):self.script_navigator_object_where,
}

	def event_switchStart(self,window,objectID,childID):
		audio.speakMessage("task switcher")

	def event_switchEnd(self,window,objectID,childID):
		audio.cancel()

	def script_dateTime(self,keyPress):
		"""Reports the current date and time"""
		text=datetime.datetime.today().strftime("%I:%M %p on %A %B %d, %Y")
		if text[0]=='0':
			text=text[1:]
		audio.speakMessage(text)

	def script_navigator_object_current(self,keyPress):
		"""Reports the object the navigator is currently on""" 
		curObject=getNavigatorObject()
		curObject.speakObject()
		return False

	def script_navigator_object_recursive(keyPress,obj=None):
		"""Reports the object that the navigator is currently on, plus any descendants of that object"""
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

	def script_navigator_object_toFocus(self,keyPress):
		"""Moves the navigator to the object with focus"""
		obj=getFocusObject()
		setNavigatorObject(obj)
		audio.speakMessage("Moved to focus")
		obj.speakObject()

	def script_navigator_object_parent(self,keyPress):
		"""Moves the navigator to the parent of the object it is currently on"""
		curObject=getNavigatorObject()
		curObject=curObject.getParent()
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage("No parent")

	def script_navigator_object_next(self,keyPress):
		"""Moves the navigator to the next object of the one it is currently on"""
		curObject=getNavigatorObject()
		curObject=curObject.getNext()
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage("No next")

	def script_navigator_object_previous(self,keyPress):
		"""Moves the navigator to the previous object of the one it is currently on"""
		curObject=getNavigatorObject()
		curObject=curObject.getPrevious()
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage("No previous")

	def script_navigator_object_firstChild(self,keyPress):
		"""Moves the navigator to the first child object of the one it is currently on"""
		curObject=getNavigatorObject()
		curObject=curObject.getFirstChild()
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage("No children")

	def script_navigator_object_doDefaultAction(self,keyPress):
		"""Performs the default action on the object the navigator is currently on (example: presses it if it is a button)."""
		curObject=getNavigatorObject()
		curObject.doDefaultAction()

	def script_navigator_object_where(self,keyPress):
		"""Reports where the navigator is, by starting at the object where the navigator is currently, and moves up the ansesters, speaking them as it goes."""
		curObject=getNavigatorObject()
		while curObject is not None:
			curObject.speakObject()
			curObject=curObject.getParent()

	def script_virtualBuffer_moveToCaret(self,keyPress):
		buf=getVirtualBuffer()
		pos=	buf.getCaretPosition()
		setVirtualBufferCursor(pos)
		audio.speakText(buf.getLine(buf.getLineNumber(pos)))

	def script_virtualBuffer_line_current(self,keyPress):
		buf=getVirtualBuffer()
		curPos=getVirtualBufferCursor()
		curLineNum=buf.getLineNumber(curPos)
		audio.speakText(buf.getLine(curLineNum))

	def script_virtualBuffer_line_next(self,keyPress):
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

	def script_virtualBuffer_line_previous(self,keyPress):
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

	def script_virtualBuffer_character_current(self,keyPress):
		buf=getVirtualBuffer()
		curPos=getVirtualBufferCursor()
		audio.speakText(buf.getCharacter(curPos))

	def script_virtualBuffer_character_next(self,keyPress):
		buf=getVirtualBuffer()
		curPos=getVirtualBufferCursor()
		nextPos=buf.nextCharacter(curPos)
		if nextPos and (buf.getLineNumber(curPos)==buf.getLineNumber(nextPos)):
			audio.speakText(buf.getCharacter(nextPos))
			setVirtualBufferCursor(nextPos)
		else:
			audio.speakMessage("right")
			audio.speakText(buf.getCharacter(curPos))

	def script_virtualBuffer_character_previous(self,keyPress):
		buf=getVirtualBuffer()
		curPos=getVirtualBufferCursor()
		prevPos=buf.previousCharacter(curPos)
		if (prevPos is not None) and (buf.getLineNumber(curPos)==buf.getLineNumber(prevPos)):
			audio.speakText(buf.getCharacter(prevPos))
			setVirtualBufferCursor(prevPos)
		else:
			audio.speakMessage("left")
			audio.speakText(buf.getCharacter(curPos))

	def script_virtualBuffer_word_current(self,keyPress):
		buf=getVirtualBuffer()
		curPos=getVirtualBufferCursor()
		audio.speakText(buf.getWord(curPos))

	def script_virtualBuffer_word_next(self,keyPress):
		buf=getVirtualBuffer()
		curPos=getVirtualBufferCursor()
		nextPos=buf.nextWord(curPos)
		if nextPos:
			audio.speakText(buf.getWord(nextPos))
			setVirtualBufferCursor(nextPos)
		else:
			audio.speakMessage("bottom")
			audio.speakText(buf.getWord(curPos))

	def script_virtualBuffer_word_previous(self,keyPress):
		buf=getVirtualBuffer()
		curPos=getVirtualBufferCursor()
		prevPos=buf.previousWord(curPos)
		if prevPos:
			audio.speakText(buf.getWord(prevPos))
			setVirtualBufferCursor(prevPos)
		else:
			audio.speakMessage("top")
			audio.speakText(buf.getWord(curPos))

	def script_virtualBuffer_activateObject(self,keyPress):
		buf=getVirtualBuffer()
		curPos=getVirtualBufferCursor()
		buf.activatePosition(curPos)

	def script_speech_toggleMute(self,keyPress):
		"""Toggles speech on and off"""
		if audio.allowSpeech:
			audio.speakMessage("Speech off")
			audio.allowSpeech=False
		else:
			audio.allowSpeech=True
			audio.speakMessage("Speech on")

	def script_quit(self,keyPress):
		"""Quits NVDA!"""
		audio.speakMessage("Exiting NVDA",wait=True)
		quit()

	def script_showGui(self,keyPress):
		"""Pops up a menu to configure NVDA objects"""
		showGui()
