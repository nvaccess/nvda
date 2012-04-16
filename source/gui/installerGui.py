#gui/installerGui.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011-2012 NV Access Limited

import os
import ctypes
import subprocess
import shellapi
import wx
import config
import versionInfo
import installer
from logHandler import log
import gui
import tones

def doInstall(createDesktopShortcut,startOnLogon,isUpdate,silent=False):
	progressDialog = IndeterminateProgressDialog(gui.mainFrame,
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
	except Exception as e:
		res=e
		log.error("Failed to execute installer",exc_info=True)
	progressDialog.done()
	del progressDialog
	if res!=0:
		log.error("Installation failed: %s"%res)
		# Translators: The message displayed when an error occurs during installation of NVDA.
		gui.messageBox(_("The installation of NVDA failed. Please check the Log Viewer for more information."),
			# Translators: The title of a dialog presented when an error occurs.
			_("Error"))
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
			# Translators: The title of a dialolg presented to indicate a successful operation.
			_("Success"))
	shellapi.ShellExecute(None, None,
		os.path.join(installer.defaultInstallPath,'nvda.exe').decode("mbcs"),
		subprocess.list2cmdline(["-r"]).decode("mbcs"),
		None, 0)

def doSilentInstall():
	prevInstall=installer.isPreviousInstall()
	doInstall(installer.isDesktopShortcutInstalled() if prevInstall else True,config.getStartOnLogonScreen() if prevInstall else True,prevInstall,True)

class InstallerDialog(wx.Dialog):

	def __init__(self, parent):
		self.isUpdate=installer.isPreviousInstall()
		# Translators: The title of the Install NVDA dialog.
		super(InstallerDialog, self).__init__(parent, title=_("Install NVDA"))
		mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: An informational message in the Install NVDA dialog.
		msg=_("To install NVDA to your hard drive, please press the Continue button.")
		if self.isUpdate:
			# Translators: An informational message in the Install NVDA dialog.
			msg+=" "+_("A previous copy of NVDA has been found on your system. This copy will be updated.") 
		dialogCaption=wx.StaticText(self,label=msg) 
		mainSizer.Add(dialogCaption)
		# Translators: The label of the grouping containing options in the Install NVDA dialog.
		optionsSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Installation options")), wx.HORIZONTAL)
		# Translators: The label of a checkbox option in the Install NVDA dialog.
		ctrl = self.startOnLogonCheckbox = wx.CheckBox(self, label=_("Use NVDA on the Windows &logon screen"))
		ctrl.Value = config.getStartOnLogonScreen()
		optionsSizer.Add(ctrl)
		# Translators: The label of a checkbox option in the Install NVDA dialog.
		ctrl = self.createDesktopShortcutCheckbox = wx.CheckBox(self, label=_("Create &desktop icon and shortcut key (control+alt+n)"))
		ctrl.Value = installer.isDesktopShortcutInstalled()
		optionsSizer.Add(ctrl)
		mainSizer.Add(optionsSizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a button to continue with the operation.
		ctrl = wx.Button(self, label=_("C&ontinue"), id=wx.ID_OK)
		ctrl.SetDefault()
		ctrl.Bind(wx.EVT_BUTTON, self.onInstall)
		sizer.Add(ctrl)
		sizer.Add(wx.Button(self, id=wx.ID_CANCEL))
		# If we bind this using button.Bind, it fails to trigger when the dialog is closed.
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Add(sizer)

		self.Sizer = mainSizer

	def onInstall(self, evt):
		self.Hide()
		doInstall(self.createDesktopShortcutCheckbox.Value,self.startOnLogonCheckbox.Value,self.isUpdate)
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

class IndeterminateProgressDialog(wx.ProgressDialog):

	def __init__(self, parent, title, message):
		super(IndeterminateProgressDialog, self).__init__(title, message, parent=parent)
		self.timer = wx.PyTimer(self.Pulse)
		self.timer.Start(1000)
		self.Raise()

	def Pulse(self):
		super(IndeterminateProgressDialog, self).Pulse()
		if self.IsActive():
			tones.beep(440, 40)

	def done(self):
		self.timer.Stop()
		if self.IsActive():
			tones.beep(1760, 40)
		self.Destroy()

class PortableCreaterDialog(wx.Dialog):

	def __init__(self, parent):
		# Translators: The title of the Create Portable NVDA dialog.
		super(PortableCreaterDialog, self).__init__(parent, title=_("Create Portable NVDA"))
		mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: An informational message displayed in the Create Portable NVDA dialog.
		dialogCaption=wx.StaticText(self,label=_("To create a portable copy of NVDA, please select the path and other options and then press Continue")) 
		mainSizer.Add(dialogCaption)
		# Translators: The label of the grouping containing options in the Create Portable NVDA dialog.
		optionsSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Portable options")), wx.HORIZONTAL)
		# Translators: The label of a grouping containing controls to select the destination directory
		# in the Create Portable NVDA dialog.
		sizer = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Portable directory:")), wx.HORIZONTAL)
		ctrl = self.portableDirectoryEdit = wx.TextCtrl(self, value='e:\\')
		sizer.Add(ctrl)
		# Translators: The label of a button to browse for a directory.
		ctrl = wx.Button(self, label=_("Browse..."))
		ctrl.Bind(wx.EVT_BUTTON, self.onBrowseForPortableDirectory)
		sizer.Add(ctrl)
		optionsSizer.Add(sizer)
		# Translators: The label of a checkbox option in the Create Portable NVDA dialog.
		ctrl = self.createAutorunCheckbox = wx.CheckBox(self, label=_("Create an &Autorun file"))
		ctrl.Value = False
		optionsSizer.Add(ctrl)
		# Translators: The label of a checkbox option in the Create Portable NVDA dialog.
		ctrl = self.copyUserConfigCheckbox = wx.CheckBox(self, label=_("Copy current &user configuration"))
		ctrl.Value = False
		optionsSizer.Add(ctrl)
		mainSizer.Add(optionsSizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		ctrl = wx.Button(self, label=_("C&ontinue"), id=wx.ID_OK)
		ctrl.SetDefault()
		ctrl.Bind(wx.EVT_BUTTON, self.onCreatePortable)
		sizer.Add(ctrl)
		sizer.Add(wx.Button(self, id=wx.ID_CANCEL))
		# If we bind this using button.Bind, it fails to trigger when the dialog is closed.
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Add(sizer)

		self.Sizer = mainSizer

	def onBrowseForPortableDirectory(self, evt):
		# Translators: The title of the dialog presented when browsing for the
		# destination directory when creating a portable copy of NVDA.
		with wx.DirDialog(self, _("Select portable  directory"), defaultPath=self.portableDirectoryEdit.Value) as d:
			if d.ShowModal() == wx.ID_OK:
				self.portableDirectoryEdit.Value = d.Path

	def onCreatePortable(self, evt):
		self.Hide()
		doCreatePortable(self.portableDirectoryEdit.Value,self.createAutorunCheckbox.Value,self.copyUserConfigCheckbox.Value)
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

def doCreatePortable(portableDirectory,createAutorun=False,copyUserConfig=False):
	d = IndeterminateProgressDialog(gui.mainFrame,
		# Translators: The title of the dialog presented while a portable copy of NVDA is bieng created.
		_("Creating Portable Copy"),
		# Translators: The message displayed while a portable copy of NVDA is bieng created.
		_("Please wait while a portable copy of NVDA is created."))
	try:
		installer.CreatePortableCopy(portableDirectory,copyUserConfig=copyUserConfig,createAutorun=createAutorun)
	except Exception as e:
		log.error("Failed to create portable copy",exc_info=True)
		d.done()
		# Translators: The message displayed when an error occurs while creating a portable copy of NVDA.
		# %s will be replaced with the specific error message.
		gui.messageBox(_("Failed to create portable copy: %s")%e,
			_("Error"))
		return
	d.done()
	# Translators: The message displayed when a portable copy of NVDA has been successfully created.
	# %s will be replaced with the destination directory.
	gui.messageBox(_("Successfully created a portable copy of NVDA at %s")%portableDirectory,
		_("Success"))
