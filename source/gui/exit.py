# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Mesar Hameed, Joseph Lee,
# Thomas Stivers, Babbage B.V., Accessolutions, Julien Cochuyt, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
# See the file COPYING for more details.


import config
import core
from enum import auto, unique
import globalVars
import languageHandler
from logHandler import log
import queueHandler
from utils.displayString import DisplayStringEnum
import weakref
import wx

from . import guiHelper
from .startupDialogs import WelcomeDialog


try:
	import updateCheck
except RuntimeError:
	updateCheck = None


@unique
class _ExitAction(DisplayStringEnum):

	EXIT = auto()
	RESTART = auto()
	RESTART_WITH_ADDONS_DISABLED = auto()
	RESTART_WITH_DEBUG_LOGGING_ENABLED = auto()
	INSTALL_PENDING_UPDATE = auto()

	@property
	def _displayStringLabels(self):
		return {
			# Translators: An option in the combo box to choose exit action.
			self.EXIT: _("Exit"),
			# Translators: An option in the combo box to choose exit action.
			self.RESTART: _("Restart"),
			# Translators: An option in the combo box to choose exit action.
			self.RESTART_WITH_ADDONS_DISABLED: _("Restart with add-ons disabled"),
			# Translators: An option in the combo box to choose exit action.
			self.RESTART_WITH_DEBUG_LOGGING_ENABLED: _("Restart with debug logging enabled"),
			# Translators: An option in the combo box to choose exit action.
			self.INSTALL_PENDING_UPDATE: _("Install pending update"),
		}


class ExitDialog(wx.Dialog):
	_instance = None

	def __new__(cls, parent):
		# Make this a singleton.
		inst = cls._instance() if cls._instance else None
		if not inst:
			return super(cls, cls).__new__(cls, parent)
		return inst

	def __init__(self, parent):
		inst = ExitDialog._instance() if ExitDialog._instance else None
		if inst:
			return
		# Use a weakref so the instance can die.
		ExitDialog._instance = weakref.ref(self)
		# Translators: The title of the dialog to exit NVDA
		super().__init__(parent, title=_("Exit NVDA"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		warningMessages = []
		contentSizerHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		if globalVars.appArgs.disableAddons:
			addonsDisabledText = _(
				# Translators: A message in the exit Dialog shown when all add-ons are disabled.
				"All add-ons are now disabled. "
				"They will be re-enabled on the next restart unless you choose to disable them again."
			)
			warningMessages.append(addonsDisabledText)
		if languageHandler.isLanguageForced():
			langForcedMsg = _(
				# Translators: A message in the exit Dialog shown when NVDA language has been
				# overwritten from the command line.
				"NVDA's interface language is now forced from the command line."
				" On the next restart, the language  saved in NVDA's configuration will be used instead."
			)
			warningMessages.append(langForcedMsg)
		if warningMessages:
			contentSizerHelper.addItem(wx.StaticText(self, wx.ID_ANY, label="\n".join(warningMessages)))

		# Translators: The label for actions list in the Exit dialog.
		labelText = _("What would you like to &do?")
		allowedActions = list(_ExitAction)
		# Windows Store version of NVDA does not support add-ons yet.
		if config.isAppX:
			allowedActions.remove(_ExitAction.RESTART_WITH_ADDONS_DISABLED)
		# Changing debug level on secure screen is not allowed.
		# Logging on secure screens could allow keylogging of passwords and retrieval from the SYSTEM user.
		if globalVars.appArgs.secure:
			allowedActions.remove(_ExitAction.RESTART_WITH_DEBUG_LOGGING_ENABLED)
		# Installing updates should not happen in secure mode.
		if globalVars.appArgs.secure or not (updateCheck and updateCheck.isPendingUpdate()):
			allowedActions.remove(_ExitAction.INSTALL_PENDING_UPDATE)
		self.actions = [i.displayString for i in allowedActions]
		self.actionsList = contentSizerHelper.addLabeledControl(labelText, wx.Choice, choices=self.actions)
		self.actionsList.SetSelection(0)

		contentSizerHelper.addDialogDismissButtons(wx.OK | wx.CANCEL)

		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)

		mainSizer.Add(contentSizerHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.actionsList.SetFocus()
		self.CentreOnScreen()

	def onOk(self, evt):
		action = [a for a in _ExitAction if a.displayString == self.actionsList.GetStringSelection()][0]
		if action == _ExitAction.EXIT:
			WelcomeDialog.closeInstances()
			if core.triggerNVDAExit():
				# there's no need to destroy ExitDialog in this instance as triggerNVDAExit will do this
				return
			else:
				log.error("NVDA already in process of exiting, this indicates a logic error.")
				return
		elif action == _ExitAction.RESTART:
			queueHandler.queueFunction(queueHandler.eventQueue, core.restart)
		elif action == _ExitAction.RESTART_WITH_ADDONS_DISABLED:
			queueHandler.queueFunction(queueHandler.eventQueue, core.restart, disableAddons=True)
		elif action == _ExitAction.RESTART_WITH_DEBUG_LOGGING_ENABLED:
			queueHandler.queueFunction(queueHandler.eventQueue, core.restart, debugLogging=True)
		elif action == _ExitAction.INSTALL_PENDING_UPDATE:
			if updateCheck:
				destPath, version, apiVersion, backCompatTo = updateCheck.getPendingUpdate()
				from addonHandler import getIncompatibleAddons
				from gui import mainFrame
				if any(getIncompatibleAddons(currentAPIVersion=apiVersion, backCompatToAPIVersion=backCompatTo)):
					confirmUpdateDialog = updateCheck.UpdateAskInstallDialog(
						parent=mainFrame,
						destPath=destPath,
						version=version,
						apiVersion=apiVersion,
						backCompatTo=backCompatTo
					)
					confirmUpdateDialog.ShowModal()
				else:
					updateCheck.executePendingUpdate()
		wx.CallAfter(self.Destroy)

	def onCancel(self, evt):
		self.Destroy()
