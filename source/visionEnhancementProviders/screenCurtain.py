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
import config
from logHandler import log


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


class VisionEnhancementProvider(vision.providerBase.VisionEnhancementProvider):
	name = "screenCurtain"
	# Translators: Description of a vision enhancement provider that disables output to the screen,
	# making it black.
	description = _("Screen Curtain")
	supportedRoles = frozenset([vision.constants.Role.COLORENHANCER])

	# Translators: Description for a screen curtain setting that shows a warning when loading
	# the screen curtain.
	warnOnLoadCheckBoxText = _(f"Always &show a warning when loading {description}")

	preInitSettings = [
		driverHandler.BooleanDriverSetting(
			"warnOnLoad",
			warnOnLoadCheckBoxText,
			defaultVal=True
		),
	]

	@classmethod
	def canStart(cls):
		return winVersion.isFullScreenMagnificationAvailable()

	def __init__(self):
		super(VisionEnhancementProvider, self).__init__()
		log.debug(f"ScreenCurtain", stack_info=True)
		Magnification.MagInitialize()
		Magnification.MagShowSystemCursor(False)
		Magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)

	def terminate(self, *args, **kwargs):
		super().terminate(*args, **kwargs)
		Magnification.MagShowSystemCursor(True)
		Magnification.MagUninitialize()

	def registerEventExtensionPoints(self, extensionPoints):
		# The screen curtain isn't interested in any events
		pass

	warnOnLoadText = _(
		# Translators: A warning shown when activating the screen curtain.
		# {description} is replaced by the translation of "screen curtain"
		f"You are about to enable {description}.\n"
		f"When {description} is enabled, the screen of your computer will go completely black.\n"
		f"Do you really want to enable {description}?"
	)

	@classmethod
	def confirmInitWithUser(cls) -> bool:
		cls._initSpecificSettings(cls, cls.preInitSettings)
		if cls.warnOnLoad:
			parent = next(
				(
					dlg for dlg, state in gui.settingsDialogs.NVDASettingsDialog._instances.items()
					if isinstance(dlg, gui.settingsDialogs.NVDASettingsDialog)
					and state == gui.settingsDialogs.SettingsDialog._DIALOG_CREATED_STATE
				),
				gui.mainFrame
			)
			with WarnOnLoadDialog(
				parent=parent,
				# Translators: Title for the screen curtain warning dialog.
				title=_("Warning"),
				message=cls.warnOnLoadText,
				dialogType=WarnOnLoadDialog.DIALOG_TYPE_WARNING
			) as dlg:
				res = dlg.ShowModal()
				if res == wx.NO:
					return False
				else:
					cls.warnOnLoad = dlg.showWarningOnLoadCheckBox.IsChecked()
					cls._saveSpecificSettings(cls, cls.preInitSettings)
		return True


class WarnOnLoadDialog(gui.nvdaControls.MessageDialog):

	def _addContents(self, contentsSizer):
		self.showWarningOnLoadCheckBox = contentsSizer.addItem(wx.CheckBox(
			self,
			label=VisionEnhancementProvider.warnOnLoadCheckBoxText
		))
		self.showWarningOnLoadCheckBox.SetValue(
			config.conf[VisionEnhancementProvider._configSection][VisionEnhancementProvider.name][
				"warnOnLoad"
			]
		)

	def _addButtons(self, buttonHelper):
		yesButton = buttonHelper.addButton(
			self,
			id=wx.ID_YES,
			# Translators: A button in the screen curtain warning dialog which allows the user to
			# agree to enabling the curtain.
			label=_("&Yes")
		)
		yesButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.YES))

		noButton = buttonHelper.addButton(
			self,
			id=wx.ID_NO,
			# Translators: A button in the screen curtain warning dialog which allows the user to
			# disagree to enabling the curtain.
			label=_("&No")
		)
		noButton.SetDefault()
		noButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.NO))
		noButton.SetFocus()
