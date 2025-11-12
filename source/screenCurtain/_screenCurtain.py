# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter

import os
from typing import TypedDict, cast

import config
import globalVars
import nvwave
import wx
from gui.nvdaControls import MessageDialog
from logHandler import log
from winBindings import magnification

from NVDAHelper.localLib import isScreenFullyBlack

# homogeneous matrix for a 4-space transformation (red, green, blue, opacity).
# https://docs.microsoft.com/en-gb/windows/win32/gdiplus/-gdiplus-using-a-color-matrix-to-transform-a-single-color-use
TRANSFORM_BLACK = magnification.MAGCOLOREFFECT()  # empty transformation
TRANSFORM_BLACK.transform[4][4] = 1.0  # retain as an affine transformation
TRANSFORM_BLACK.transform[3][3] = 1.0  # retain opacity, while scaling other colours to zero (#12491)

# Translators: Description for a Screen Curtain setting that shows a warning when enabling
# the screen curtain.
warnOnLoadCheckBoxText = _("Always &show a warning when enabling Screen Curtain")


class ScreenCurtainSettings(TypedDict):
	"""Type information for the "screenCurtain" section of the config."""

	enabled: bool
	warnOnLoad: bool
	playToggleSounds: bool


class WarnOnLoadDialog(MessageDialog):
	"""Warning shown to users when enabling Screen Curtain."""

	showWarningOnLoadCheckBox: wx.CheckBox
	noButton: wx.Button

	def __init__(
		self,
		screenCurtainSettingsStorage: ScreenCurtainSettings,
		parent: wx.Window,
		title: str = _("Warning"),
		message: str = _(
			# Translators: A warning shown when activating the screen curtain.
			# the translation of "Screen Curtain" should match the "translated name"
			"Enabling Screen Curtain will make the screen of your computer completely black. "
			"Ensure you will be able to navigate without any use of your screen before continuing. "
			"\n\n"
			"Do you wish to continue?",
		),
		dialogType: int = MessageDialog.DIALOG_TYPE_WARNING,
	):
		"""Initializer.

		:param screenCurtainSettingsStorage: Dictionary containing Screen Curtain settings.
		:param parent: Parent window of this dialog.
		:param title: Title of the dialog, defaults to "Warning"
		:param message: Message to show, has default
		:param dialogType: Type of the dialog, defaults to MessageDialog.DIALOG_TYPE_WARNING
		"""
		self._settingsStorage = screenCurtainSettingsStorage
		super().__init__(parent, title, message, dialogType)
		self.noButton.SetFocus()

	def _addContents(self, contentsSizer):
		self.showWarningOnLoadCheckBox: wx.CheckBox = wx.CheckBox(
			self,
			label=warnOnLoadCheckBoxText,
		)
		contentsSizer.addItem(self.showWarningOnLoadCheckBox)
		self.showWarningOnLoadCheckBox.SetValue(
			self._settingsStorage["warnOnLoad"],
		)

	def _addButtons(self, buttonHelper):
		yesButton = buttonHelper.addButton(
			self,
			id=wx.ID_YES,
			# Translators: A button in the screen curtain warning dialog which allows the user to
			# agree to enabling the curtain.
			label=_("&Yes"),
		)
		yesButton.Bind(wx.EVT_BUTTON, lambda evt: self._exitDialog(wx.YES))

		noButton: wx.Button = buttonHelper.addButton(
			self,
			id=wx.ID_NO,
			# Translators: A button in the screen curtain warning dialog which allows the user to
			# disagree to enabling the curtain.
			label=_("&No"),
		)
		noButton.SetDefault()
		noButton.Bind(wx.EVT_BUTTON, lambda evt: self._exitDialog(wx.NO))
		self.noButton = noButton  # so we can manually set the focus.

	def _exitDialog(self, result: int):
		"""Handles persisting the state of the checkbox if the user answers in the affirmative.

		:param result: either wx.YES or wx.No
		"""
		if result == wx.YES:
			self._settingsStorage["warnOnLoad"] = self.showWarningOnLoadCheckBox.IsChecked()
		self.EndModal(result)

	def _onActivateEvent(self, evt: wx.ActivateEvent):
		"""Activate event handler."""
		# focus is normally set to the first child, however, we want people to easily be able to cancel this
		# dialog
		super()._onActivateEvent(evt)
		self.noButton.SetFocus()

	def _onShowEvent(self, evt: wx.ShowEvent):
		"""Show event handler.

		When no other dialogs have been opened first, focus lands in the wrong place (on the checkbox),
		so we correct it after the dialog is opened.
		"""
		if evt.IsShown():
			self.noButton.SetFocus()
		super()._onShowEvent(evt)


class ScreenCurtain:
	"""
	Screen curtain implementation.

	This class should be treated as a singleton:
	There should only ever be a single object created from this class at a time.
	"""

	def __init__(self):
		"""Initializer."""
		super().__init__()
		self._settings: ScreenCurtainSettings = cast(ScreenCurtainSettings, config.conf["screenCurtain"])
		self._enabled: bool = False
		if self.settings["enabled"]:
			self.enable()

	@property
	def settings(self) -> ScreenCurtainSettings:
		"""The settings for the Screen Curtain."""
		return self._settings

	@property
	def enabled(self) -> bool:
		"""Whether the Screen Curtain is currently enabled."""
		return self._enabled

	def enable(self, *, persist: bool = False) -> None:
		"""Enables the screen curtain.

		This method is idempotent.

		:param persist: Whether to write that the Screen Curtain has been enabled to config, defaults to False
		:raises RuntimeError: On failure to activate the Screen Curtain
		"""
		if self._enabled:
			log.debug("ScreenCurtain is already enabled.")
			return
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
		self._enabled = True
		if persist:
			self.settings["enabled"] = True
		if self.settings["playToggleSounds"]:
			try:
				nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "screenCurtainOn.wav"))
			except Exception:
				log.exception()

	def disable(self, *, persist: bool = True):
		"""Disables the Screen Curtain.

		This method is idempotent.

		:param persist: Whether to store that the Screen Curtain has been disabled to config, defaults to True
		"""
		if not self._enabled:
			log.debug("ScreenCurtain is already disabled")
			return
		log.debug("Disabling ScreenCurtain")
		magnification.MagShowSystemCursor(True)
		magnification.MagUninitialize()
		self._enabled = False
		if persist:
			self.settings["enabled"] = False
		if self.settings["playToggleSounds"]:
			try:
				nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "screenCurtainOff.wav"))
			except Exception:
				log.exception()

	def __del__(self):
		"""Custom deleter that disables the Screen Curtain if necessary when this object is garbage collected."""
		if self._enabled:
			self.disable(persist=False)
		if hasattr(super(), "__del__"):
			super().__del__(self)
