#speechViewer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import gui
import config
from logHandler import log

class SpeechViewerFrame(wx.Dialog):

	def __init__(self, onDestroyCallBack):
		super(SpeechViewerFrame, self).__init__(gui.mainFrame, wx.ID_ANY, _("NVDA Speech Viewer"), style=wx.CAPTION | wx.RESIZE_BORDER | wx.STAY_ON_TOP)
		self.onDestroyCallBack = onDestroyCallBack
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.textCtrl = wx.TextCtrl(self, -1,size=(500,500),style=wx.TE_RICH2|wx.TE_READONLY|wx.TE_MULTILINE)
		sizer.Add(self.textCtrl, proportion=1, flag=wx.EXPAND)
		# Translators: The label for a setting in the speech viewer that controls whether the speech viewer is shown at startup or not.
		self.shouldShowOnStartupCheckBox = wx.CheckBox(self,wx.NewId(),label=_("&Show Speech Viewer on Startup"))
		self.shouldShowOnStartupCheckBox.SetValue(config.conf["speechViewer"]["showSpeechViewerAtStartup"])
		self.shouldShowOnStartupCheckBox.Bind(wx.EVT_CHECKBOX, self.onShouldShowOnStartupChanged)
		sizer.Add(self.shouldShowOnStartupCheckBox, border=5, flag=wx.ALL)
		# set the check box as having focus, by default the textCtrl has focus which stops the speechviewer output (even if another window is in focus)
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
		config.conf["speechViewer"]["showSpeechViewerAtStartup"] = self.shouldShowOnStartupCheckBox.IsChecked()

	def onDestroy(self, evt):
		log.debug("SpeechViewer destroyed")
		self.onDestroyCallBack()

_guiFrame=None
isActive=False

def activate():
	global _guiFrame, isActive
	_guiFrame = SpeechViewerFrame(_cleanup)
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

def _cleanup():
	global _guiFrame, isActive
	if not isActive:
		return
	isActive=False
	_guiFrame = None

def deactivate():
	global _guiFrame, isActive
	if not isActive:
		return
	_guiFrame.Destroy()
