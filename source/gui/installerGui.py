#gui/installerGui.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011-2012 NV Access Limited

import os
import ctypes
import shellapi
import winUser
import wx
import config
import globalVars
import versionInfo
import installer
from logHandler import log
import gui
import tones

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
		res=config.execElevated(config.SLAVE_FILENAME,["install",str(int(createDesktopShortcut)),str(int(startOnLogon))],wait=True,handleAlreadyElevated=True)
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
		shellapi.ShellExecute(None, None,
			os.path.join(installer.defaultInstallPath,'nvda.exe'),
			u"-r",
			None, winUser.SW_SHOWNORMAL)
	else:
		wx.GetApp().ExitMainLoop()

def doSilentInstall(startAfterInstall=True):
	prevInstall=installer.comparePreviousInstall() is not None
	doInstall(installer.isDesktopShortcutInstalled() if prevInstall else True,config.getStartOnLogonScreen() if prevInstall else True,False,prevInstall,silent=True,startAfterInstall=startAfterInstall)

class InstallerDialog(wx.Dialog):

	def __init__(self, parent, isUpdate):
		self.isUpdate=isUpdate
		# Translators: The title of the Install NVDA dialog.
		super(InstallerDialog, self).__init__(parent, title=_("Install NVDA"))
		mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: An informational message in the Install NVDA dialog.
		msg=_("To install NVDA to your hard drive, please press the Continue button.")
		if self.isUpdate:
			# Translators: An informational message in the Install NVDA dialog.
			msg+=" "+_("A previous copy of NVDA has been found on your system. This copy will be updated.") 
			if not os.path.isdir(installer.defaultInstallPath):
				# Translators: a message in the installer telling the user NVDA is now located in a different place.
				msg+=" "+_("The installation path for NVDA has changed. it will now  be installed in {path}").format(path=installer.defaultInstallPath)
		dialogCaption=wx.StaticText(self,label=msg) 
		mainSizer.Add(dialogCaption)
		optionsSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: The label of a checkbox option in the Install NVDA dialog.
		ctrl = self.startOnLogonCheckbox = wx.CheckBox(self, label=_("Use NVDA on the Windows &logon screen"))
		ctrl.Value = config.getStartOnLogonScreen() if self.isUpdate else True
		optionsSizer.Add(ctrl)
		shortcutIsPrevInstalled=installer.isDesktopShortcutInstalled()
		if self.isUpdate and shortcutIsPrevInstalled:
			# Translators: The label of a checkbox option in the Install NVDA dialog.
			ctrl = self.createDesktopShortcutCheckbox = wx.CheckBox(self, label=_("&Keep existing desktop shortcut"))
		else:
			# Translators: The label of the option to create a desktop shortcut in the Install NVDA dialog.
			# If the shortcut key has been changed for this locale,
			# this change must also be reflected here.
			ctrl = self.createDesktopShortcutCheckbox = wx.CheckBox(self, label=_("Create &desktop icon and shortcut key (control+alt+n)"))
		ctrl.Value = shortcutIsPrevInstalled if self.isUpdate else True 
		optionsSizer.Add(ctrl)
		# Translators: The label of a checkbox option in the Install NVDA dialog.
		ctrl = self.copyPortableConfigCheckbox = wx.CheckBox(self, label=_("Copy &portable configuration to current user account"))
		ctrl.Value = False
		if globalVars.appArgs.launcher:
			ctrl.Disable()
		optionsSizer.Add(ctrl)
		mainSizer.Add(optionsSizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a button to continue with the operation.
		ctrl = wx.Button(self, label=_("&Continue"), id=wx.ID_OK)
		ctrl.SetDefault()
		ctrl.Bind(wx.EVT_BUTTON, self.onInstall)
		sizer.Add(ctrl)
		sizer.Add(wx.Button(self, id=wx.ID_CANCEL))
		# If we bind this using button.Bind, it fails to trigger when the dialog is closed.
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Add(sizer)

		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onInstall(self, evt):
		self.Hide()
		doInstall(self.createDesktopShortcutCheckbox.Value,self.startOnLogonCheckbox.Value,self.copyPortableConfigCheckbox.Value,self.isUpdate)
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

def showInstallGui():
	gui.mainFrame.prePopup()
	previous = installer.comparePreviousInstall()
	if previous > 0:
		# The existing installation is newer, which means this will be a downgrade.
		# Translators: The title of a warning dialog.
		d = wx.Dialog(gui.mainFrame, title=_("Warning"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		item = wx.StaticText(d,
			# Translators: A warning presented when the user attempts to downgrade NVDA
			# to an older version.
			label=_("You are attempting to install an earlier version of NVDA than the version currently installed. "
			"If you really wish to revert to an earlier version, you should first cancel this installation and completely uninstall NVDA before installing the earlier version."))
		mainSizer.Add(item)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		item = wx.Button(d, id=wx.ID_OK,
			# Translators: The label of a button to proceed with installation,
			# even though this is not recommended.
			label=_("&Proceed with installation (not recommended)"))
		sizer.Add(item)
		item = wx.Button(d, id=wx.ID_CANCEL)
		sizer.Add(item)
		item.SetFocus()
		mainSizer.Add(sizer)
		d.Sizer = mainSizer
		mainSizer.Fit(d)
		d.Center(wx.BOTH | wx.CENTER_ON_SCREEN)
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
		# Translators: An informational message displayed in the Create Portable NVDA dialog.
		dialogCaption=wx.StaticText(self,label=_("To create a portable copy of NVDA, please select the path and other options and then press Continue")) 
		mainSizer.Add(dialogCaption)
		optionsSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: The label of a grouping containing controls to select the destination directory
		# in the Create Portable NVDA dialog.
		sizer = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Portable &directory:")), wx.HORIZONTAL)
		ctrl = self.portableDirectoryEdit = wx.TextCtrl(self)
		sizer.Add(ctrl)
		# Translators: The label of a button to browse for a directory.
		ctrl = wx.Button(self, label=_("Browse..."))
		ctrl.Bind(wx.EVT_BUTTON, self.onBrowseForPortableDirectory)
		sizer.Add(ctrl)
		optionsSizer.Add(sizer)
		# Translators: The label of a checkbox option in the Create Portable NVDA dialog.
		ctrl = self.copyUserConfigCheckbox = wx.CheckBox(self, label=_("Copy current &user configuration"))
		ctrl.Value = False
		if globalVars.appArgs.launcher:
			ctrl.Disable()
		optionsSizer.Add(ctrl)
		mainSizer.Add(optionsSizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		ctrl = wx.Button(self, label=_("&Continue"), id=wx.ID_OK)
		ctrl.SetDefault()
		ctrl.Bind(wx.EVT_BUTTON, self.onCreatePortable)
		sizer.Add(ctrl)
		sizer.Add(wx.Button(self, id=wx.ID_CANCEL))
		# If we bind this using button.Bind, it fails to trigger when the dialog is closed.
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Add(sizer)

		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onBrowseForPortableDirectory(self, evt):
		# Translators: The title of the dialog presented when browsing for the
		# destination directory when creating a portable copy of NVDA.
		with wx.DirDialog(self, _("Select portable  directory"), defaultPath=self.portableDirectoryEdit.Value or "c:\\") as d:
			if d.ShowModal() == wx.ID_OK:
				self.portableDirectoryEdit.Value = d.Path

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
		doCreatePortable(self.portableDirectoryEdit.Value,self.copyUserConfigCheckbox.Value)
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

def doCreatePortable(portableDirectory,copyUserConfig=False):
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
				return doCreatePortable(portableDirectory,copyUserConfig)
		# Translators: The message displayed when an error occurs while creating a portable copy of NVDA.
		# %s will be replaced with the specific error message.
		gui.messageBox(_("Failed to create portable copy: %s")%e,
			_("Error"),
			wx.OK | wx.ICON_ERROR)
		return
	d.done()
	# Translators: The message displayed when a portable copy of NVDA has been successfully created.
	# %s will be replaced with the destination directory.
	gui.messageBox(_("Successfully created a portable copy of NVDA at %s")%portableDirectory,
		_("Success"))
