# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2026 NV Access Limited, Bram Duvigneau
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""GUI functionality for managing NVDA configuration, including factory reset with undo support."""

import os
import shutil

import config
import core
import NVDAState
import queueHandler
import ui
import wx
from logHandler import log

from .message import (
	Button,
	DefaultButton,
	displayDialogAsModal,
	MessageDialog,
	ReturnCode,
)


class FactoryResetUndoDialog(MessageDialog):
	"""Dialog shown after a factory reset, allowing the user to undo the reset or keep it."""

	def __init__(self, backupPath: str, configPath: str):
		self._backupPath = backupPath
		self._configPath = configPath
		# Translators: The title of the dialog shown after resetting configuration to factory defaults.
		title = _("Factory Defaults Restored")
		message = _(
			# Translators: The message shown in the dialog after the configuration has been reset to factory defaults.
			# The user can choose to keep the factory defaults or undo the reset.
			"Your configuration has been reset to factory defaults.\n"
			"Choose OK to keep factory defaults, or Undo to restore your previous configuration.",
		)
		undoButton = Button(
			id=ReturnCode.CUSTOM_1,
			# Translators: The label of the undo button in the factory defaults reset dialog.
			# Pressing this button restores the previous configuration.
			label=_("&Undo"),
			fallbackAction=True,
		)
		super().__init__(
			None,
			message,
			title,
			buttons=(
				DefaultButton.OK,
				undoButton,
			),
		)

	def showAndHandleResult(self) -> None:
		"""Show the dialog modally and handle the user's choice."""
		result = displayDialogAsModal(self)
		if result == ReturnCode.CUSTOM_1:
			self._handleUndo()
		else:
			self._handleKeepDefaults()
		self._cleanupBackup()

	def _handleUndo(self) -> None:
		"""Restore the previous configuration from backup."""
		if not os.path.isfile(self._backupPath):
			log.error("Backup configuration file not found for undo")
			return
		try:
			shutil.copy2(self._backupPath, self._configPath)
		except OSError:
			log.error("Failed to restore configuration from backup", exc_info=True)
		else:
			queueHandler.queueFunction(
				queueHandler.eventQueue,
				core.resetConfiguration,
			)
			queueHandler.queueFunction(
				queueHandler.eventQueue,
				ui.message,
				# Translators: Reported when a factory reset has been undone
				# and the previous configuration has been restored.
				_("Factory reset undone. Previous configuration restored."),
			)

	def _handleKeepDefaults(self) -> None:
		"""Save the factory defaults to disk."""
		try:
			config.conf.save()
		except OSError:
			log.error("Failed to save factory default configuration to disk", exc_info=True)

	def _cleanupBackup(self) -> None:
		"""Remove the backup file."""
		try:
			if os.path.isfile(self._backupPath):
				os.remove(self._backupPath)
		except OSError:
			log.debugWarning("Failed to remove configuration backup file", exc_info=True)


def confirmRevertToDefaultConfiguration() -> None:
	"""Reset config to factory defaults, then show a dialog allowing the user to undo the reset.

	If the configuration cannot be backed up (e.g. read-only media), the reset proceeds
	without showing the undo dialog, as undo would not be possible.
	This is used when triggered from the NVDA menu.
	"""
	configPath = NVDAState.WritePaths.nvdaConfigFile
	backupPath = configPath + ".beforeReset.bak"
	backupSucceeded = False
	# Back up the current config file before resetting.
	try:
		if os.path.isfile(configPath):
			shutil.copy2(configPath, backupPath)
			backupSucceeded = True
	except OSError:
		log.error("Failed to back up configuration file before factory reset", exc_info=True)
	queueHandler.queueFunction(queueHandler.eventQueue, core.resetConfiguration, factoryDefaults=True)
	if backupSucceeded:
		queueHandler.queueFunction(
			queueHandler.eventQueue,
			_showFactoryResetUndoDialog,
			backupPath,
			configPath,
		)
	else:
		queueHandler.queueFunction(
			queueHandler.eventQueue,
			ui.message,
			# Translators: Reported when configuration has been restored to defaults,
			# by using restore configuration to factory defaults item in NVDA menu.
			_("Configuration restored to factory defaults"),
		)


def _showFactoryResetUndoDialog(backupPath: str, configPath: str) -> None:
	"""Create and show the factory reset undo dialog on the wx GUI thread."""
	wx.CallAfter(FactoryResetUndoDialog(backupPath, configPath).showAndHandleResult)
