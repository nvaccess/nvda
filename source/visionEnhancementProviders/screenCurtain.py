# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Screen curtain implementation based on the windows magnification API.
The Magnification API has been marked by MS as unsupported for WOW64 applications such as NVDA. (#12491)
This module has been tested on Windows versions specified by winVersion.isFullScreenMagnificationAvailable.
"""

import os
import vision
from vision import providerBase
import winVersion
from ctypes import Structure, windll, c_float, POINTER, WINFUNCTYPE, WinError
from ctypes.wintypes import BOOL
from autoSettingsUtils.driverSetting import BooleanDriverSetting
from autoSettingsUtils.autoSettings import SupportedSettingType
import wx
import gui
from logHandler import log
from typing import Optional, Type
import nvwave
import globalVars


class MAGCOLOREFFECT(Structure):
	_fields_ = (("transform", c_float * 5 * 5),)


# homogeneous matrix for a 4-space transformation (red, green, blue, opacity).
# https://docs.microsoft.com/en-gb/windows/win32/gdiplus/-gdiplus-using-a-color-matrix-to-transform-a-single-color-use
TRANSFORM_BLACK = MAGCOLOREFFECT()  # empty transformation
TRANSFORM_BLACK.transform[4][4] = 1.0  # retain as an affine transformation
TRANSFORM_BLACK.transform[3][3] = 1.0  # retain opacity, while scaling other colours to zero (#12491)


def _errCheck(result, func, args):
	if result == 0:
		raise WinError()
	return args


class Magnification:
	"""Static class that wraps necessary functions from the Windows magnification API."""

	_magnification = windll.Magnification

	# Set full screen color effect
	_MagSetFullscreenColorEffectFuncType = WINFUNCTYPE(BOOL, POINTER(MAGCOLOREFFECT))
	_MagSetFullscreenColorEffectArgTypes = ((1, "effect"),)

	# Get full screen color effect
	_MagGetFullscreenColorEffectFuncType = WINFUNCTYPE(BOOL, POINTER(MAGCOLOREFFECT))
	_MagGetFullscreenColorEffectArgTypes = ((2, "effect"),)

	# show system cursor
	_MagShowSystemCursorFuncType = WINFUNCTYPE(BOOL, BOOL)
	_MagShowSystemCursorArgTypes = ((1, "showCursor"),)

	# initialize
	_MagInitializeFuncType = WINFUNCTYPE(BOOL)
	MagInitialize = _MagInitializeFuncType(("MagInitialize", _magnification))
	MagInitialize.errcheck = _errCheck

	# uninitialize
	_MagUninitializeFuncType = WINFUNCTYPE(BOOL)
	MagUninitialize = _MagUninitializeFuncType(("MagUninitialize", _magnification))
	MagUninitialize.errcheck = _errCheck

	# These magnification functions are not available on versions of Windows prior to Windows 8,
	# and therefore looking them up from the magnification library will raise an AttributeError.
	try:
		MagSetFullscreenColorEffect = _MagSetFullscreenColorEffectFuncType(
			("MagSetFullscreenColorEffect", _magnification),
			_MagSetFullscreenColorEffectArgTypes
		)
		MagSetFullscreenColorEffect.errcheck = _errCheck
		MagGetFullscreenColorEffect = _MagGetFullscreenColorEffectFuncType(
			("MagGetFullscreenColorEffect", _magnification),
			_MagGetFullscreenColorEffectArgTypes
		)
		MagGetFullscreenColorEffect.errcheck = _errCheck
		MagShowSystemCursor = _MagShowSystemCursorFuncType(
			("MagShowSystemCursor", _magnification),
			_MagShowSystemCursorArgTypes
		)
		MagShowSystemCursor.errcheck = _errCheck
	except AttributeError:
		MagSetFullscreenColorEffect = None
		MagGetFullscreenColorEffect = None
		MagShowSystemCursor = None


# Translators: Name for a vision enhancement provider that disables output to the screen,
# making it black.
screenCurtainTranslatedName = _("Screen Curtain")

# Translators: Description for a Screen Curtain setting that shows a warning when loading
# the screen curtain.
warnOnLoadCheckBoxText = _("Always &show a warning when loading Screen Curtain")

# Translators: Description for a screen curtain setting to play sounds when enabling/disabling the curtain
playToggleSoundsCheckBoxText = _("&Play sound when toggling Screen Curtain")


class ScreenCurtainSettings(providerBase.VisionEnhancementProviderSettings):

	warnOnLoad: bool
	playToggleSounds: bool

	@classmethod
	def getId(cls) -> str:
		return "screenCurtain"

	@classmethod
	def getDisplayName(cls) -> str:
		return screenCurtainTranslatedName

	def _get_supportedSettings(self) -> SupportedSettingType:
		return [
			BooleanDriverSetting(
				"warnOnLoad",
				warnOnLoadCheckBoxText,
				defaultVal=True
			),
			BooleanDriverSetting(
				"playToggleSounds",
				playToggleSoundsCheckBoxText,
				defaultVal=True
			),
		]

warnOnLoadText = _(
	# Translators: A warning shown when activating the screen curtain.
	# the translation of "Screen Curtain" should match the "translated name"
	"Enabling Screen Curtain will make the screen of your computer completely black. "
	"Ensure you will be able to navigate without any use of your screen before continuing. "
	"\n\n"
	"Do you wish to continue?"
)


class WarnOnLoadDialog(gui.nvdaControls.MessageDialog):

	showWarningOnLoadCheckBox: wx.CheckBox
	noButton: wx.Button

	def __init__(
			self,
			screenCurtainSettingsStorage: ScreenCurtainSettings,
			parent,
			title=_("Warning"),
			message=warnOnLoadText,
			dialogType=gui.nvdaControls.MessageDialog.DIALOG_TYPE_WARNING
	):
		self._settingsStorage = screenCurtainSettingsStorage
		super().__init__(parent, title, message, dialogType)
		self.noButton.SetFocus()

	def _addContents(self, contentsSizer):
		self.showWarningOnLoadCheckBox: wx.CheckBox = wx.CheckBox(
			self,
			label=warnOnLoadCheckBoxText
		)
		contentsSizer.addItem(self.showWarningOnLoadCheckBox)
		self.showWarningOnLoadCheckBox.SetValue(
			self._settingsStorage.warnOnLoad
		)

	def _addButtons(self, buttonHelper):
		yesButton = buttonHelper.addButton(
			self,
			id=wx.ID_YES,
			# Translators: A button in the screen curtain warning dialog which allows the user to
			# agree to enabling the curtain.
			label=_("&Yes")
		)
		yesButton.Bind(wx.EVT_BUTTON, lambda evt: self._exitDialog(wx.YES))

		noButton: wx.Button = buttonHelper.addButton(
			self,
			id=wx.ID_NO,
			# Translators: A button in the screen curtain warning dialog which allows the user to
			# disagree to enabling the curtain.
			label=_("&No")
		)
		noButton.SetDefault()
		noButton.Bind(wx.EVT_BUTTON, lambda evt: self._exitDialog(wx.NO))
		self.noButton = noButton  # so we can manually set the focus.

	def _exitDialog(self, result: int):
		"""
		@param result: either wx.YES or wx.No
		"""
		if result == wx.YES:
			settingsStorage = self._settingsStorage
			settingsStorage.warnOnLoad = self.showWarningOnLoadCheckBox.IsChecked()
			settingsStorage._saveSpecificSettings(settingsStorage, settingsStorage.supportedSettings)
		self.EndModal(result)

	def _onDialogActivated(self, evt):
		# focus is normally set to the first child, however, we want people to easily be able to cancel this
		# dialog
		super()._onDialogActivated(evt)
		self.noButton.SetFocus()

	def _onShowEvt(self, evt):
		"""When no other dialogs have been opened first, focus lands in the wrong place (on the checkbox),
		so we correct it after the dialog is opened.
		"""
		if evt.IsShown():
			self.noButton.SetFocus()
		super()._onShowEvt(evt)


class ScreenCurtainGuiPanel(
		gui.AutoSettingsMixin,
		gui.SettingsPanel,
):

	_enabledCheckbox: wx.CheckBox
	_enableCheckSizer: wx.BoxSizer
	
	helpId = "VisionSettingsScreenCurtain"

	from gui.settingsDialogs import VisionProviderStateControl

	def __init__(
			self,
			parent,
			providerControl: VisionProviderStateControl
	):
		self._providerControl = providerControl
		super().__init__(parent)

	def _buildGui(self):
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)

		self._enabledCheckbox = wx.CheckBox(
			self,
			#  Translators: option to enable screen curtain in the vision settings panel
			label=_("Make screen black (immediate effect)")
		)
		isProviderActive = bool(self._providerControl.getProviderInstance())
		self._enabledCheckbox.SetValue(isProviderActive)

		self.mainSizer.Add(self._enabledCheckbox)
		self.mainSizer.AddSpacer(size=self.scaleSize(10))
		# this options separator is done with text rather than a group box because a groupbox is too verbose,
		# but visually some separation is helpful, since the rest of the options are really sub-settings.
		self.optionsText = wx.StaticText(
			self,
			# Translators: The label for a group box containing the NVDA highlighter options.
			label=_("Options:")
		)
		self.mainSizer.Add(self.optionsText)
		self.lastControl = self.optionsText
		self.settingsSizer = wx.BoxSizer(wx.VERTICAL)
		self.makeSettings(self.settingsSizer)
		self.mainSizer.Add(self.settingsSizer, border=self.scaleSize(15), flag=wx.LEFT | wx.EXPAND)
		self.mainSizer.Fit(self)
		self.SetSizer(self.mainSizer)

	def getSettings(self) -> ScreenCurtainSettings:
		return ScreenCurtainProvider.getSettings()

	def makeSettings(self, sizer: wx.BoxSizer):
		self.updateDriverSettings()
		self.Bind(wx.EVT_CHECKBOX, self._onCheckEvent)

	def onPanelActivated(self):
		self.lastControl = self._enabledCheckbox

	def _onCheckEvent(self, evt: wx.CommandEvent):
		if evt.GetEventObject() is self._enabledCheckbox:
			self._ensureEnableState(evt.IsChecked())

	def _ensureEnableState(self, shouldBeEnabled: bool):
		currentlyEnabled = bool(self._providerControl.getProviderInstance())
		if shouldBeEnabled and not currentlyEnabled:
			confirmed = self.confirmInitWithUser()
			if not confirmed or not self._providerControl.startProvider():
				self._enabledCheckbox.SetValue(False)
		elif not shouldBeEnabled and currentlyEnabled:
			self._providerControl.terminateProvider()

	def confirmInitWithUser(self) -> bool:
		settingsStorage = self._getSettingsStorage()
		if not settingsStorage.warnOnLoad:
			return True
		parent = self
		with WarnOnLoadDialog(
			screenCurtainSettingsStorage=settingsStorage,
			parent=parent
		) as dlg:
			res = dlg.ShowModal()
			# WarnOnLoadDialog can change settings, reload them
			self.updateDriverSettings()
			return res == wx.YES


class ScreenCurtainProvider(providerBase.VisionEnhancementProvider):
	_settings = ScreenCurtainSettings()

	@classmethod
	def canStart(cls):
		"""
		While the Magnification API has been marked by MS as unsupported for WOW64 applications such as NVDA.
		ScreenCurtain's specific usage of the API has been tested to confirm the approach works in released
		versions of Windows, this may not continue to be true in the future. The Magnification API was
		introduced by Microsoft with Windows 8.
		"""
		return winVersion.isFullScreenMagnificationAvailable()

	@classmethod
	def getSettingsPanelClass(cls) -> Optional[Type]:
		"""Returns the instance to be used in order to construct a settings panel for the provider.
		@return: Optional[SettingsPanel]
		@remarks: When None is returned, L{gui.settingsDialogs.VisionProviderSubPanel_Wrapper} is used.
		"""
		return ScreenCurtainGuiPanel

	@classmethod
	def getSettings(cls) -> ScreenCurtainSettings:
		return cls._settings

	def __init__(self):
		super().__init__()
		log.debug(f"Starting ScreenCurtain")
		Magnification.MagInitialize()
		try:
			Magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)
			Magnification.MagShowSystemCursor(False)
		except Exception as e:
			Magnification.MagUninitialize()
			raise e
		if self.getSettings().playToggleSounds:
			try:
				nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "screenCurtainOn.wav"))
			except Exception:
				log.exception()

	def terminate(self):
		log.debug(f"Terminating ScreenCurtain")
		try:
			super().terminate()
		finally:
			Magnification.MagShowSystemCursor(True)
			Magnification.MagUninitialize()
			if self.getSettings().playToggleSounds:
				try:
					nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "screenCurtainOff.wav"))
				except Exception:
					log.exception()

	def registerEventExtensionPoints(self, extensionPoints):
		# The screen curtain isn't interested in any events
		pass


VisionEnhancementProvider = ScreenCurtainProvider
