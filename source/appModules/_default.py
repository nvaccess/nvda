import datetime
from keyboardHandler import key
from constants import *
from api import *
import audio
import NVDAObjects
import synthDriverHandler
import gui
import lang

class appModule(object):

	def __init__(self,hwnd,processID):
		self.hwnd=hwnd
		self.processID=processID
		self.keyMap={
			key("insert+n"):self.script_showGui,
			key("insert+q"):self.script_quit,
			key("insert+s"):self.script_speech_toggleMute,
			key("insert+F12"):self.script_dateTime,
			key("insert+extendedPrior"):self.script_increaseRate,
			key("insert+extendedNext"):self.script_decreaseRate,
			key("insert+2"):self.script_toggleSpeakTypedCharacters,
			key("insert+3"):self.script_toggleSpeakTypedWords,
			key("insert+4"):self.script_toggleSpeakCommandKeys,
			key("insert+extendedDivide"):self.script_moveMouseToNavigatorObject,
			key("insert+Multiply"):self.script_moveNavigatorObjectToMouse,
			key("Insert+Clear"):self.script_navigator_object_current,
			key("insert+Subtract"):self.script_navigator_object_toFocus,
			key("Insert+Up"):self.script_navigator_object_parent,
			key("Insert+Down"):self.script_navigator_object_firstChild,
			key("Insert+Left"):self.script_navigator_object_previous,
			key("Insert+Right"):self.script_navigator_object_next,
			key("Insert+ExtendedReturn"):self.script_navigator_object_doDefaultAction,
			key("Insert+Add"):self.script_navigator_object_recursive,
			key("Insert+Shift+Add"):self.script_navigator_object_where,
			key("end"):self.script_navigator_review_previousCharacter,
			key("shift+end"):self.script_navigator_review_startOfLine,
			key("down"):self.script_navigator_review_currentCharacter,
			key("next"):self.script_navigator_review_nextCharacter,
			key("shift+next"):self.script_navigator_review_endOfLine,
			key("left"):self.script_navigator_review_previousWord,
			key("clear"):self.script_navigator_review_currentWord,
			key("right"):self.script_navigator_review_nextWord,
			key("home"):self.script_navigator_review_previousLine,
			key("shift+home"):self.script_navigator_review_top,
			key("up"):self.script_navigator_review_currentLine,
			key("prior"):self.script_navigator_review_nextLine,
			key("shift+prior"):self.script_navigator_review_bottom,
		}

	def event_switchStart(self,window,objectID,childID):
		audio.speakMessage(lang.messages["taskSwitcher"])

	def event_switchEnd(self,window,objectID,childID):
		audio.cancel()

	def script_dateTime(self,keyPress):
		"""Reports the current date and time"""
		text=datetime.datetime.today().strftime("%I:%M %p on %A %B %d, %Y")
		if text[0]=='0':
			text=text[1:]
		audio.speakMessage(text)

	def script_increaseRate(self,keyPress):
		synthDriverHandler.setRate(synthDriverHandler.getRate()+5)
		audio.speakMessage(lang.messages["rate"]+" %s%%"%synthDriverHandler.getRate())

	def script_decreaseRate(self,keyPress):
		synthDriverHandler.setRate(synthDriverHandler.getRate()-5)
		audio.speakMessage(lang.messages["rate"]+" %s%%"%synthDriverHandler.getRate())

	def script_toggleSpeakTypedCharacters(self,keyPress):
		if conf["keyboard"]["speakTypedCharacters"]:
			onOff=lang.messages["off"]
			conf["keyboard"]["speakTypedCharacters"]=False
		else:
			onOff=lang.messages["on"]
			conf["keyboard"]["speakTypedCharacters"]=True
		audio.speakMessage(lang.messages["speakTypedCharacters"]+" "+lang.messages[onOff])

	def script_toggleSpeakTypedWords(self,keyPress):
		if conf["keyboard"]["speakTypedWords"]:
			onOff=lang.messages["off"]
			conf["keyboard"]["speakTypedWords"]=False
		else:
			onOff=lang.messages["on"]
			conf["keyboard"]["speakTypedWords"]=True
		audio.speakMessage(lang.messages["speakTypedWords"]+" "+lang.messages[onOff])

	def script_toggleSpeakCommandKeys(self,keyPress):
		if conf["keyboard"]["speakCommandKeys"]:
			onOff=lang.messages["off"]
			conf["keyboard"]["speakCommandKeys"]=False
		else:
			onOff=lang.messages["on"]
			conf["keyboard"]["speakCommandKeys"]=True
		audio.speakMessage(lang.messages["speakCommandKeys"]+" "+lang.messages[onOff])

	def script_moveMouseToNavigatorObject(self,keyPress):
		"""Moves the mouse pointer to the current navigator object"""
		audio.speakMessage("Move mouse to navigator")
		location=getNavigatorObject().getLocation()
		if location and (len(location)==4):
			winUser.setCursorPos(location[0],location[1])

	def script_moveNavigatorObjectToMouse(self,keyPress):
		audio.speakMessage("Move navigator object to mouse")
		(x,y)=winUser.getCursorPos()
		obj=NVDAObjects.getNVDAObjectByPoint(x,y)
		if obj:
			setNavigatorObject(obj)
			obj.speakObject()

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
				audio.speakMessage(lang.messages["noChildren"])
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
		audio.speakMessage(lang.messages["moveToFocus"])
		obj.speakObject()

	def script_navigator_object_parent(self,keyPress):
		"""Moves the navigator to the parent of the object it is currently on"""
		curObject=getNavigatorObject()
		curObject=curObject.getParent()
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(lang.messages["noParent"])

	def script_navigator_object_next(self,keyPress):
		"""Moves the navigator to the next object of the one it is currently on"""
		curObject=getNavigatorObject()
		curObject=curObject.getNext()
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(lang.messages["noNext"])

	def script_navigator_object_previous(self,keyPress):
		"""Moves the navigator to the previous object of the one it is currently on"""
		curObject=getNavigatorObject()
		curObject=curObject.getPrevious()
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(lang.messages["noPrevious"])

	def script_navigator_object_firstChild(self,keyPress):
		"""Moves the navigator to the first child object of the one it is currently on"""
		curObject=getNavigatorObject()
		curObject=curObject.getFirstChild()
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(lang.messages["noChildren"])

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

	def script_navigator_review_top(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_top"):
			getattr(obj,"review_top")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_bottom(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_bottom"):
			getattr(obj,"review_bottom")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_previousLine(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_previousLine"):
			getattr(obj,"review_previousLine")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_currentLine(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_currentLine"):
			getattr(obj,"review_currentLine")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_nextLine(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_nextLine"):
			getattr(obj,"review_nextLine")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_previousWord(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_previousWord"):
			getattr(obj,"review_previousWord")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_currentWord(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_currentWord"):
			getattr(obj,"review_currentWord")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_nextWord(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_nextWord"):
			getattr(obj,"review_nextWord")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_previousCharacter(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_previousCharacter"):
			getattr(obj,"review_previousCharacter")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_currentCharacter(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_currentCharacter"):
			getattr(obj,"review_currentCharacter")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_nextCharacter(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_nextCharacter"):
			getattr(obj,"review_nextCharacter")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_startOfLine(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_startOfLine"):
			getattr(obj,"review_startOfLine")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_navigator_review_endOfLine(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_endOfLine"):
			getattr(obj,"review_endOfLine")()
		else:
			audio.speakMessage(lang.messages["notSupported"])

	def script_speech_toggleMute(self,keyPress):
		"""Toggles speech on and off"""
		if audio.allowSpeech:
			audio.speakMessage(lang.messages["speech"]+" "+lang.messages["off"])
			audio.allowSpeech=False
		else:
			audio.allowSpeech=True
			audio.speakMessage(lang.messages["speech"]+" "+lang.messages["on"])

	def script_quit(self,keyPress):
		"""Quits NVDA!"""
		gui.exit()

	def script_showGui(self,keyPress):
		gui.showGui()

