# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Screen curtain implementation based on the windows magnification API.
This implementation only works on Windows 8 and above.
"""

import vision
import winVersion
from ctypes import Structure, windll, c_float, POINTER, WINFUNCTYPE, WinError
from ctypes.wintypes import BOOL
import driverHandler
import wx
import gui
from logHandler import log
from vision.providerBase import VisionEnhancementProviderSettings, SupportedSettingType
from typing import Optional, Type, Callable


class MAGCOLOREFFECT(Structure):
	_fields_ = (("transform", c_float * 5 * 5),)


# homogeneous matrix for a 4-space transformation (red, green, blue, opacity).
# https://docs.microsoft.com/en-gb/windows/win32/gdiplus/-gdiplus-using-a-color-matrix-to-transform-a-single-color-use
TRANSFORM_BLACK = MAGCOLOREFFECT()
TRANSFORM_BLACK.transform[4][4] = 1.0


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

	# initialise
	_MagInitializeFuncType = WINFUNCTYPE(BOOL)
	MagInitialize = _MagInitializeFuncType(("MagInitialize", _magnification))
	MagInitialize.errcheck = _errCheck

	# uninitialize
	_MagUninitializeFuncType = WINFUNCTYPE(BOOL)
	MagUninitialize = _MagUninitializeFuncType(("MagUninitialize", _magnification))
	MagUninitialize.errcheck = _errCheck

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
	except AttributeError:
		MagSetFullscreenColorEffect = None
		MagGetFullscreenColorEffect = None
	MagShowSystemCursor = _MagShowSystemCursorFuncType(
		("MagShowSystemCursor", _magnification),
		_MagShowSystemCursorArgTypes
	)
	MagShowSystemCursor.errcheck = _errCheck


# Translators: Description of a vision enhancement provider that disables output to the screen,
# making it black.
screenCurtainTranslatedName = _("Screen Curtain")

warnOnLoadCheckBoxText = (
	# Translators: Description for a screen curtain setting that shows a warning when loading
	# the screen curtain.
	_(f"Always &show a warning when loading {screenCurtainTranslatedName}")
)


class ScreenCurtainSettings(VisionEnhancementProviderSettings):

	warnOnLoad: bool

	@classmethod
	def getId(cls) -> str:
		return "screenCurtain"

	@classmethod
	def getTranslatedName(cls) -> str:
		return screenCurtainTranslatedName

	@classmethod
	def _get_preInitSettings(cls) -> SupportedSettingType:
		return [
			driverHandler.BooleanDriverSetting(
				"warnOnLoad",
				warnOnLoadCheckBoxText,
				defaultVal=True
			),
		]

	def _get_supportedSettings(self) -> SupportedSettingType:
		return super().supportedSettings


warnOnLoadText = _(
	# Translators: A warning shown when activating the screen curtain.
	# {description} is replaced by the translation of "screen curtain"
	f"You are about to enable {screenCurtainTranslatedName}.\n"
	f"When {screenCurtainTranslatedName} is enabled, the screen of your computer will go completely black.\n"
	f"Do you really want to enable {screenCurtainTranslatedName}?"
)


class WarnOnLoadDialog(gui.nvdaControls.MessageDialog):

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

		noButton = buttonHelper.addButton(
			self,
			id=wx.ID_NO,
			# Translators: A button in the screen curtain warning dialog which allows the user to
			# disagree to enabling the curtain.
			label=_("&No")
		)
		noButton.SetDefault()
		noButton.Bind(wx.EVT_BUTTON, lambda evt: self._exitDialog(wx.NO))
		noButton.SetFocus()

	def _exitDialog(self, result: int):
		"""
		@param result: either wx.YES or wx.No
		"""
		if result == wx.YES:
			settingsStorage = self._settingsStorage
			settingsStorage.warnOnLoad = self.showWarningOnLoadCheckBox.IsChecked()
			settingsStorage._saveSpecificSettings(settingsStorage, settingsStorage.preInitSettings)
		self.EndModal(result)


class ScreenCurtainGuiPanel(
		gui.DriverSettingsMixin,
		gui.SettingsPanel,
):

	_enabledCheckbox: wx.CheckBox
	_enableCheckSizer: wx.BoxSizer

	def __init__(
			self,
			parent,
			getProvider: Callable[[], Optional[vision.VisionEnhancementProvider]],
			initProvider: Callable[[], bool],
			terminateProvider: Callable[[], None]
	):
		self._getProvider = getProvider
		self._initProvider = initProvider
		self._terminateProvider = terminateProvider
		super().__init__(parent)

	def getSettings(self) -> ScreenCurtainSettings:
		return ScreenCurtainProvider.getSettings()

	def makeSettings(self, sizer: wx.BoxSizer):
		self._enabledCheckbox = wx.CheckBox(
			self,
			#  Translators: option to enable screen curtain in the vision settings panel
			label=_("Make screen black (immediate effect)")
		)
		self.lastControl = self._enabledCheckbox
		sizer.Add(self._enabledCheckbox)
		self._enableCheckSizer = sizer
		self.mainSizer.Add(self._enableCheckSizer, flag=wx.ALL | wx.EXPAND)
		optionsSizer = wx.StaticBoxSizer(
			wx.StaticBox(
				self,
				# Translators: The label for a group box containing the NVDA welcome dialog options.
				label=_("Options")
			),
			wx.VERTICAL
		)
		self.settingsSizer = optionsSizer
		self.updateDriverSettings()
		self.Bind(wx.EVT_CHECKBOX, self._onCheckEvent)

	def onPanelActivated(self):
		self.lastControl = self._enabledCheckbox

	def _onCheckEvent(self, evt: wx.CommandEvent):
		if evt.GetEventObject() is self._enabledCheckbox:
			self._ensureEnableState(evt.IsChecked())

	def _ensureEnableState(self, shouldBeEnabled: bool):
		currentlyEnabled = bool(self._getProvider())
		if shouldBeEnabled and not currentlyEnabled:
			log.debug("init provider")
			confirmed = self.confirmInitWithUser()
			if confirmed:
				self._initProvider()
			else:
				self._enabledCheckbox.SetValue(False)
		elif not shouldBeEnabled and currentlyEnabled:
			log.debug("terminate provider")
			self._terminateProvider()

	def confirmInitWithUser(self) -> bool:
		settingsStorage = self._getSettingsStorage()
		if not settingsStorage.warnOnLoad:
			return True
		parent = self
		dlg = WarnOnLoadDialog(
			screenCurtainSettingsStorage=settingsStorage,
			parent=parent
		)
		res = dlg.ShowModal()
		# WarnOnLoadDialog can change settings, reload them
		self.updateDriverSettings()
		return res == wx.YES


class ScreenCurtainProvider(vision.providerBase.VisionEnhancementProvider):
	_settings = ScreenCurtainSettings()

	@classmethod
	def canStart(cls):
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
		super(VisionEnhancementProvider, self).__init__()
		log.debug(f"ScreenCurtain", stack_info=True)
		Magnification.MagInitialize()
		Magnification.MagShowSystemCursor(False)
		Magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)

	def terminate(self):
		super().terminate()
		Magnification.MagShowSystemCursor(True)
		Magnification.MagUninitialize()

	def registerEventExtensionPoints(self, extensionPoints):
		# The screen curtain isn't interested in any events
		pass


VisionEnhancementProvider = ScreenCurtainProvider
