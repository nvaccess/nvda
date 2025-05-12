# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Mesar Hameed, Joseph Lee,
# Thomas Stivers, Babbage B.V., Accessolutions, Julien Cochuyt, Cyrille Bougot, Luke Davis
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from collections.abc import Callable
import os
import ctypes
import warnings
import wx
import wx.adv

import globalVars
import tones
import ui
from documentationUtils import getDocFilePath, displayLicense, reportNoDocumentation
from logHandler import log
import config
import versionInfo
import speech
import queueHandler
import core
from typing import (
	Any,
	Optional,
	Type,
)
import systemUtils
from .message import (
	# messageBox is accessed through `gui.messageBox` as opposed to `gui.message.messageBox` throughout NVDA,
	# be cautious when removing
	messageBox,
	MessageDialog,
	displayDialogAsModal,
)
from . import blockAction
from .speechDict import (
	DefaultDictionaryDialog,
	VoiceDictionaryDialog,
	TemporaryDictionaryDialog,
)
from .nvdaControls import _ContinueCancelDialog

# ExitDialog is accessed through `import gui.ExitDialog` as opposed to `gui.exit.ExitDialog`.
# Be careful when removing, and only do in a compatibility breaking release.
from .exit import ExitDialog
from .settingsDialogs import (
	AudioPanel,
	BrailleDisplaySelectionDialog,
	BrailleSettingsPanel,
	BrowseModePanel,
	DocumentFormattingPanel,
	GeneralSettingsPanel,
	InputCompositionPanel,
	KeyboardSettingsPanel,
	MouseSettingsPanel,
	MultiCategorySettingsDialog,
	NVDASettingsDialog,
	ObjectPresentationPanel,
	RemoteSettingsPanel,
	SettingsDialog,
	SpeechSettingsPanel,
	SpeechSymbolsDialog,
	SynthesizerSelectionDialog,
	TouchInteractionPanel,
	ReviewCursorPanel,
	UwpOcrPanel,
)
from .startupDialogs import WelcomeDialog
from .inputGestures import InputGesturesDialog
from . import logViewer
import speechViewer
import winUser
import api
import NVDAState


if NVDAState._allowDeprecatedAPI():

	def quit():
		"""
		Deprecated, use `wx.CallAfter(mainFrame.onExitCommand, None)` directly instead.
		"""
		log.debugWarning("Deprecated function called: gui.quit", stack_info=True)
		wx.CallAfter(mainFrame.onExitCommand, None)


try:
	import updateCheck
except RuntimeError:
	updateCheck = None

### Constants
NVDA_PATH = globalVars.appDir
ICON_PATH = os.path.join(NVDA_PATH, "images", "nvda.ico")
DONATE_URL = f"{versionInfo.url}/donate/"

### Globals
mainFrame: Optional["MainFrame"] = None
"""Set by initialize. Should be used as the parent for "top level" dialogs.
"""


def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	from gui.settingsDialogs import AutoSettingsMixin, SettingsPanel

	if attrName == "AutoSettingsMixin" and NVDAState._allowDeprecatedAPI():
		log.warning(
			"Importing AutoSettingsMixin from here is deprecated. "
			"Import AutoSettingsMixin from gui.settingsDialogs instead. ",
			# Include stack info so testers can report warning to add-on author.
			stack_info=True,
		)
		return AutoSettingsMixin
	if attrName == "SettingsPanel" and NVDAState._allowDeprecatedAPI():
		log.warning(
			"Importing SettingsPanel from here is deprecated. "
			"Import SettingsPanel from gui.settingsDialogs instead. ",
			# Include stack info so testers can report warning to add-on author.
			stack_info=True,
		)
		return SettingsPanel
	if attrName == "ExecAndPump" and NVDAState._allowDeprecatedAPI():
		log.warning(
			"Importing ExecAndPump from here is deprecated. Import ExecAndPump from systemUtils instead. ",
			# Include stack info so testers can report warning to add-on author.
			stack_info=True,
		)
		import systemUtils

		return systemUtils.ExecAndPump
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")


class MainFrame(wx.Frame):
	"""A hidden window, intended to act as the parent to all dialogs."""

	def __init__(self):
		style = wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX | wx.FRAME_NO_TASKBAR
		super(MainFrame, self).__init__(None, wx.ID_ANY, versionInfo.name, size=(1, 1), style=style)
		self.Bind(wx.EVT_CLOSE, self.onExitCommand)
		self.sysTrayIcon = SysTrayIcon(self)
		#: The focus before the last popup or C{None} if unknown.
		#: This is only valid before L{prePopup} is called,
		#: so it should be used as early as possible in any popup that needs it.
		#: @type: L{NVDAObject}
		self.prevFocus = None
		#: The focus ancestors before the last popup or C{None} if unknown.
		#: @type: list of L{NVDAObject}
		self.prevFocusAncestors = None
		# If NVDA has the uiAccess privilege, it can always set the foreground window.
		if not systemUtils.hasUiAccess():
			# This makes Windows return to the previous foreground window and also seems to allow NVDA to be brought to the foreground.
			self.Show()
			self.Hide()
			if winUser.isWindowVisible(self.Handle):
				# HACK: Work around a wx bug where Hide() doesn't actually hide the window,
				# but IsShown() returns False and Hide() again doesn't fix it.
				# This seems to happen if the call takes too long.
				self.Show()
				self.Hide()

	def prePopup(self):
		"""Prepare for a popup.
		This should be called before any dialog or menu which should pop up for the user.
		L{postPopup} should be called after the dialog or menu has been shown.
		@postcondition: A dialog or menu may be shown.
		"""
		focus = api.getFocusObject()
		# Do not set prevFocus if the focus is on a control rendered by NVDA itself, such as the NVDA menu.
		# This allows to refer to the control that had focus before opening the menu while still using NVDA
		# on its own controls.
		# The check for NVDA process ID can be bypassed by setting the optional attribute
		# L{isPrevFocusOnNvdaPopup} to L{True} when a NVDA dialog offers customizable bound gestures,
		# eg. the NVDA Python Console.
		if focus.processID != globalVars.appPid or getattr(focus, "isPrevFocusOnNvdaPopup", False):
			self.prevFocus = focus
			self.prevFocusAncestors = api.getFocusAncestors()
		if winUser.getWindowThreadProcessID(winUser.getForegroundWindow())[0] != globalVars.appPid:
			# This process is not the foreground process, so bring it to the foreground.
			self.Raise()

	def postPopup(self):
		"""Clean up after a popup dialog or menu.
		This should be called after a dialog or menu was popped up for the user.
		"""
		self.prevFocus = None
		self.prevFocusAncestors = None
		if not winUser.isWindowVisible(winUser.getForegroundWindow()):
			# The current foreground window is invisible, so we want to return to the previous foreground window.
			# Showing and hiding our main window seems to achieve this.
			self.Show()
			self.Hide()

	def showGui(self):
		# The menu pops up at the location of the mouse, which means it pops up at an unpredictable location.
		# Therefore, move the mouse to the center of the screen so that the menu will always pop up there.
		location = api.getDesktopObject().location
		winUser.setCursorPos(*location.center)
		self.sysTrayIcon.onActivate(None)

	def onRevertToSavedConfigurationCommand(self, evt):
		queueHandler.queueFunction(queueHandler.eventQueue, core.resetConfiguration)
		# Translators: Reported when last saved configuration has been applied by using revert to saved configuration option in NVDA menu.
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Configuration applied"))

	def onRevertToDefaultConfigurationCommand(self, evt):
		queueHandler.queueFunction(queueHandler.eventQueue, core.resetConfiguration, factoryDefaults=True)
		queueHandler.queueFunction(
			queueHandler.eventQueue,
			ui.message,
			# Translators: Reported when configuration has been restored to defaults,
			# by using restore configuration to factory defaults item in NVDA menu.
			_("Configuration restored to factory defaults"),
		)

	@blockAction.when(
		blockAction.Context.SECURE_MODE,
		blockAction.Context.RUNNING_LAUNCHER,
	)
	def onSaveConfigurationCommand(self, evt):
		try:
			config.conf.save()
			# Translators: Reported when current configuration has been saved.
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Configuration saved"))
		except PermissionError:
			messageBox(
				# Translators: Message shown when current configuration cannot be saved,
				# such as when running NVDA from a CD.
				_("Could not save configuration - probably read only file system"),
				# Translators: the title of an error message dialog
				_("Error"),
				wx.OK | wx.ICON_ERROR,
			)
		except Exception:
			messageBox(
				# Translators: Message shown when current configuration cannot be saved, for an unknown reason.
				_("Could not save configuration; see the log for more details."),
				# Translators: the title of an error message dialog
				_("Error"),
				wx.OK | wx.ICON_ERROR,
			)

	@blockAction.when(blockAction.Context.MODAL_DIALOG_OPEN)
	def popupSettingsDialog(self, dialog: Type[SettingsDialog], *args, **kwargs):
		self.prePopup()
		try:
			dialog(self, *args, **kwargs).Show()
		except SettingsDialog.MultiInstanceErrorWithDialog as errorWithDialog:
			errorWithDialog.dialog.SetFocus()
		except MultiCategorySettingsDialog.CategoryUnavailableError:
			messageBox(
				# Translators: Message shown when trying to open an unavailable category of a multi category settings dialog.
				# Example: when trying to open touch interaction settings on an unsupported system.
				_("The settings panel you tried to open is unavailable on this system."),
				# Translators: the title of an error message dialog
				_("Error"),
				style=wx.OK | wx.ICON_ERROR,
			)

		self.postPopup()

	if NVDAState._allowDeprecatedAPI():

		def _popupSettingsDialog(self, dialog: Type[SettingsDialog], *args, **kwargs):
			log.warning(
				"_popupSettingsDialog is deprecated, use popupSettingsDialog instead.",
				stack_info=True,
			)
			self.popupSettingsDialog(dialog, *args, **kwargs)

	@blockAction.when(blockAction.Context.SECURE_MODE)
	def onDefaultDictionaryCommand(self, evt):
		self.popupSettingsDialog(DefaultDictionaryDialog)

	@blockAction.when(blockAction.Context.SECURE_MODE)
	def onVoiceDictionaryCommand(self, evt):
		self.popupSettingsDialog(VoiceDictionaryDialog)

	@blockAction.when(blockAction.Context.SECURE_MODE)
	def onTemporaryDictionaryCommand(self, evt):
		self.popupSettingsDialog(TemporaryDictionaryDialog)

	@blockAction.when(blockAction.Context.SECURE_MODE)
	def onExecuteUpdateCommand(self, evt):
		if updateCheck and updateCheck.isPendingUpdate():
			destPath, version, apiVersion, backCompatToAPIVersion = updateCheck.getPendingUpdate()
			from addonHandler import getIncompatibleAddons

			if any(getIncompatibleAddons(apiVersion, backCompatToAPIVersion)):
				confirmUpdateDialog = updateCheck.UpdateAskInstallDialog(
					parent=mainFrame,
					destPath=destPath,
					version=version,
					apiVersion=apiVersion,
					backCompatTo=backCompatToAPIVersion,
				)
				runScriptModalDialog(confirmUpdateDialog, confirmUpdateDialog.callback)
			else:
				updateCheck.executePendingUpdate()

	def evaluateUpdatePendingUpdateMenuItemCommand(self):
		log.warning(
			"MainFrame.evaluateUpdatePendingUpdateMenuItemCommand is deprecated. "
			"Use SysTrayIcon.evaluateUpdatePendingUpdateMenuItemCommand instead.",
			stack_info=True,
		)
		self.sysTrayIcon.evaluateUpdatePendingUpdateMenuItemCommand()

	@blockAction.when(blockAction.Context.MODAL_DIALOG_OPEN)
	def onExitCommand(self, evt):
		if config.conf["general"]["askToExit"]:
			self.prePopup()
			d = ExitDialog(self)
			d.Raise()
			d.Show()
			self.postPopup()
		else:
			if not core.triggerNVDAExit():
				log.error("NVDA already in process of exiting, this indicates a logic error.")

	def onNVDASettingsCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog)

	def onGeneralSettingsCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, GeneralSettingsPanel)

	def onSelectSynthesizerCommand(self, evt):
		self.popupSettingsDialog(SynthesizerSelectionDialog)

	def onSpeechSettingsCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, SpeechSettingsPanel)

	def onSelectBrailleDisplayCommand(self, evt):
		self.popupSettingsDialog(BrailleDisplaySelectionDialog)

	def onBrailleSettingsCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, BrailleSettingsPanel)

	def onAudioSettingsCommand(self, evt: wx.CommandEvent):
		self.popupSettingsDialog(NVDASettingsDialog, AudioPanel)

	def onKeyboardSettingsCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, KeyboardSettingsPanel)

	def onMouseSettingsCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, MouseSettingsPanel)

	def onTouchInteractionCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, TouchInteractionPanel)

	def onReviewCursorCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, ReviewCursorPanel)

	def onInputCompositionCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, InputCompositionPanel)

	def onObjectPresentationCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, ObjectPresentationPanel)

	def onBrowseModeCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, BrowseModePanel)

	def onDocumentFormattingCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, DocumentFormattingPanel)

	def onUwpOcrCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, UwpOcrPanel)

	@blockAction.when(blockAction.Context.SECURE_MODE)
	def onRemoteAccessSettingsCommand(self, evt):
		self.popupSettingsDialog(NVDASettingsDialog, RemoteSettingsPanel)

	@blockAction.when(blockAction.Context.SECURE_MODE)
	def onSpeechSymbolsCommand(self, evt):
		self.popupSettingsDialog(SpeechSymbolsDialog)

	@blockAction.when(blockAction.Context.SECURE_MODE)
	def onInputGesturesCommand(self, evt):
		self.popupSettingsDialog(InputGesturesDialog)

	def onAboutCommand(self, evt):
		# Translators: The title of the dialog to show about info for NVDA.
		MessageDialog(None, versionInfo.aboutMessage, _("About NVDA")).Show()

	@blockAction.when(blockAction.Context.SECURE_MODE)
	def onCheckForUpdateCommand(self, evt):
		updateCheck.UpdateChecker().check()

	def onViewLogCommand(self, evt):
		logViewer.activate()

	def onSpeechViewerEnabled(self, isEnabled):
		# its possible for this to be called after the sysTrayIcon is destroyed if we are exiting NVDA
		if self.sysTrayIcon and self.sysTrayIcon.menu_tools_toggleSpeechViewer:
			self.sysTrayIcon.menu_tools_toggleSpeechViewer.Check(isEnabled)

	@blockAction.when(blockAction.Context.SECURE_MODE)
	def onToggleSpeechViewerCommand(self, evt):
		if not speechViewer.isActive:
			speechViewer.activate()
		else:
			speechViewer.deactivate()

	def onBrailleViewerChangedState(self, created):
		# its possible for this to be called after the sysTrayIcon is destroyed if we are exiting NVDA
		if self.sysTrayIcon and self.sysTrayIcon.menu_tools_toggleBrailleViewer:
			self.sysTrayIcon.menu_tools_toggleBrailleViewer.Check(created)

	@blockAction.when(blockAction.Context.SECURE_MODE)
	def onToggleBrailleViewerCommand(self, evt):
		import brailleViewer

		if brailleViewer.isBrailleViewerActive():
			brailleViewer.destroyBrailleViewer()
		else:
			brailleViewer.createBrailleViewerTool()

	@blockAction.when(blockAction.Context.SECURE_MODE)
	def onPythonConsoleCommand(self, evt):
		import pythonConsole

		if not pythonConsole.consoleUI:
			pythonConsole.initialize()
		pythonConsole.activate()

	if NVDAState._allowDeprecatedAPI():

		def onAddonsManagerCommand(self, evt: wx.MenuEvent):
			log.warning(
				"onAddonsManagerCommand is deprecated, use onAddonStoreCommand instead.",
				stack_info=True,
			)
			self.onAddonStoreCommand(evt)

	@blockAction.when(
		blockAction.Context.SECURE_MODE,
		blockAction.Context.MODAL_DIALOG_OPEN,
		blockAction.Context.WINDOWS_LOCKED,
		blockAction.Context.WINDOWS_STORE_VERSION,
		blockAction.Context.RUNNING_LAUNCHER,
	)
	def onAddonStoreCommand(self, evt: wx.MenuEvent):
		from .addonStoreGui import AddonStoreDialog
		from .addonStoreGui.viewModels.store import AddonStoreVM

		_storeVM = AddonStoreVM()
		_storeVM.refresh()
		self.popupSettingsDialog(AddonStoreDialog, _storeVM)

	@blockAction.when(
		blockAction.Context.SECURE_MODE,
		blockAction.Context.MODAL_DIALOG_OPEN,
		blockAction.Context.WINDOWS_LOCKED,
		blockAction.Context.WINDOWS_STORE_VERSION,
		blockAction.Context.RUNNING_LAUNCHER,
	)
	def onAddonStoreUpdatableCommand(self, evt: wx.MenuEvent | None):
		from .addonStoreGui import AddonStoreDialog
		from .addonStoreGui.viewModels.store import AddonStoreVM
		from addonStore.models.status import _StatusFilterKey

		_storeVM = AddonStoreVM()
		_storeVM.refresh()
		self.popupSettingsDialog(AddonStoreDialog, _storeVM, openToTab=_StatusFilterKey.UPDATE)

	def onReloadPluginsCommand(self, evt):
		import appModuleHandler
		import globalPluginHandler
		from NVDAObjects import NVDAObject

		appModuleHandler.reloadAppModules()
		globalPluginHandler.reloadGlobalPlugins()
		NVDAObject.clearDynamicClassCache()

	@blockAction.when(
		blockAction.Context.SECURE_MODE,
		blockAction.Context.MODAL_DIALOG_OPEN,
	)
	def onCreatePortableCopyCommand(self, evt):
		self.prePopup()
		from . import installerGui

		d = installerGui.PortableCreaterDialog(mainFrame)
		d.Show()
		self.postPopup()

	@blockAction.when(
		blockAction.Context.SECURE_MODE,
		blockAction.Context.MODAL_DIALOG_OPEN,
	)
	def onInstallCommand(self, evt):
		from . import installerGui

		installerGui.showInstallGui()

	_CRFT_INTRO_MESSAGE: str = _(
		# Translators: Explain the COM Registration Fixing tool to users before running
		"Welcome to the COM Registration Fixing tool.\n\n"
		"Installing and uninstalling programs, as well as other events, can damage accessibility entries in the "
		"Windows registry. This can cause previously accessible elements to be presented incorrectly, "
		'or can cause "unknown" or "pane" to be spoken or brailled in some applications or Windows components, '
		"instead of the content you were expecting.\n\n"
		"This tool attempts to fix such common problems. "
		"Note that the tool must access the system registry, which requires administrative privileges.\n\n"
		"Press Continue to run the tool now.",
	)
	"""
	Contains the intro dialog contents for the COM Registration Fixing Tool.
	Used by `gui.MainFrame.onRunCOMRegistrationFixesCommand`.
	"""

	@blockAction.when(
		blockAction.Context.SECURE_MODE,
		blockAction.Context.MODAL_DIALOG_OPEN,
	)
	def onRunCOMRegistrationFixesCommand(self, evt: wx.CommandEvent) -> None:
		"""Manages the interactive running of the COM Registration Fixing Tool.
		Shows a dialog to the user, giving an overview of what is going to happen.
		If the user chooses to continue: runs the tool, and displays a completion dialog.
		Cancels the run attempt if the user fails or declines the UAC prompt.
		"""
		# Translators: The title of various dialogs displayed when using the COM Registration Fixing tool
		genericTitle: str = _("Fix COM Registrations")
		introDialog = _ContinueCancelDialog(
			self,
			genericTitle,
			self._CRFT_INTRO_MESSAGE,
			helpId="RunCOMRegistrationFixingTool",
		)
		response: int = introDialog.ShowModal()
		if response == wx.CANCEL:
			log.debug("Run of COM Registration Fixing Tool canceled before UAC.")
			return
		progressDialog = IndeterminateProgressDialog(
			mainFrame,
			genericTitle,
			# Translators: The message displayed while NVDA is running the COM Registration fixing tool
			_("Please wait while NVDA attempts to fix your system's COM registrations..."),
		)
		error: str | None = None
		try:
			systemUtils.execElevated(config.SLAVE_FILENAME, ["fixCOMRegistrations"])
		except WindowsError as e:
			# 1223 is "The operation was canceled by the user."
			if e.winerror == 1223:
				# Same as if the user selected "no" in the initial dialog.
				log.debug("Run of COM Registration Fixing Tool canceled during UAC.")
				return
			else:
				log.error("Could not execute fixCOMRegistrations command", exc_info=True)
				error = e  # Hold for later display to the user
				return  # Safe because of finally block
		except Exception:
			log.error("Could not execute fixCOMRegistrations command", exc_info=True)
			return  # Safe because of finally block
		finally:  # Clean up the progress dialog, and display any important error to the user before returning
			progressDialog.done()
			del progressDialog
			self.postPopup()
			# If there was a Windows error, inform the user because it may have support value
			if error is not None:
				messageBox(
					_(
						# Translators: message shown to the user on COM Registration Fix fail
						"The COM Registration Fixing Tool was unsuccessful. This Windows "
						"error may provide more information.\n{error}",
					).format(error=error),
					# Translators: The title of a COM Registration Fixing Tool dialog, when the tool has failed
					_("COM Registration Fixing Tool Failed"),
					wx.OK,
				)
		# Display success dialog if there were no errors
		messageBox(
			_(
				# Translators: Message shown when the COM Registration Fixing tool completes.
				"The COM Registration Fixing Tool has completed successfully.\n"
				"It is highly recommended that you restart your computer now, to make sure the changes take full effect.",
			),
			genericTitle,
			wx.OK,
		)

	@blockAction.when(blockAction.Context.MODAL_DIALOG_OPEN)
	def onConfigProfilesCommand(self, evt):
		self.prePopup()
		from .configProfiles import ProfilesDialog

		ProfilesDialog(mainFrame).Show()
		self.postPopup()


class SysTrayIcon(wx.adv.TaskBarIcon):
	def __init__(self, frame: MainFrame):
		super(SysTrayIcon, self).__init__()
		icon = wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO)
		self.SetIcon(icon, versionInfo.name)

		self.menu = wx.Menu()
		menu_preferences = self.preferencesMenu = wx.Menu()
		item = menu_preferences.Append(
			wx.ID_ANY,
			# Translators: The label for the menu item to open NVDA Settings dialog.
			_("&Settings..."),
			# Translators: The description for the menu item to open NVDA Settings dialog.
			_("NVDA settings"),
		)
		self.Bind(wx.EVT_MENU, frame.onNVDASettingsCommand, item)
		if not globalVars.appArgs.secure:
			# Translators: The label for a submenu under NvDA Preferences menu to select speech dictionaries.
			menu_preferences.AppendSubMenu(self._createSpeechDictsSubMenu(frame), _("Speech &dictionaries"))
			# Translators: The label for the menu item to open Punctuation/symbol pronunciation dialog.
			item = menu_preferences.Append(wx.ID_ANY, _("&Punctuation/symbol pronunciation..."))
			self.Bind(wx.EVT_MENU, frame.onSpeechSymbolsCommand, item)
			# Translators: The label for the menu item to open the Input Gestures dialog.
			item = menu_preferences.Append(wx.ID_ANY, _("I&nput gestures..."))
			self.Bind(wx.EVT_MENU, frame.onInputGesturesCommand, item)
		# Translators: The label for Preferences submenu in NVDA menu.
		self.menu.AppendSubMenu(menu_preferences, _("&Preferences"))

		menu_tools = self.toolsMenu = wx.Menu()
		if not globalVars.appArgs.secure:
			# Translators: The label for the menu item to open NVDA Log Viewer.
			item = menu_tools.Append(wx.ID_ANY, _("View &log"))
			self.Bind(wx.EVT_MENU, frame.onViewLogCommand, item)

			item = self.menu_tools_toggleSpeechViewer = menu_tools.AppendCheckItem(
				wx.ID_ANY,
				# Translators: The label for the menu item to toggle Speech Viewer.
				_("&Speech viewer"),
			)
			item.Check(speechViewer.isActive)
			self.Bind(wx.EVT_MENU, frame.onToggleSpeechViewerCommand, item)

			self.menu_tools_toggleBrailleViewer: wx.MenuItem = menu_tools.AppendCheckItem(
				wx.ID_ANY,
				# Translators: The label for the menu item to toggle Braille Viewer.
				_("&Braille viewer"),
			)

			item = self.menu_tools_toggleBrailleViewer
			self.Bind(wx.EVT_MENU, frame.onToggleBrailleViewerCommand, item)
			import brailleViewer

			self.menu_tools_toggleBrailleViewer.Check(brailleViewer.isBrailleViewerActive())
			brailleViewer.postBrailleViewerToolToggledAction.register(frame.onBrailleViewerChangedState)

		if not config.isAppX and NVDAState.shouldWriteToDisk():
			# Translators: The label of a menu item to open the Add-on store
			item = menu_tools.Append(wx.ID_ANY, _("&Add-on store..."))
			self.Bind(wx.EVT_MENU, frame.onAddonStoreCommand, item)

		if not globalVars.appArgs.secure and not config.isAppX:
			# Translators: The label for the menu item to open NVDA Python Console.
			item = menu_tools.Append(wx.ID_ANY, _("&Python console"))
			self.Bind(wx.EVT_MENU, frame.onPythonConsoleCommand, item)

		if not globalVars.appArgs.secure and not config.isAppX and not NVDAState.isRunningAsSource():
			# Translators: The label for the menu item to create a portable copy of NVDA from an installed or another portable version.
			item = menu_tools.Append(wx.ID_ANY, _("&Create portable copy..."))
			self.Bind(wx.EVT_MENU, frame.onCreatePortableCopyCommand, item)
			if not config.isInstalledCopy():
				# Translators: The label for the menu item to install NVDA on the computer.
				item = menu_tools.Append(wx.ID_ANY, _("&Install NVDA..."))
				self.Bind(wx.EVT_MENU, frame.onInstallCommand, item)
			# Translators: The label for the menu item to run the COM registration fix tool
			item = menu_tools.Append(wx.ID_ANY, _("Run COM Registration Fixing tool..."))
			self.Bind(wx.EVT_MENU, frame.onRunCOMRegistrationFixesCommand, item)
		if not config.isAppX:
			# Translators: The label for the menu item to reload plugins.
			item = menu_tools.Append(wx.ID_ANY, _("Reload plugins"))
			self.Bind(wx.EVT_MENU, frame.onReloadPluginsCommand, item)
		# Translators: The label for the Tools submenu in NVDA menu.
		self.menu.AppendSubMenu(menu_tools, _("&Tools"))

		self._appendHelpSubMenu(frame)

		self._appendConfigManagementSection(frame)

		if not globalVars.appArgs.secure:
			self.menu.AppendSeparator()
			# Translators: The label for the menu item to open donate page.
			item = self.menu.Append(wx.ID_ANY, _("&Donate"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(DONATE_URL), item)

		self._appendPendingUpdateSection(frame)

		self.menu.AppendSeparator()
		item = self.menu.Append(
			wx.ID_EXIT,
			# Translators: The label for the menu item to exit NVDA
			_("E&xit"),
			# Translators: The help string for the menu item to exit NVDA
			_("Exit NVDA"),
		)
		self.Bind(wx.EVT_MENU, frame.onExitCommand, item)

		self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.onActivate)
		self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.onActivate)

	def evaluateUpdatePendingUpdateMenuItemCommand(self):
		try:
			self.menu.Remove(self.installPendingUpdateMenuItem)
		except Exception:
			log.debug("Error while removing pending update menu item", exc_info=True)
		if not globalVars.appArgs.secure and updateCheck and updateCheck.isPendingUpdate():
			self.menu.Insert(self.installPendingUpdateMenuItemPos, self.installPendingUpdateMenuItem)

	def onActivate(self, evt):
		self.evaluateUpdatePendingUpdateMenuItemCommand()
		mainFrame.prePopup()
		import appModules.nvda

		if not appModules.nvda.nvdaMenuIaIdentity:
			# The NVDA app module doesn't know how to identify the NVDA menu yet.
			# Signal that the NVDA menu has just been opened.
			appModules.nvda.nvdaMenuIaIdentity = True
		self.PopupMenu(self.menu)
		if appModules.nvda.nvdaMenuIaIdentity is True:
			# The NVDA menu didn't actually appear for some reason.
			appModules.nvda.nvdaMenuIaIdentity = None
		mainFrame.postPopup()

	def _createSpeechDictsSubMenu(self, frame: MainFrame) -> wx.Menu:
		subMenu_speechDicts = wx.Menu()
		item = subMenu_speechDicts.Append(
			wx.ID_ANY,
			# Translators: The label for the menu item to open Default speech dictionary dialog.
			_("&Default dictionary..."),
			# Translators: The help text for the menu item to open Default speech dictionary dialog.
			_("A dialog where you can set default dictionary by adding dictionary entries to the list"),
		)
		self.Bind(wx.EVT_MENU, frame.onDefaultDictionaryCommand, item)
		item = subMenu_speechDicts.Append(
			wx.ID_ANY,
			# Translators: The label for the menu item to open Voice specific speech dictionary dialog.
			_("&Voice dictionary..."),
			_(
				# Translators: The help text for the menu item
				# to open Voice specific speech dictionary dialog.
				"A dialog where you can set voice-specific dictionary by adding"
				" dictionary entries to the list",
			),
		)
		self.Bind(wx.EVT_MENU, frame.onVoiceDictionaryCommand, item)
		item = subMenu_speechDicts.Append(
			wx.ID_ANY,
			# Translators: The label for the menu item to open Temporary speech dictionary dialog.
			_("&Temporary dictionary..."),
			# Translators: The help text for the menu item to open Temporary speech dictionary dialog.
			_("A dialog where you can set temporary dictionary by adding dictionary entries to the edit box"),
		)
		self.Bind(wx.EVT_MENU, frame.onTemporaryDictionaryCommand, item)
		return subMenu_speechDicts

	def _appendConfigManagementSection(self, frame: MainFrame) -> None:
		self.menu.AppendSeparator()
		# Translators: The label for the menu item to open the Configuration Profiles dialog.
		item = self.menu.Append(wx.ID_ANY, _("&Configuration profiles..."))
		self.Bind(wx.EVT_MENU, frame.onConfigProfilesCommand, item)
		item = self.menu.Append(
			wx.ID_ANY,
			# Translators: The label for the menu item to revert to saved configuration.
			_("&Revert to saved configuration"),
			# Translators: The help text for the menu item to revert to saved configuration.
			_("Reset all settings to saved state"),
		)
		self.Bind(wx.EVT_MENU, frame.onRevertToSavedConfigurationCommand, item)
		item = self.menu.Append(
			wx.ID_ANY,
			# Translators: The label for the menu item to reset settings to default settings.
			# Here, default settings means settings that were there when the user first used NVDA.
			_("Reset configuration to &factory defaults"),
			# Translators: The help text for the menu item to reset settings to default settings.
			# Here, default settings means settings that were there when the user first used NVDA.
			_("Reset all settings to default state"),
		)
		self.Bind(wx.EVT_MENU, frame.onRevertToDefaultConfigurationCommand, item)
		if NVDAState.shouldWriteToDisk():
			item = self.menu.Append(
				wx.ID_SAVE,
				# Translators: The label for the menu item to save current settings.
				_("&Save configuration"),
				# Translators: The help text for the menu item to save current settings.
				_("Write the current configuration to nvda.ini"),
			)
			self.Bind(wx.EVT_MENU, frame.onSaveConfigurationCommand, item)

	def _appendHelpSubMenu(self, frame: MainFrame) -> None:
		self.helpMenu = wx.Menu()

		if not globalVars.appArgs.secure:
			# Translators: The label of a menu item to open NVDA user guide.
			item = self.helpMenu.Append(wx.ID_ANY, _("&User Guide"))
			self.Bind(wx.EVT_MENU, lambda evt: self._openDocumentationFile("userGuide.html"), item)
			# Translators: The label of a menu item to open the Commands Quick Reference document.
			item = self.helpMenu.Append(wx.ID_ANY, _("Commands &Quick Reference"))
			self.Bind(wx.EVT_MENU, lambda evt: self._openDocumentationFile("keyCommands.html"), item)
			# Translators: The label for the menu item to open What's New document.
			item = self.helpMenu.Append(wx.ID_ANY, _("What's &new"))
			self.Bind(wx.EVT_MENU, lambda evt: self._openDocumentationFile("changes.html"), item)

			self.helpMenu.AppendSeparator()

			# Translators: The label for the menu item to view the NVDA website
			item = self.helpMenu.Append(wx.ID_ANY, _("NV Access &web site"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(versionInfo.url), item)
			# Translators: The label for the menu item to view the NVDA website's get help section
			item = self.helpMenu.Append(wx.ID_ANY, _("&Help, training and support"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(f"{versionInfo.url}/get-help/"), item)
			# Translators: The label for the menu item to view the NVDA website's get help section
			item = self.helpMenu.Append(wx.ID_ANY, _("NV Access &shop"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(f"{versionInfo.url}/shop/"), item)

			self.helpMenu.AppendSeparator()

			# Translators: The label for the menu item to view the NVDA License.
			item = self.helpMenu.Append(wx.ID_ANY, _("L&icense"))
			self.Bind(wx.EVT_MENU, lambda evt: displayLicense(), item)

			# Translators: The label for the menu item to open NVDA Welcome Dialog.
			item = self.helpMenu.Append(wx.ID_ANY, _("We&lcome dialog..."))
			self.Bind(wx.EVT_MENU, lambda evt: WelcomeDialog.run(), item)

			if updateCheck:
				# Translators: The label of a menu item to manually check for an updated version of NVDA.
				item = self.helpMenu.Append(wx.ID_ANY, _("&Check for update..."))
				self.Bind(wx.EVT_MENU, frame.onCheckForUpdateCommand, item)

		# Translators: The label for the menu item to open About dialog to get information about NVDA.
		item = self.helpMenu.Append(wx.ID_ABOUT, _("&About..."), _("About NVDA"))
		self.Bind(wx.EVT_MENU, frame.onAboutCommand, item)

		# Translators: The label for the Help submenu in NVDA menu.
		self.menu.AppendSubMenu(self.helpMenu, _("&Help"))

	def _openDocumentationFile(self, fileName: str) -> None:
		helpFile = getDocFilePath(fileName)
		if helpFile is None:
			reportNoDocumentation(fileName, useMsgBox=True)
			return
		os.startfile(helpFile)

	def _appendPendingUpdateSection(self, frame: MainFrame) -> None:
		if not globalVars.appArgs.secure and updateCheck:
			# installPendingUpdateMenuItemPos is later toggled based on if an update is available.
			self.installPendingUpdateMenuItemPos = self.menu.GetMenuItemCount()
			item = self.installPendingUpdateMenuItem = self.menu.Append(
				wx.ID_ANY,
				# Translators: The label for the menu item to run a pending update.
				_("Install pending &update"),
				# Translators: The description for the menu item to run a pending update.
				_("Execute a previously downloaded NVDA update"),
			)
			self.Bind(wx.EVT_MENU, frame.onExecuteUpdateCommand, item)


def initialize():
	global mainFrame
	if mainFrame:
		raise RuntimeError("GUI already initialized")
	mainFrame = MainFrame()
	wxLang = core.getWxLangOrNone()
	if wxLang:
		# otherwise the system default will be used
		mainFrame.SetLayoutDirection(wxLang.LayoutDirection)
	wx.GetApp().SetTopWindow(mainFrame)
	import monkeyPatches

	monkeyPatches.applyWxMonkeyPatches(mainFrame, winUser, wx)


def terminate():
	global mainFrame
	mainFrame = None


def showGui():
	wx.CallAfter(mainFrame.showGui)


def runScriptModalDialog(dialog: wx.Dialog, callback: Callable[[int], Any] | None = None):
	"""Run a modal dialog from a script.
	This will not block the caller, but will instead call callback (if provided) with the result from the dialog.
	The dialog will be destroyed once the callback has returned.

	This function is deprecated.
	Use :class:`message.MessageDialog` instead.

	:param dialog: The dialog to show.
	:param callback: The optional callable to call with the result from the dialog.
	"""
	warnings.warn(
		"showScriptModalDialog is deprecated. Use an instance of message.MessageDialog and wx.CallAfter instead.",
		DeprecationWarning,
	)

	def run():
		res = displayDialogAsModal(dialog)
		if callback:
			callback(res)
		dialog.Destroy()

	wx.CallAfter(run)


class IndeterminateProgressDialog(wx.ProgressDialog):
	def __init__(self, parent: wx.Window, title: str, message: str):
		super().__init__(title, message, parent=parent)
		self._speechCounter = -1
		self.timer = wx.PyTimer(self.Pulse)
		self.timer.Start(1000)
		self.CentreOnScreen()
		self.Raise()

	def Pulse(self):
		super(IndeterminateProgressDialog, self).Pulse()
		# We want progress to be spoken on the first pulse and every 10 pulses thereafter.
		# Therefore, cycle from 0 to 9 inclusive.
		self._speechCounter = (self._speechCounter + 1) % 10
		pbConf = config.conf["presentation"]["progressBarUpdates"]
		if pbConf["progressBarOutputMode"] == "off":
			return
		if not pbConf["reportBackgroundProgressBars"] and not self.IsActive():
			return
		if pbConf["progressBarOutputMode"] in ("beep", "both"):
			tones.beep(440, 40)
		if pbConf["progressBarOutputMode"] in ("speak", "both") and self._speechCounter == 0:
			# Translators: Announced periodically to indicate progress for an indeterminate progress bar.
			speech.speakMessage(_("Please wait"))

	def IsActive(self):
		# 4714: In wxPython 3, ProgressDialog.IsActive always seems to return False.
		return winUser.isDescendantWindow(winUser.getForegroundWindow(), self.Handle)

	def done(self):
		self.timer.Stop()
		pbConf = config.conf["presentation"]["progressBarUpdates"]
		if pbConf["progressBarOutputMode"] in ("beep", "both") and (
			pbConf["reportBackgroundProgressBars"] or self.IsActive()
		):
			tones.beep(1760, 40)
		self.Hide()
		self.Destroy()


def shouldConfigProfileTriggersBeSuspended():
	"""Determine whether configuration profile triggers should be suspended in relation to NVDA's GUI.
	For NVDA configuration dialogs, the configuration should remain the same as it was before the GUI was popped up
	so the user can change settings in the correct profile.
	Top-level windows that require this behavior should have a C{shouldSuspendConfigProfileTriggers} attribute set to C{True}.
	Because these dialogs are often opened via the NVDA menu, this applies to the NVDA menu as well.
	"""
	if winUser.getGUIThreadInfo(ctypes.windll.kernel32.GetCurrentThreadId()).flags & 0x00000010:
		# The NVDA menu is active.
		return True
	for window in wx.GetTopLevelWindows():
		if window.IsShown() and getattr(window, "shouldSuspendConfigProfileTriggers", False):
			return True
	return False


class NonReEntrantTimer(wx.Timer):
	"""
	Before WXPython 4, wx.Timer was nonre-entrant,
	meaning that if code within its callback pumped messages (E.g. called wx.Yield) and this timer was ready to fire again,
	the timer would not fire until the first callback had completed.
	However, in WXPython 4, wx.Timer is now re-entrant.
	Code in NVDA is not written to handle re-entrant timers, so this class provides a Timer with the old behaviour.
	This should be used in place of wx.Timer and wx.PyTimer where the callback will directly or indirectly call wx.Yield or some how process the Windows window message queue.
	For example, NVDA's core pump or other timers that run in NVDA's main thread.
	Timers on braille display drivers for key detection don't need to use this as they only queue gestures rather than actually executing them.
	"""

	def __init__(self, run=None):
		if run is not None:
			self.run = run
		self._inNotify = False
		super(NonReEntrantTimer, self).__init__()

	def run(self):
		"""Subclasses can override or specify in constructor."""
		raise NotImplementedError

	def Notify(self):
		if self._inNotify:
			return
		self._inNotify = True
		try:
			self.run()
		finally:
			self._inNotify = False


def _isDebug():
	return config.conf["debugLog"]["gui"]
