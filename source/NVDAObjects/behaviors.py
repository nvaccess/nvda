#NVDAObjects/behaviors.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>, Peter Vágner <peter.v@datagate.sk>

"""Mix-in classes which provide common behaviour for particular types of controls across different APIs.
"""

import time
import threading
import difflib
import tones
import queueHandler
import eventHandler
import controlTypes
import speech
import config
from . import NVDAObject, NVDAObjectTextInfo
import textInfos
import editableText
from logHandler import log

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
			if childRole in (controlTypes.ROLE_PROPERTYPAGE,controlTypes.ROLE_PANE,controlTypes.ROLE_PANEL,controlTypes.ROLE_WINDOW,controlTypes.ROLE_GROUPING):
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
			if childName and index<(childCount-1) and children[index+1].role not in (controlTypes.ROLE_GRAPHIC,controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_SEPARATOR,controlTypes.ROLE_WINDOW,controlTypes.ROLE_PANE) and children[index+1].name==childName:
				continue
			childText=child.makeTextInfo(textInfos.POSITION_ALL).text
			if not childText or childText.isspace() and child.TextInfo!=NVDAObjectTextInfo:
				childText=child.basicText
			textList.append(childText)
		return " ".join(textList)

	def _get_description(self):
		superDesc = super(Dialog, self).description
		if superDesc and not superDesc.isspace():
			# The object already provides a useful description, so don't override it.
			return superDesc
		return self.getDialogText(self)

	value = None

class EditableText(editableText.EditableText, NVDAObject):
	"""Provides scripts to report appropriately when moving the caret in editable text fields.
	This does not handle selection changes.
	To handle selection changes, use either L{EditableTextWithAutoSelectDetection} or L{EditableTextWithoutAutoSelectDetection}.
	"""

	shouldFireCaretMovementFailedEvents = True

class EditableTextWithAutoSelectDetection(EditableText):
	"""In addition to L{EditableText}, handles reporting of selection changes for objects which notify of them.
	To have selection changes reported, the object must notify of selection changes via the caret event.
	Optionally, it may notify of changes to content via the textChange, textInsert and textRemove events.
	If the object supports selection but does not notify of selection changes, L{EditableTextWithoutAutoSelectDetection} should be used instead.
	"""

	def event_gainFocus(self):
		super(EditableText, self).event_gainFocus()
		self.initAutoSelectDetection()

	def event_caret(self):
		super(EditableText, self).event_caret()
		self.detectPossibleSelectionChange()

	def event_textChange(self):
		self.hasContentChangedSinceLastSelection = True

	def event_textInsert(self):
		self.hasContentChangedSinceLastSelection = True

	def event_textRemove(self):
		self.hasContentChangedSinceLastSelection = True

class EditableTextWithoutAutoSelectDetection(editableText.EditableTextWithoutAutoSelectDetection, EditableText):
	"""In addition to L{EditableText}, provides scripts to report appropriately when the selection changes.
	This should be used when an object does not notify of selection changes.
	"""

	initOverlayClass = editableText.EditableTextWithoutAutoSelectDetection.initClass

class LiveText(NVDAObject):
	"""An object for which new text should be reported automatically.
	These objects present text as a single chunk
	and only fire an event indicating that some part of the text has changed; i.e. they don't provide the new text.
	Monitoring must be explicitly started and stopped using the L{startMonitoring} and L{stopMonitoring} methods.
	The object should notify of text changes using the textChange event.
	"""
	#: The time to wait before fetching text after a change event.
	STABILIZE_DELAY = 0
	# If the text is live, this is definitely content.
	presentationType = NVDAObject.presType_content

	def initOverlayClass(self):
		self._event = threading.Event()
		self._monitorThread = None
		self._keepMonitoring = False

	def startMonitoring(self):
		"""Start monitoring for new text.
		New text will be reported when it is detected.
		@note: If monitoring has already been started, this will have no effect.
		@see: L{stopMonitoring}
		"""
		if self._monitorThread:
			return
		self._monitorThread = threading.Thread(target=self._monitor)
		self._keepMonitoring = True
		self._event.clear()
		self._monitorThread.start()

	def stopMonitoring(self):
		"""Stop monitoring previously started with L{startMonitoring}.
		@note: If monitoring has not been started, this will have no effect.
		@see: L{startMonitoring}
		"""
		if not self._monitorThread:
			return
		self._keepMonitoring = False
		self._event.set()
		self._monitorThread = None

	def event_textChange(self):
		"""Fired when the text changes.
		@note: It is safe to call this directly from threads other than the main thread.
		"""
		self._event.set()

	def _getTextLines(self):
		"""Retrieve the text of this object in lines.
		This will be used to determine the new text to speak.
		The base implementation uses the L{TextInfo}.
		However, subclasses should override this if there is a better way to retrieve the text.
		@return: The current lines of text.
		@rtype: list of str
		"""
		return list(self.makeTextInfo(textInfos.POSITION_ALL).getTextInChunks(textInfos.UNIT_LINE))

	def _reportNewText(self, line):
		"""Report a line of new text.
		"""
		speech.speakText(line)

	def _monitor(self):
		try:
			oldLines = self._getTextLines()
		except:
			log.exception("Error getting initial lines")
			oldLines = []

		while self._keepMonitoring:
			self._event.wait()
			if not self._keepMonitoring:
				break
			if self.STABILIZE_DELAY > 0:
				# wait for the text to stabilise.
				time.sleep(self.STABILIZE_DELAY)
				if not self._keepMonitoring:
					# Monitoring was stopped while waiting for the text to stabilise.
					break
			self._event.clear()

			try:
				newLines = self._getTextLines()
				if config.conf["presentation"]["reportDynamicContentChanges"]:
					outLines = self._calculateNewText(newLines, oldLines)
					if len(outLines) == 1 and len(outLines[0]) == 1:
						# This is only a single character,
						# which probably means it is just a typed character,
						# so ignore it.
						del outLines[0]
					for line in outLines:
						queueHandler.queueFunction(queueHandler.eventQueue, self._reportNewText, line)
				oldLines = newLines
			except:
				log.exception("Error getting lines or calculating new text")

	def _calculateNewText(self, newLines, oldLines):
		outLines = []

		prevLine = None
		for line in difflib.ndiff(oldLines, newLines):
			if line[0] == "?":
				# We're never interested in these.
				continue
			if line[0] != "+":
				# We're only interested in new lines.
				prevLine = line
				continue
			text = line[2:]
			if not text or text.isspace():
				prevLine = line
				continue

			if prevLine and prevLine[0] == "-" and len(prevLine) > 2:
				# It's possible that only a few characters have changed in this line.
				# If so, we want to speak just the changed section, rather than the entire line.
				prevText = prevLine[2:]
				textLen = len(text)
				prevTextLen = len(prevText)
				# Find the first character that differs between the two lines.
				for pos in xrange(min(textLen, prevTextLen)):
					if text[pos] != prevText[pos]:
						start = pos
						break
				else:
					# We haven't found a differing character so far and we've hit the end of one of the lines.
					# This means that the differing text starts here.
					start = pos + 1
				# Find the end of the differing text.
				if textLen != prevTextLen:
					# The lines are different lengths, so assume the rest of the line changed.
					end = textLen
				else:
					for pos in xrange(textLen - 1, start - 1, -1):
						if text[pos] != prevText[pos]:
							end = pos + 1
							break

				if end - start < 15:
					# Less than 15 characters have changed, so only speak the changed chunk.
					text = text[start:end]

			if text and not text.isspace():
				outLines.append(text)
			prevLine = line

		return outLines

class Terminal(LiveText, EditableText):
	"""An object which both accepts text input and outputs text which should be reported automatically.
	This is an L{EditableText} object,
	as well as a L{liveText} object for which monitoring is automatically enabled and disabled based on whether it has focus.
	"""
	role = controlTypes.ROLE_TERMINAL

	def event_gainFocus(self):
		super(Terminal, self).event_gainFocus()
		self.startMonitoring()

	def event_loseFocus(self):
		self.stopMonitoring()
