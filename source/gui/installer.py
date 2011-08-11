import os
import wx
import config
import versionInfo

class InstallerDialog(wx.Dialog):

	def __init__(self, parent):
		super(InstallerDialog, self).__init__(parent, title=_("Install NVDA"))
		mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)

		ctrl = self.startOnLogonCheckbox = wx.CheckBox(self, label=_("Use NVDA on the Windows &logon screen"))
		ctrl.Value = config.getStartOnLogonScreen()
		mainSizer.Add(ctrl)
		ctrl = self.advancedCheckbox = wx.CheckBox(self, label=_("Show &advanced options"))
		ctrl.Bind(wx.EVT_CHECKBOX, self.onAdvanced)
		ctrl.SetValue(False)
		mainSizer.Add(ctrl)

		advancedSizer = self.advancedSizer = wx.BoxSizer(wx.VERTICAL)

		sizer = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Install &to folder:")), wx.HORIZONTAL)
		# FIXME: Don't use os.getenv to get the path to Program Files.
		ctrl = self.programFolderEdit = wx.TextCtrl(self, value=os.path.join(unicode(os.getenv("ProgramFiles")), versionInfo.name))
		sizer.Add(ctrl)
		ctrl = wx.Button(self, label=_("Browse..."))
		ctrl.Bind(wx.EVT_BUTTON, self.onBrowseForProgramFolder)
		sizer.Add(ctrl)
		advancedSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(wx.StaticText(self, label=_("&Start Menu folder:")))
		ctrl = self.startMenuFolderEdit = wx.TextCtrl(self, value=versionInfo.name)
		sizer.Add(ctrl)
		advancedSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.VERTICAL)
		ctrl = self.createDesktopShortcutCheckbox = wx.CheckBox(self, label=_("Create &desktop icon and shortcut key (control+alt+n)"))
		ctrl.Value = True
		sizer.Add(ctrl)
		ctrl = self.installServiceCheckbox = wx.CheckBox(self, label=_("Install NVDA ser&vice (Windows logon/secure screen support)"))
		ctrl.Value = True
		sizer.Add(ctrl)
		advancedSizer.Add(sizer)

		mainSizer.Add(advancedSizer)
		mainSizer.Hide(advancedSizer, recursive=True)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		ctrl = wx.Button(self, label=_("&Install"), id=wx.ID_OK)
		ctrl.Bind(wx.EVT_BUTTON, self.onInstall)
		sizer.Add(ctrl)
		sizer.Add(wx.Button(self, id=wx.ID_CANCEL))
		# If we bind this using button.Bind, it fails to trigger when the dialog is closed.
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Add(sizer)

		self.SetSizer(mainSizer)

	def onAdvanced(self, evt):
		self.mainSizer.Show(self.advancedSizer, show=evt.IsChecked(), recursive=True)
		self.mainSizer.Layout()

	def onBrowseForProgramFolder(self, evt):
		with wx.DirDialog(self, _("Select Installation Folder"), defaultPath=self.programFolderEdit.Value) as d:
			if d.ShowModal() == wx.ID_OK:
				self.programFolderEdit.Value = d.Path

	def onInstall(self, evt):
		self.Hide()
		self.progressDialog = IndeterminateProgressDialog(self, _("Installing NVDA"), _("Please wait while NVDA is being installed."))
		self.progressDialog.Raise()
		wx.CallLater(5000, self.installDone)

	def installDone(self):
		self.progressDialog.done()
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

class IndeterminateProgressDialog(wx.ProgressDialog):

	def __init__(self, parent, title, message):
		super(IndeterminateProgressDialog, self).__init__(title, message, parent=parent)
		self.timer = wx.PyTimer(self.Pulse)
		self.timer.Start(1000)

	def done(self):
		self.timer.Stop()
		self.Destroy()
