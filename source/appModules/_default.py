#appModules/_default.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
import comtypesClient
import datetime
from keyboardHandler import key
import api
import audio
import sayAllHandler
import virtualBuffers
import NVDAObjects
import synthDriverHandler
import gui
import core
import config
import winUser

class appModule(object):

	def __init__(self,hwnd,processID):
		self.hwnd=hwnd
		self.processID=processID
		self._keyMap={}

	def getScript(self,keyPress):
		if self._keyMap.has_key(keyPress):
			return self._keyMap[keyPress]

	def registerScriptKey(self,keyPress,methodName):
		self._keyMap[keyPress]=methodName

	def registerScriptKeys(self,keyDict):
		self._keyMap.update(keyDict)


	def event_IAccessible_switchStart(self,window,objectID,childID):
		audio.cancel()

	def event_IAccessible_switchEnd(self,window,objectID,childID):
		audio.cancel()

	def script_dateTime(self,keyPress):
		"""Reports the current date and time"""
		text=datetime.datetime.today().strftime("%I:%M %p on %A %B %d, %Y")
		if text[0]=='0':
			text=text[1:]
		audio.speakMessage(text)

	def script_increaseRate(self,keyPress):
		synthDriverHandler.setRate(synthDriverHandler.getRate()+5)
		audio.speakMessage(_("rate %d%%")%synthDriverHandler.getRate())

	def script_decreaseRate(self,keyPress):
		synthDriverHandler.setRate(synthDriverHandler.getRate()-5)
		audio.speakMessage(_("rate %d%%")%synthDriverHandler.getRate())

	def script_toggleSpeakTypedCharacters(self,keyPress):
		if config.conf["keyboard"]["speakTypedCharacters"]:
			onOff=_("off")
			config.conf["keyboard"]["speakTypedCharacters"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakTypedCharacters"]=True
		audio.speakMessage(_("speak typed characters")+" "+onOff)

	def script_toggleSpeakTypedWords(self,keyPress):
		if config.conf["keyboard"]["speakTypedWords"]:
			onOff=_("off")
			config.conf["keyboard"]["speakTypedWords"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakTypedWords"]=True
		audio.speakMessage(_("speak typed words")+" "+onOff)

	def script_toggleSpeakCommandKeys(self,keyPress):
		if config.conf["keyboard"]["speakCommandKeys"]:
			onOff=_("off")
			config.conf["keyboard"]["speakCommandKeys"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakCommandKeys"]=True
		audio.speakMessage(_("speak command keys")+" "+onOff)

	def script_toggleSpeakPunctuation(self,keyPress):
		if config.conf["speech"]["speakPunctuation"]:
			onOff=_("off")
			config.conf["speech"]["speakPunctuation"]=False
		else:
			onOff=_("on")
			config.conf["speech"]["speakPunctuation"]=True
		audio.speakMessage(_("speak punctuation")+" "+onOff)



	def script_moveMouseToNavigatorObject(self,keyPress):
		"""Moves the mouse pointer to the current navigator object"""
		audio.speakMessage("Move mouse to navigator")
		api.moveMouseToNVDAObject(api.getNavigatorObject())

	def script_moveNavigatorObjectToMouse(self,keyPress):
		audio.speakMessage("Move navigator object to mouse")
		(x,y)=winUser.getCursorPos()
		obj=NVDAObjects.IAccessible.getNVDAObjectFromPoint(x,y)
		if obj:
			api.setNavigatorObject(obj)
			obj.speakObject()

	def script_navigatorObject_current(self,keyPress):
		"""Reports the object the navigator is currently on""" 
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject.speakObject()
		return False

	def script_navigatorObject_currentDimensions(self,keyPress):
		obj=api.getNavigatorObject()
		if not obj:
			audio.speakMessage(_("no navigator object"))
		location=obj.location
		if not location:
			audio.speakMessage(_("No location information for navigator object"))
		(left,top,width,height)=location
		audio.speakMessage("%d wide by %d high, located %d from left and %d from top"%(width,height,left,top))
   
	def script_navigatorObject_toFocus(self,keyPress):
		"""Moves the navigator to the object with focus"""
		obj=api.getFocusObject()
		if not isinstance(obj,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no focus"))
		api.setNavigatorObject(obj)
		audio.speakMessage(_("move to focus"))
		obj.speakObject()

	def script_navigatorObject_parent(self,keyPress):
		"""Moves the navigator to the parent of the object it is currently on"""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.parent
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No parents"))

	def script_navigatorObject_next(self,keyPress):
		"""Moves the navigator to the next object of the one it is currently on"""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.next
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No next"))

	def script_navigatorObject_previous(self,keyPress):
		"""Moves the navigator to the previous object of the one it is currently on"""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.previous
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No previous"))

	def script_navigatorObject_firstChild(self,keyPress):
		"""Moves the navigator to the first child object of the one it is currently on"""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.firstChild
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No children"))

	def script_navigatorObject_doDefaultAction(self,keyPress):
		"""Performs the default action on the object the navigator is currently on (example: presses it if it is a button)."""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject.doDefaultAction()

	def script_navigatorObject_where(self,keyPress):
		"""Reports where the navigator is, by starting at the object where the navigator is currently, and moves up the ansesters, speaking them as it goes."""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.parent
		while curObject is not None:
			audio.speakMessage("in")
			curObject.speakObject()
			curObject=curObject.parent

	def script_review_top(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_top(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_bottom(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_bottom(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_previousLine(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_prevLine(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_currentLine(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_currentLine(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_nextLine(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_nextLine(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_previousWord(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_prevWord(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_currentWord(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_currentWord(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_nextWord(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_nextWord(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_previousCharacter(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_prevCharacter(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_currentCharacter(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_currentCharacter(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_nextCharacter(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_nextCharacter(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_startOfLine(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_startOfLine(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_endOfLine(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_endOfLine(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_moveToCaret(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_moveToCaret(keyPress)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_speechMode(self,keyPress):
		"""Toggles speech on and off"""
		curMode=audio.speechMode
		audio.speechMode=audio.speechMode_talk
		newMode=(curMode+1)%3
		if newMode==audio.speechMode_off:
			name=_("off")
		elif newMode==audio.speechMode_beeps:
			name=_("beeps")
		elif newMode==audio.speechMode_talk:
			name=_("talk")
		audio.speakMessage(_("speech mode %s")%name)
		audio.speechMode=newMode

	def script_toggleVirtualBufferPassThrough(self,keyPress):
		api.toggleVirtualBufferPassThrough()

	def script_quit(self,keyPress):
		"""Quits NVDA!"""
		gui.quit()

	def script_showGui(self,keyPress):
		gui.showGui()

	def script_sayAll_review(self,keyPress):
		o=api.getNavigatorObject()
		sayAllHandler.sayAll(o.text_reviewOffset,o.text_characterCount,o.text_getNextFieldOffsets,o.text_getText,o.text_reportNewPresentation,o._set_text_reviewOffset)

	def script_sayAll_caret(self,keyPress):
		o=api.getFocusObject()
		v=virtualBuffers.getVirtualBuffer(o)
		if v and not api.isVirtualBufferPassThrough():
			sayAllHandler.sayAll(v.text_reviewOffset,v.text_characterCount,v.text_getNextLineOffsets,v.text_getText,v.text_reportNewPresentation,v._set_text_reviewOffset)
		else:
			sayAllHandler.sayAll(o.text_caretOffset,o.text_characterCount,o.text_getNextFieldOffsets,o.text_getText,o.text_reportNewPresentation,o._set_text_caretOffset)

	def script_review_reportPresentation(self,keyPress):
		o=api.getFocusObject()
		v=virtualBuffers.getVirtualBuffer(o)
		if v and not api.isVirtualBufferPassThrough():
			o=v
		o.text_reportPresentation(o.text_reviewOffset)

	def script_reportCurrentFocus(self,keyPress):
		#focusObject=api.getFocusObject()
		focusObject=api.findObjectWithFocus()
		if isinstance(focusObject,NVDAObjects.baseType.NVDAObject):
			focusObject.speakObject()
		else:
			audio.speakMessage(_("no focus"))

	def script_reportStatusLine(self,keyPress):
		foregroundObject=api.getForegroundObject()
		if not foregroundObject:
			audio.speakMessage(_("no foreground object"))
			return
		statusBarObject=foregroundObject.statusBar
		if not statusBarObject:
			audio.speakMessage(_("no stats bar found"))
			return
		statusBarObject.speakObject()
		api.setNavigatorObject(statusBarObject)

	def script_toggleReportObjectUnderMouse(self,keyPress):
		config.conf["mouse"]["reportObjectUnderMouse"]=not config.conf["mouse"]["reportObjectUnderMouse"]
		if config.conf["mouse"]["reportObjectUnderMouse"]:
			audio.speakMessage(_("speak object under mouse"))
		else:
			audio.speakMessage(_("don't speak object under mouse"))

	def script_title(self,keyPress):
		"""Reports the title of the current application or foreground window"""
		obj=api.getForegroundObject()
		if obj:
			obj.speakObject()

	def script_speakForeground(self,keyPress):
		obj=api.getForegroundObject()
		if obj:
			obj.speakObject()
			obj.speakDescendantObjects()

	def script_test_navigatorWindowInfo(self,keyPress):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.window.NVDAObject_window):
			audio.speakMessage("handle: %s"%obj.windowHandle)
			audio.speakMessage("Class: %s"%obj.windowClassName)
			for char in obj.windowClassName:
				audio.speakSymbol("%s"%char)
			audio.speakMessage("internal text: %s"%winUser.getWindowText(obj.windowHandle))
			audio.speakMessage("text: %s"%obj.windowText)
			textLen=winUser.sendMessage(obj.windowHandle,winUser.LB_GETTEXTLEN,1,0)
			buf=ctypes.create_unicode_buffer(1024)
			winUser.sendMessage(obj.windowHandle,winUser.LB_GETTEXT,0,buf)
			audio.speakMessage("list item count: %s"%winUser.sendMessage(obj.windowHandle,0x1004,0,0))

	def script_test_navigatorIsIaccessible2(self,keyPress):
		obj=api.getNavigatorObject()
		if not obj:
			return
		ia2lib=comtypesClient.GetModule('.\\ia2.tlb')
		newPacc=obj._pacc.QueryInterface(ia2lib.IAccessible2)
		audio.speakMessage("%s"%newPacc)
