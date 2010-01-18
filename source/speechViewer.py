#speechViewer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import gui

class SpeechViewerFrame(wx.MiniFrame):

	def __init__(self):
		super(SpeechViewerFrame, self).__init__(gui.mainFrame, wx.ID_ANY, _("NVDA Speech Viewer"), style=wx.CAPTION | wx.RESIZE_BORDER | wx.STAY_ON_TOP)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.textCtrl = wx.TextCtrl(self, -1,size=(500,500),style=wx.TE_RICH2|wx.TE_READONLY|wx.TE_MULTILINE)
		sizer.Add(self.textCtrl, proportion=1, flag=wx.EXPAND)
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
	_guiFrame.textCtrl.AppendText(text + "\n")

def deactivate():
	global _guiFrame, isActive
	if not isActive:
		return
	isActive=False
	_guiFrame.Destroy()
	_guiFrame = None
