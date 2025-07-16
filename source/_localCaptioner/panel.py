# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
from __future__ import unicode_literals

import wx

import gui
from gui import guiHelper

import config
from logHandler import log
import addonHandler


try:
	addonHandler.initTranslation()
	ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]
except:
	ADDON_SUMMARY = "Local Captioner"


class CaptionLocalSettingsPanel(gui.settingsDialogs.SettingsPanel):
	"""Settings panel for Caption Local add-on configuration.

	This panel allows users to configure the local model path and
	initialization settings for the Caption Local add-on.
	"""

	title = ADDON_SUMMARY

	# Translators: A message presented in the settings panel when opened while no-default profile is active.
	NO_DEFAULT_PROFILE_MESSAGE = _(
		"{name} add-on can only be configured from the Normal Configuration profile.\n"
		"Please close this dialog, set your config profile to default and try again.",
	).format(name=ADDON_SUMMARY)

	def makeSettings(self, settingsSizer: wx.Sizer) -> None:
		"""Create the settings controls for the panel.

		Args:
			settingsSizer: The sizer to add settings controls to.
		"""
		if config.conf.profiles[-1].name is not None or len(config.conf.profiles) != 1:
			self.panelDescription = self.NO_DEFAULT_PROFILE_MESSAGE
			helper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
			textItem = helper.addItem(wx.StaticText(self, label=self.panelDescription.replace("&", "&&")))
			textItem.Wrap(self.scaleSize(544))
			return

		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		# Translators: This is a label for an edit field in the CaptionLocal Settings panel.
		modelPathLabel = _("model path")

		groupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=modelPathLabel)
		groupBox = groupSizer.GetStaticBox()
		groupHelper = sHelper.addItem(gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer))

		# Translators: The label of a button to browse for a directory or a file.
		browseText = _("Browse...")
		# Translators: The title of the dialog presented when browsing for the directory.
		dirDialogTitle = _("Select a directory")

		directoryPathHelper = gui.guiHelper.PathSelectionHelper(groupBox, browseText, dirDialogTitle)
		directoryEntryControl = groupHelper.addItem(directoryPathHelper)
		self.modelPathEdit = directoryEntryControl.pathControl
		self.modelPathEdit.Value = config.conf["captionLocal"]["localModelPath"]

		# Translators: A setting in addon settings dialog.
		self.loadModelWhenInit = sHelper.addItem(
			wx.CheckBox(self, label=_("load model when init (may cause high use of memory)")),
		)
		self.loadModelWhenInit.SetValue(config.conf["captionLocal"]["loadModelWhenInit"])

	@staticmethod
	def getParameterBound(name: str, boundType: str) -> int | None:
		"""Get the bound of a parameter in the "ndtt" section of the config.

		Args:
			name: The name of the parameter.
			boundType: Either "min" or "max".

		Returns:
			The bound value if found, None otherwise.
		"""
		try:
			return config.conf.getConfigValidation(("ndtt", name)).kwargs[boundType]
		except TypeError:
			# For older version of configObj (e.g. used in NVDA 2019.2.1)
			return config.conf.getConfigValidationParameter(["ndtt", name], boundType)

	def onSave(self) -> None:
		"""Save the configuration settings.

		Only saves if operating in the default profile to prevent
		configuration issues with custom profiles.
		"""
		# Make sure we're operating in the "normal" profile
		if config.conf.profiles[-1].name is None and len(config.conf.profiles) == 1:
			config.conf["captionLocal"]["localModelPath"] = self.modelPathEdit.GetValue()
			config.conf["captionLocal"]["loadModelWhenInit"] = self.loadModelWhenInit.GetValue()
		else:
			log.debugWarning(
				"No configuration saved for CaptionLocal since the current profile is not the default one.",
			)
