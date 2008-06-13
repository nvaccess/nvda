#synthDrivers/display.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import gui
import synthDriverHandler

class SynthFrame(wx.MiniFrame):

	def __init__(self):
		wx.MiniFrame.__init__(self, gui.mainFrame, wx.ID_ANY, "NVDA Display Synth", style=wx.CAPTION | wx.RESIZE_BORDER | wx.STAY_ON_TOP)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.textCtrl = wx.TextCtrl(self, -1,size=(500,500),style=wx.TE_RICH2|wx.TE_READONLY|wx.TE_MULTILINE)
		sizer.Add(self.textCtrl, proportion=1, flag=wx.EXPAND)
		sizer.Fit(self)
		self.SetSizer(sizer)
		self.Show(True)

	def onClose(self, evt):
		if not evt.CanVeto():
			return
		evt.Veto()

class SynthDriver(synthDriverHandler.SynthDriver):
	name = "display"
	description = _("A virtual synth which displays text in a window")

	@classmethod
	def check(cls):
		return True

	def initialize(self):
		self.frame = SynthFrame()

	def speakText(self,text,wait=False,index=None):
		self.frame.textCtrl.AppendText(text + "\n")

	def terminate(self):
		if not self.frame:
			return
		self.frame.Close()
		self.frame.Destroy()
		self.frame = None
