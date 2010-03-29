#NVDAObjects/behaviors.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>, Peter Vágner <peter.v@datagate.sk>

"""Mix-in classes which provide common behaviour for particular types of controls across different APIs.
"""

import time
import tones
import api
import queueHandler
import controlTypes
import globalVars
import speech
import config
import eventHandler
from scriptHandler import isScriptWaiting
from . import NVDAObject, NVDAObjectTextInfo
import textInfos

class ProgressBar(NVDAObject):

	progressValueCache={} #key is made of "speech" or "beep" and an x,y coordinate, value is the last percentage
 
	def event_valueChange(self):
		pbConf=config.conf["presentation"]["progressBarUpdates"]
		states=self.states
		if pbConf["progressBarOutputMode"]=="off" or controlTypes.STATE_INVISIBLE in states or controlTypes.STATE_OFFSCREEN in states:
			return super(ProgressBar,self).event_valueChange()
		val=self.value
		if val:
			val=val.rstrip('%\x00')
		if not val:
			return super(ProgressBar,self).event_valueChange()
		percentage = min(max(0.0, float(val)), 100.0)
		if not pbConf["reportBackgroundProgressBars"] and not self.isInForeground:
			return
		try:
			left,top,width,height=self.location
		except:
			left=top=width=height=0
		x=left+(width/2)
		y=top+(height/2)
		lastBeepProgressValue=self.progressValueCache.get("beep,%d,%d"%(x,y),None)
		if pbConf["progressBarOutputMode"] in ("beep","both") and (lastBeepProgressValue is None or abs(percentage-lastBeepProgressValue)>=pbConf["beepPercentageInterval"]):
			tones.beep(pbConf["beepMinHZ"]*2**(percentage/25.0),40)
			self.progressValueCache["beep,%d,%d"%(x,y)]=percentage
		lastSpeechProgressValue=self.progressValueCache.get("speech,%d,%d"%(x,y),None)
		if pbConf["progressBarOutputMode"] in ("speak","both") and (lastSpeechProgressValue is None or abs(percentage-lastSpeechProgressValue)>=pbConf["speechPercentageInterval"]):
			queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,_("%d percent")%percentage)
			self.progressValueCache["speech,%d,%d"%(x,y)]=percentage

class Dialog(NVDAObject):
	"""Overrides the description property to obtain dialog text.
	"""

	@classmethod
	def getDialogText(cls,obj):
		"""This classmethod walks through the children of the given object, and collects up and returns any text that seems to be  part of a dialog's message text.
		@param obj: the object who's children you want to collect the text from
		@type obj: L{IAccessible}
		"""
		children=obj.children
		textList=[]
		childCount=len(children)
		for index in xrange(childCount):
			child=children[index]
			childStates=child.states
			childRole=child.role
			#We don't want to handle invisible or unavailable objects
			if controlTypes.STATE_INVISIBLE in childStates or controlTypes.STATE_UNAVAILABLE in childStates: 
				continue
			#For particular objects, we want to descend in to them and get their children's message text
			if childRole in (controlTypes.ROLE_PROPERTYPAGE,controlTypes.ROLE_PANE,controlTypes.ROLE_PANEL,controlTypes.ROLE_WINDOW):
				textList.append(cls.getDialogText(child))
				continue
			# We only want text from certain controls.
			if not (
				 # Static text, labels and links
				 childRole in (controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_LABEL,controlTypes.ROLE_LINK)
				# Read-only, non-multiline edit fields
				or (childRole==controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_READONLY in childStates and controlTypes.STATE_MULTILINE not in childStates)
			):
				continue
			#We should ignore a text object directly after a grouping object, as it's probably the grouping's description
			if index>0 and children[index-1].role==controlTypes.ROLE_GROUPING:
				continue
			#Like the last one, but a graphic might be before the grouping's description
			if index>1 and children[index-1].role==controlTypes.ROLE_GRAPHIC and children[index-2].role==controlTypes.ROLE_GROUPING:
				continue
			childName=child.name
			#Ignore objects that have another object directly after them with the same name, as this object is probably just a label for that object.
			#However, graphics, static text, separators and Windows are ok.
			if childName and index<(childCount-1) and children[index+1].role not in (controlTypes.ROLE_GRAPHIC,controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_SEPARATOR,controlTypes.ROLE_WINDOW) and children[index+1].name==childName:
				continue
			childText=child.makeTextInfo(textInfos.POSITION_ALL).text
			if not childText or childText.isspace() and child.TextInfo!=NVDAObjectTextInfo:
				childText=child.basicText
			textList.append(childText)
		return " ".join(textList)

	def _get_description(self):
		return self.getDialogText(self)

	value = None

class EditableText(NVDAObject):
	"""Provides scripts to report appropriately when moving the caret in editable text fields.
	This assumes the object can automatically detect selection changes and therefore does not handle the selection change keys.
	Use L{EditableTextWithoutAutoSelectDetection} if your object does not automatically detect selection changes.
	"""

	def _hasCaretMoved(self, bookmark, retryInterval=0.01, timeout=0.03):
		elapsed = 0
		while elapsed < timeout:
			if isScriptWaiting():
				return False
			api.processPendingEvents(processEventQueue=False)
			if eventHandler.isPendingEvents("gainFocus"):
				oldInCaretMovement=globalVars.inCaretMovement
				globalVars.inCaretMovement=True
				try:
					api.processPendingEvents()
				finally:
					globalVars.inCaretMovement=oldInCaretMovement
				return True
			#The caret may stop working as the focus jumps, we want to stay in the while loop though
			try:
				newBookmark = self.makeTextInfo(textInfos.POSITION_CARET).bookmark
				if newBookmark!=bookmark:
					return True
			except:
				pass
			time.sleep(retryInterval)
			elapsed += retryInterval
		return False

	def script_caret_moveByLine(self,gesture):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			gesture.send()
			return
		bookmark=info.bookmark
		gesture.send()
		if not self._hasCaretMoved(bookmark):
			eventHandler.executeEvent("caretMovementFailed", self, gesture=gesture)
		if not isScriptWaiting():
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if config.conf["reviewCursor"]["followCaret"]:
				api.setReviewPosition(info.copy())
			info.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(info)

	def script_caret_moveByCharacter(self,gesture):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			gesture.send()
			return
		bookmark=info.bookmark
		gesture.send()
		if not self._hasCaretMoved(bookmark):
			eventHandler.executeEvent("caretMovementFailed", self, gesture=gesture)
		if not isScriptWaiting():
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if config.conf["reviewCursor"]["followCaret"]:
				api.setReviewPosition(info.copy())
			info.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER)

	def script_caret_moveByWord(self,gesture):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			gesture.send()
			return
		bookmark=info.bookmark
		gesture.send()
		if not self._hasCaretMoved(bookmark):
			eventHandler.executeEvent("caretMovementFailed", self, gesture=gesture)
		if not isScriptWaiting():
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if config.conf["reviewCursor"]["followCaret"]:
				api.setReviewPosition(info.copy())
			info.expand(textInfos.UNIT_WORD)
			speech.speakTextInfo(info,unit=textInfos.UNIT_WORD)

	def script_caret_moveByParagraph(self,gesture):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			gesture.send()
			return
		bookmark=info.bookmark
		gesture.send()
		if not self._hasCaretMoved(bookmark):
			eventHandler.executeEvent("caretMovementFailed", self, gesture=gesture)
		if not isScriptWaiting():
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if config.conf["reviewCursor"]["followCaret"]:
				api.setReviewPosition(info.copy())
			info.expand(textInfos.UNIT_PARAGRAPH)
			speech.speakTextInfo(info)

	def _backspaceScriptHelper(self,unit,gesture):
		try:
			oldInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			gesture.send()
			return
		oldBookmark=oldInfo.bookmark
		testInfo=oldInfo.copy()
		res=testInfo.move(textInfos.UNIT_CHARACTER,-1)
		if res<0:
			testInfo.expand(unit)
			delChunk=testInfo.text
		else:
			delChunk=""
		gesture.send()
		if self._hasCaretMoved(oldBookmark):
			if len(delChunk)>1:
				speech.speakMessage(delChunk)
			else:
				speech.speakSpelling(delChunk)
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if config.conf["reviewCursor"]["followCaret"]:
				api.setReviewPosition(info)

	def script_caret_backspaceCharacter(self,gesture):
		self._backspaceScriptHelper(textInfos.UNIT_CHARACTER,gesture)

	def script_caret_backspaceWord(self,gesture):
		self._backspaceScriptHelper(textInfos.UNIT_WORD,gesture)

	def script_caret_delete(self,gesture):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			gesture.send()
			return
		bookmark=info.bookmark
		gesture.send()
		# We'll try waiting for the caret to move, but we don't care if it doesn't.
		self._hasCaretMoved(bookmark)
		if not isScriptWaiting():
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if config.conf["reviewCursor"]["followCaret"]:
				api.setReviewPosition(info.copy())
			info.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER)

	def initOverlayClass(self):
		for keyName, scriptName in (
			("ExtendedUp", "caret_moveByLine"),
			("ExtendedDown", "caret_moveByLine"),
			("ExtendedLeft", "caret_moveByCharacter"),
			("ExtendedRight", "caret_moveByCharacter"),
			("ExtendedPrior", "caret_moveByLine"),
			("ExtendedNext", "caret_moveByLine"),
			("Control+ExtendedLeft", "caret_moveByWord"),
			("Control+ExtendedRight", "caret_moveByWord"),
			("control+extendedUp", "caret_moveByParagraph"),
			("control+extendedDown", "caret_moveByParagraph"),
			("ExtendedHome", "caret_moveByCharacter"),
			("ExtendedEnd", "caret_moveByCharacter"),
			("control+extendedHome", "caret_moveByLine"),
			("control+extendedEnd", "caret_moveByLine"),
			("ExtendedDelete", "caret_delete"),
			("Back", "caret_backspaceCharacter"),
			("Control+Back", "caret_backspaceWord"),
		):
			self.bindKey_runtime(keyName, scriptName)

class EditableTextWithoutAutoSelectDetection(EditableText):
	"""In addition to L{EditableText}, provides scripts to report appropriately when the selection changes.
	This should be used when an object cannot automatically detect when the selection changes.
	"""

	def script_caret_changeSelection(self,gesture):
		try:
			oldInfo=self.makeTextInfo(textInfos.POSITION_SELECTION)
		except:
			gesture.send()
			return
		gesture.send()
		if not isScriptWaiting():
			api.processPendingEvents()
			focus=api.getFocusObject()
			try:
				newInfo=focus.makeTextInfo(textInfos.POSITION_SELECTION)
			except:
				return
			speech.speakSelectionChange(oldInfo,newInfo)

	def initOverlayClass(self):
		for keyName in (
			"shift+ExtendedUp",
			"shift+ExtendedDown",
			"shift+ExtendedLeft",
			"shift+ExtendedRight",
			"shift+ExtendedPrior",
			"shift+ExtendedNext",
			"shift+Control+ExtendedLeft",
			"shift+Control+ExtendedRight",
			"shift+control+extendedUp",
			"shift+control+extendedDown",
			"shift+ExtendedHome",
			"shift+ExtendedEnd",
			"shift+control+extendedHome",
			"shift+control+extendedEnd",
		):
			self.bindKey_runtime(keyName, "caret_changeSelection")
