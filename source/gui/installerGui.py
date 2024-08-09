# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2011-2023 NV Access Limited, Babbage B.v., Cyrille Bougot, Julien Cochuyt, Accessolutions,
# Bill Dengler, Joseph Lee, Takuya Nishimoto

import os
import subprocess
import sys

import winUser
import wx
import config
import core
import globalVars
import installer
from logHandler import log
import gui
from gui import guiHelper
import gui.contextHelp
from gui.dpiScalingHelper import DpiScalingHelperMixinWithoutInit
import systemUtils
import ui
from NVDAState import WritePaths
from .message import displayDialogAsModal


def _canPortableConfigBeCopied() -> bool:
	# In some cases even though user requested to copy config from the portable copy during installation
	# it should not be done.
	if globalVars.appArgs.launcher:
		# Normally when running from the launcher
		# and configPath is not overridden by the user copying config during installation is rather pointless
		# as we would  copy it into itself.
		# However, if a user wants to run the launcher with a custom configPath,
		# it is likely that he wants to copy that configuration when installing.
		return WritePaths.configDir != config.getUserDefaultConfigPath(useInstalledPathIfExists=True)
	else:
		# For portable copies we want to avoid copying the configuration to itself,
		# so return True only if the configPath
		# does not point to the config of the installed copy in appdata.
		confPath = config.getInstalledUserConfigPath()
		if confPath and confPath == WritePaths.configDir:
			return False
		return True


def doInstall(
	createDesktopShortcut=True,
	startOnLogon=True,
	isUpdate=False,
	copyPortableConfig=False,
	silent=False,
	startAfterInstall=True,
):
	progressDialog = gui.IndeterminateProgressDialog(
		gui.mainFrame,
		# Translators: The title of the dialog presented while NVDA is being updated.
		_("Updating NVDA")
		if isUpdate
		# Translators: The title of the dialog presented while NVDA is being installed.
		else _("Installing NVDA"),
		# Translators: The message displayed while NVDA is being updated.
		_("Please wait while your previous installation of NVDA is being updated.")
		if isUpdate
		# Translators: The message displayed while NVDA is being installed.
		else _("Please wait while NVDA is being installed"),
	)
	try:
		res = systemUtils.execElevated(
			config.SLAVE_FILENAME,
			["install", str(int(createDesktopShortcut)), str(int(startOnLogon))],
			wait=True,
			handleAlreadyElevated=True,
		)
		if res == 2:
			raise installer.RetriableFailure
		if copyPortableConfig:
			installedUserConfigPath = config.getInstalledUserConfigPath()
			if installedUserConfigPath:
				if _canPortableConfigBeCopied():
					systemUtils.ExecAndPump(installer.copyUserConfig, installedUserConfigPath)
	except Exception as e:
		res = e
		log.error("Failed to execute installer", exc_info=True)
	progressDialog.done()
	del progressDialog
	if isinstance(res, installer.RetriableFailure):
		message = _(
			# Translators: a message dialog asking to retry or cancel when NVDA install fails
			"The installation is unable to remove or overwrite a file. "
			"Another copy of NVDA may be running on another logged-on user account. "
			"Please make sure all installed copies of NVDA are shut down and try the installation again.",
		)
		# Translators: the title of a retry cancel dialog when NVDA installation fails
		title = _("File in Use")
		if winUser.MessageBox(None, message, title, winUser.MB_RETRYCANCEL) == winUser.IDRETRY:
			return doInstall(
				createDesktopShortcut=createDesktopShortcut,
				startOnLogon=startOnLogon,
				copyPortableConfig=copyPortableConfig,
				isUpdate=isUpdate,
				silent=silent,
				startAfterInstall=startAfterInstall,
			)
	if res != 0:
		log.error("Installation failed: %s" % res)
		gui.messageBox(
			# Translators: The message displayed when an error occurs during installation of NVDA.
			_("The installation of NVDA failed. Please check the Log Viewer for more information."),
			# Translators: The title of a dialog presented when an error occurs.
			_("Error"),
			wx.OK | wx.ICON_ERROR,
		)
		return
	if not silent:
		msg = (
			# Translators: The message displayed when NVDA has been successfully installed.
			_("Successfully installed NVDA. ")
			if not isUpdate
			# Translators: The message displayed when NVDA has been successfully updated.
			else _("Successfully updated your installation of NVDA. ")
		)
		gui.messageBox(
			# Translators: The message displayed to the user after NVDA is installed
			# and the installed copy is about to be started.
			msg + _("Please press OK to start the installed copy."),
			# Translators: The title of a dialog presented to indicate a successful operation.
			_("Success"),
		)

	newNVDA = None
	if startAfterInstall:
		newNVDA = core.NewNVDAInstance(
			filePath=os.path.join(installer.defaultInstallPath, "nvda.exe"),
			parameters=_generate_executionParameters(),
		)
	if not core.triggerNVDAExit(newNVDA):
		log.error("NVDA already in process of exiting, this indicates a logic error.")


def _generate_executionParameters() -> str:
	executeParams: list[str] = []
	if globalVars.appArgs.disableAddons:
		executeParams.append("--disable-addons")
	# pass the config path to the new instance, so that if a custom config path is in use, it will be
	# inherited. We can't rely on WritePaths.configDir or appArgs.configPath here, as they could be set to
	# the default path, which may be a temporary directory, so we must sniff sys.argv.
	# Read sys.argv backwards, since the last instance of a CLI option takes effect.
	# We start from len-2 as the -c option must have a value, so it is guaranteed to take up 2 items in argv.
	for i in range(len(sys.argv) - 2, 0, -1):
		if sys.argv[i] in ("-c", "--config-path"):
			# We don't absolutise -c here because if it was provided by a previous copy of NVDA this will
			# have already been done, and if it was provided by the user absolutising it now will result in
			# it being in a temporary directory, which is almost certainly not what they want.
			executeParams.extend(("--config-path", sys.argv[i + 1]))
			break
	return subprocess.list2cmdline(executeParams)


def doSilentInstall(
	copyPortableConfig=False,
	startAfterInstall=True,
):
	prevInstall = installer.comparePreviousInstall() is not None
	startOnLogon = globalVars.appArgs.enableStartOnLogon
	if startOnLogon is None:
		startOnLogon = config.getStartOnLogonScreen() if prevInstall else True
	doInstall(
		createDesktopShortcut=installer.isDesktopShortcutInstalled() if prevInstall else True,
		startOnLogon=startOnLogon,
		isUpdate=prevInstall,
		copyPortableConfig=copyPortableConfig,
		silent=True,
		startAfterInstall=startAfterInstall,
	)


class InstallerDialog(
	DpiScalingHelperMixinWithoutInit,
	gui.contextHelp.ContextHelpMixin,
	wx.Dialog,  # wxPython does not seem to call base class initializer, put last in MRO
):
	helpId = "InstallingNVDA"

	def __init__(self, parent, isUpdate):
		self.isUpdate = isUpdate
		self.textWrapWidth = 600
		# Translators: The title of the Install NVDA dialog.
		super().__init__(parent, title=_("Install NVDA"))

		import addonHandler
		from addonStore.models.version import (
			getAddonCompatibilityConfirmationMessage,
			getAddonCompatibilityMessage,
		)

		shouldAskAboutAddons = any(
			addonHandler.getIncompatibleAddons(
				# the defaults from the installer are ok. We are testing against the running version.
			),
		)

		mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		# Translators: An informational message in the Install NVDA dialog.
		msg = _("To install NVDA to your hard drive, please press the Continue button.")
		if self.isUpdate:
			msg += " " + _(
				# Translators: An informational message in the Install NVDA dialog.
				"A previous copy of NVDA has been found on your system. This copy will be updated.",
			)
			if not os.path.isdir(installer.defaultInstallPath):
				msg += " " + _(
					# Translators: a message in the installer telling the user NVDA is now located in a different place.
					"The installation path for NVDA has changed. it will now  be installed in {path}",
				).format(path=installer.defaultInstallPath)
		if shouldAskAboutAddons:
			msg += "\n\n" + getAddonCompatibilityMessage()

		text = sHelper.addItem(wx.StaticText(self, label=msg))
		text.Wrap(self.scaleSize(self.textWrapWidth))
		if shouldAskAboutAddons:
			self.confirmationCheckbox = sHelper.addItem(
				wx.CheckBox(
					self,
					label=getAddonCompatibilityConfirmationMessage(),
				),
			)
			self.bindHelpEvent("InstallWithIncompatibleAddons", self.confirmationCheckbox)
			self.confirmationCheckbox.SetFocus()

		# Translators: The label for a group box containing the NVDA installation dialog options.
		optionsLabel = _("Options")
		optionsSizer = sHelper.addItem(wx.StaticBoxSizer(wx.VERTICAL, self, label=optionsLabel))
		optionsHelper = guiHelper.BoxSizerHelper(self, sizer=optionsSizer)
		optionsBox = optionsSizer.GetStaticBox()

		# Translators: The label of a checkbox option in the Install NVDA dialog.
		startOnLogonText = _("Use NVDA during sign-in")
		self.startOnLogonCheckbox = optionsHelper.addItem(wx.CheckBox(optionsBox, label=startOnLogonText))
		self.bindHelpEvent("StartAtWindowsLogon", self.startOnLogonCheckbox)
		if globalVars.appArgs.enableStartOnLogon is not None:
			self.startOnLogonCheckbox.Value = globalVars.appArgs.enableStartOnLogon
		else:
			self.startOnLogonCheckbox.Value = config.getStartOnLogonScreen() if self.isUpdate else True

		shortcutIsPrevInstalled = installer.isDesktopShortcutInstalled()
		if self.isUpdate and shortcutIsPrevInstalled:
			# Translators: The label of a checkbox option in the Install NVDA dialog.
			keepShortCutText = _("&Keep existing desktop shortcut")
			keepShortCutBox = wx.CheckBox(optionsBox, label=keepShortCutText)
			self.createDesktopShortcutCheckbox = optionsHelper.addItem(keepShortCutBox)
		else:
			# Translators: The label of the option to create a desktop shortcut in the Install NVDA dialog.
			# If the shortcut key has been changed for this locale,
			# this change must also be reflected here.
			createShortcutText = _("Create &desktop icon and shortcut key (control+alt+n)")
			createShortcutBox = wx.CheckBox(optionsBox, label=createShortcutText)
			self.createDesktopShortcutCheckbox = optionsHelper.addItem(createShortcutBox)
		self.bindHelpEvent("CreateDesktopShortcut", self.createDesktopShortcutCheckbox)
		self.createDesktopShortcutCheckbox.Value = shortcutIsPrevInstalled if self.isUpdate else True

		# Translators: The label of a checkbox option in the Install NVDA dialog.
		createPortableText = _("Copy &portable configuration to current user account")
		createPortableBox = wx.CheckBox(optionsBox, label=createPortableText)
		self.copyPortableConfigCheckbox = optionsHelper.addItem(createPortableBox)
		self.bindHelpEvent("CopyPortableConfigurationToCurrentUserAccount", self.copyPortableConfigCheckbox)
		self.copyPortableConfigCheckbox.Value = (
			bool(globalVars.appArgs.copyPortableConfig) and _canPortableConfigBeCopied()
		)
		self.copyPortableConfigCheckbox.Enable(_canPortableConfigBeCopied())

		bHelper = sHelper.addDialogDismissButtons(guiHelper.ButtonHelper(wx.HORIZONTAL))
		if shouldAskAboutAddons:
			# Translators: The label of a button to launch the add-on compatibility review dialog.
			reviewAddonButton = bHelper.addButton(self, label=_("&Review add-ons..."))
			self.bindHelpEvent("InstallWithIncompatibleAddons", reviewAddonButton)
			reviewAddonButton.Bind(wx.EVT_BUTTON, self.onReviewAddons)

		# Translators: The label of a button to continue with the operation.
		continueButton = bHelper.addButton(self, label=_("&Continue"), id=wx.ID_OK)
		continueButton.SetDefault()
		continueButton.Bind(wx.EVT_BUTTON, self.onInstall)
		if shouldAskAboutAddons:
			self.confirmationCheckbox.Bind(
				wx.EVT_CHECKBOX,
				lambda evt: continueButton.Enable(not continueButton.Enabled),
			)
			continueButton.Enable(False)

		bHelper.addButton(self, id=wx.ID_CANCEL)
		# If we bind this using button.Bind, it fails to trigger when the dialog is closed.
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.CentreOnScreen()

	def onInstall(self, evt):
		self.Hide()
		doInstall(
			createDesktopShortcut=self.createDesktopShortcutCheckbox.Value,
			startOnLogon=self.startOnLogonCheckbox.Value,
			copyPortableConfig=self.copyPortableConfigCheckbox.Value,
			isUpdate=self.isUpdate,
		)
		wx.GetApp().ScheduleForDestruction(self)

	def onCancel(self, evt):
		self.Destroy()

	def onReviewAddons(self, evt):
		from gui import addonGui

		incompatibleAddons = addonGui.IncompatibleAddonsDialog(
			parent=self,
			# the defaults from the installer are fine. We are testing against the running version.
		)
		displayDialogAsModal(incompatibleAddons)


class InstallingOverNewerVersionDialog(
	DpiScalingHelperMixinWithoutInit,
	gui.contextHelp.ContextHelpMixin,
	wx.Dialog,  # wxPython does not seem to call base class initializer, put last in MRO
):
	helpId = "InstallingNVDA"

	def __init__(self):
		# Translators: The title of a warning dialog.
		super().__init__(gui.mainFrame, title=_("Warning"))

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentSizer = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		text = wx.StaticText(
			self,
			label=_(
				# Translators: A warning presented when the user attempts to downgrade NVDA
				# to an older version.
				"You are attempting to install an earlier version of NVDA "
				"than the version currently installed. "
				"If you really wish to revert to an earlier version, "
				"you should first cancel this installation "
				"and completely uninstall NVDA before installing the earlier version.",
			),
		)
		text.Wrap(self.scaleSize(600))
		contentSizer.addItem(text)

		buttonHelper = guiHelper.ButtonHelper(orientation=wx.HORIZONTAL)
		buttonHelper.addButton(
			parent=self,
			id=wx.ID_OK,
			# Translators: The label of a button to proceed with installation,
			# even though this is not recommended.
			label=_("&Proceed with installation (not recommended)"),
		)
		cancelButton = buttonHelper.addButton(
			parent=self,
			id=wx.ID_CANCEL,
		)
		contentSizer.addDialogDismissButtons(buttonHelper)

		cancelButton.SetFocus()
		mainSizer.Add(contentSizer.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		self.CentreOnScreen()


def showInstallGui():
	gui.mainFrame.prePopup()
	previous = installer.comparePreviousInstall()
	if previous is not None and previous > 0:
		# The existing installation is newer, which means this will be a downgrade.
		d = InstallingOverNewerVersionDialog()
		with d:
			if d.ShowModal() == wx.ID_CANCEL:
				gui.mainFrame.postPopup()
				return
	InstallerDialog(gui.mainFrame, previous is not None).Show()
	gui.mainFrame.postPopup()


def _nvdaExistsInDir(directory: str) -> bool:
	return os.path.exists(os.path.join(directory, "nvda.exe"))


def _warnAndConfirmForNonEmptyDirectory(portableDirectory: str) -> bool:
	"""
	Display a warning message if the specified directory is not empty.
	:param portableDirectory: The directory to check.
	:return: True if the user wants to continue, False if the user wants to cancel.
	"""
	if not os.path.exists(portableDirectory):
		# The directory does not exist, so we can proceed.
		return True
	if not any(os.scandir(portableDirectory)):
		# The directory is empty, so we can proceed.
		return True
	if _nvdaExistsInDir(portableDirectory):
		return wx.YES == gui.messageBox(
			_(
				# Translators: The message displayed when the user has specified a destination directory
				# that already has a portable copy in the Create Portable NVDA dialog.
				"A portable copy already exists in the directory '{portableDirectory}'. "
				"Do you want to update it?",
			).format(portableDirectory=portableDirectory),
			# Translators: The title of a dialog presented when the user has specified a destination directory
			# that already has a portable copy in the Create Portable NVDA dialog.
			_("Portable Copy Exists"),
			wx.YES_NO | wx.ICON_QUESTION,
		)
	return wx.YES == gui.messageBox(
		_(
			# Translators: The message displayed when the user has specified a destination directory
			# that already exists in the Create Portable NVDA dialog.
			"The specified directory '{portableDirectory}' is not empty. "
			"Proceeding will delete and replace existing files in the directory. "
			"Do you want to overwrite the contents of this folder? ",
		).format(portableDirectory=portableDirectory),
		# Translators: The title of a dialog presented when the user has specified a destination directory
		# that already exists in the Create Portable NVDA dialog.
		_("Directory Exists"),
		wx.YES_NO | wx.ICON_QUESTION,
	)


def _getUniqueNewPortableDirectory(basePath: str) -> str:
	"""
	Generate a new directory name for a portable copy of NVDA.
	:param basePath: The base path to use.
	:return: A new directory name.
	"""
	newPortableDirectory = os.path.join(basePath, "NVDA")
	i = 1
	while os.path.exists(newPortableDirectory):
		newPortableDirectory = os.path.join(basePath, f"NVDA_{i}")
		i += 1
	return newPortableDirectory


class PortableCreaterDialog(
	gui.contextHelp.ContextHelpMixin,
	wx.Dialog,  # wxPython does not seem to call base class initializer, put last in MRO
):
	helpId = "CreatePortableCopy"

	def __init__(self, parent):
		# Translators: The title of the Create Portable NVDA dialog.
		super().__init__(parent, title=_("Create Portable NVDA"))
		mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		dialogCaption = _(
			# Translators: An informational message displayed in the Create Portable NVDA dialog.
			"To create a portable copy of NVDA, please select the path and other options and then press Continue",
		)
		sHelper.addItem(wx.StaticText(self, label=dialogCaption))

		# Translators: The label of a grouping containing controls to select the destination directory
		# in the Create Portable NVDA dialog.
		directoryGroupText = _("Portable directory:")
		groupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=directoryGroupText)
		groupHelper = sHelper.addItem(guiHelper.BoxSizerHelper(self, sizer=groupSizer))
		groupBox = groupSizer.GetStaticBox()
		# Translators: The label of a button to browse for a directory.
		browseText = _("Browse...")
		# Translators: The title of the dialog presented when browsing for the
		# destination directory when creating a portable copy of NVDA.
		dirDialogTitle = _("Select portable directory")
		directoryPathHelper = guiHelper.PathSelectionHelper(groupBox, browseText, dirDialogTitle)
		directoryEntryControl = groupHelper.addItem(directoryPathHelper)
		self.portableDirectoryEdit = directoryEntryControl.pathControl
		if globalVars.appArgs.portablePath:
			self.portableDirectoryEdit.Value = globalVars.appArgs.portablePath

		# Translators: The label of a checkbox option in the Create Portable NVDA dialog.
		newFolderText = _("Create a &new folder for the portable copy")
		self.newFolderCheckBox = sHelper.addItem(wx.CheckBox(self, label=newFolderText))
		self.newFolderCheckBox.Value = True

		# Translators: The label of a checkbox option in the Create Portable NVDA dialog.
		copyConfText = _("Copy current &user configuration")
		self.copyUserConfigCheckbox = sHelper.addItem(wx.CheckBox(self, label=copyConfText))
		self.copyUserConfigCheckbox.Value = False
		if globalVars.appArgs.launcher:
			self.copyUserConfigCheckbox.Disable()
		# Translators: The label of a checkbox option in the Create Portable NVDA dialog.
		startAfterCreateText = _("&Start the new portable copy after creation")
		self.startAfterCreateCheckbox = sHelper.addItem(wx.CheckBox(self, label=startAfterCreateText))
		self.startAfterCreateCheckbox.Value = False

		bHelper = sHelper.addDialogDismissButtons(guiHelper.ButtonHelper(wx.HORIZONTAL), separated=True)

		continueButton = bHelper.addButton(self, label=_("&Continue"), id=wx.ID_OK)
		continueButton.SetDefault()
		continueButton.Bind(wx.EVT_BUTTON, self.onCreatePortable)

		bHelper.addButton(self, id=wx.ID_CANCEL)
		# If we bind this using button.Bind, it fails to trigger when the dialog is closed.
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.CentreOnScreen()

	def onCreatePortable(self, evt):
		if not self.portableDirectoryEdit.Value:
			gui.messageBox(
				# Translators: The message displayed when the user has not specified a destination directory
				# in the Create Portable NVDA dialog.
				_("Please specify a directory in which to create the portable copy."),
				# Translators: the title of an error dialog.
				_("Error"),
				wx.OK | wx.ICON_ERROR,
			)
			return
		expandedPortableDirectory = os.path.expandvars(self.portableDirectoryEdit.Value)
		if not os.path.isabs(expandedPortableDirectory):
			gui.messageBox(
				_(
					# Translators: The message displayed when the user has not specified an absolute destination directory
					# in the Create Portable NVDA dialog.
					"Please specify the absolute path where the portable copy should be created. "
					"It may include system variables (%temp%, %homepath%, etc.).",
				),
				# Translators: The message title displayed when the user has not specified an absolute
				# destination directory in the Create Portable NVDA dialog.
				_("Error"),
				wx.OK | wx.ICON_ERROR,
			)
			return
		# isabs determines if the path is absolute, with or without a drive letter. abspath adds any missing initial
		# components to that path to make it absolute from other contexts, by adding a drive letter/share path if
		# needed. The OS's idea of the current drive is used, as in os.getcwd(). (#14681)
		expandedPortableDirectory = os.path.abspath(expandedPortableDirectory)
		if self.newFolderCheckBox.Value:
			expandedPortableDirectory = _getUniqueNewPortableDirectory(expandedPortableDirectory)

		# Warn here so that users can update the directory
		if not _warnAndConfirmForNonEmptyDirectory(expandedPortableDirectory):
			return

		self.Hide()
		doCreatePortable(
			expandedPortableDirectory,
			copyUserConfig=self.copyUserConfigCheckbox.Value,
			silent=False,
			startAfterCreate=self.startAfterCreateCheckbox.Value,
			warnForNonEmptyDirectory=False,
		)
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()


def doCreatePortable(
	portableDirectory: str,
	copyUserConfig: bool = False,
	silent: bool = False,
	startAfterCreate: bool = False,
	warnForNonEmptyDirectory: bool = True,
) -> None:
	"""
	Create a portable copy of NVDA.
	:param portableDirectory: The directory in which to create the portable copy.
	:param copyUserConfig: Whether to copy the current user configuration.
	:param silent: Whether to suppress messages.
	:param startAfterCreate: Whether to start the new portable copy after creation.
	:param warnForNonEmptyDirectory: Whether to warn if the destination directory is not empty.
	"""
	if warnForNonEmptyDirectory and not _warnAndConfirmForNonEmptyDirectory(portableDirectory):
		# Translators: The message displayed when the user cancels the creation of a portable copy of NVDA.
		ui.message(_("Portable copy creation cancelled."))
		return
	d = gui.IndeterminateProgressDialog(
		gui.mainFrame,
		# Translators: The title of the dialog presented while a portable copy of NVDA is being created.
		_("Creating Portable Copy"),
		# Translators: The message displayed while a portable copy of NVDA is being created.
		_("Please wait while a portable copy of NVDA is created."),
	)
	try:
		systemUtils.ExecAndPump(installer.createPortableCopy, portableDirectory, copyUserConfig)
	except Exception as e:
		log.error("Failed to create portable copy", exc_info=True)
		d.done()
		if isinstance(e, installer.RetriableFailure):
			# Translators: a message dialog asking to retry or cancel when NVDA portable copy creation fails
			message = _("NVDA is unable to remove or overwrite a file.")
			# Translators: the title of a retry cancel dialog when NVDA portable copy creation  fails
			title = _("File in Use")
			if winUser.MessageBox(None, message, title, winUser.MB_RETRYCANCEL) == winUser.IDRETRY:
				return doCreatePortable(portableDirectory, copyUserConfig, silent, startAfterCreate)
		gui.messageBox(
			# Translators: The message displayed when an error occurs while creating a portable copy of NVDA.
			# {error} will be replaced with the specific error message.
			_("Failed to create portable copy: {error}.").format(error=e),
			# Translators: Title of an error dialog shown when an error occurs while creating a portable copy of NVDA.
			_("Error"),
			wx.OK | wx.ICON_ERROR,
		)
		return
	d.done()
	if not silent:
		gui.messageBox(
			# Translators: The message displayed when a portable copy of NVDA has been successfully created.
			# {dir} will be replaced with the destination directory.
			_("Successfully created a portable copy of NVDA at {dir}").format(dir=portableDirectory),
			# Translators: Title of a dialog shown when a portable copy of NVDA is created.
			_("Success"),
		)
	if silent or startAfterCreate:
		newNVDA = None
		if startAfterCreate:
			newNVDA = core.NewNVDAInstance(
				filePath=os.path.join(portableDirectory, "nvda.exe"),
				parameters=_generate_executionParameters(),
			)
		if not core.triggerNVDAExit(newNVDA):
			log.error("NVDA already in process of exiting, this indicates a logic error.")
