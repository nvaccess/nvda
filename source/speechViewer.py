# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2021 NV Access Limited, Thomas Stivers, Accessolutions, Julien Cochuyt
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import wx
import gui
import config
from logHandler import log
from speech import SpeechSequence
import gui.contextHelp


# Inherit from wx.Frame because these windows show in the alt+tab menu (where miniFrame does not)
# We have to manually add a wx.Panel to get correct tab ordering behaviour.
# wx.Dialog causes a crash on destruction when multiple were created at the same time (brailleViewer
# may start at the same time)
class SpeechViewerFrame(
		gui.contextHelp.ContextHelpMixin,
		wx.Frame  # wxPython does not seem to call base class initializer, put last in MRO
):
	helpId = "SpeechViewer"

	def _getDialogSizeAndPosition(self):
		dialogSize = wx.Size(500, 500)
		dialogPos = wx.DefaultPosition
		if not config.conf["speechViewer"]["autoPositionWindow"] and self.doDisplaysMatchConfig():
			log.debug("Setting speechViewer window position")
			speechViewSection = config.conf["speechViewer"]
			dialogSize = wx.Size(speechViewSection["width"], speechViewSection["height"])
			dialogPos = wx.Point(x=speechViewSection["x"], y=speechViewSection["y"])
		return dialogSize, dialogPos

	def __init__(self, onDestroyCallBack):
		dialogSize, dialogPos = self._getDialogSizeAndPosition()
		super().__init__(
			gui.mainFrame,
			title=_("NVDA Speech Viewer"),
			size=dialogSize,
			pos=dialogPos,
			style=wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.STAY_ON_TOP
		)
		self._isDestroyed = False
		self.onDestroyCallBack = onDestroyCallBack
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)
		self.Bind(wx.EVT_ACTIVATE, self._onDialogActivated, source=self)

		self.frameContentsSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(self.frameContentsSizer)
		self.panel = wx.Panel(self)
		self.frameContentsSizer.Add(self.panel, proportion=1, flag=wx.EXPAND)

		self.panelContentsSizer = wx.BoxSizer(wx.VERTICAL)
		self.panel.SetSizer(self.panelContentsSizer)

		self._createControls(sizer=self.panelContentsSizer, parent=self.panel)

		# Don't let speech viewer to steal keyboard focus when opened
		self.ShowWithoutActivating()

	def _createControls(self, sizer, parent):
		self.textCtrl = wx.TextCtrl(
			parent,
			style=wx.TE_RICH2 | wx.TE_READONLY | wx.TE_MULTILINE
		)
		sizer.Add(
			self.textCtrl,
			proportion=1,
			flag=wx.EXPAND
		)

		self.shouldShowOnStartupCheckBox = wx.CheckBox(
			parent,
			# Translators: The label for a setting in the speech viewer that controls
			# whether the speech viewer is shown at startup or not.
			label=_("&Show Speech Viewer on Startup")
		)
		sizer.Add(
			self.shouldShowOnStartupCheckBox,
			border=5,
			flag=wx.EXPAND | wx.ALL
		)
		self.shouldShowOnStartupCheckBox.SetValue(config.conf["speechViewer"]["showSpeechViewerAtStartup"])
		self.shouldShowOnStartupCheckBox.Bind(
			wx.EVT_CHECKBOX,
			self.onShouldShowOnStartupChanged
		)

	def _onDialogActivated(self, evt):
		# Check for destruction, if the speechviewer window has focus when we exit NVDA it regains focus briefly
		# when the quit NVDA dialog disappears. Then shouldShowOnStartupCheckBox is a deleted window when we
		# try to setFocus
		if not self._isDestroyed:
			# focus is normally set to the first child, however,
			# the checkbox gives more context, and makes it obvious how to stop showing the dialog.
			self.shouldShowOnStartupCheckBox.SetFocus()

	def onClose(self, evt):
		assert isActive, "Cannot close Speech Viewer as it is already inactive"
		deactivate()

	def onShouldShowOnStartupChanged(self, evt):
		config.conf["speechViewer"]["showSpeechViewerAtStartup"] = self.shouldShowOnStartupCheckBox.IsChecked()

	_isDestroyed: bool

	def onDestroy(self, evt):
		self._isDestroyed = True
		log.debug("SpeechViewer destroyed")
		self.onDestroyCallBack()
		evt.Skip()

	def doDisplaysMatchConfig(self):
		configSizes = config.conf["speechViewer"]["displays"]
		attachedSizes = self.getAttachedDisplaySizesAsStringArray()
		return len(configSizes) == len(attachedSizes) and all( configSizes[i] == attachedSizes[i] for i in range(len(configSizes)))

	def getAttachedDisplaySizesAsStringArray(self):
		displays = ( wx.Display(i).GetGeometry().GetSize() for i in range(wx.Display.GetCount()) )
		return [repr( (i.width, i.height) ) for i in displays]

	def savePositionInformation(self):
		position = self.GetPosition()
		config.conf["speechViewer"]["x"] = position.x
		config.conf["speechViewer"]["y"] = position.y
		size = self.GetSize()
		config.conf["speechViewer"]["width"] = size.width
		config.conf["speechViewer"]["height"] = size.height
		config.conf["speechViewer"]["displays"] = self.getAttachedDisplaySizesAsStringArray()
		config.conf["speechViewer"]["autoPositionWindow"] = False

_guiFrame=None
isActive=False

def activate():
	"""
		Function to call to trigger the speech viewer window to open.
	"""
	_setActive(True, SpeechViewerFrame(_cleanup))

def _setActive(isNowActive, speechViewerFrame=None):
	global _guiFrame, isActive
	isActive = isNowActive
	_guiFrame = speechViewerFrame
	if gui and gui.mainFrame:
		gui.mainFrame.onSpeechViewerEnabled(isNowActive)


#: How to separate items in a speech sequence
SPEECH_ITEM_SEPARATOR = "  "
#: How to separate speech sequences
SPEECH_SEQUENCE_SEPARATOR = "\n"


def appendSpeechSequence(sequence: SpeechSequence) -> None:
	""" Appends a speech sequence to the speech viewer.
	@param sequence: To append, items are separated with . Concluding with a newline.
	"""
	if not isActive:
		return
	# If the speech viewer text control has the focus, we want to disable updates
	# Otherwise it would be impossible to select text, or even just read it (as a blind person).
	if _guiFrame.FindFocus() == _guiFrame.textCtrl:
		return

	# to make the speech easier to read, we must separate the items.
	text = SPEECH_ITEM_SEPARATOR.join(
		speech for speech in sequence if isinstance(speech, str)
	)
	_guiFrame.textCtrl.AppendText(text + SPEECH_SEQUENCE_SEPARATOR)

def _cleanup():
	global isActive
	if not isActive:
		return
	_setActive(False)

def deactivate():
	global _guiFrame, isActive
	if not isActive:
		return
	# #7077: If the window is destroyed, text control will be gone, so save speech viewer position before destroying the window.
	_guiFrame.savePositionInformation()
	_guiFrame.Destroy()
