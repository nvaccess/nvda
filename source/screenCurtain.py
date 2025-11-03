# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Screen curtain implementation based on the windows magnification API."""

import os
from typing import TypedDict, cast

# from vision import providerBase
# from autoSettingsUtils.driverSetting import BooleanDriverSetting
# from autoSettingsUtils.autoSettings import SupportedSettingType
# import wx
# from gui.nvdaControls import MessageDialog
# from gui.settingsDialogs import (
# 	AutoSettingsMixin,
# 	SettingsPanel,
# 	VisionProviderStateControl,
# )
import config
from logHandler import log

# from typing import Optional, Type
import nvwave
import globalVars
from NVDAHelper.localLib import isScreenFullyBlack
from winBindings import magnification


# homogeneous matrix for a 4-space transformation (red, green, blue, opacity).
# https://docs.microsoft.com/en-gb/windows/win32/gdiplus/-gdiplus-using-a-color-matrix-to-transform-a-single-color-use
TRANSFORM_BLACK = magnification.MAGCOLOREFFECT()  # empty transformation
TRANSFORM_BLACK.transform[4][4] = 1.0  # retain as an affine transformation
TRANSFORM_BLACK.transform[3][3] = 1.0  # retain opacity, while scaling other colours to zero (#12491)

# # Translators: Name for a vision enhancement provider that disables output to the screen,
# # making it black.
# screenCurtainTranslatedName = _("Screen Curtain")

# # Translators: Description for a Screen Curtain setting that shows a warning when loading
# # the screen curtain.
# warnOnLoadCheckBoxText = _("Always &show a warning when loading Screen Curtain")

# # Translators: Description for a screen curtain setting to play sounds when enabling/disabling the curtain
# playToggleSoundsCheckBoxText = _("&Play sound when toggling Screen Curtain")


# warnOnLoadText = _(
# 	# Translators: A warning shown when activating the screen curtain.
# 	# the translation of "Screen Curtain" should match the "translated name"
# 	"Enabling Screen Curtain will make the screen of your computer completely black. "
# 	"Ensure you will be able to navigate without any use of your screen before continuing. "
# 	"\n\n"
# 	"Do you wish to continue?",
# )


# class WarnOnLoadDialog(MessageDialog):
# 	showWarningOnLoadCheckBox: wx.CheckBox
# 	noButton: wx.Button

# 	def __init__(
# 		self,
# 		screenCurtainSettingsStorage: ScreenCurtainSettings,
# 		parent,
# 		title=_("Warning"),
# 		message=warnOnLoadText,
# 		dialogType=MessageDialog.DIALOG_TYPE_WARNING,
# 	):
# 		self._settingsStorage = screenCurtainSettingsStorage
# 		super().__init__(parent, title, message, dialogType)
# 		self.noButton.SetFocus()

# 	def _addContents(self, contentsSizer):
# 		self.showWarningOnLoadCheckBox: wx.CheckBox = wx.CheckBox(
# 			self,
# 			label=warnOnLoadCheckBoxText,
# 		)
# 		contentsSizer.addItem(self.showWarningOnLoadCheckBox)
# 		self.showWarningOnLoadCheckBox.SetValue(
# 			self._settingsStorage.warnOnLoad,
# 		)

# 	def _addButtons(self, buttonHelper):
# 		yesButton = buttonHelper.addButton(
# 			self,
# 			id=wx.ID_YES,
# 			# Translators: A button in the screen curtain warning dialog which allows the user to
# 			# agree to enabling the curtain.
# 			label=_("&Yes"),
# 		)
# 		yesButton.Bind(wx.EVT_BUTTON, lambda evt: self._exitDialog(wx.YES))

# 		noButton: wx.Button = buttonHelper.addButton(
# 			self,
# 			id=wx.ID_NO,
# 			# Translators: A button in the screen curtain warning dialog which allows the user to
# 			# disagree to enabling the curtain.
# 			label=_("&No"),
# 		)
# 		noButton.SetDefault()
# 		noButton.Bind(wx.EVT_BUTTON, lambda evt: self._exitDialog(wx.NO))
# 		self.noButton = noButton  # so we can manually set the focus.

# 	def _exitDialog(self, result: int):
# 		"""
# 		@param result: either wx.YES or wx.No
# 		"""
# 		if result == wx.YES:
# 			settingsStorage = self._settingsStorage
# 			settingsStorage.warnOnLoad = self.showWarningOnLoadCheckBox.IsChecked()
# 			settingsStorage._saveSpecificSettings(settingsStorage, settingsStorage.supportedSettings)
# 		self.EndModal(result)

# 	def _onActivateEvent(self, evt: wx.ActivateEvent):
# 		# focus is normally set to the first child, however, we want people to easily be able to cancel this
# 		# dialog
# 		super()._onActivateEvent(evt)
# 		self.noButton.SetFocus()

# 	def _onShowEvent(self, evt: wx.ShowEvent):
# 		"""When no other dialogs have been opened first, focus lands in the wrong place (on the checkbox),
# 		so we correct it after the dialog is opened.
# 		"""
# 		if evt.IsShown():
# 			self.noButton.SetFocus()
# 		super()._onShowEvent(evt)


# class ScreenCurtainGuiPanel(
# 	AutoSettingsMixin,
# 	SettingsPanel,
# ):
# 	_enabledCheckbox: wx.CheckBox
# 	_enableCheckSizer: wx.BoxSizer

# 	helpId = "VisionSettingsScreenCurtain"

# 	def __init__(
# 		self,
# 		parent,
# 		providerControl: VisionProviderStateControl,
# 	):
# 		self._providerControl = providerControl
# 		super().__init__(parent)

# 	def _buildGui(self):
# 		self.mainSizer = wx.BoxSizer(wx.VERTICAL)

# 		self._enabledCheckbox = wx.CheckBox(
# 			self,
# 			#  Translators: option to enable screen curtain in the vision settings panel
# 			label=_("Make screen black (immediate effect)"),
# 		)
# 		isProviderActive = bool(self._providerControl.getProviderInstance())
# 		self._enabledCheckbox.SetValue(isProviderActive)

# 		self.mainSizer.Add(self._enabledCheckbox)
# 		self.mainSizer.AddSpacer(size=self.scaleSize(10))
# 		# this options separator is done with text rather than a group box because a groupbox is too verbose,
# 		# but visually some separation is helpful, since the rest of the options are really sub-settings.
# 		self.optionsText = wx.StaticText(
# 			self,
# 			# Translators: The label for a group box containing the NVDA highlighter options.
# 			label=_("Options:"),
# 		)
# 		self.mainSizer.Add(self.optionsText)
# 		self.lastControl = self.optionsText
# 		self.settingsSizer = wx.BoxSizer(wx.VERTICAL)
# 		self.makeSettings(self.settingsSizer)
# 		self.mainSizer.Add(self.settingsSizer, border=self.scaleSize(15), flag=wx.LEFT | wx.EXPAND)
# 		self.mainSizer.Fit(self)
# 		self.SetSizer(self.mainSizer)

# 	def getSettings(self) -> ScreenCurtainSettings:
# 		return ScreenCurtainProvider.getSettings()

# 	def makeSettings(self, sizer: wx.BoxSizer):
# 		self.updateDriverSettings()
# 		self.Bind(wx.EVT_CHECKBOX, self._onCheckEvent)

# 	def onPanelActivated(self):
# 		self.lastControl = self._enabledCheckbox

# 	def _onCheckEvent(self, evt: wx.CommandEvent):
# 		if evt.GetEventObject() is self._enabledCheckbox:
# 			self._ensureEnableState(evt.IsChecked())

# 	def _ocrActive(self) -> bool:
# 		"""Outputs a message when trying to activate screen curtain when OCR is active.
# 		@returns: C{True} when OCR is active, C{False} otherwise.
# 		"""
# 		import api
# 		from contentRecog.recogUi import RefreshableRecogResultNVDAObject
# 		import speech
# 		import ui

# 		focusObj = api.getFocusObject()
# 		if isinstance(focusObj, RefreshableRecogResultNVDAObject) and focusObj.recognizer.allowAutoRefresh:
# 			# Translators: Warning message when trying to enable the screen curtain when OCR is active.
# 			warningMessage = _("Could not enable screen curtain when performing content recognition")
# 			ui.message(warningMessage, speechPriority=speech.priorities.Spri.NOW)
# 			return True
# 		return False

# 	def _ensureEnableState(self, shouldBeEnabled: bool):
# 		currentlyEnabled = bool(self._providerControl.getProviderInstance())
# 		if shouldBeEnabled and not currentlyEnabled:
# 			confirmed = self.confirmInitWithUser()
# 			if not confirmed or self._ocrActive() or not self._providerControl.startProvider():
# 				self._enabledCheckbox.SetValue(False)
# 		elif not shouldBeEnabled and currentlyEnabled:
# 			self._providerControl.terminateProvider()

# 	def confirmInitWithUser(self) -> bool:
# 		settingsStorage = self._getSettingsStorage()
# 		if not settingsStorage.warnOnLoad:
# 			return True
# 		parent = self
# 		with WarnOnLoadDialog(
# 			screenCurtainSettingsStorage=settingsStorage,
# 			parent=parent,
# 		) as dlg:
# 			res = dlg.ShowModal()
# 			# WarnOnLoadDialog can change settings, reload them
# 			self.updateDriverSettings()
# 			return res == wx.YES


class _ScreenCurtainSettings(TypedDict):
	enabled: bool
	warnOnLoad: bool
	playToggleSounds: bool


class _ScreenCurtain:
	def __init__(self):
		super().__init__()
		self._settings: _ScreenCurtainSettings = cast(_ScreenCurtainSettings, config.conf["screenCurtain"])
		self._enabled: bool = False
		if self.settings["enabled"]:
			self.enable()

	@property
	def settings(self) -> _ScreenCurtainSettings:
		return self._settings

	@property
	def enabled(self) -> bool:
		return self._enabled

	def enable(self) -> None:
		if self._enabled:
			log.debug("ScreenCurtain is already enabled.")
			return
		else:
			log.debug("Enabling ScreenCurtain")
			magnification.MagInitialize()
			try:
				magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)
				magnification.MagShowSystemCursor(False)
				if not isScreenFullyBlack():
					raise RuntimeError("Screen is not black.")
			except Exception as e:
				magnification.MagUninitialize()
				raise e
			else:
				self._enabled = True
			if self.settings["playToggleSounds"]:
				try:
					nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "screenCurtainOn.wav"))
				except Exception:
					log.exception()

	def disable(self):
		if not self._enabled:
			log.debug("ScreenCurtain is already disabled")
			return
		else:
			log.debug("Disabling ScreenCurtain")
			magnification.MagShowSystemCursor(True)
			magnification.MagUninitialize()
			self._enabled = False
			if self.settings["playToggleSounds"]:
				try:
					nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "screenCurtainOff.wav"))
				except Exception:
					log.exception()

	def __del__(self):
		self.disable()
		if hasattr(super(), "__del__"):
			super().__del__(self)


screenCurtain: _ScreenCurtain | None = None


def initialize():
	global screenCurtain
	if screenCurtain is None:
		screenCurtain = _ScreenCurtain()


def terminate():
	global screenCurtain
	if screenCurtain is not None:
		screenCurtain.disable()
		screenCurtain = None
