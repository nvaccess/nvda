# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Bram Duvigneau
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""GUI functionality for managing NVDA configuration, including factory reset with undo support."""

import core
import queueHandler
import ui
import wx

from .message import (
	Button,
	DefaultButton,
	displayDialogAsModal,
	MessageDialog,
	ReturnCode,
)


class FactoryResetUndoDialog(MessageDialog):
	"""Dialog shown after a factory reset, allowing the user to undo the reset or keep it."""

	def __init__(self):
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

	def _handleUndo(self) -> None:
		"""Restore the previous configuration by reloading from disk."""
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


def confirmRevertToDefaultConfiguration() -> None:
	"""Reset config to factory defaults in memory, then show a dialog allowing the user to undo.

	The on-disk configuration is not modified. If the user chooses to undo, the configuration
	is reloaded from disk. If the user keeps the factory defaults, the in-memory defaults
	will be saved to disk on normal NVDA shutdown.
	This is used when triggered from the NVDA menu.
	"""
	queueHandler.queueFunction(queueHandler.eventQueue, core.resetConfiguration, factoryDefaults=True)
	queueHandler.queueFunction(
		queueHandler.eventQueue,
		_showFactoryResetUndoDialog,
	)


def _showFactoryResetUndoDialog() -> None:
	"""Create and show the factory reset undo dialog on the wx GUI thread."""
	wx.CallAfter(FactoryResetUndoDialog().showAndHandleResult)
