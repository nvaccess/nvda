#appModules/excel.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import re
import ctypes
import pythoncom
import win32com.client
import comtypes.automation
import wx
import gui
import gui.scriptUI
import IAccessibleHandler
import controlTypes
import speech
from keyUtils import sendKey, key
from . import IAccessible
import appModuleHandler

re_dollaredAddress=re.compile(r"^\$?([a-zA-Z]+)\$?([0-9]+)")

class CellEditDialog(gui.scriptUI.ModalDialog):

	def __init__(self,cell):
		super(CellEditDialog,self).__init__(None)
		self._cell=cell

	def onCellTextChar(self,evt):
		if evt.GetKeyCode() == wx.WXK_RETURN:
			if evt.AltDown():
				i=self._cellText.GetInsertionPoint()
				self._cellText.Replace(i,i,"\n")
			else:
				self.onOk(None)
			return
		evt.Skip(True)

	def onOk(self,evt):
		self._cell.formulaLocal=self._cellText.GetValue()
		self.dialog.EndModal(wx.ID_OK)

	def makeDialog(self):
		d=wx.Dialog(gui.mainFrame, wx.ID_ANY, title=_("NVDA Excel Cell Editor"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer.Add(wx.StaticText(d,wx.ID_ANY, label=_("Enter cell contents")))
		self._cellText=wx.TextCtrl(d, wx.ID_ANY, size=(300, 200), style=wx.TE_RICH|wx.TE_MULTILINE)
		self._cellText.Bind(wx.EVT_KEY_DOWN, self.onCellTextChar)
		self._cellText.SetValue(self._cell.formulaLocal)
		mainSizer.Add(self._cellText)
		mainSizer.Add(d.CreateButtonSizer(wx.OK|wx.CANCEL))
		d.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		d.SetSizer(mainSizer)
		self._cellText.SetFocus()
		return d

class ExcelGrid(IAccessible):

	def __init__(self,*args,**vars):
		IAccessible.__init__(self,*args,**vars)
		ptr=ctypes.c_void_p()
		if ctypes.windll.oleacc.AccessibleObjectFromWindow(self.windowHandle,IAccessibleHandler.OBJID_NATIVEOM,ctypes.byref(comtypes.automation.IDispatch._iid_),ctypes.byref(ptr))!=0:
			raise OSError("No native object model")
		#We use pywin32 for large IDispatch interfaces since it handles them much better than comtypes
		o=pythoncom._univgw.interface(ptr.value,pythoncom.IID_IDispatch)
		t=o.GetTypeInfo()
		a=t.GetTypeAttr()
		oleRepr=win32com.client.build.DispatchItem(attr=a)
		self.excelObject=win32com.client.CDispatch(o,oleRepr)

	def _get_role(self):
		return controlTypes.ROLE_TABLE

	def getSelectedRange(self):
		return self.excelObject.Selection
	selectedRange=property(fget=getSelectedRange)

	def getActiveCell(self):
		time.sleep(0.01)
		return self.excelObject.ActiveCell
	activeCell=property(fget=getActiveCell)

	def getCellAddress(self,cell):
		return re_dollaredAddress.sub(r"\1\2",cell.Address)

	def getCellText(self,cell):
		return cell.Text

	def cellHasFormula(self,cell):
		return cell.HasFormula

	def speakSelection(self):
		try:
			cells=self.getSelectedRange()
			if cells.Count>1:
				first=cells.Item(1)
				last=cells.Item(cells.Count)
				speech.speakMessage((_("selected")+" %s %s "+_("through")+" %s %s")%(self.getCellAddress(first),self.getCellText(first),self.getCellAddress(last),self.getCellText(last)))
			else:
				text=self.getCellAddress(self.getActiveCell())
				if self.cellHasFormula(self.getActiveCell()):
					text+=" "+_("has formula")
				text+=" %s"%self.getCellText(self.getActiveCell())
				speech.speakMessage(text)
		except:
			pass

	def getFontName(self,cell):
		return cell.Font.Name

	def getFontSize(self,cell):
		return int(cell.Font.Size)

	def isBold(self,cell):
		return cell.Font.Bold

	def isItalic(self,cell):
		return cell.Font.Italic

	def isUnderline(self,cell):
		return cell.Font.Underline

	def event_gainFocus(self):
		super(ExcelGrid,self).event_gainFocus()
		self.speakSelection()

	def script_moveByCell(self,keyPress):
		"""Moves to a cell and speaks its coordinates and content"""
		sendKey(keyPress)
		self.speakSelection()
	script_moveByCell.__doc__=_("Moves to a cell and speaks its coordinates and content")

	def script_editCell(self,keyPress):
		cell=self.getSelectedRange().Item(1)
		cellEditDialog=CellEditDialog(cell)
		cellEditDialog.run()

	def text_reportPresentation(self,offset):
		"""Reports the current font name, font size, font attributes of the active cell"""
		speech.speakMessage(_("font")+": %s"%self.getFontName(self.getActiveCell()))
		speech.speakMessage("%s %s"%(self.getFontSize(self.getActiveCell()),_("point")))
		if self.isBold(self.getActiveCell()):
			speech.speakMessage(_("bold"))
		if self.isItalic(self.getActiveCell()):
			speech.speakMessage(_("italic"))
		if self.isUnderline(self.getActiveCell()):
			speech.speakMessage(_("underline"))

[ExcelGrid.bindKey(keyName,scriptName) for keyName,scriptName in [
	("Tab","moveByCell"),
	("Shift+Tab","moveByCell"),
	("ExtendedUp","moveByCell"),
	("ExtendedDown","moveByCell"),
	("ExtendedLeft","moveByCell"),
	("ExtendedRight","moveByCell"),
	("Control+ExtendedUp","moveByCell"),
	("Control+ExtendedDown","moveByCell"),
	("Control+ExtendedLeft","moveByCell"),
	("Control+ExtendedRight","moveByCell"),
	("ExtendedHome","moveByCell"),
	("ExtendedEnd","moveByCell"),
	("Control+ExtendedHome","moveByCell"),
	("Control+ExtendedEnd","moveByCell"),
	("Shift+ExtendedUp","moveByCell"),
	("Shift+ExtendedDown","moveByCell"),
	("Shift+ExtendedLeft","moveByCell"),
	("Shift+ExtendedRight","moveByCell"),
	("Shift+Control+ExtendedUp","moveByCell"),
	("Shift+Control+ExtendedDown","moveByCell"),
	("Shift+Control+ExtendedLeft","moveByCell"),
	("Shift+Control+ExtendedRight","moveByCell"),
	("Shift+ExtendedHome","moveByCell"),
	("Shift+ExtendedEnd","moveByCell"),
	("Shift+Control+ExtendedHome","moveByCell"),
	("Shift+Control+ExtendedEnd","moveByCell"),
	("f2","editCell"),
]]
