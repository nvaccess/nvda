# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited, Luke Davis
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import wx

from .nvdaControls import MessageDialog


class ContinueCancelDialog(MessageDialog):
	def __init__(
		self,
		parent,
		title: str,
		message: str,
		dialogType: int = MessageDialog.DIALOG_TYPE_STANDARD,
		continueByDefault: bool = True,
	) -> None:
		self.continueByDefault: bool = continueByDefault
		super().__init__(parent, message, title, dialogType)

	def _addButtons(self, buttonHelper) -> None:
		"""Override to add Continue and Cancel buttons."""
		# Translators: The label for the Continue button in an NVDA dialog.
		continueButton = buttonHelper.addButton(self, id=wx.ID_OK, label=_("&Continue"))
		continueButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.OK))
		# Translators: The label for the Cancel button in an NVDA dialog.
		cancelButton = buttonHelper.addButton(self, id=wx.ID_CANCEL, label=_("Cancel"))
		cancelButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.CANCEL))
		if self.continueByDefault:
			continueButton.SetDefault()
		else:
			cancelButton.SetDefault()
