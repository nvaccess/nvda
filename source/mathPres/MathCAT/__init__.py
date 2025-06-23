# -*- coding: UTF-8 -*-

"""
MathCAT add-on: generates speech, braille, and allows exploration of expressions written in MathML.
The goal of this add-on is to replicate/improve upon the functionality of MathPlayer which has been discontinued.
Author: Neil Soiffer
Copyright: this file is copyright GPL2
  The code additionally makes use of the MathCAT library (written in Rust) which is covered by the MIT license
  and also (obviously) requires external speech engines and braille drivers.
  The plugin also requires the use of a small python dll: python3.dll
  python3.dll has "Copyright © 2001-2022 Python Software Foundation; All Rights Reserved
"""

import globalPluginHandler  # we are a global plugin
import globalVars
import mathPres  # math plugin stuff
import wx
import addonHandler
from gui import mainFrame
from .MathCAT import MathCAT
from .MathCATPreferences import UserInterface

# Import the _ function for translation
_ = wx.GetTranslation
addonHandler.initTranslation()
mathPres.registerProvider(MathCAT(), speech=True, braille=True, interaction=True)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""
	Global plugin for the MathCAT add-on.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Initialize the Global Plugin and add the MathCAT menu.

		:param args: Additional positional arguments.
		:param kwargs: Additional keyword arguments.
		"""
		super().__init__(*args, **kwargs)
		# MathCAT.__init__(self)
		self.addMathCATMenu()

	def addMathCATMenu(self) -> None:
		"""
		Adds the MathCAT settings menu to the NVDA preferences.
		"""
		if not globalVars.appArgs.secure:
			self.preferencesMenu = mainFrame.sysTrayIcon.preferencesMenu
			# Translators: this show up in the NVDA preferences dialog. It opens the MathCAT preferences dialog
			self.settings = self.preferencesMenu.Append(wx.ID_ANY, _("&MathCAT Settings..."))
			mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onSettings, self.settings)

	def onSettings(self, evt: wx.CommandEvent) -> None:
		"""
		Opens the MathCAT preferences dialog.

		:param evt: The event that triggered this action.
		"""
		mainFrame.popupSettingsDialog(UserInterface)

	def terminate(self) -> None:
		"""
		Cleans up by removing the MathCAT menu item upon termination.
		"""
		try:
			if not globalVars.appArgs.secure:
				self.preferencesMenu.Remove(self.settings)
		except (AttributeError, RuntimeError):
			pass
