#braille.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import louis
import baseObject
import config
from logHandler import log
import controlTypes

__path__ = ["brailleDisplayDrivers"]

TABLES_DIR = r"louis\tables"

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

	def update(self):
		mode = louis.MODE.dotsIO
		if config.conf["braille"]["expandAtCursor"] and self.cursorPos is not None:
			mode |= louis.MODE.compbrlAtCursor
		braille, self.brailleToRawPos, self.rawToBraillePos, brailleCursorPos = louis.translate([os.path.join(TABLES_DIR, handler.translationTable)], unicode(self.rawText), mode=mode, cursorPos=self.cursorPos or 0)
		# liblouis gives us back a character string of cells, so convert it to a list of ints.
		# For some reason, the highest bit is set, so only grab the lower 8 bits.
		self.brailleCells = [ord(cell) & 255 for cell in braille]
		if self.cursorPos is not None:
			self.brailleCursorPos = brailleCursorPos

	def routeTo(self, braillePos):
		pass

class TextRegion(Region):

	def __init__(self, text):
		super(TextRegion, self).__init__()
		self.rawText = text

class NVDAObjectRegion(Region):

	def __init__(self, obj):
		super(NVDAObjectRegion, self).__init__()
		self.obj = obj

	def update(self):
		textList = [self.obj.name]
		#TODO: Don't use speech stuff.
		textList.append(controlTypes.speechRoleLabels[self.obj.role])
		self.rawText = " ".join(textList)
		super(NVDAObjectRegion, self).update()

	def routeTo(self, braillePos):
		self.obj.doDefaultAction()

class BrailleBuffer(baseObject.AutoPropertyObject):

	def __init__(self, handler):
		self.handler = handler
		#: The regions in this buffer.
		#: @type: [L{Region}, ...]
		self.regions = []
		#: The region containing the cursor, C{None} if no region contains the cursor.
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

	def _get_regionsWithPositions(self):
		start = 0
		for region in self.regions:
			end = start + len(region.brailleCells)
			yield region, start, end
			start = end

	def bufferPosToRegionPos(self, bufferPos):
		for region, start, end in self.regionsWithPositions:
			if end >= bufferPos:
				return region, bufferPos - start
		raise LookupError("No such position")

	def regionPosToBufferPos(self, region, pos):
		for testRegion, start, end in self.regionsWithPositions:
			if region == testRegion:
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
		end = self.windowEndPos
		if end < len(self.brailleCells):
			self.windowStartPos = end
		self.updateDisplay()

	def scrollBack(self):
		start = self.windowStartPos
		if start > 0:
			self.windowEndPos = start
		self.updateDisplay()

	def scrollTo(self, region, pos):
		pos = self.regionPosToBufferPos(region, pos)
		if pos > self.windowEndPos:
			self.windowEndPos = pos
		elif pos < self.windowStartPos:
			self.windowStartPos = pos
		self.updateDisplay()

	def update(self, updateDisplay=True):
		self.brailleCells = []
		self.cursorPos = None
		start = 0
		for region in self.regions:
			cells = region.brailleCells
			self.brailleCells.extend(cells)
			if region.brailleCursorPos is not None:
				self.cursorPos = start + region.brailleCursorPos
			start += len(cells)
		if updateDisplay:
			self.updateDisplay()

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

class BrailleHandler(baseObject.AutoPropertyObject):

	def __init__(self):
		self.translationTable = config.conf["braille"]["translationTable"]
		self.display = None
		self.displaySize = 0
		self.mainBuffer = BrailleBuffer(self)
		self.buffer = self.mainBuffer

	def setDisplayByName(self, name):
		if not name:
			self.display = None
			self.displaySize = 0
			return
		try:
			self.display = _getDisplayDriver(name)()
			self.displaySize = self.display.numCells
		except:
			log.error("Error initializing display driver", exc_info=True)
			return

	def update(self):
		self.display.display(self.buffer.windowBrailleCells)
		self.display.cursorPos = self.buffer.cursorWindowPos

	def NVDAObjectGainFocus(self, obj):
		self.buffer.clear()
		region = NVDAObjectRegion(obj)
		self.buffer.regions.append(region)
		region.update()
		self.buffer.update()

def initialize():
	global handler
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
		@return: The number of cells.
		@rtype: int
		"""
		# Zero wouldn't make sense even for a null device ;-)
		return 80

	def display(self, cells):
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
