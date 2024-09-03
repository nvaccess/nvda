# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited, Luke Davis
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import wx

from gui.nvdaControls import MessageDialog


class ContinueCancelDialog(MessageDialog):

	def __init__(
			self,
			parent,
			message: str,
			title: str,
			continueByDefault: bool = True,
			dialogType: int = MessageDialog.DIALOG_TYPE_STANDARD
	) -> None:
		super().__init__(parent, message, title)
		self.dialogType: int = dialogType
		self.continueByDefault: bool = continueByDefault

	def _addButtons(self) -> None:
		"""Override to add Continue and Cancel buttons."""
		# Translators: The label for the Continue button in an NVDA dialog.
		continueButton = wx.Button(self, wx.ID_OK, _("&Continue"))
		# Translators: The label for a Cancel button in an NVDA dialog.
		cancelButton = wx.Button(self, wx.ID_CANCEL, _("Cancel"))
		self.Sizer.Add(continueButton, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
		self.Sizer.Add(cancelButton, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
		self.SetAffirmativeId(wx.ID_OK)
		self.SetEscapeId(wx.ID_CANCEL)
		if self.continueByDefault:
			continueButton.SetDefault()
		else:
			cancelButton.SetDefault()
