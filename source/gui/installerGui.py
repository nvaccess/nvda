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

class InstallerDialog(wx.Dialog):

	def __init__(self, parent):
		super(InstallerDialog, self).__init__(parent, title=_("Install NVDA"))
		mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		dialogCaption=wx.StaticText(self,label=_("If you wish to install NVDA to your hard drive, please review the following options and then press the Install button to continue.")) 
		mainSizer.Add(dialogCaption)
		optionsSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Installation options")), wx.HORIZONTAL)
		ctrl = self.startOnLogonCheckbox = wx.CheckBox(self, label=_("Use NVDA on the Windows &logon screen"))
		ctrl.Value = config.getStartOnLogonScreen()
		optionsSizer.Add(ctrl)
		ctrl = self.createDesktopShortcutCheckbox = wx.CheckBox(self, label=_("Create &desktop icon and shortcut key (control+alt+n)"))
		ctrl.Value = True
		optionsSizer.Add(ctrl)
		mainSizer.Add(optionsSizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		ctrl = wx.Button(self, label=_("&Install"), id=wx.ID_OK)
		ctrl.Bind(wx.EVT_BUTTON, self.onInstall)
		sizer.Add(ctrl)
		sizer.Add(wx.Button(self, id=wx.ID_CANCEL))
		# If we bind this using button.Bind, it fails to trigger when the dialog is closed.
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Add(sizer)

		self.Sizer = mainSizer

	def onInstall(self, evt):
		self.Hide()
		self.progressDialog = IndeterminateProgressDialog(self, _("Installing NVDA"), _("Please wait while NVDA is being installed."))
		try:
			res=config.execElevated(config.SLAVE_FILENAME,["install",str(int(self.createDesktopShortcutCheckbox.Value)),str(int(self.startOnLogonCheckbox.Value))],wait=True)
		except Exception as e:
			res=e
			log.error("Failed to execute installer",exc_info=True)
		self.progressDialog.done()
		self.Destroy()
		if res!=0:
			log.error("Installation failed: %s"%res)
			gui.messageBox(_("The installation of NVDA failed. Please check the log viewer for more information."),_("Error"))
			return
		gui.messageBox(_("Successfully installed NVDA. Please press OK to start the newly installed copy."),_("Success"))
		shellapi.ShellExecute(None, None,
		os.path.join(installer.defaultInstallPath,'nvda_uiAccess.exe').decode("mbcs"),
		subprocess.list2cmdline(["-r"]).decode("mbcs"),
		None, 0)

	def onCancel(self, evt):
		self.Destroy()

class UpdaterDialog(wx.Dialog):

	def __init__(self, parent):
		super(UpdaterDialog, self).__init__(parent, title=_("Update NVDA"))
		mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		dialogCaption=wx.StaticText(self,label=_("This will update your previously installed copy of NVDA to the currently running version (%s). Please press the Update button to continue.")%versionInfo.version)
		mainSizer.Add(dialogCaption)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		ctrl = wx.Button(self, label=_("&Update"), id=wx.ID_OK)
		ctrl.Bind(wx.EVT_BUTTON, self.onUpdate)
		sizer.Add(ctrl)
		sizer.Add(wx.Button(self, id=wx.ID_CANCEL))
		# If we bind this using button.Bind, it fails to trigger when the dialog is closed.
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Add(sizer)

		self.Sizer = mainSizer

	def onUpdate(self, evt):
		self.Hide()
		self.progressDialog = IndeterminateProgressDialog(self, _("Updating NVDA installation"), _("Please wait while NVDA is being updated."))
		try:
			res=config.execElevated(config.SLAVE_FILENAME,["updateInstall"],wait=True)
		except Exception as e:
			res=e
			log.error("Failed to execute updater",exc_info=True)
		self.progressDialog.done()
		self.Destroy()
		if res!=0:
			log.error("Update failed: %s"%res)
			gui.messageBox(_("NVDA update failed. Please check the log viewer for more information."),_("Error"))
			return
		gui.messageBox(_("Successfully updated NVDA. Please press OK to start the updated copy."),_("Success"))
		shellapi.ShellExecute(None, None,
		os.path.join(installer.defaultInstallPath,'nvda_uiAccess.exe').decode("mbcs"),
		subprocess.list2cmdline(["-r"]).decode("mbcs"),
		None, 0)

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
