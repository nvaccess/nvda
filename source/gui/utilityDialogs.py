# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited, Luke Davis
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import wx

from .nvdaControls import MessageDialog


class ContinueCancelDialog(MessageDialog):
	"""
	This implementation of a `gui.nvdaControls.MessageDialog`, provides `Continue` and `Cancel` buttons as its controls.
	These serve the same functions as `OK` and `Cancel` in other dialogs, but may be more desirable in some situations.
	"""

	def __init__(
		self,
		parent: wx.Frame,
		title: str,
		message: str,
		dialogType: int = MessageDialog.DIALOG_TYPE_STANDARD,
		continueButtonFirst: bool = True,
	) -> None:
		"""Creates a ContinueCancelDialog MessageDialog.

		:param parent: The parent window for the dialog, usually `gui.mainFrame`.
		:param title: The title or caption of the dialog.
		:param message: The message to be shown in the dialog.
		:param dialogType: One of the dialog type constants from MessageDialog, defaults to standard.
		:param continueButtonFirst: If True, the Continue button will appear first, and be selected when the dialog
			opens; if False, the Cancel button will. Defaults to True.
		"""
		self.continueButtonFirst: bool = continueButtonFirst
		super().__init__(parent, title, message, dialogType)

	def _addButtons(self, buttonHelper) -> None:
		"""Override to add Continue and Cancel buttons."""

		# Note: the order of the Continue and Cancel buttons is important, because running SetDefault()
		# on the Cancel button while the Continue button is first, has no effect. Therefore the only way to
		# allow a caller to make Cancel the default, is to put it first.
		def _makeContinue(self, buttonHelper) -> wx.Button:
			# Translators: The label for the Continue button in an NVDA dialog.
			return buttonHelper.addButton(self, id=wx.ID_OK, label=_("&Continue"))

		def _makeCancel(self, buttonHelper) -> wx.Button:
			# Translators: The label for the Cancel button in an NVDA dialog.
			return buttonHelper.addButton(self, id=wx.ID_CANCEL, label=_("Cancel"))

		if self.continueButtonFirst:
			continueButton = _makeContinue(self, buttonHelper)
			cancelButton = _makeCancel(self, buttonHelper)
		else:
			cancelButton = _makeCancel(self, buttonHelper)
			continueButton = _makeContinue(self, buttonHelper)
		continueButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.OK))
		cancelButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.CANCEL))
