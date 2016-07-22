#speechViewer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import gui
import config

class SpeechViewerFrame(wx.Dialog):

	def __init__(self):
		super(SpeechViewerFrame, self).__init__(gui.mainFrame, wx.ID_ANY, _("NVDA Speech Viewer"), style=wx.CAPTION | wx.RESIZE_BORDER | wx.STAY_ON_TOP)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.textCtrl = wx.TextCtrl(self, -1,size=(500,500),style=wx.TE_RICH2|wx.TE_READONLY|wx.TE_MULTILINE)
		sizer.Add(self.textCtrl, proportion=1, flag=wx.EXPAND)
		# Translators: The label for a setting in the speech viewer that controls whether the speech viewer is shown at startup or not.
		self.shouldShowOnStartupCheckBox = wx.CheckBox(self,wx.NewId(),label=_("&Show Speech Viewer on Startup"))
		self.shouldShowOnStartupCheckBox.SetValue(config.conf["speechView"]["showSpeechViewerAtStartup"])
		self.shouldShowOnStartupCheckBox.Bind(wx.EVT_CHECKBOX, self.onShouldShowOnStartupChanged)
		# set the check box as having focus, by default the textCtrl has focus which stops the speechviewer output (even if another window is in focus)
		sizer.Add(self.shouldShowOnStartupCheckBox, border=5, flag=wx.ALL)
		self.shouldShowOnStartupCheckBox.SetFocus()
		sizer.Fit(self)
		self.SetSizer(sizer)
		self.Show(True)

	def onClose(self, evt):
		deactivate()
		return
		if not evt.CanVeto():
			self.Destroy()
			return
		evt.Veto()

	def onShouldShowOnStartupChanged(self, evt):
		config.conf["speechView"]["showSpeechViewerAtStartup"] = self.shouldShowOnStartupCheckBox.IsChecked()

_guiFrame=None
isActive=False

def activate():
	global _guiFrame, isActive
	_guiFrame = SpeechViewerFrame()
	isActive=True

def appendText(text):
	if not isActive:
		return
	if not isinstance(text,basestring):
		return
	#If the speech viewer text control has the focus, we want to disable updates
	#Otherwise it would be impossible to select text, or even just read it (as a blind person).
	if _guiFrame.FindFocus()==_guiFrame.textCtrl:
		return
	_guiFrame.textCtrl.AppendText(text + "\n")

def deactivate():
	global _guiFrame, isActive
	if not isActive:
		return
	isActive=False
	_guiFrame.Destroy()
	_guiFrame = None
