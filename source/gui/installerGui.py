#gui/installerGui.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011-2018 NV Access Limited, Babbage B.v.

import os
import ctypes

import buildVersion
import shellapi
import winUser
import wx
import config
import globalVars
import versionInfo
import installer
from logHandler import log
import gui
from gui import guiHelper
from gui.dpiScalingHelper import DpiScalingHelperMixin
import tones
import systemUtils

def doInstall(createDesktopShortcut,startOnLogon,copyPortableConfig,isUpdate,silent=False,startAfterInstall=True):
	progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame,
		# Translators: The title of the dialog presented while NVDA is being updated.
		_("Updating NVDA") if isUpdate
		# Translators: The title of the dialog presented while NVDA is being installed.
		else _("Installing NVDA"),
		# Translators: The message displayed while NVDA is being updated.
		_("Please wait while your previous installation of NVDA is being updated.") if isUpdate
		# Translators: The message displayed while NVDA is being installed.
		else _("Please wait while NVDA is being installed"))
	try:
		res = systemUtils.execElevated(
			config.SLAVE_FILENAME,
			["install", str(int(createDesktopShortcut)), str(int(startOnLogon))],
			wait=True,
			handleAlreadyElevated=True
		)
		if res==2: raise installer.RetriableFailure
		if copyPortableConfig:
			installedUserConfigPath=config.getInstalledUserConfigPath()
			if installedUserConfigPath:
				gui.ExecAndPump(installer.copyUserConfig,installedUserConfigPath)
	except Exception as e:
		res=e
		log.error("Failed to execute installer",exc_info=True)
	progressDialog.done()
	del progressDialog
	if isinstance(res,installer.RetriableFailure):
		# Translators: a message dialog asking to retry or cancel when NVDA install fails
		message=_("The installation is unable to remove or overwrite a file. Another copy of NVDA may be running on another logged-on user account. Please make sure all installed copies of NVDA are shut down and try the installation again.")
		# Translators: the title of a retry cancel dialog when NVDA installation fails
		title=_("File in Use")
		if winUser.MessageBox(None,message,title,winUser.MB_RETRYCANCEL)==winUser.IDRETRY:
			return doInstall(createDesktopShortcut,startOnLogon,copyPortableConfig,isUpdate,silent,startAfterInstall)
	if res!=0:
		log.error("Installation failed: %s"%res)
		# Translators: The message displayed when an error occurs during installation of NVDA.
		gui.messageBox(_("The installation of NVDA failed. Please check the Log Viewer for more information."),
			# Translators: The title of a dialog presented when an error occurs.
			_("Error"),
			wx.OK | wx.ICON_ERROR)
		return
	if not silent:
		msg = (
			# Translators: The message displayed when NVDA has been successfully installed.
			_("Successfully installed NVDA. ") if not isUpdate
			# Translators: The message displayed when NVDA has been successfully updated.
			else _("Successfully updated your installation of NVDA. "))
		# Translators: The message displayed to the user after NVDA is installed
		# and the installed copy is about to be started.
		gui.messageBox(msg+_("Please press OK to start the installed copy."),
			# Translators: The title of a dialog presented to indicate a successful operation.
			_("Success"))
	if startAfterInstall:
		# #4475: ensure that the first window of the new process is not hidden by providing SW_SHOWNORMAL  
		shellapi.ShellExecute(
			None,
			None,
			os.path.join(installer.defaultInstallPath,'nvda.exe'),
			None,
			None,
			winUser.SW_SHOWNORMAL
		)
	else:
		wx.GetApp().ExitMainLoop()

def doSilentInstall(startAfterInstall=True):
	prevInstall=installer.comparePreviousInstall() is not None
	startOnLogon=globalVars.appArgs.enableStartOnLogon
	if startOnLogon is None:
		startOnLogon=config.getStartOnLogonScreen() if prevInstall else True
	doInstall(
		installer.isDesktopShortcutInstalled() if prevInstall else True,
		startOnLogon,
		False,
		prevInstall,
		silent=True,
		startAfterInstall=startAfterInstall
	)

class InstallerDialog(wx.Dialog, DpiScalingHelperMixin):

	def __init__(self, parent, isUpdate):
		self.isUpdate=isUpdate
		self.textWrapWidth = 600
		# Translators: The title of the Install NVDA dialog.
		wx.Dialog.__init__(self, parent, title=_("Install NVDA"))
		DpiScalingHelperMixin.__init__(self, self.GetHandle())

		import addonHandler
		shouldAskAboutAddons = any(addonHandler.getIncompatibleAddons(
			# the defaults from the installer are ok. We are testing against the running version.
		))

		mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		# Translators: An informational message in the Install NVDA dialog.
		msg=_("To install NVDA to your hard drive, please press the Continue button.")
		if self.isUpdate:
			# Translators: An informational message in the Install NVDA dialog.
			msg+=" "+_("A previous copy of NVDA has been found on your system. This copy will be updated.") 
			if not os.path.isdir(installer.defaultInstallPath):
				# Translators: a message in the installer telling the user NVDA is now located in a different place.
				msg+=" "+_("The installation path for NVDA has changed. it will now  be installed in {path}").format(path=installer.defaultInstallPath)
		if shouldAskAboutAddons:
			# Translators: A message in the installer to let the user know that some addons are not compatible.
			msg+=_(
				"\n\n"
				"However, your NVDA configuration contains add-ons that are incompatible with this version of NVDA. "
				"These add-ons will be disabled after installation. If you rely on these add-ons, "
				"please review the list to decide whether to continue with the installation"
			)

		text = sHelper.addItem(wx.StaticText(self, label=msg))
		text.Wrap(self.scaleSize(self.textWrapWidth))
		if shouldAskAboutAddons:
			self.confirmationCheckbox = sHelper.addItem(wx.CheckBox(
					self,
					# Translators: A message to confirm that the user understands that addons that have not been reviewed and made
					# available, will be disabled after installation.
					label=_("I understand that these incompatible add-ons will be disabled")
				))
			self.confirmationCheckbox.SetFocus()

		optionsSizer = guiHelper.BoxSizerHelper(self, sizer=sHelper.addItem(wx.StaticBoxSizer(
			wx.StaticBox(
				self,
				# Translators: The label for a group box containing the NVDA installation dialog options.
				label=_("Options")
			),
			wx.VERTICAL
		)))

		# Translators: The label of a checkbox option in the Install NVDA dialog.
		startOnLogonText = _("Use NVDA on the Windows &logon screen")
		self.startOnLogonCheckbox = optionsSizer.addItem(wx.CheckBox(self, label=startOnLogonText))
		if globalVars.appArgs.enableStartOnLogon is not None:
			self.startOnLogonCheckbox.Value = globalVars.appArgs.enableStartOnLogon
		else:
			self.startOnLogonCheckbox.Value = config.getStartOnLogonScreen() if self.isUpdate else True

		shortcutIsPrevInstalled=installer.isDesktopShortcutInstalled()
		if self.isUpdate and shortcutIsPrevInstalled:
			# Translators: The label of a checkbox option in the Install NVDA dialog.
			keepShortCutText = _("&Keep existing desktop shortcut")
			self.createDesktopShortcutCheckbox = optionsSizer.addItem(wx.CheckBox(self, label=keepShortCutText))
		else:
			# Translators: The label of the option to create a desktop shortcut in the Install NVDA dialog.
			# If the shortcut key has been changed for this locale,
			# this change must also be reflected here.
			createShortcutText = _("Create &desktop icon and shortcut key (control+alt+n)")
			self.createDesktopShortcutCheckbox = optionsSizer.addItem(wx.CheckBox(self, label=createShortcutText))
		self.createDesktopShortcutCheckbox.Value = shortcutIsPrevInstalled if self.isUpdate else True 
		
		# Translators: The label of a checkbox option in the Install NVDA dialog.
		createPortableText = _("Copy &portable configuration to current user account")
		self.copyPortableConfigCheckbox = optionsSizer.addItem(wx.CheckBox(self, label=createPortableText))
		self.copyPortableConfigCheckbox.Value = False
		if globalVars.appArgs.launcher:
			self.copyPortableConfigCheckbox.Disable()

		bHelper = sHelper.addDialogDismissButtons(guiHelper.ButtonHelper(wx.HORIZONTAL))
		if shouldAskAboutAddons:
			# Translators: The label of a button to launch the add-on compatibility review dialog.
			reviewAddonButton = bHelper.addButton(self, label=_("&Review add-ons..."))
			reviewAddonButton.Bind(wx.EVT_BUTTON, self.onReviewAddons)

		# Translators: The label of a button to continue with the operation.
		continueButton = bHelper.addButton(self, label=_("&Continue"), id=wx.ID_OK)
		continueButton.SetDefault()
		continueButton.Bind(wx.EVT_BUTTON, self.onInstall)
		if shouldAskAboutAddons:
			self.confirmationCheckbox.Bind(
				wx.EVT_CHECKBOX,
				lambda evt: continueButton.Enable(not continueButton.Enabled)
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
		doInstall(self.createDesktopShortcutCheckbox.Value,self.startOnLogonCheckbox.Value,self.copyPortableConfigCheckbox.Value,self.isUpdate)
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

	def onReviewAddons(self, evt):
		from gui import addonGui
		incompatibleAddons = addonGui.IncompatibleAddonsDialog(
			parent=self,
			# the defaults from the installer are fine. We are testing against the running version.
		)
		incompatibleAddons.ShowModal()

class InstallingOverNewerVersionDialog(wx.Dialog, DpiScalingHelperMixin):
	def __init__(self):
		# Translators: The title of a warning dialog.
		wx.Dialog.__init__(self, gui.mainFrame, title=_("Warning"))
		DpiScalingHelperMixin.__init__(self, self.GetHandle())

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentSizer = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		text = wx.StaticText(
			self,
			# Translators: A warning presented when the user attempts to downgrade NVDA
			# to an older version.
			label=_(
				"You are attempting to install an earlier version of NVDA than the version currently installed. "
				"If you really wish to revert to an earlier version, you should first cancel this installation "
				"and completely uninstall NVDA before installing the earlier version."
			))
		text.Wrap(self.scaleSize(600))
		contentSizer.addItem(text)

		buttonHelper = guiHelper.ButtonHelper(orientation=wx.HORIZONTAL)
		okButton = buttonHelper.addButton(
			parent=self,
			id=wx.ID_OK,
			# Translators: The label of a button to proceed with installation,
			# even though this is not recommended.
			label=_("&Proceed with installation (not recommended)")
		)
		cancelButton = buttonHelper.addButton(
			parent=self,
			id=wx.ID_CANCEL
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

class PortableCreaterDialog(wx.Dialog):

	def __init__(self, parent):
		# Translators: The title of the Create Portable NVDA dialog.
		super(PortableCreaterDialog, self).__init__(parent, title=_("Create Portable NVDA"))
		mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		# Translators: An informational message displayed in the Create Portable NVDA dialog.
		dialogCaption=_("To create a portable copy of NVDA, please select the path and other options and then press Continue")
		sHelper.addItem(wx.StaticText(self, label=dialogCaption))

		# Translators: The label of a grouping containing controls to select the destination directory
		# in the Create Portable NVDA dialog.
		directoryGroupText = _("Portable &directory:")
		groupHelper = sHelper.addItem(gui.guiHelper.BoxSizerHelper(self, sizer=wx.StaticBoxSizer(wx.StaticBox(self, label=directoryGroupText), wx.VERTICAL)))
		# Translators: The label of a button to browse for a directory.
		browseText = _("Browse...")
		# Translators: The title of the dialog presented when browsing for the
		# destination directory when creating a portable copy of NVDA.
		dirDialogTitle = _("Select portable  directory")
		directoryEntryControl = groupHelper.addItem(gui.guiHelper.PathSelectionHelper(self, browseText, dirDialogTitle))
		self.portableDirectoryEdit = directoryEntryControl.pathControl
		if globalVars.appArgs.portablePath:
			self.portableDirectoryEdit.Value = os.path.abspath(globalVars.appArgs.portablePath)

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

		bHelper = sHelper.addDialogDismissButtons(gui.guiHelper.ButtonHelper(wx.HORIZONTAL))
		
		continueButton = bHelper.addButton(self, label=_("&Continue"), id=wx.ID_OK)
		continueButton.SetDefault()
		continueButton.Bind(wx.EVT_BUTTON, self.onCreatePortable)
		
		bHelper.addButton(self, id=wx.ID_CANCEL)
		# If we bind this using button.Bind, it fails to trigger when the dialog is closed.
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		
		mainSizer.Add(sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.CentreOnScreen()

	def onCreatePortable(self, evt):
		if not self.portableDirectoryEdit.Value:
			# Translators: The message displayed when the user has not specified a destination directory
			# in the Create Portable NVDA dialog.
			gui.messageBox(_("Please specify a directory in which to create the portable copy."),
				_("Error"),
				wx.OK | wx.ICON_ERROR)
			return
		drv=os.path.splitdrive(self.portableDirectoryEdit.Value)[0]
		if drv and not os.path.isdir(drv):
			# Translators: The message displayed when the user specifies an invalid destination drive
			# in the Create Portable NVDA dialog.
			gui.messageBox(_("Invalid drive %s")%drv,
				_("Error"),
				wx.OK | wx.ICON_ERROR)
			return
		self.Hide()
		doCreatePortable(self.portableDirectoryEdit.Value,self.copyUserConfigCheckbox.Value,False,self.startAfterCreateCheckbox.Value)
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

def doCreatePortable(portableDirectory,copyUserConfig=False,silent=False,startAfterCreate=False):
	d = gui.IndeterminateProgressDialog(gui.mainFrame,
		# Translators: The title of the dialog presented while a portable copy of NVDA is bieng created.
		_("Creating Portable Copy"),
		# Translators: The message displayed while a portable copy of NVDA is bieng created.
		_("Please wait while a portable copy of NVDA is created."))
	try:
		gui.ExecAndPump(installer.createPortableCopy,portableDirectory,copyUserConfig)
	except Exception as e:
		log.error("Failed to create portable copy",exc_info=True)
		d.done()
		if isinstance(e,installer.RetriableFailure):
			# Translators: a message dialog asking to retry or cancel when NVDA portable copy creation fails
			message=_("NVDA is unable to remove or overwrite a file.")
			# Translators: the title of a retry cancel dialog when NVDA portable copy creation  fails
			title=_("File in Use")
			if winUser.MessageBox(None,message,title,winUser.MB_RETRYCANCEL)==winUser.IDRETRY:
				return doCreatePortable(portableDirectory,copyUserConfig,silent,startAfterCreate)
		# Translators: The message displayed when an error occurs while creating a portable copy of NVDA.
		# %s will be replaced with the specific error message.
		gui.messageBox(_("Failed to create portable copy: %s")%e,
			_("Error"),
			wx.OK | wx.ICON_ERROR)
		return
	d.done()
	if silent:
		wx.GetApp().ExitMainLoop()
	else:
		# Translators: The message displayed when a portable copy of NVDA has been successfully created.
		# %s will be replaced with the destination directory.
		gui.messageBox(_("Successfully created a portable copy of NVDA at %s")%portableDirectory,
			_("Success"))
		if startAfterCreate:
			# #4475: ensure that the first window of the new process is not hidden by providing SW_SHOWNORMAL  
			shellapi.ShellExecute(
				None,
				None,
				os.path.join(os.path.abspath(portableDirectory),'nvda.exe'),
				None,
				None,
				winUser.SW_SHOWNORMAL
			)
