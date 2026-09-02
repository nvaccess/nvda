# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Settings UI for on-device OCR."""

import addonHandler
import config
import wx
from gui import guiHelper
from gui.settingsDialogs import SettingsPanel

addonHandler.initTranslation()

_CONFIG_SECTION = "onDeviceOcr"
_MODEL_PROFILES = ("tiny", "small")


class OnDeviceOcrSettingsPanel(SettingsPanel):
	# Translators: The title of the on-device OCR settings panel.
	title = _("On-device OCR")

	def makeSettings(self, settingsSizer: wx.BoxSizer) -> None:
		helper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: Label for the OCR model profile setting.
		modelLabel = _("OCR &model:")
		modelChoices = (
			# Translators: Name of the smallest and fastest OCR model.
			_("Tiny (Chinese, English and Latin scripts; fastest)"),
			# Translators: Name of the more accurate multilingual OCR model.
			_("Small (adds Japanese; more accurate)"),
		)
		self.modelChoice = helper.addLabeledControl(modelLabel, wx.Choice, choices=modelChoices)
		profile = str(config.conf[_CONFIG_SECTION]["modelProfile"])
		try:
			profileIndex = _MODEL_PROFILES.index(profile)
		except ValueError:
			profileIndex = 0
		self.modelChoice.SetSelection(profileIndex)

		# Translators: Label for automatically reading OCR output.
		autoSayAllLabel = _("Automatically &read the result")
		self.autoSayAllCheckbox = helper.addItem(wx.CheckBox(self, label=autoSayAllLabel))
		self.autoSayAllCheckbox.SetValue(bool(config.conf[_CONFIG_SECTION]["autoSayAllOnResult"]))

		# Translators: Label for how long the external OCR process remains loaded.
		idleTimeoutLabel = _("Keep the OCR engine loaded for (seconds):")
		self.idleTimeoutSpin = helper.addLabeledControl(
			idleTimeoutLabel,
			wx.SpinCtrl,
			min=0,
			max=3600,
			initial=int(config.conf[_CONFIG_SECTION]["workerIdleTimeoutSeconds"]),
		)
		# Translators: Explains first-use model download and privacy behavior.
		helper.addItem(
			wx.StaticText(
				self,
				label=_(
					"The selected model is downloaded and SHA-256 verified on first use. "
					"Recognition then runs locally; captured images are not uploaded.",
				),
			),
		)

	def onSave(self) -> None:
		selection = self.modelChoice.GetSelection()
		if selection not in range(len(_MODEL_PROFILES)):
			selection = 0
		config.conf[_CONFIG_SECTION]["modelProfile"] = _MODEL_PROFILES[selection]
		config.conf[_CONFIG_SECTION]["autoSayAllOnResult"] = self.autoSayAllCheckbox.IsChecked()
		config.conf[_CONFIG_SECTION]["workerIdleTimeoutSeconds"] = self.idleTimeoutSpin.GetValue()
