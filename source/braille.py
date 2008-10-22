#braille.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import itertools
import os
import wx
import louis
import baseObject
import config
from logHandler import log
import controlTypes
import api
import textHandler
import speech

__path__ = ["brailleDisplayDrivers"]

#: The directory in which liblouis braille tables are located.
TABLES_DIR = r"louis\tables"

#: The table filenames and descriptions.
TABLES = (
	("en-us-comp6.ctb", _("English (U.S.) 6 dot computer braille")),
	("en-us-comp8.ctb", _("English (U.S.) 8 dot computer braille")),
	("UEBC-g1.utb", _("Unified English Braille Code grade 1")),
	("UEBC-g2.ctb", _("Unified English Braille Code grade 2")),
)

roleLabels = {
	controlTypes.ROLE_EDITABLETEXT: _("edt"),
	controlTypes.ROLE_LISTITEM: None,
	controlTypes.ROLE_MENUBAR: _("mnubar"),
	controlTypes.ROLE_MENU: _("mnu"),
	controlTypes.ROLE_MENUITEM: None,
	controlTypes.ROLE_BUTTON: _("btn"),
	controlTypes.ROLE_CHECKBOX: _("chk"),
	controlTypes.ROLE_RADIOBUTTON: _("rbtn"),
	controlTypes.ROLE_COMBOBOX: _("cbo"),
	controlTypes.ROLE_LINK: _("lnk"),
	controlTypes.ROLE_DIALOG: _("dlg"),
}

positiveStateLabels = {
	controlTypes.STATE_CHECKED: _("(x)"),
	controlTypes.STATE_SELECTED: _("sel"),
	controlTypes.STATE_HASPOPUP: _("submnu"),
}
negativeStateLabels = {
	controlTypes.STATE_CHECKED: _("( )"),
}

def _getDisplayDriver(name):
	return __import__(name,globals(),locals(),[]).BrailleDisplayDriver

def getDisplayList():
	displayList = []
	for name in (os.path.splitext(x)[0] for x in os.listdir(__path__[0]) if (x.endswith('.py') and not x.startswith('_'))):
		try:
			display = _getDisplayDriver(name)
			if display.check():
				displayList.append((display.name, display.description))
		except:
			pass
	return displayList

class Region(object):
	"""A region of braille to be displayed.
	Each portion of braille to be displayed is represented by a region.
	The region is responsible for retrieving its text and cursor position, translating it into braille cells and handling cursor routing requests relative to its braille cells.
	The L{BrailleBuffer} containing this region will call L{update} and expect that L{brailleCells} and L{brailleCursorPos} will be set appropriately.
	L{routeTo} will be called to handle a cursor routing request.
	"""

	def __init__(self):
		#: The original, raw text of this region.
		self.rawText = ""
		#: The position of the cursor in L{rawText}, C{None} if the cursor is not in this region.
		#: @type: int
		self.cursorPos = None
		#: The translated braille representation of this region.
		#: @type: [int, ...]
		self.brailleCells = []
		#: A list mapping positions in L{rawText} to positions in L{brailleCells}.
		#: @type: [int, ...]
		self.rawToBraillePos = []
		#: A list mapping positions in L{brailleCells} to positions in L{rawText}.
		#: @type: [int, ...]
		self.brailleToRawPos = []
		#: The position of the cursor in L{brailleCells}, C{None} if the cursor is not in this region.
		#: @type: int
		self.brailleCursorPos = None
		#: Whether to hide all previous regions.
		#: @type: bool
		self.hidePreviousRegions = False
		#: Whether this region should be positioned at the absolute left of the display when focused.
		#: @type: bool
		self.focusToHardLeft = False

	def update(self):
		"""Update this region.
		Subclasses should extend this to update L{rawText} and L{cursorPos} if necessary.
		The base class method handles translation of L{rawText} into braille, placing the result in L{brailleCells}. L{rawToBraillePos} and L{brailleToRawPos} are updated according to the translation.
		L{brailleCursorPos} is similarly updated based on L{cursorPos}.
		@postcondition: L{brailleCells} and L{brailleCursorPos} are updated and ready for rendering.
		"""
		mode = louis.dotsIO
		if config.conf["braille"]["expandAtCursor"] and self.cursorPos is not None:
			mode |= louis.compbrlAtCursor
		braille, self.brailleToRawPos, self.rawToBraillePos, brailleCursorPos = louis.translate([os.path.join(TABLES_DIR, config.conf["braille"]["translationTable"])], unicode(self.rawText), mode=mode, cursorPos=self.cursorPos or 0)
		# liblouis gives us back a character string of cells, so convert it to a list of ints.
		# For some reason, the highest bit is set, so only grab the lower 8 bits.
		self.brailleCells = [ord(cell) & 255 for cell in braille]
		if self.cursorPos is not None:
			self.brailleCursorPos = brailleCursorPos

	def routeTo(self, braillePos):
		"""Handle a cursor routing request.
		For example, this might activate an object or move the cursor to the requested position.
		@param braillePos: The routing position in L{brailleCells}.
		@type braillePos: int
		@note: If routing the cursor, L{brailleToRawPos} can be used to translate L{braillePos} into a position in L{rawText}.
		"""
		pass

	def nextLine(self):
		"""Move to the next line if possible.
		"""
		pass

	def previousLine(self):
		"""Move to the previous line if possible.
		"""
		pass

class TextRegion(Region):
	"""A simple region containing a string of text.
	"""

	def __init__(self, text):
		super(TextRegion, self).__init__()
		self.rawText = text

def getBrailleTextForProperties(**propertyValues):
	# TODO: Don't use speech functions.
	textList = []
	name = propertyValues.get("name")
	if name:
		textList.append(name)
	role = propertyValues.get("role")
	if role is not None:
		roleText = roleLabels.get(role, controlTypes.speechRoleLabels[role])
	else:
		role = propertyValues.get("_role")
		roleText = None
	value = propertyValues.get("value")
	if value and role not in speech.silentValuesForRoles:
		textList.append(value)
	states = propertyValues.get("states")
	if states:
		positiveStates = speech.processPositiveStates(role, states, speech.REASON_FOCUS, states)
		textList.extend(positiveStateLabels.get(state, controlTypes.speechStateLabels[state]) for state in positiveStates)
		negativeStates = speech.processNegativeStates(role, states, speech.REASON_FOCUS, None)
		textList.extend(negativeStateLabels.get(state, controlTypes.speechStateLabels[state]) for state in negativeStates)
	if roleText:
		textList.append(roleText)
	description = propertyValues.get("description")
	if description:
		textList.append(description)
	keyboardShortcut = propertyValues.get("keyboardShortcut")
	if keyboardShortcut:
		textList.append(keyboardShortcut)
	positionString = propertyValues["positionString"]
	if positionString:
		textList.append(positionString)
	level = propertyValues.get("level")
	if level:
		textList.append(_("lvl %s") % level)
	return " ".join([x for x in textList if x])

class NVDAObjectRegion(Region):
	"""A region to provide a braille representation of an NVDAObject.
	This region will update based on the current state of the associated NVDAObject.
	A cursor routing request will activate the object's default action.
	"""

	def __init__(self, obj, appendText=""):
		"""Constructor.
		@param obj: The associated NVDAObject.
		@type obj: L{NVDAObjects.NVDAObject}
		@param appendText: Text which should always be appended to the NVDAObject text, useful if this region will always precede other regions.
		@type appendText: str
		"""
		super(NVDAObjectRegion, self).__init__()
		self.obj = obj
		self.appendText = appendText

	def update(self):
		obj = self.obj
		text = getBrailleTextForProperties(name=obj.name, role=obj.role, value=obj.value, states=obj.states, description=obj.description, keyboardShortcut=obj.keyboardShortcut, positionString=obj.positionString)
		self.rawText = text + self.appendText
		super(NVDAObjectRegion, self).update()

	def routeTo(self, braillePos):
		self.obj.doDefaultAction()

class ReviewNVDAObjectRegion(NVDAObjectRegion):

	def routeTo(self, braillePos):
		pass

class TextInfoRegion(Region):

	def __init__(self, obj):
		super(TextInfoRegion, self).__init__()
		self.obj = obj

	def _isMultiline(self):
		# Terminals are inherently multiline, so they don't have the multiline state.
		return (self.obj.role == controlTypes.ROLE_TERMINAL or controlTypes.STATE_MULTILINE in self.obj.states)

	def _getSelection(self):
		"""Retrieve the selection.
		@return: The selection.
		@rtype: L{textHandler.TextInfo}
		"""
		return self.obj.makeTextInfo(textHandler.POSITION_SELECTION)

	def _setSelection(self, info):
		"""Set the selection.
		@param info: The range to which the selection should be moved.
		@type info: L{textHandler.TextInfo}
		"""
		info.updateSelection()

	def update(self):
		caret = self._getSelection()
		caret.collapse()
		# Get the line at the caret.
		self._line = line = caret.copy()
		line.expand(textHandler.UNIT_LINE)
		# Not all text APIs support offsets, so we can't always get the offset of the caret relative to the start of the line.
		# Therefore, grab the line in two parts.
		# First, the chunk from the start of the line up to the caret.
		chunk = line.copy()
		chunk.collapse()
		chunk.setEndPoint(caret, "endToEnd")
		self.rawText = chunk.text or ""
		# The cursor position is the length of this chunk, as its end is the caret.
		self.cursorPos = len(self.rawText)
		# Now, get the chunk from the caret to the end of the line.
		chunk.setEndPoint(line, "endToEnd")
		chunk.setEndPoint(caret, "startToStart")
		# Strip line ending characters, but add a space in case the caret is at the end of the line.
		self.rawText += (chunk.text or "").rstrip("\r\n\0\v\f") + " "
		# If this is not the first line, hide all previous regions.
		start = caret.obj.makeTextInfo(textHandler.POSITION_FIRST)
		self.hidePreviousRegions = (start.compareEndPoints(line, "startToStart") < 0)
		# If this is a multiline control, position it at the absolute left of the display when focused.
		self.focusToHardLeft = self._isMultiline()
		super(TextInfoRegion, self).update()

	def routeTo(self, braillePos):
		pos = self.brailleToRawPos[braillePos]
		# pos is relative to the start of the line.
		# Therefore, get the start of the line...
		dest = self._line.copy()
		dest.collapse()
		# and move pos characters from there.
		dest.move(textHandler.UNIT_CHARACTER, pos)
		self._setSelection(dest)

	def nextLine(self):
		dest = self._line.copy()
		moved = dest.move(textHandler.UNIT_LINE, 1)
		if not moved:
			return
		dest.collapse()
		self._setSelection(dest)

	def previousLine(self):
		dest = self._line.copy()
		dest.collapse()
		# Move to the last character of the previous line.
		moved = dest.move(textHandler.UNIT_CHARACTER, -1)
		if not moved:
			return
		dest.collapse()
		self._setSelection(dest)

class CursorManagerRegion(TextInfoRegion):

	def _isMultiline(self):
		return True

	def _getSelection(self):
		return self.obj.selection

	def _setSelection(self, info):
		self.obj.selection = info

class ReviewTextInfoRegion(TextInfoRegion):

	def _getSelection(self):
		return api.getReviewPosition()

	def _setSelection(self, info):
		api.setReviewPosition(info)

	def _isMultiline(self):
		return True

class BrailleBuffer(baseObject.AutoPropertyObject):

	def __init__(self, handler):
		self.handler = handler
		#: The regions in this buffer.
		#: @type: [L{Region}, ...]
		self.regions = []
		#: The position of the cursor in L{brailleCells}, C{None} if no region contains the cursor.
		#: @type: int
		self.cursorPos = None
		#: The translated braille representation of the entire buffer.
		#: @type: [int, ...]
		self.brailleCells = []
		#: The position in L{brailleCells} where the display window starts (inclusive).
		#: @type: int
		self.windowStartPos = 0

	def clear(self):
		"""Clear the entire buffer.
		This removes all regions and resets the window position to 0.
		"""
		self.regions = []
		self.cursorPos = None
		self.brailleCursorPos = None
		self.brailleCells = []
		self.windowStartPos = 0

	def _get_visibleRegions(self):
		if not self.regions:
			return
		if self.regions[-1].hidePreviousRegions:
			yield self.regions[-1]
			return
		for region in self.regions:
			yield region

	def _get_regionsWithPositions(self):
		start = 0
		for region in self.visibleRegions:
			end = start + len(region.brailleCells)
			yield region, start, end
			start = end

	def bufferPosToRegionPos(self, bufferPos):
		for region, start, end in self.regionsWithPositions:
			if end > bufferPos:
				return region, bufferPos - start
		raise LookupError("No such position")

	def regionPosToBufferPos(self, region, pos):
		for testRegion, start, end in self.regionsWithPositions:
			if region == testRegion:
				if pos < end:
					return start + pos
		raise LookupError("No such position")

	def bufferPosToWindowPos(self, bufferPos):
		if not (self.windowStartPos <= bufferPos < self.windowEndPos):
			raise LookupError("Buffer position not in window")
		return bufferPos - self.windowStartPos

	def _get_windowEndPos(self):
		try:
			lineEnd = self.brailleCells.index(-1, self.windowStartPos)
		except ValueError:
			lineEnd = len(self.brailleCells)
		return min(lineEnd, self.windowStartPos + self.handler.displaySize)

	def _set_windowEndPos(self, endPos):
		lineStart = endPos - 1
		# Find the end of the previous line.
		while lineStart >= 0:
			if self.brailleCells[lineStart] == -1:
				break
			lineStart -= 1
		lineStart += 1
		self.windowStartPos = max(endPos - self.handler.displaySize, lineStart)

	def scrollForward(self):
		oldStart = self.windowStartPos
		end = self.windowEndPos
		if end < len(self.brailleCells):
			self.windowStartPos = end
		if self.windowStartPos == oldStart:
			# The window could not be scrolled, so try moving to the next line.
			if self.regions:
				self.regions[-1].nextLine()
		else:
			# Scrolling succeeded.
			self.updateDisplay()

	def scrollBack(self):
		start = self.windowStartPos
		if start > 0:
			self.windowEndPos = start
		if self.windowStartPos == start:
			# The window could not be scrolled, so try moving to the previous line.
			if self.regions:
				self.regions[-1].previousLine()
		else:
			# Scrolling succeeded.
			self.updateDisplay()

	def scrollTo(self, region, pos):
		pos = self.regionPosToBufferPos(region, pos)
		if pos >= self.windowEndPos:
			self.windowEndPos = pos + 1
		elif pos < self.windowStartPos:
			self.windowStartPos = pos
		self.updateDisplay()

	def focus(self, region):
		"""Bring the specified region into focus.
		The region is placed at the start of the display.
		However, if the region has not set L{Region.focusToHardLeft} and there is extra space at the end of the display, the display is scrolled left so that as much as possible is displayed.
		@param region: The region to focus.
		@type region: L{Region}
		"""
		pos = self.regionPosToBufferPos(region, 0)
		self.windowStartPos = pos
		if region.focusToHardLeft:
			return
		end = self.windowEndPos
		if end - pos < self.handler.displaySize:
			# We can fit more on the display while still keeping pos visible.
			# Force windowStartPos to be recalculated based on windowEndPos.
			self.windowEndPos = end

	def update(self):
		self.brailleCells = []
		self.cursorPos = None
		start = 0
		for region in self.visibleRegions:
			cells = region.brailleCells
			self.brailleCells.extend(cells)
			if region.brailleCursorPos is not None:
				self.cursorPos = start + region.brailleCursorPos
			start += len(cells)

	def updateDisplay(self):
		if self is self.handler.buffer:
			self.handler.update()

	def _get_cursorWindowPos(self):
		if self.cursorPos is None:
			return None
		try:
			return self.bufferPosToWindowPos(self.cursorPos)
		except LookupError:
			return None

	def _get_windowBrailleCells(self):
		return self.brailleCells[self.windowStartPos:self.windowEndPos]

	def routeTo(self, windowPos):
		pos = self.windowStartPos + windowPos
		if pos >= self.windowEndPos:
			return
		region, pos = self.bufferPosToRegionPos(pos)
		region.routeTo(pos)

	def saveWindow(self):
		"""Save the current window so that it can be restored after the buffer is updated.
		The window start position is saved as a position relative to a region.
		This allows it to be restored even after other regions are added, removed or updated.
		It can be restored with L{restoreWindow}.
		@postcondition: The window is saved and can be restored with L{restoreWindow}.
		"""
		self._savedWindow = self.bufferPosToRegionPos(self.windowStartPos)

	def restoreWindow(self, ignoreErrors=False):
		"""Restore the window saved by L{saveWindow}.
		@param ignoreErrors: Whether to ignore errors.
		@type ignoreErrors: bool
		@precondition: L{saveWindow} has been called.
		@postcondition: If the saved position is valid, the window is restored.
		@raise LookupError: If C{ignoreErrors} is C{False} and the saved region position is invalid.
		"""
		try:
			self.windowStartPos = self.regionPosToBufferPos(*self._savedWindow)
		except LookupError:
			if not ignoreErrors:
				raise

def getContextRegions(obj):
	# Late import to avoid circular import.
	from virtualBuffers import VirtualBuffer
	if isinstance(obj,VirtualBuffer):
		obj=obj.rootNVDAObject
	ancestors=[]
	ancestor=obj.parent
	while ancestor:
		ancestors.append(ancestor)
		ancestor=ancestor.parent
	ancestors.reverse()
	for parent in ancestors[1:]:
		role=parent.role
		if role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_WINDOW,controlTypes.ROLE_SECTION,controlTypes.ROLE_TREEVIEWITEM,controlTypes.ROLE_LISTITEM,controlTypes.ROLE_PARAGRAPH,controlTypes.ROLE_PROGRESSBAR,controlTypes.ROLE_EDITABLETEXT,controlTypes.ROLE_MENUITEM):
			continue
		name=parent.name
		description=parent.description
		if role in (controlTypes.ROLE_PANEL,controlTypes.ROLE_PROPERTYPAGE,controlTypes.ROLE_TABLECELL,controlTypes.ROLE_TEXTFRAME,controlTypes.ROLE_SECTION) and not name and not description:
			continue
		states=parent.states
		if controlTypes.STATE_INVISIBLE in states or controlTypes.STATE_UNAVAILABLE in states:
			continue
		yield NVDAObjectRegion(parent, appendText=" ")

def getFocusRegions(obj, review=False):
	# Late import to avoid circular import.
	from virtualBuffers import VirtualBuffer
	from cursorManager import CursorManager
	if isinstance(obj, CursorManager):
		region2 = (ReviewTextInfoRegion if review else CursorManagerRegion)(obj)
	elif (obj.role in (controlTypes.ROLE_EDITABLETEXT, controlTypes.ROLE_TERMINAL) or controlTypes.STATE_EDITABLE in obj.states):
		region2 = (ReviewTextInfoRegion if review else TextInfoRegion)(obj)
	else:
		region2 = None
	if isinstance(obj, VirtualBuffer):
		obj = obj.rootNVDAObject
	yield (ReviewNVDAObjectRegion if review else NVDAObjectRegion)(obj, appendText=" " if region2 else "")
	if region2:
		yield region2

class BrailleHandler(baseObject.AutoPropertyObject):
	TETHER_FOCUS = "focus"
	TETHER_REVIEW = "review"

	def __init__(self):
		self.display = None
		self.displaySize = 0
		self.mainBuffer = BrailleBuffer(self)
		self.messageBuffer = BrailleBuffer(self)
		self._messageCallLater = None
		self.buffer = self.mainBuffer
		self._tether = self.TETHER_FOCUS
		#: Whether braille is enabled.
		#: @type: bool
		self.enabled = False

	def _get_tether(self):
		return self._tether

	def _set_tether(self, tether):
		if tether == self._tether:
			return
		self._tether = tether
		self.mainBuffer.clear()
		if tether == self.TETHER_REVIEW:
			self.handleReviewMove()
		else:
			self.handleGainFocus(api.getFocusObject())

	def setDisplayByName(self, name):
		if not name:
			self.display = None
			self.displaySize = 0
			return
		try:
			self.display = _getDisplayDriver(name)()
			self.displaySize = self.display.numCells
			self.enabled = bool(self.displaySize)
			config.conf["braille"]["display"] = name
			log.info("Loaded braille display driver %s" % name)
			self.configDisplay()
			return True
		except:
			log.error("Error initializing display driver", exc_info=True)
			self.setDisplayByName("noBraille")
			return False

	def configDisplay(self):
		"""Configure the braille display driver based on the user's configuration.
		@precondition: L{display} has been set.
		"""
		self.display.cursorBlinkRate = config.conf["braille"]["cursorBlinkRate"]
		self.display.cursorShape = 0xc0

	def update(self):
		self.display.display(self.buffer.windowBrailleCells)
		self.display.cursorPos = self.buffer.cursorWindowPos

	def scrollForward(self):
		self.buffer.scrollForward()
		if self.buffer is self.messageBuffer:
			self._resetMessageTimer()

	def scrollBack(self):
		self.buffer.scrollBack()
		if self.buffer is self.messageBuffer:
			self._resetMessageTimer()

	def routeTo(self, windowPos):
		self.buffer.routeTo(windowPos)
		if self.buffer is self.messageBuffer:
			self._dismissMessage()

	def message(self, text):
		"""Display a message to the user which times out after a configured interval.
		The timeout will be reset if the user scrolls the display.
		The message will be dismissed immediately if the user presses a cursor routing key.
		@postcondition: The message is displayed.
		"""
		if not self.enabled:
			return
		if self.buffer is self.messageBuffer:
			self.buffer.clear()
		else:
			self.buffer = self.messageBuffer
		region = TextRegion(text)
		region.update()
		self.buffer.regions.append(region)
		self.buffer.update()
		self.update()
		self._resetMessageTimer()

	def _resetMessageTimer(self):
		"""Reset the message timeout.
		@precondition: A message is currently being displayed.
		"""
		# Configured timeout is in seconds.
		timeout = config.conf["braille"]["messageTimeout"] * 1000
		if self._messageCallLater:
			self._messageCallLater.Restart(timeout)
		else:
			self._messageCallLater = wx.CallLater(timeout, self._dismissMessage)

	def _dismissMessage(self):
		"""Dismiss the current message.
		@precondition: A message is currently being displayed.
		@postcondition: The display returns to the main buffer.
		"""
		self.buffer.clear()
		self.buffer = self.mainBuffer
		self._messageCallLater.Stop()
		self._messageCallLater = None
		self.update()

	def handleGainFocus(self, obj):
		if not self.enabled:
			return
		if self.tether != self.TETHER_FOCUS:
			return
		self._doNewRegions(itertools.chain(getContextRegions(obj), getFocusRegions(obj)))

	def _doNewRegions(self, regions):
		self.mainBuffer.clear()
		for region in regions:
			self.mainBuffer.regions.append(region)
			region.update()
		self.mainBuffer.update()
		# Last region should receive focus.
		self.mainBuffer.focus(region)
		if region.brailleCursorPos is not None:
			self.mainBuffer.scrollTo(region, region.brailleCursorPos)
		if self.buffer is self.mainBuffer:
			self.update()

	def handleCaretMove(self, obj):
		if not self.enabled:
			return
		if self.tether != self.TETHER_FOCUS:
			return
		if not self.mainBuffer.regions:
			return
		region = self.mainBuffer.regions[-1]
		if region.obj is not obj:
			return
		self._doCursorMove(region)

	def _doCursorMove(self, region):
		self.mainBuffer.saveWindow()
		region.update()
		self.mainBuffer.update()
		self.mainBuffer.restoreWindow(ignoreErrors=True)
		if region.brailleCursorPos is not None:
			self.mainBuffer.scrollTo(region, region.brailleCursorPos)
		if self.buffer is self.mainBuffer:
			self.update()

	def handleUpdate(self, obj):
		if not self.enabled:
			return
		# Optimisation: It is very likely that it is the focus object that is being updated.
		# If the focus object is in the braille buffer, it will be the last region, so scan the regions backwards.
		for region in reversed(list(self.mainBuffer.visibleRegions)):
			if hasattr(region, "obj") and region.obj == obj:
				break
		else:
			# No region for this object.
			return
		self.mainBuffer.saveWindow()
		region.update()
		self.mainBuffer.update()
		self.mainBuffer.restoreWindow(ignoreErrors=True)
		if self.buffer is self.mainBuffer:
			self.update()

	def handleReviewMove(self):
		if not self.enabled:
			return
		if self.tether != self.TETHER_REVIEW:
			return
		reviewPos = api.getReviewPosition()
		region = self.mainBuffer.regions[-1] if self.mainBuffer.regions else None
		if region and region.obj == reviewPos.obj:
			self._doCursorMove(region)
		else:
			# We're reviewing a different object.
			self._doNewRegions(getFocusRegions(reviewPos.obj, review=True))

def initialize():
	global handler
	log.info("Using liblouis version %s" % louis.version())
	handler = BrailleHandler()
	handler.setDisplayByName(config.conf["braille"]["display"])

def terminate():
	global handler
	handler = None

class BrailleDisplayDriver(baseObject.AutoPropertyObject):
	"""Abstract base braille display driver.
	Each braille display driver should be a separate Python module in the root brailleDisplayDrivers directory containing a BrailleDisplayDriver class which inherits from this base class.
	
	At a minimum, drivers must set L{name} and L{description} and override the L{check} method.
	"""
	#: The name of the braille display; must be the original module file name.
	#: @type: str
	name = ""
	#: A description of the braille display.
	#: @type: str
	description = ""

	@classmethod
	def check(cls):
		"""Determine whether this braille display is available.
		The display will be excluded from the list of available displays if this method returns C{False}.
		For example, if this display is not present, C{False} should be returned.
		@return: C{True} if this display is available, C{False} if not.
		@rtype: bool
		"""
		return False

	def _get_numCells(self):
		"""Obtain the number of braille cells on this  display.
		@note: 0 indicates that braille should be disabled.
		@return: The number of cells.
		@rtype: int
		"""
		return 0

	def display(self, cells):
		"""Display the given braille cells.
		@param cells: The braille cells to display.
		@type cells: [int, ...]
		"""
		pass

	def _get_cursorPos(self):
		return None

	def _set_cursorPos(self, pos):
		pass

	def _get_cursorShape(self):
		return None

	def _set_cursorShape(self, shape):
		pass

	def _get_cursorBlinkRate(self):
		return 0

	def _set_cursorBlinkRate(self, rate):
		pass

class BrailleDisplayDriverWithCursor(BrailleDisplayDriver):
	"""Abstract base braille display driver which manages its own cursor.
	This should be used by braille display drivers where the display or underlying driver does not provide support for a cursor.
	Instead of overriding L{display}, subclasses should override L{_display}.
	"""

	def __init__(self):
		self._cursorPos = None
		self._cursorBlinkRate = 0
		self._cursorBlinkUp = True
		self._cursorShape = 0
		self._cells = []
		self._cursorBlinkTimer = None
		self._initCursor()

	def _initCursor(self):
		if self._cursorBlinkTimer:
			self._cursorBlinkTimer.Stop()
		self._cursorBlinkUp = True
		self._displayWithCursor()
		if self._cursorBlinkRate:
			self._cursorBlinkTimer = wx.PyTimer(self._blink)
			self._cursorBlinkTimer.Start(self._cursorBlinkRate)

	def _blink(self):
		self._cursorBlinkUp = not self._cursorBlinkUp
		self._displayWithCursor()

	def _get_cursorPos(self):
		return self._cursorPos

	def _set_cursorPos(self, pos):
		self._cursorPos = pos
		self._initCursor()

	def _get_cursorBlinkRate(self):
		return self._cursorBlinkRate

	def _set_cursorBlinkRate(self, rate):
		self._cursorBlinkRate = rate
		self._initCursor()

	def _get_cursorShape(self):
		return self._cursorShape

	def _set_cursorShape(self, shape):
		self._cursorShape = shape
		self._initCursor()

	def display(self, cells):
		# cells might not be the full length of the display.
		# Therefore, pad it with spaces to fill the display so that the cursor can lie beyond it.
		self._cells = cells + [0] * (self.numCells - len(cells))
		self._displayWithCursor()

	def _displayWithCursor(self):
		if not self._cells:
			return
		cells = list(self._cells)
		if self._cursorPos is not None and self._cursorBlinkUp:
			cells[self._cursorPos] |= self._cursorShape
		self._display(cells)

	def _display(self, cells):
		"""Actually display the given cells to the display.
		L{display} calls methods to handle the cursor representation as appropriate.
		However, this method (L{_display}) is called to actually display the final cells.
		"""
		pass
