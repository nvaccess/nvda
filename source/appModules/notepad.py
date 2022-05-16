# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Windows Notepad.
While this app module also covers older Notepad releases,
this module provides workarounds for Windows 11 Notepad."""

import appModuleHandler
import api


class AppModule(appModuleHandler.AppModule):

	def _get_statusBar(self):
		# #13688: Notepad 11 uses Windows 11 user interface, therefore status bar is harder to obtain.
		# This does not affect earlier versions.
		notepadVersion = int(self.productVersion.split(".")[0])
		if notepadVersion < 11:
			raise NotImplementedError()
		# And no, status bar is shown when editing documents.
		# Thankfully, of all the UIA objects encountered, document window has a unique window class name.
		if api.getFocusObject().windowClassName != "RichEditD2DPT":
			raise NotImplementedError()
		# Look for a specific child as some children report the same UIA properties such as class name.
		# Make sure to look for a foreground UIA element which hosts status bar content if visible.
		notepadStatusBarIndex = 7
		statusBar = api.getForegroundObject().children[notepadStatusBarIndex].firstChild
		# No location for a disabled status bar i.e. location is 0 (x, y, width, height).
		if not any(statusBar.location):
			raise NotImplementedError()
		return statusBar
