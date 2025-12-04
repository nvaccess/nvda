# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
from typing import TypedDict, cast, Final

import config
import globalVars
import nvwave
import wx
from gui.guiHelper import BoxSizerHelper, ButtonHelper
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
WARN_ON_LOAD_CHECKBOX_TEXT = pgettext("screenCurtain", "Always &show a warning when enabling Screen Curtain")

UNAVAILABLE_WHEN_RECOGNISING_CONTENT_MESSAGE = pgettext(
	"screenCurtain",
	# Translators: Warning message when trying to enable the screen curtain when OCR is active.
	"Cannot enable screen curtain while performing content recognition",
)

# Translators: Reported when the screen curtain could not be enabled.
ERROR_ENABLING_MESSAGE = _("Could not enable screen curtain")


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
		# Translators: The title of a dialog.
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

	def _addContents(self, contentsSizer: BoxSizerHelper) -> None:
		self.showWarningOnLoadCheckBox: wx.CheckBox = wx.CheckBox(
			self,
			label=WARN_ON_LOAD_CHECKBOX_TEXT,
		)
		contentsSizer.addItem(self.showWarningOnLoadCheckBox)
		self.showWarningOnLoadCheckBox.SetValue(
			self._settingsStorage["warnOnLoad"],
		)

	def _addButtons(self, buttonHelper: ButtonHelper) -> None:
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

	def _exitDialog(self, result: int) -> None:
		"""Handles persisting the state of the checkbox if the user answers in the affirmative.

		:param result: either wx.YES or wx.No
		"""
		if result == wx.YES:
			self._settingsStorage["warnOnLoad"] = self.showWarningOnLoadCheckBox.IsChecked()
		self.EndModal(result)

	def _onActivateEvent(self, evt: wx.ActivateEvent) -> None:
		"""Activate event handler."""
		# focus is normally set to the first child, however, we want people to easily be able to cancel this
		# dialog
		super()._onActivateEvent(evt)
		self.noButton.SetFocus()

	def _onShowEvent(self, evt: wx.ShowEvent) -> None:
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

	_MAX_ENABLE_RETRIES: Final[int] = 3
	"""Maximum number of times to try enabling Screen Curtain."""

	def __init__(self):
		"""Initializer."""
		super().__init__()
		self._settings: ScreenCurtainSettings = cast(ScreenCurtainSettings, config.conf["screenCurtain"])
		self._enabled: bool = False
		if self.settings["enabled"]:
			try:
				self.enable()
			except RuntimeError:
				log.error("Failed to enable Screen Curtain", exc_info=True)

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
		for attempt in range(self._MAX_ENABLE_RETRIES):
			exception: Exception | None = None
			try:
				if not magnification.MagInitialize():
					raise RuntimeError("Failed to initialize magnification runtime")
				if not magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK):
					raise RuntimeError("Failed to set full screen color effect.")
				if not magnification.MagShowSystemCursor(False):
					raise RuntimeError("Failed to hide the system cursor")
				if not isScreenFullyBlack():
					raise RuntimeError("Screen is not black.")
				break
			except Exception as e:
				# We must call MagUninitialize at least as many times as we call MagInitialize,
				# as if we don't, we are liable to get permission errors
				# when attempting to use the magnification API
				magnification.MagUninitialize()
				log.debugWarning(f"Failed to enable Screen Curtain on attempt {attempt + 1}.", exc_info=e)
				exception = e
		else:
			log.debug(f"Failed to enable Screen Curtain after {self._MAX_ENABLE_RETRIES} attempts.")
			raise exception
		log.debug("Screen Curtain enabled")
		self._enabled = True
		if persist:
			self.settings["enabled"] = True
		if self.settings["playToggleSounds"]:
			try:
				nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "screenCurtainOn.wav"))
			except Exception:
				log.exception()

	def disable(self, *, persist: bool = True) -> None:
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

	def __del__(self) -> None:
		"""Custom deleter that disables the Screen Curtain if necessary when this object is garbage collected."""
		if self._enabled:
			self.disable(persist=False)
		if hasattr(super(), "__del__"):
			super().__del__(self)
