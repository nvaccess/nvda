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

def doInstall(createDesktopShortcut,startOnLogon,isUpdate,silent=False):
	progressDialog = IndeterminateProgressDialog(None, _("Updating NVDA") if isUpdate else _("Installing NVDA"), _("Please wait while your previous installation of NVDA is being updated.") if isUpdate else _("Please wait while NVDA is being installed"))
	try:
		res=config.execElevated(config.SLAVE_FILENAME,["install",str(int(createDesktopShortcut)),str(int(startOnLogon))],wait=True)
	except Exception as e:
		res=e
		log.error("Failed to execute installer",exc_info=True)
	progressDialog.done()
	del progressDialog
	if res!=0:
		log.error("Installation failed: %s"%res)
		gui.messageBox(_("The installation of NVDA failed. Please check the log viewer for more information."),_("Error"))
		return
	if not silent:
		msg=_("Successfully installed NVDA. ") if not isUpdate else _("Successfully updated your installation of NVDA. ")
		gui.messageBox(msg+_("Please press OK to start the installed copy."),_("Success"))
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
		super(InstallerDialog, self).__init__(parent, title=_("Install NVDA"))
		mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		msg=_("To install NVDA to your hard drive, please press the Continue button.")
		if self.isUpdate:
			msg+=" "+_("A previous copy of NVDA has been found on your system. This copy will be updated.") 
		dialogCaption=wx.StaticText(self,label=msg) 
		mainSizer.Add(dialogCaption)
		optionsSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Installation options")), wx.HORIZONTAL)
		ctrl = self.startOnLogonCheckbox = wx.CheckBox(self, label=_("Use NVDA on the Windows &logon screen"))
		ctrl.Value = config.getStartOnLogonScreen()
		optionsSizer.Add(ctrl)
		ctrl = self.createDesktopShortcutCheckbox = wx.CheckBox(self, label=_("Create &desktop icon and shortcut key (control+alt+n)"))
		ctrl.Value = installer.isDesktopShortcutInstalled()
		optionsSizer.Add(ctrl)
		mainSizer.Add(optionsSizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		ctrl = wx.Button(self, label=_("C&ontinue"), id=wx.ID_OK)
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

	def onCancel(self, evt):
		self.Destroy()


class IndeterminateProgressDialog(wx.ProgressDialog):

	def __init__(self, parent, title, message):
		super(IndeterminateProgressDialog, self).__init__(title, message, parent=parent)
		self.timer = wx.PyTimer(self.Pulse)
		self.timer.Start(1000)
		self.Raise()

	def done(self):
		self.timer.Stop()
		self.Destroy()

def createPortableCopy():
		with wx.DirDialog(gui.mainFrame,_("Choose where you wish to place the portable copy of NVDA")) as d:
			if d.ShowModal()!=wx.ID_OK:
				return
			path=d.Path
		copyUserConfig=gui.messageBox(_("Would you like to include your current NVDA settings in the portable copy?"), _("Copy User Configuration"), wx.YES_NO|wx.ICON_QUESTION) == wx.YES
		createAutorun=(ctypes.windll.kernel32.GetDriveTypeW(os.path.splitdrive(path)[0]+u'\\')==2 and gui.messageBox(_("Would you like to create an autorun file for your removable drive to allow NVDA to start automatically?"), _("Removable Drive Detected"), wx.YES_NO|wx.ICON_QUESTION) == wx.YES)

		d = IndeterminateProgressDialog(gui.mainFrame, _("Creating Portable Copy"), _("Please wait while a portable copy of NVDA is created."))
		try:
			installer.CreatePortableCopy(path,copyUserConfig=copyUserConfig,createAutorun=createAutorun)
		except OSError:
			d.done()
			gui.messageBox(_("Failed to create portable copy"),_("Error"))
			return
		d.done()
		gui.messageBox(_("Successfully created a portable copy of NVDA at %s")%path,_("Success"))
