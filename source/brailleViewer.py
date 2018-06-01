#brailleViewer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014-2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import gui
import braille
from braille import BrailleDisplayDriver
import config
from logHandler import log
import extensionPoints

# global braille viewer driver:
_display = None

# this extension points action is triggered every time the the brailleDisplayTool
# is created or destroyed.
# Args given to Notify:
# created - A boolean argument is given, True for created, False for destructed.
postBrailleViewerToolToggledAction = extensionPoints.Action()

def isBrailleDisplayCreated():
	return bool(_display)

def getBrailleViewerTool():
	return _display

def toggleBrailleViewerTool():
	if isBrailleDisplayCreated():
		destroyBrailleViewerTool()
	else:
		createBrailleViewerTool()

def destroyBrailleViewerTool():
	global _display
	if not _display:
		return
	d = _display
	_display = None
	try:
		d.terminate()
	except:
		log.error("Error terminating braille viewer tool", exc_info=True)
	postBrailleViewerToolToggledAction.notify(created=False)

DEFAULT_NUM_CELLS = 40
def createBrailleViewerTool():
	if not gui.mainFrame:
		raise RuntimeError("Can not initialise the BrailleViewerGui: gui.mainFrame not yet initialised")
	if not braille.handler:
		raise RuntimeError("Can not initialise the BrailleViewerGui: braille.handler not yet initialised")

	cells = DEFAULT_NUM_CELLS if not braille.handler.displaySize else braille.handler.displaySize
	global _display
	if _display:
		d = _display
		destroyBrailleViewerTool()
		_display = d
		_display.__init__(cells)
	else:
		_display = BrailleViewerDriver(cells)
	postBrailleViewerToolToggledAction.notify(created=True)

BRAILLE_UNICODE_PATTERNS_START = 0x2800
SPACE_CHARACTER = u" "

# Inherit from wx.Frame because these windows show in the alt+tab menu (where miniFrame does not)
# wx.Dialog causes a crash on destruction when multiple were created at the same time (speechViewer
# may start at the same time)
class BrailleViewerFrame(wx.Frame):

	#Translators: The title of the NVDA Braille Viewer tool window.
	title = _("NVDA Braille Viewer")

	def __init__(self, numCells, onDestroyed):
		dialogPos=None
		if not config.conf["brailleViewer"]["autoPositionWindow"] and self.doDisplaysMatchConfig():
			log.debug("Setting brailleViewer window position")
			brailleViewSection = config.conf["brailleViewer"]
			dialogPos = wx.Point(x=brailleViewSection["x"], y=brailleViewSection["y"])
		super(BrailleViewerFrame, self).__init__(
			parent=gui.mainFrame,
			id=wx.ID_ANY,
			title=self.title,
			pos=dialogPos,
			style=wx.CAPTION | wx.STAY_ON_TOP
		)
		self._notifyOfDestroyed = onDestroyed
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)
		self.lastBraille = SPACE_CHARACTER * numCells
		self.lastText = SPACE_CHARACTER
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		item = self.output = wx.StaticText(self, label=self.lastBraille)
		item.Font = self.setFont(item.GetFont(), forBraille=True)
		mainSizer.Add(item, flag=wx.EXPAND)

		item = self.rawoutput = wx.StaticText(self, label=SPACE_CHARACTER)
		item.Font = self.setFont(item.Font)
		mainSizer.Add(item, flag=wx.EXPAND)

		# Translators: The label for a setting in the braille viewer that controls whether the braille viewer is shown at
		# startup or not.
		showOnStartupCheckboxLabel = _("&Show Braille Viewer on Startup")
		self.shouldShowOnStartupCheckBox = wx.CheckBox(
			parent=self,
			label=showOnStartupCheckboxLabel)
		self.shouldShowOnStartupCheckBox.SetValue(config.conf["brailleViewer"]["showBrailleViewerAtStartup"])
		self.shouldShowOnStartupCheckBox.Bind(wx.EVT_CHECKBOX, self.onShouldShowOnStartupChanged)
		mainSizer.Add(self.shouldShowOnStartupCheckBox, border=5, flag=wx.ALL)

		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.Show()

	def onShouldShowOnStartupChanged(self, evt):
		config.conf["brailleViewer"]["showBrailleViewerAtStartup"] = self.shouldShowOnStartupCheckBox.IsChecked()

	def doDisplaysMatchConfig(self):
		configSizes = config.conf["brailleViewer"]["displays"]
		attachedSizes = self.getAttachedDisplaySizesAsStringArray()
		return len(configSizes) == len(attachedSizes) and all( configSizes[i] == attachedSizes[i] for i in xrange(len(configSizes)))

	def updateValues(self, braille, text):
		brailleEqual = self.lastBraille == braille
		textEqual = self.lastText == text
		if brailleEqual and textEqual:
			return
		self.Freeze()
		if not brailleEqual:
			self.output.Label = self.lastBraille = braille
		if not textEqual:
			self.rawoutput.Label = self.lastText = text
		self.Thaw()
		self.Refresh()
		self.Update()

	def setFont(self, font, forBraille=False):
		# Braille characters are much smaller than the raw text characters, override the size
		# I assume this is because the "Courier New" font does not support this unicode range
		# so the system falls back to another font.
		font.PointSize = 20 if not forBraille else 22
		font.Family = wx.FONTFAMILY_TELETYPE
		font.FaceName = "Courier New"
		return font

	def getAttachedDisplaySizesAsStringArray(self):
		displays = ( wx.Display(i).GetGeometry().GetSize() for i in xrange(wx.Display.GetCount()) )
		return [repr( (i.width, i.height) ) for i in displays]

	def savePositionInformation(self):
		position = self.GetPosition()
		config.conf["brailleViewer"]["x"] = position.x
		config.conf["brailleViewer"]["y"] = position.y
		config.conf["brailleViewer"]["displays"] = self.getAttachedDisplaySizesAsStringArray()
		config.conf["brailleViewer"]["autoPositionWindow"] = False

	def onClose(self, evt):
		log.debug("braille viewer gui onClose")
		if not evt.CanVeto():
			self.Destroy()
			return
		evt.Veto()

	def onDestroy(self, evt):
		log.debug("braille viewer gui destroyed")
		self.savePositionInformation()
		self._notifyOfDestroyed()
		evt.Skip()


class BrailleViewerDriver(BrailleDisplayDriver):
	name = "brailleViewer"
	#Translators: Description of the braille viewer tool
	description = _("Braille viewer")
	numCells = DEFAULT_NUM_CELLS  # Overriden to match an active braille display
	_brailleGui = None  # A BrailleViewer instance

	@classmethod
	def check(cls):
		return True

	def __init__(self, numCells):
		super(BrailleViewerDriver, self).__init__()
		self.numCells = numCells
		self.rawText = u""
		self._hasTerminated = False
		self._setupBrailleGui()

	def _setupBrailleGui(self):
		# check we have not initialialised yet
		if self._brailleGui:
			return True

		if self._hasTerminated:
			return False

		self._brailleGui = BrailleViewerFrame(self.numCells, self.onBrailleGuiDestroyed)
		return self._brailleGui

	def display(self, cells):
		if not self._setupBrailleGui():
			return
		brailleUnicodeChars = (unichr(BRAILLE_UNICODE_PATTERNS_START + cell) for cell in cells)
		# replace braille "space" with regular space because the width of the braille space
		# does not match the other braille characters, the result is better, but not perfect.
		brailleSpace = unichr(BRAILLE_UNICODE_PATTERNS_START)
		spaceReplaced = (cell.replace(brailleSpace, SPACE_CHARACTER) for cell in brailleUnicodeChars)
		self._brailleGui.updateValues(u"".join(spaceReplaced), self.rawText)

	def terminate(self):
		super(BrailleViewerDriver, self).terminate()
		if self._brailleGui and not self._hasTerminated:
			try:
				self._brailleGui.Destroy()
			except wx.PyDeadObjectError:
				# NVDA's GUI has already terminated.
				pass
		self.onBrailleGuiDestroyed()

	def onBrailleGuiDestroyed(self):
		self._brailleGui = None
		self._hasTerminated = True
		destroyBrailleViewerTool()
