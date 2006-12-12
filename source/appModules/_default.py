import ctypes
import datetime
from keyboardHandler import key
from constants import *
from api import *
import audio
import NVDAObjects
import synthDriverHandler
import gui
import core

class appModule(object):

	def __init__(self,hwnd,processID):
		self.hwnd=hwnd
		self.processID=processID
		self._keyMap={}
		self.registerScriptKeys({
			key("insert+n"):self.script_showGui,
			key("insert+q"):self.script_quit,
			key("insert+s"):self.script_speech_toggleMute,
			key("insert+F12"):self.script_dateTime,
			key("insert+extendedPrior"):self.script_increaseRate,
			key("insert+extendedNext"):self.script_decreaseRate,
			key("insert+2"):self.script_toggleSpeakTypedCharacters,
			key("insert+3"):self.script_toggleSpeakTypedWords,
			key("insert+4"):self.script_toggleSpeakCommandKeys,
			key("insert+p"):self.script_toggleSpeakPunctuation,
			key("insert+space"):self.script_toggleVirtualBufferPassThrough,
			key("insert+extendedEnd"):self.script_reportStatusLine,
			key("insert+extendedDivide"):self.script_moveMouseToNavigatorObject,
			key("insert+Multiply"):self.script_moveNavigatorObjectToMouse,
			key("insert+extendedUp"):self.script_currentFocus,
			key("Insert+Clear"):self.script_navigator_object_current,
			key("insert+Subtract"):self.script_navigator_object_toFocus,
			key("Insert+Up"):self.script_navigator_object_parent,
			key("Insert+Down"):self.script_navigator_object_firstChild,
			key("Insert+Left"):self.script_navigator_object_previous,
			key("Insert+Right"):self.script_navigator_object_next,
			key("Insert+ExtendedReturn"):self.script_navigator_object_doDefaultAction,
			key("Insert+Add"):self.script_navigator_object_where,
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
			key("insert+extendedDown"):self.script_sayAll,
			key("insert+f"):self.script_formatInfo,
		})

	def getScript(self,keyPress):
		if self._keyMap.has_key(keyPress):
			return self._keyMap[keyPress]

	def registerScriptKey(self,keyPress,methodName):
		self._keyMap[keyPress]=methodName

	def registerScriptKeys(self,keyDict):
		self._keyMap.update(keyDict)

	def event_switchStart(self,window,objectID,childID):
		audio.speakMessage(_("task switcher"))

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
		audio.speakMessage(_("rate")+" %s%%"%synthDriverHandler.getRate())

	def script_decreaseRate(self,keyPress):
		synthDriverHandler.setRate(synthDriverHandler.getRate()-5)
		audio.speakMessage(_("rate")+" %s%%"%synthDriverHandler.getRate())

	def script_toggleSpeakTypedCharacters(self,keyPress):
		if conf["keyboard"]["speakTypedCharacters"]:
			onOff=_("off")
			conf["keyboard"]["speakTypedCharacters"]=False
		else:
			onOff=_("on")
			conf["keyboard"]["speakTypedCharacters"]=True
		audio.speakMessage(_("speak typed characters")+" "+onOff)

	def script_toggleSpeakTypedWords(self,keyPress):
		if conf["keyboard"]["speakTypedWords"]:
			onOff=_("off")
			conf["keyboard"]["speakTypedWords"]=False
		else:
			onOff=_("on")
			conf["keyboard"]["speakTypedWords"]=True
		audio.speakMessage(_("speak typed words")+" "+onOff)

	def script_toggleSpeakCommandKeys(self,keyPress):
		if conf["keyboard"]["speakCommandKeys"]:
			onOff=_("off")
			conf["keyboard"]["speakCommandKeys"]=False
		else:
			onOff=_("on")
			conf["keyboard"]["speakCommandKeys"]=True
		audio.speakMessage(_("speak command keys")+" "+onOff)

	def script_toggleSpeakPunctuation(self,keyPress):
		if conf["speech"][synthDriverHandler.driverName]["speakPunctuation"]:
			onOff=_("off")
			conf["speech"][synthDriverHandler.driverName]["speakPunctuation"]=False
		else:
			onOff=_("on")
			conf["speech"][synthDriverHandler.driverName]["speakPunctuation"]=True
		audio.speakMessage(_("speak punctuation")+" "+onOff)



	def script_moveMouseToNavigatorObject(self,keyPress):
		"""Moves the mouse pointer to the current navigator object"""
		audio.speakMessage("Move mouse to navigator")
		location=getNavigatorObject().location
		if location and (len(location)==4):
			winUser.setCursorPos(location[0],location[1])

	def script_moveNavigatorObjectToMouse(self,keyPress):
		audio.speakMessage("Move navigator object to mouse")
		(x,y)=winUser.getCursorPos()
		obj=NVDAObjects.MSAA.getNVDAObjectFromPoint(x,y)
		if obj:
			setNavigatorObject(obj)
			obj.speakObject()

	def script_navigator_object_current(self,keyPress):
		"""Reports the object the navigator is currently on""" 
		curObject=getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject.speakObject()
		return False

	def script_navigator_object_toFocus(self,keyPress):
		"""Moves the navigator to the object with focus"""
		obj=getFocusObject()
		if not isinstance(obj,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no focus"))
		setNavigatorObject(obj)
		audio.speakMessage(_("move to focus"))
		obj.speakObject()

	def script_navigator_object_parent(self,keyPress):
		"""Moves the navigator to the parent of the object it is currently on"""
		curObject=getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.parent
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No parents"))

	def script_navigator_object_next(self,keyPress):
		"""Moves the navigator to the next object of the one it is currently on"""
		curObject=getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.next
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No next"))

	def script_navigator_object_previous(self,keyPress):
		"""Moves the navigator to the previous object of the one it is currently on"""
		curObject=getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.previous
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No previous"))

	def script_navigator_object_firstChild(self,keyPress):
		"""Moves the navigator to the first child object of the one it is currently on"""
		curObject=getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.firstChild
		if curObject is not None:
			setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No children"))

	def script_navigator_object_doDefaultAction(self,keyPress):
		"""Performs the default action on the object the navigator is currently on (example: presses it if it is a button)."""
		curObject=getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject.doDefaultAction()

	def script_navigator_object_where(self,keyPress):
		"""Reports where the navigator is, by starting at the object where the navigator is currently, and moves up the ansesters, speaking them as it goes."""
		curObject=getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		while curObject is not None:
			curObject.speakObject()
			curObject=curObject.parent

	def script_navigator_review_top(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_top"):
			getattr(obj,"review_top")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_bottom(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_bottom"):
			getattr(obj,"review_bottom")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_previousLine(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_previousLine"):
			getattr(obj,"review_previousLine")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_currentLine(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_currentLine"):
			getattr(obj,"review_currentLine")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_nextLine(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_nextLine"):
			getattr(obj,"review_nextLine")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_previousWord(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_previousWord"):
			getattr(obj,"review_previousWord")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_currentWord(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_currentWord"):
			getattr(obj,"review_currentWord")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_nextWord(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_nextWord"):
			getattr(obj,"review_nextWord")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_previousCharacter(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_previousCharacter"):
			getattr(obj,"review_previousCharacter")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_currentCharacter(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_currentCharacter"):
			getattr(obj,"review_currentCharacter")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_nextCharacter(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_nextCharacter"):
			getattr(obj,"review_nextCharacter")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_startOfLine(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_startOfLine"):
			getattr(obj,"review_startOfLine")()
		else:
			audio.speakMessage(_("not supported"))

	def script_navigator_review_endOfLine(self,keyPress):
		obj=getNavigatorObject()
		if hasattr(obj,"review_endOfLine"):
			getattr(obj,"review_endOfLine")()
		else:
			audio.speakMessage(_("not supported"))

	def script_speech_toggleMute(self,keyPress):
		"""Toggles speech on and off"""
		if audio.allowSpeech:
			audio.speakMessage(_("speech")+" "+_("off"))
			audio.allowSpeech=False
		else:
			audio.allowSpeech=True
			audio.speakMessage(_("speech")+" "+_("on"))

	def script_toggleVirtualBufferPassThrough(self,keyPress):
		toggleVirtualBufferPassThrough()

	def script_quit(self,keyPress):
		"""Quits NVDA!"""
		gui.exit()

	def script_showGui(self,keyPress):
		gui.showGui()

	def script_sayAll(self,keyPress):
		virtualBuffer=virtualBuffers.getVirtualBuffer(getFocusObject())
		if virtualBuffer:
			core.newThread(virtualBuffer.sayAllGenerator())
		elif hasattr(getFocusObject(),"sayAllGenerator"):
			core.newThread(getFocusObject().sayAllGenerator())
		else:
			audio.speakMessage(_("no sayAll functionality here"))

	def script_formatInfo(self,keyPress):
		virtualBuffer=virtualBuffers.getVirtualBuffer(getFocusObject())
		if virtualBuffer and hasattr(virtualBuffer,"reportFormatInfo"):
			virtualBuffer.reportFormatInfo()
		elif hasattr(getFocusObject(),"reportFormatInfo"):
			getFocusObject().reportFormatInfo()
		else:
			audio.speakMessage(_("no format info"))

	def script_currentFocus(self,keyPress):
		focusObject=getFocusObject()
		if isinstance(focusObject,NVDAObjects.baseType.NVDAObject):
			focusObject.speakObject()
		else:
			audio.speakMessage(_("no focus"))

	def script_reportStatusLine(self,keyPress):
		fg=winUser.getForegroundWindow()
		statusWindow=ctypes.windll.user32.FindWindowExW(fg,0,u'msctls_statusbar32',0)
		statusObject=NVDAObjects.MSAA.getNVDAObjectFromEvent(statusWindow,OBJID_CLIENT,0)
		if not isinstance(statusObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("could not find status bar object"))
			return 
		statusObject.speakObject()

