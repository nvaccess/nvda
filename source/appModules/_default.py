#appModules/_default.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import gc
import comtypes.client
import datetime
import time
import tones
from keyUtils import key
import keyboardHandler
import mouseHandler
import IAccessibleHandler
import controlTypes
import api
import textInfos
import speech
import sayAllHandler
from NVDAObjects import NVDAObject, NVDAObjectTextInfo
import globalVars
from logHandler import log
from synthDriverHandler import *
import gui
import wx
import core
import config
import winUser
import appModuleHandler
import winKernel
import ctypes
from gui import mainFrame
import virtualBufferHandler
import scriptHandler
import ui
import braille

class AppModule(appModuleHandler.AppModule):

	def script_keyboardHelp(self,keyPress):
		if not globalVars.keyboardHelp:
 			state=_("on")
			globalVars.keyboardHelp=True
		else:
			state=_("off")
			globalVars.keyboardHelp=False
		ui.message(_("keyboard help %s")%state)
	script_keyboardHelp.__doc__=_("Turns keyboard help on and off. When on, pressing a key on the keyboard will tell you what script is associated with it, if any.")

	def script_reportCurrentLine(self,keyPress):
		obj=api.getFocusObject()
		virtualBuffer=obj.virtualBuffer
		if hasattr(virtualBuffer,'TextInfo') and not virtualBuffer.passThrough:
			obj=virtualBuffer
		try:
			info=obj.makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError, RuntimeError):
			info=obj.makeTextInfo(textInfos.POSITION_FIRST)
		info.expand(textInfos.UNIT_LINE)
		if scriptHandler.getLastScriptRepeatCount()==0:
			speech.speakTextInfo(info,reason=speech.REASON_CARET)
		else:
			speech.speakSpelling(info.text)
	script_reportCurrentLine.__doc__=_("Reports the current line under the application cursor. Pressing this key twice will spell the current line")

	def script_leftMouseClick(self,keyPress):
		ui.message(_("left click"))
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
	script_leftMouseClick.__doc__=_("Clicks the left mouse button once at the current mouse position")

	def script_rightMouseClick(self,keyPress):
		ui.message(_("right click"))
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTUP,0,0,None,None)
	script_rightMouseClick.__doc__=_("Clicks the right mouse button once at the current mouse position")

	def script_toggleLeftMouseButton(self,keyPress):
		if winUser.getKeyState(winUser.VK_LBUTTON)&32768:
			ui.message(_("left mouse button unlock"))
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		else:
			ui.message(_("left mouse button lock"))
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
	script_toggleLeftMouseButton.__doc__=_("Locks or unlocks the left mouse button")

	def script_toggleRightMouseButton(self,keyPress):
		if winUser.getKeyState(winUser.VK_RBUTTON)&32768:
			ui.message(_("right mouse button unlock"))
			winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTUP,0,0,None,None)
		else:
			ui.message(_("right mouse button lock"))
			winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTDOWN,0,0,None,None)
	script_toggleRightMouseButton.__doc__=_("Locks or unlocks the right mouse button")

	def script_reportCurrentSelection(self,keyPress):
		obj=api.getFocusObject()
		virtualBuffer=obj.virtualBuffer
		if hasattr(virtualBuffer,'TextInfo') and not virtualBuffer.passThrough:
			obj=virtualBuffer
		try:
			info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
		except (RuntimeError, NotImplementedError):
			info=None
		if not info or info.isCollapsed:
			speech.speakMessage(_("no selection"))
		else:
			speech.speakMessage(_("selected %s")%info.text)
	script_reportCurrentSelection.__doc__=_("Announces the current selection in edit controls and documents. If there is no selection it says so.")

	def script_dateTime(self,keyPress):
		if scriptHandler.getLastScriptRepeatCount()==0:
			text=winKernel.GetTimeFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.TIME_NOSECONDS, None, None)
		else:
			text=winKernel.GetDateFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.DATE_LONGDATE, None, None)
		ui.message(text)
	script_dateTime.__doc__=_("If pressed once, reports the current time. If pressed twice, reports the current date")

	def script_increaseSynthSetting(self,keyPress):
		settingName=globalVars.settingsRing.currentSettingName
		if not settingName:
			ui.message(_("No settings"))
			return
		settingValue=globalVars.settingsRing.increase()
		ui.message("%s %s" % (settingName,settingValue))
	script_increaseSynthSetting.__doc__=_("Increases the currently active setting in the synth settings ring")

	def script_decreaseSynthSetting(self,keyPress):
		settingName=globalVars.settingsRing.currentSettingName
		if not settingName:
			ui.message(_("No settings"))
			return
		settingValue=globalVars.settingsRing.decrease()
		ui.message("%s %s" % (settingName,settingValue))
	script_decreaseSynthSetting.__doc__=_("Decreases the currently active setting in the synth settings ring")

	def script_nextSynthSetting(self,keyPress):
		nextSettingName=globalVars.settingsRing.next()
		if not nextSettingName:
			ui.message(_("No settings"))
			return
		nextSettingValue=globalVars.settingsRing.currentSettingValue
		ui.message("%s %s"%(nextSettingName,nextSettingValue))
	script_nextSynthSetting.__doc__=_("Moves to the next available setting in the synth settings ring")

	def script_previousSynthSetting(self,keyPress):
		previousSettingName=globalVars.settingsRing.previous()
		if not previousSettingName:
			ui.message(_("No settings"))
			return
		previousSettingValue=globalVars.settingsRing.currentSettingValue
		ui.message("%s %s"%(previousSettingName,previousSettingValue))
	script_previousSynthSetting.__doc__=_("Moves to the previous available setting in the synth settings ring")

	def script_toggleSpeakTypedCharacters(self,keyPress):
		if config.conf["keyboard"]["speakTypedCharacters"]:
			onOff=_("off")
			config.conf["keyboard"]["speakTypedCharacters"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakTypedCharacters"]=True
		ui.message(_("speak typed characters")+" "+onOff)
	script_toggleSpeakTypedCharacters.__doc__=_("Toggles on and off the speaking of typed characters")

	def script_toggleSpeakTypedWords(self,keyPress):
		if config.conf["keyboard"]["speakTypedWords"]:
			onOff=_("off")
			config.conf["keyboard"]["speakTypedWords"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakTypedWords"]=True
		ui.message(_("speak typed words")+" "+onOff)
	script_toggleSpeakTypedWords.__doc__=_("Toggles on and off the speaking of typed words")

	def script_toggleSpeakCommandKeys(self,keyPress):
		if config.conf["keyboard"]["speakCommandKeys"]:
			onOff=_("off")
			config.conf["keyboard"]["speakCommandKeys"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakCommandKeys"]=True
		ui.message(_("speak command keys")+" "+onOff)
	script_toggleSpeakCommandKeys.__doc__=_("Toggles on and off the speaking of typed keys, that are not specifically characters")

	def script_toggleSpeakPunctuation(self,keyPress):
		if config.conf["speech"]["speakPunctuation"]:
			onOff=_("off")
			config.conf["speech"]["speakPunctuation"]=False
		else:
			onOff=_("on")
			config.conf["speech"]["speakPunctuation"]=True
		ui.message(_("speak punctuation")+" "+onOff)
	script_toggleSpeakPunctuation.__doc__=_("Toggles on and off the speaking of punctuation. When on NVDA will say the names of punctuation symbols, when off it will be up to the synthesizer as to how it speaks punctuation")

	def script_moveMouseToNavigatorObject(self,keyPress):
		obj=api.getNavigatorObject() 
		try:
			p=api.getReviewPosition().pointAtStart
		except NotImplementedError:
			p=None
		if p:
			x=p.x
			y=p.y
		else:
			try:
				(left,top,width,height)=obj.location
			except:
				ui.message(_("object has no location"))
				return
			x=left+(width/2)
			y=top+(height/2)
		winUser.setCursorPos(x,y)
		mouseHandler.executeMouseMoveEvent(x,y)
	script_moveMouseToNavigatorObject.__doc__=_("Moves the mouse pointer to the current navigator object")

	def script_moveNavigatorObjectToMouse(self,keyPress):
		ui.message(_("Move navigator object to mouse"))
		obj=api.getMouseObject()
		api.setNavigatorObject(obj)
		speech.speakObject(obj)
	script_moveNavigatorObjectToMouse.__doc__=_("Sets the navigator object to the current object under the mouse pointer and speaks it")

	def script_navigatorObject_current(self,keyPress):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		if scriptHandler.getLastScriptRepeatCount()>=1:
			if curObject.TextInfo!=NVDAObjectTextInfo:
				textList=[]
				if curObject.name and isinstance(curObject.name, basestring) and not curObject.name.isspace():
					textList.append(curObject.name)
				try:
					info=curObject.makeTextInfo(textInfos.POSITION_SELECTION)
					if not info.isCollapsed:
						textList.append(info.text)
					else:
						info.expand(textInfos.UNIT_LINE)
						if not info.isCollapsed:
							textList.append(info.text)
				except (RuntimeError, NotImplementedError):
					# No caret or selection on this object.
					pass
			else:
				textList=[prop for prop in (curObject.name, curObject.value) if prop and isinstance(prop, basestring) and not prop.isspace()]
			text=" ".join(textList)
			if len(text)>0 and not text.isspace():
				if scriptHandler.getLastScriptRepeatCount()==1:
					speech.speakSpelling(text)
				else:
					if api.copyToClip(text):
						speech.speakMessage(_("%s copied to clipboard")%text)
		else:
			speech.speakObject(curObject,reason=speech.REASON_QUERY)
	script_navigatorObject_current.__doc__=_("Reports the current navigator object or, if pressed three times, Copies name and value of current navigator object to the clipboard")

	def script_navigatorObject_currentDimensions(self,keyPress):
		obj=api.getNavigatorObject()
		if not obj:
			ui.message(_("no navigator object"))
		location=obj.location
		if not location:
			ui.message(_("No location information for navigator object"))
		(left,top,width,height)=location
		deskLocation=api.getDesktopObject().location
		if not deskLocation:
			ui.message(_("No location information for screen"))
		(deskLeft,deskTop,deskWidth,deskHeight)=deskLocation
		percentFromLeft=(float(left-deskLeft)/deskWidth)*100
		percentFromTop=(float(top-deskTop)/deskHeight)*100
		percentWidth=(float(width)/deskWidth)*100
		percentHeight=(float(height)/deskHeight)*100
		ui.message(_("Object edges positioned %.1f per cent from left edge of screen, %.1f per cent from top edge of screen, width is %.1f per cent of screen, height is %.1f per cent of screen")%(percentFromLeft,percentFromTop,percentWidth,percentHeight))
	script_navigatorObject_currentDimensions.__doc__=_("Reports the hight, width and position of the current navigator object")

	def script_navigatorObject_toFocus(self,keyPress):
		obj=api.getFocusObject()
		if not isinstance(obj,NVDAObject):
			speech.speakMessage(_("no focus"))
		api.setNavigatorObject(obj)
		speech.speakMessage(_("move to focus"))
		speech.speakObject(obj,reason=speech.REASON_QUERY)
	script_navigatorObject_toFocus.__doc__=_("Sets the navigator object to the current focus")

	def script_navigatorObject_moveFocus(self,keyPress):
		obj=api.getNavigatorObject()
		if not isinstance(obj,NVDAObject):
			speech.speakMessage(_("no focus"))
		obj.setFocus()
		speech.speakMessage(_("move focus"))
	script_navigatorObject_toFocus.__doc__=_("Sets the keyboard focus to the navigator object")

	def script_navigatorObject_parent(self,keyPress):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		curObject=curObject.parent
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=speech.REASON_QUERY)
		else:
			speech.speakMessage(_("No parents"))
	script_navigatorObject_parent.__doc__=_("Sets the navigator object to the parent of the object it is currently on and speaks it")

	def script_navigatorObject_next(self,keyPress):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		curObject=curObject.next
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=speech.REASON_QUERY)
		else:
			speech.speakMessage(_("No next"))
	script_navigatorObject_next.__doc__=_("Sets the navigator object to the object next to the one it is currently on and speaks it")

	def script_navigatorObject_previous(self,keyPress):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		curObject=curObject.previous
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=speech.REASON_QUERY)
		else:
			speech.speakMessage(_("No previous"))
	script_navigatorObject_previous.__doc__=_("Sets the navigator object to the object previous to the one it is currently on and speaks it")

	def script_navigatorObject_firstChild(self,keyPress):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		curObject=curObject.firstChild
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=speech.REASON_QUERY)
		else:
			speech.speakMessage(_("No children"))
	script_navigatorObject_firstChild.__doc__=_("Sets the navigator object to the first child object of the one it is currently on and speaks it")

	def script_navigatorObject_nextInFlow(self,keyPress):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		up=[]
		down=[]
		curObject=curObject.getNextInFlow(up=up,down=down)
		if curObject is not None:
			api.setNavigatorObject(curObject)
			if len(up)>0:
				for count in range(len(up)+1):
					tones.beep(880*(1.25**count),50)
					time.sleep(0.025)
			if len(down)>0:
				for count in range(len(down)+1):
					tones.beep(880/(1.25**count),50)
					time.sleep(0.025)
			speech.speakObject(curObject,reason=speech.REASON_QUERY)
		else:
			speech.speakMessage(_("end of flow"))
	script_navigatorObject_nextInFlow.__doc__=_("Sets the navigator object to the object this object flows to and speaks it")

	def script_navigatorObject_previousInFlow(self,keyPress):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		up=[]
		down=[]
		curObject=curObject.getPreviousInFlow(up=up,down=down)
		if curObject is not None:
			api.setNavigatorObject(curObject)
			if len(up)>0:
				for count in range(len(up)+1):
					tones.beep(880*(1.25**count),50)
					time.sleep(0.025)
			if len(down)>0:
				for count in range(len(down)+1):
					tones.beep(880/(1.25**count),50)
					time.sleep(0.025)
			speech.speakObject(curObject,reason=speech.REASON_QUERY)
		else:
			speech.speakMessage(_("Beginning of flow"))
	script_navigatorObject_previousInFlow.__doc__=_("Sets the navigator object to the object this object flows from and speaks it")

	def script_navigatorObject_doDefaultAction(self,keyPress):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		try:
			action=curObject.getActionName()
		except NotImplementedError:
			ui.message(_("No default action"))
			return
		try:
			curObject.doAction()
		except NotImplementedError:
			ui.message(_("default action failed"))
			return
		ui.message("%s"%action)
	script_navigatorObject_doDefaultAction.__doc__=_("Performs the default action on the current navigator object (example: presses it if it is a button).")

	def script_review_top(self,keyPress):
		info=api.getReviewPosition().obj.makeTextInfo(textInfos.POSITION_FIRST)
		api.setReviewPosition(info.copy())
		info.expand(textInfos.UNIT_LINE)
		speech.speakMessage(_("top"))
		speech.speakTextInfo(info,reason=speech.REASON_CARET)
	script_review_top.__doc__=_("Moves the review cursor to the top line of the current navigator object and speaks it")

	def script_review_previousLine(self,keyPress):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse()
		res=info.move(textInfos.UNIT_LINE,-1)
		api.setReviewPosition(info.copy())
		info.expand(textInfos.UNIT_LINE)
		if res==0:
			speech.speakMessage(_("top"))
		speech.speakTextInfo(info,reason=speech.REASON_CARET)
	script_review_previousLine.__doc__=_("Moves the review cursor to the previous line of the current navigator object and speaks it")

	def script_review_currentLine(self,keyPress):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		if scriptHandler.getLastScriptRepeatCount()==0:
			speech.speakTextInfo(info,reason=speech.REASON_CARET)
		else:
			speech.speakSpelling(info._get_text())
	script_review_currentLine.__doc__=_("Reports the line of the current navigator object where the review cursor is situated. If this key is pressed twice, the current line will be spelled")

	def script_review_nextLine(self,keyPress):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse()
		res=info.move(textInfos.UNIT_LINE,1)
		api.setReviewPosition(info.copy())
		info.expand(textInfos.UNIT_LINE)
		if res==0:
			speech.speakMessage(_("bottom"))
		speech.speakTextInfo(info,reason=speech.REASON_CARET)
	script_review_nextLine.__doc__=_("Moves the review cursor to the next line of the current navigator object and speaks it")

	def script_review_bottom(self,keyPress):
		info=api.getReviewPosition().obj.makeTextInfo(textInfos.POSITION_LAST)
		api.setReviewPosition(info.copy())
		info.expand(textInfos.UNIT_LINE)
		speech.speakMessage(_("bottom"))
		speech.speakTextInfo(info,reason=speech.REASON_CARET)
	script_review_bottom.__doc__=_("Moves the review cursor to the bottom line of the current navigator object and speaks it")

	def script_review_previousWord(self,keyPress):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_WORD)
		info.collapse()
		res=info.move(textInfos.UNIT_WORD,-1)
		api.setReviewPosition(info.copy())
		info.expand(textInfos.UNIT_WORD)
		if res==0:
			speech.speakMessage(_("top"))
		speech.speakTextInfo(info,reason=speech.REASON_CARET,unit=textInfos.UNIT_WORD)
	script_review_previousWord.__doc__=_("Moves the review cursor to the previous word of the current navigator object and speaks it")

	def script_review_currentWord(self,keyPress):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_WORD)
		if scriptHandler.getLastScriptRepeatCount()==0:
			speech.speakTextInfo(info,reason=speech.REASON_CARET,unit=textInfos.UNIT_WORD)
		else:
			speech.speakSpelling(info._get_text())
	script_review_currentWord.__doc__=_("Speaks the word of the current navigator object where the review cursor is situated. If this key is pressed twice, the word will be spelled")

	def script_review_nextWord(self,keyPress):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_WORD)
		info.collapse()
		res=info.move(textInfos.UNIT_WORD,1)
		api.setReviewPosition(info.copy())
		info.expand(textInfos.UNIT_WORD)
		if res==0:
			speech.speakMessage(_("bottom"))
		speech.speakTextInfo(info,reason=speech.REASON_CARET,unit=textInfos.UNIT_WORD)
	script_review_nextWord.__doc__=_("Moves the review cursor to the next word of the current navigator object and speaks it")

	def script_review_startOfLine(self,keyPress):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse()
		api.setReviewPosition(info.copy())
		info.expand(textInfos.UNIT_CHARACTER)
		speech.speakMessage(_("left"))
		speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER,reason=speech.REASON_CARET)
	script_review_startOfLine.__doc__=_("Moves the review cursor to the first character of the line where it is situated in the current navigator object and speaks it")

	def script_review_previousCharacter(self,keyPress):
		lineInfo=api.getReviewPosition().copy()
		lineInfo.expand(textInfos.UNIT_LINE)
		charInfo=api.getReviewPosition().copy()
		charInfo.expand(textInfos.UNIT_CHARACTER)
		charInfo.collapse()
		res=charInfo.move(textInfos.UNIT_CHARACTER,-1)
		if res==0 or charInfo.compareEndPoints(lineInfo,"startToStart")<0:
			speech.speakMessage(_("left"))
			reviewInfo=api.getReviewPosition().copy()
			reviewInfo.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(reviewInfo,unit=textInfos.UNIT_CHARACTER,reason=speech.REASON_CARET)
		else:
			api.setReviewPosition(charInfo.copy())
			charInfo.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(charInfo,unit=textInfos.UNIT_CHARACTER,reason=speech.REASON_CARET)
	script_review_previousCharacter.__doc__=_("Moves the review cursor to the previous character of the current navigator object and speaks it")

	def script_review_currentCharacter(self,keyPress):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_CHARACTER)
		if scriptHandler.getLastScriptRepeatCount()==0:
			speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER,reason=speech.REASON_CARET)
		else:
			try:
				c = ord(info._get_text())
				speech.speakMessage("%d," % c)
				speech.speakSpelling(hex(c))
			except:
				speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER,reason=speech.REASON_CARET)
	script_review_currentCharacter.__doc__=_("Reports the character of the current navigator object where the review cursor is situated. If this key is pressed twice, ascii and hexadecimal values are spoken for the character")

	def script_review_nextCharacter(self,keyPress):
		lineInfo=api.getReviewPosition().copy()
		lineInfo.expand(textInfos.UNIT_LINE)
		charInfo=api.getReviewPosition().copy()
		charInfo.expand(textInfos.UNIT_CHARACTER)
		charInfo.collapse()
		res=charInfo.move(textInfos.UNIT_CHARACTER,1)
		if res==0 or charInfo.compareEndPoints(lineInfo,"endToEnd")>=0:
			speech.speakMessage(_("right"))
			reviewInfo=api.getReviewPosition().copy()
			reviewInfo.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(reviewInfo,unit=textInfos.UNIT_CHARACTER,reason=speech.REASON_CARET)
		else:
			api.setReviewPosition(charInfo.copy())
			charInfo.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(charInfo,unit=textInfos.UNIT_CHARACTER,reason=speech.REASON_CARET)
	script_review_nextCharacter.__doc__=_("Moves the review cursor to the next character of the current navigator object and speaks it")

	def script_review_endOfLine(self,keyPress):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse(end=True)
		info.move(textInfos.UNIT_CHARACTER,-1)
		api.setReviewPosition(info.copy())
		info.expand(textInfos.UNIT_CHARACTER)
		speech.speakMessage(_("right"))
		speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER,reason=speech.REASON_CARET)
	script_review_endOfLine.__doc__=_("Moves the review cursor to the last character of the line where it is situated in the current navigator object and speaks it")

	def script_review_moveToCaret(self,keyPress):
		try:
			info=api.getReviewPosition().obj.makeTextInfo(textInfos.POSITION_CARET)
		except NotImplementedError:
				ui.message(_("No caret"))
				return
		api.setReviewPosition(info.copy())
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info,reason=speech.REASON_CARET)
	script_review_moveToCaret.__doc__=_("Moves the review cursor to the position of the system caret, in the current navigator object")

	def script_review_moveCaretHere(self,keyPress):
		review=api.getReviewPosition()
		try:
			review.updateCaret()
		except NotImplementedError:
			ui.message(_("no caret"))
			return
		info=review.copy()
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info,reason=speech.REASON_CARET)
	script_review_moveCaretHere.__doc__=_("Moves the system caret to the position of the review cursor , in the current navigator object")

	def script_speechMode(self,keyPress):
		curMode=speech.speechMode
		speech.speechMode=speech.speechMode_talk
		newMode=(curMode+1)%3
		if newMode==speech.speechMode_off:
			name=_("off")
		elif newMode==speech.speechMode_beeps:
			name=_("beeps")
		elif newMode==speech.speechMode_talk:
			name=_("talk")
		speech.cancelSpeech()
		ui.message(_("speech mode %s")%name)
		speech.speechMode=newMode
	script_speechMode.__doc__=_("Toggles between the speech modes of off, beep and talk. When set to off NVDA will not speak anything. If beeps then NVDA will simply beep each time it its supposed to speak something. If talk then NVDA wil just speak normally.")

	def _getDocumentForFocusedEmbeddedObject(self):
		for ancestor in reversed(api.getFocusAncestors()):
			if ancestor.role == controlTypes.ROLE_DOCUMENT:
				return ancestor

	def script_toggleVirtualBufferPassThrough(self,keyPress):
		vbuf = api.getFocusObject().virtualBuffer
		if not vbuf:
			# We might be in an embedded object or application, so try searching the ancestry for an object which can return focus to the document.
			docObj = self._getDocumentForFocusedEmbeddedObject()
			if not docObj:
				return
			docObj.setFocus()
			return

		# Toggle virtual buffer pass-through.
		vbuf.passThrough = not vbuf.passThrough
		# If we are enabling pass-through, the user has explicitly chosen to do so, so disable auto-pass-through.
		# If we're disabling pass-through, re-enable auto-pass-through.
		vbuf.disableAutoPassThrough = vbuf.passThrough
		virtualBufferHandler.reportPassThrough(vbuf)
	script_toggleVirtualBufferPassThrough.__doc__=_("Toggles between browse mode and focus mode. When in focus mode, keys will pass straight through to the application, allowing you to interact directly with a control. When in browse mode, you can navigate the document with the cursor, quick navigation keys, etc.")

	def script_quit(self,keyPress):
		gui.quit()
	script_quit.__doc__=_("Quits NVDA!")

	def script_showGui(self,keyPress):
		gui.showGui()
	script_showGui.__doc__=_("Shows the NVDA menu")

	def script_review_sayAll(self,keyPress):
		info=api.getReviewPosition().copy()
		sayAllHandler.readText(info,sayAllHandler.CURSOR_REVIEW)
	script_review_sayAll.__doc__ = _("reads from the review cursor  up to end of current text, moving the review cursor as it goes")

	def script_navigatorObject_sayAll(self,keyPress):
		obj=api.getNavigatorObject()
		sayAllHandler.readObjects(obj)
	script_navigatorObject_sayAll.__doc__ = _("reads from the navigator object ")

	def script_sayAll(self,keyPress):
		o=api.getFocusObject()
		v=o.virtualBuffer
		if v and not v.passThrough:
			o=v
		try:
			info=o.makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError, RuntimeError):
			return
		sayAllHandler.readText(info,sayAllHandler.CURSOR_CARET)
	script_sayAll.__doc__ = _("reads from the system caret up to the end of the text, moving the caret as it goes")

	def script_reportFormatting(self,keyPress):
		formatConfig={
			"detectFormatAfterCursor":False,
			"reportFontName":True,"reportFontSize":True,"reportFontAttributes":True,
			"reportStyle":True,"reportAlignment":True,"reportSpellingErrors":True,
			"reportPage":False,"reportLineNumber":False,"reportTables":False,
			"reportLinks":False,"reportHeadings":False,"reportLists":False,
			"reportBlockQuotes":False,
		}
		o=api.getFocusObject()
		v=o.virtualBuffer
		if v and not v.passThrough:
			o=v
		try:
			info=o.makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError, RuntimeError):
			info=o.makeTextInfo(textInfos.POSITION_FIRST)
		info.expand(textInfos.UNIT_CHARACTER)
		formatField=textInfos.FormatField()
		for field in info.getTextWithFields(formatConfig):
			if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField):
				formatField.update(field.field)
		text=speech.getFormatFieldSpeech(formatField,formatConfig=formatConfig) if formatField else None
		if not text:
			ui.message(_("No formatting information"))
			return
		ui.message(text)
	script_reportFormatting.__doc__ = _("Reports formatting info for the current cursor position within a document")

	def script_reportCurrentFocus(self,keyPress):
		focusObject=api.getFocusObject()
		if isinstance(focusObject,NVDAObject):
			if scriptHandler.getLastScriptRepeatCount()==0:
				speech.speakObject(focusObject, reason=speech.REASON_QUERY)
			else:
				speech.speakSpelling(focusObject.name)
		else:
			speech.speakMessage(_("no focus"))
	script_reportCurrentFocus.__doc__ = _("reports the object with focus")

	def script_reportStatusLine(self,keyPress):
		obj = api.getStatusBar()
		if not obj:
			ui.message(_("no status bar found"))
			return
		text = api.getStatusBarText(obj)

		if scriptHandler.getLastScriptRepeatCount()==0:
			ui.message(text)
		else:
			speech.speakSpelling(text)
		api.setNavigatorObject(obj)
	script_reportStatusLine.__doc__ = _("reads the current application status bar and moves the navigator to it")

	def script_toggleMouseTracking(self,keyPress):
		if config.conf["mouse"]["enableMouseTracking"]:
			onOff=_("off")
			config.conf["mouse"]["enableMouseTracking"]=False
		else:
			onOff=_("on")
			config.conf["mouse"]["enableMouseTracking"]=True
		ui.message(_("Mouse tracking")+" "+onOff)
	script_toggleMouseTracking.__doc__=_("Toggles the reporting of information as the mouse moves")

	def script_title(self,keyPress):
		obj=api.getForegroundObject()
		title=obj.name
		if not isinstance(title,basestring) or not title or title.isspace():
			title=obj.appModule.appName  if obj.appModule else None
			if not isinstance(title,basestring) or not title or title.isspace():
				title=_("no title")
		repeatCount=scriptHandler.getLastScriptRepeatCount()
		if repeatCount==0:
			ui.message(title)
		elif repeatCount==1:
			speech.speakSpelling(title)
		else:
			if api.copyToClip(title):
				ui.message(_("%s copied to clipboard")%title)
	script_title.__doc__=_("Reports the title of the current application or foreground window. If pressed twice, spells the title. If pressed thrice, copies the title to the clipboard")

	def script_speakForeground(self,keyPress):
		obj=api.getForegroundObject()
		if obj:
			speech.speakObject(obj,reason=speech.REASON_QUERY)
			obj.speakDescendantObjects()
	script_speakForeground.__doc__ = _("speaks the current foreground object")

	def script_test_navigatorWindowInfo(self,keyPress):
		obj=api.getNavigatorObject()
		import ctypes
		import winUser
		w=ctypes.windll.user32.GetAncestor(obj.windowHandle,3)
		w=ctypes.windll.user32.GetAncestor(w,3)
		className=winUser.getClassName(w)
		speech.speakMessage("%s, %s"%(w,className))
		if not isinstance(obj,NVDAObject): 
			speech.speakMessage(_("no navigator object"))
			return
		if scriptHandler.getLastScriptRepeatCount()>=1:
			if api.copyToClip("Control ID: %s\r\nClass: %s\r\ninternal text: %s"%(winUser.getControlID(obj.windowHandle),obj.windowClassName,winUser.getWindowText(obj.windowHandle))):
				speech.speakMessage(_("copied to clipboard"))
		else:
			log.info("%s %s"%(obj.role,obj.windowHandle))
			speech.speakMessage("%s"%obj)
			speech.speakMessage(_("Control ID: %s")%winUser.getControlID(obj.windowHandle))
			speech.speakMessage(_("Class: %s")%obj.windowClassName)
			speech.speakSpelling(obj.windowClassName)
			speech.speakMessage(_("internal text: %s")%winUser.getWindowText(obj.windowHandle))
			speech.speakMessage(_("text: %s")%obj.windowText)
			speech.speakMessage("is unicode: %s"%ctypes.windll.user32.IsWindowUnicode(obj.windowHandle))
	script_test_navigatorWindowInfo.__doc__ = _("reports some information about the current navigator object, mainly useful for developers. When pressed 2 times it copies control id, class and internal text to the windows clipboard")

	def script_toggleProgressBarOutput(self,keyPress):
		outputMode=config.conf["presentation"]["progressBarUpdates"]["progressBarOutputMode"]
		if outputMode=="both":
			outputMode="off"
			ui.message(_("no progress bar updates"))
		elif outputMode=="off":
			outputMode="speak"
			ui.message(_("speak progress bar updates"))
		elif outputMode=="speak":
			outputMode="beep"
			ui.message(_("beep for progress bar updates"))
		else:
			outputMode="both"
			ui.message(_("beep and speak progress bar updates"))
		config.conf["presentation"]["progressBarUpdates"]["progressBarOutputMode"]=outputMode
	script_toggleProgressBarOutput.__doc__=_("Toggles between beeps, speech, beeps and speech, and off, for reporting progress bar updates")

	def script_toggleReportDynamicContentChanges(self,keyPress):
		if globalVars.reportDynamicContentChanges:
			onOff=_("off")
			globalVars.reportDynamicContentChanges=False
		else:
			onOff=_("on")
			globalVars.reportDynamicContentChanges=True
		ui.message(_("report dynamic content changes")+" "+onOff)
	script_toggleReportDynamicContentChanges.__doc__=_("Toggles on and off the reporting of dynamic content changes, such as new text in dos console windows")

	def script_toggleCaretMovesReviewCursor(self,keyPress):
		if globalVars.caretMovesReviewCursor:
			onOff=_("off")
			globalVars.caretMovesReviewCursor=False
		else:
			onOff=_("on")
			globalVars.caretMovesReviewCursor=True
		ui.message(_("caret moves review cursor")+" "+onOff)
	script_toggleCaretMovesReviewCursor.__doc__=_("Toggles on and off the movement of the review cursor due to the caret moving.")

	def script_toggleFocusMovesNavigatorObject(self,keyPress):
		if globalVars.focusMovesNavigatorObject:
			onOff=_("off")
			globalVars.focusMovesNavigatorObject=False
		else:
			onOff=_("on")
			globalVars.focusMovesNavigatorObject=True
		ui.message(_("focus moves navigator object")+" "+onOff)
	script_toggleFocusMovesNavigatorObject.__doc__=_("Toggles on and off the movement of the navigator object due to focus changes") 

	#added by Rui Batista<ruiandrebatista@gmail.com> to implement a battery status script
	def script_say_battery_status(self,keyPress):
		UNKNOWN_BATTERY_STATUS = 0xFF
		AC_ONLINE = 0X1
		NO_SYSTEM_BATTERY = 0X80
		sps = winKernel.SYSTEM_POWER_STATUS()
		if not winKernel.GetSystemPowerStatus(sps) or sps.BatteryFlag is UNKNOWN_BATTERY_STATUS:
			log.error("error accessing system power status")
			return
		if sps.BatteryFlag & NO_SYSTEM_BATTERY:
			ui.message(_("no system battery"))
			return
		text = _("%d percent") % sps.BatteryLifePercent + " "
		if sps.ACLineStatus & AC_ONLINE: text += _("AC power on")
		elif sps.BatteryLifeTime!=0xffffffff: 
			text += _("%d hours and %d minutes remaining") % (sps.BatteryLifeTime / 3600, (sps.BatteryLifeTime % 3600) / 60)
		ui.message(text)
	script_say_battery_status.__doc__ = _("reports battery status and time remaining if AC is not plugged in")

	def script_passNextKeyThrough(self,keyPress):
		keyboardHandler.passNextKeyThrough()
		ui.message(_("Pass next key through"))
 	script_passNextKeyThrough.__doc__=_("The next key that is pressed will not be handled at all by NVDA, it will be passed directly through to Windows.")

	def script_reportAppModuleInfo(self,keyPress):
		focus=api.getFocusObject()
		appName=appModuleHandler.getAppNameFromProcessID(focus.processID,True)
		message = _("Currently running application is %s") % appName
		mod=focus.appModule
		if isinstance(mod,appModuleHandler.AppModule) and type(mod)!=appModuleHandler.AppModule:
			message += _(" and currently loaded module is %s") % mod.appModuleName.split(".")[0]
		ui.message(message)
	script_reportAppModuleInfo.__doc__ = _("Speaks the filename of the active application along with the name of the currently loaded appModule")

	def script_activateGeneralSettingsDialog(self,keyPress):
		mainFrame.onGeneralSettingsCommand(None)
	script_activateGeneralSettingsDialog.__doc__ = _("Shows the NVDA general settings dialog")

	def script_activateSynthesizerDialog(self,keyPress):
		mainFrame.onSynthesizerCommand(None)
	script_activateSynthesizerDialog.__doc__ = _("Shows the NVDA synthesizer dialog")

	def script_activateVoiceDialog(self,keyPress):
		mainFrame.onVoiceCommand(None)
	script_activateVoiceDialog.__doc__ = _("Shows the NVDA voice settings dialog")

	def script_activateKeyboardSettingsDialog(self,keyPress):
		mainFrame.onKeyboardSettingsCommand(None)
	script_activateKeyboardSettingsDialog.__doc__ = _("Shows the NVDA keyboard settings dialog")

	def script_activateMouseSettingsDialog(self,keyPress):
		mainFrame.onMouseSettingsCommand(None)
	script_activateMouseSettingsDialog.__doc__ = _("Shows the NVDA mouse settings dialog")

	def script_activateObjectPresentationDialog(self,keyPress):
		mainFrame. onObjectPresentationCommand(None)
	script_activateObjectPresentationDialog.__doc__ = _("Shows the NVDA object presentation settings dialog")

	def script_activateVirtualBuffersDialog(self,keyPress):
		mainFrame.onVirtualBuffersCommand(None)
	script_activateVirtualBuffersDialog.__doc__ = _("Shows the NVDA virtual buffers settings dialog")

	def script_activateDocumentFormattingDialog(self,keyPress):
		mainFrame.onDocumentFormattingCommand(None)
	script_activateDocumentFormattingDialog.__doc__ = _("Shows the NVDA document formatting settings dialog")

	def script_saveConfiguration(self,keyPress):
		wx.CallAfter(mainFrame.onSaveConfigurationCommand, None)
	script_saveConfiguration.__doc__ = _("Saves the current NVDA configuration")

	def script_revertToSavedConfiguration(self,keyPress):
		mainFrame.onRevertToSavedConfigurationCommand(None)
	script_revertToSavedConfiguration.__doc__ = _("loads the saved NVDA configuration, overriding current changes")

	def script_activatePythonConsole(self,keyPress):
		if globalVars.appArgs.secure:
			return
		import pythonConsole
		if not pythonConsole.consoleUI:
			pythonConsole.initialize()
		pythonConsole.consoleUI.updateNamespaceSnapshotVars()
		pythonConsole.activate()
	script_activatePythonConsole.__doc__ = _("Activates the NVDA Python Console, primarily useful for development")

	def script_braille_toggleTether(self, keyPress):
		if braille.handler.tether == braille.handler.TETHER_FOCUS:
			braille.handler.tether = braille.handler.TETHER_REVIEW
			tetherMsg = _("review")
		else:
			braille.handler.tether = braille.handler.TETHER_FOCUS
			tetherMsg = _("focus")
		ui.message(_("Braille tethered to %s") % tetherMsg)
	script_braille_toggleTether.__doc__ = _("Toggle tethering of braille between the focus and the review position")

	def script_reportClipboardText(self,keyPress):
		try:
			text = api.getClipData()
		except:
			text = None
		if not text or not isinstance(text,basestring) or text.isspace():
			ui.message(_("There is no text on the clipboard"))
			return
		if len(text) < 1024: 
			ui.message(text)
		else:
			ui.message(_("The clipboard contains a large portion of text. It is %s characters long") % len(text))
	script_reportClipboardText.__doc__ = _("Reports the text on the Windows clipboard")

	def script_review_markStartForCopy(self, keyPress):
		self._copyStartMarker = api.getReviewPosition().copy()
		ui.message(_("Start marked"))
	script_review_markStartForCopy.__doc__ = _("Marks the current position of the review cursor as the start of text to be copied")

	def script_review_copy(self, keyPress):
		if not getattr(self, "_copyStartMarker", None):
			ui.message(_("No start marker set"))
			return
		pos = api.getReviewPosition().copy()
		if self._copyStartMarker.obj != pos.obj:
			ui.message(_("The start marker must reside within the same object"))
			return
		pos.move(textInfos.UNIT_CHARACTER, 1, endPoint="end")
		pos.setEndPoint(self._copyStartMarker, "startToStart")
		if pos.compareEndPoints(pos, "startToEnd") < 0 and pos.copyToClipboard():
			ui.message(_("Review selection copied to clipboard"))
		else:
			ui.message(_("No text to copy"))
			return
		self._copyStartMarker = None
	script_review_copy.__doc__ = _("Retrieves the text from the previously set start marker up to and including the current position of the review cursor and copies it to the clipboard")
