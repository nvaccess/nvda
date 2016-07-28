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

	def __init__(self):
		dialogSize=wx.Size(w=500, h=500)
		dialogPos=None
		if not config.conf["speechViewer"]["autoPositionWindow"] and self.doDisplaysMatchConfig():
			log.debug("Setting speechViewer window position")
			speechViewSection = config.conf["speechViewer"]
			dialogSize = wx.Size(w=int(speechViewSection["width"]), h=int(speechViewSection["height"]))
			dialogPos = wx.Point(x=int(speechViewSection["x"]), y=int(speechViewSection["y"]))
		super(SpeechViewerFrame, self).__init__(gui.mainFrame, wx.ID_ANY, _("NVDA Speech Viewer"), size=dialogSize, pos=dialogPos, style=wx.CAPTION | wx.RESIZE_BORDER | wx.STAY_ON_TOP)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.textCtrl = wx.TextCtrl(self, -1,style=wx.TE_RICH2|wx.TE_READONLY|wx.TE_MULTILINE)
		sizer.Add(self.textCtrl, proportion=1, flag=wx.EXPAND)
		self.SetSizer(sizer)
		self.Show(True)

	def onClose(self, evt):
		deactivate()
		return
		if not evt.CanVeto():
			self.Destroy()
			return
		evt.Veto()

	def onDestroy(self, evt):
		log.debug("SpeechViewer Destroyed")
		self.savePositionInformation()
		evt.Skip()

	def doDisplaysMatchConfig(self):
		configSizes = config.conf["speechViewer"]["displays"]
		attachedSizes = self.getAttachedDisplaySizesAsStringArray()
		return len(configSizes) == len(attachedSizes) and all( configSizes[i] == attachedSizes[i] for i in range(0, len(configSizes)))

	def getAttachedDisplaySizesAsStringArray(self):
		displays = (wx.Display(i) for i in range(wx.Display.GetCount()))
		displays = [display.GetGeometry().GetSize() for display in displays]
		return [repr( (i.width, i.height) ) for i in displays]


	def savePositionInformation(self):
		position = self.GetPosition()
		config.conf["speechViewer"]["x"] = position.x
		config.conf["speechViewer"]["y"] = position.y
		size = self.GetSize()
		config.conf["speechViewer"]["width"] = size.width
		config.conf["speechViewer"]["height"] = size.height
		config.conf["speechViewer"]["displays"] = self.getAttachedDisplaySizesAsStringArray()
		config.conf["speechViewer"]["autoPositionWindow"] = False

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
	#Otherwize it would be impossible to select text, or even just read it (as a blind person).
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
