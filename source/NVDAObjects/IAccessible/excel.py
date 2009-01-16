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
import eventHandler
import gui
import gui.scriptUI
import IAccessibleHandler
import controlTypes
import speech
from keyUtils import sendKey, key
from . import IAccessible
import appModuleHandler
import NVDAObjects.window

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
		eventHandler.executeEvent("gainFocus",ExcelCell(self,self.getSelectedRange()))

	def script_moveByCell(self,keyPress):
		"""Moves to a cell and speaks its coordinates and content"""
		sendKey(keyPress)
		obj=ExcelCell(self,self.getSelectedRange())
		eventHandler.executeEvent('gainFocus',obj)
	script_moveByCell.__doc__=_("Moves to a cell and speaks its coordinates and content")
	script_moveByCell.canPropagate=True

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
]]

class ExcelCell(NVDAObjects.window.Window):

	def __init__(self,parentNVDAObject,cellRange):
		self.parent=parentNVDAObject
		self.firstCell=cellRange.Item(1)
		count=cellRange.count
		if count>1:
			self.lastCell=cellRange.Item(count)
		else:
			self.lastCell=None
		super(ExcelCell,self).__init__(parentNVDAObject.windowHandle)

	def _isEqual(self,other):
		if not super(ExcelCell,self)._isEqual(other):
			return False
		thisFirstAddr=self.parent.getCellAddress(self.firstCell)
		otherFirstAddr=other.parent.getCellAddress(other.firstCell)
		if thisFirstAddr!=otherFirstAddr:
			return False
		thisLastAddr=self.parent.getCellAddress(self.lastCell) if self.lastCell else ""
		otherLastAddr=other.parent.getCellAddress(other.lastCell) if other.lastCell else ""
		if thisLastAddr==otherLastAddr:
			return False
		return True

	def _get_name(self):
		firstAddr=self.parent.getCellAddress(self.firstCell)
		if not self.lastCell:
			return firstAddr
		lastAddr=self.parent.getCellAddress(self.lastCell)
		return _("selected")

	def _get_role(self):
		if self.lastCell:
			return controlTypes.ROLE_GROUPING
		else:
			return controlTypes.ROLE_TABLECELL

	def _get_value(self):
		if not self.lastCell: 
			return self.parent.getCellText(self.firstCell)
		else:
			return ("%s %s "+_("through")+" %s %s")%(self.parent.getCellAddress(self.firstCell),self.parent.getCellText(self.firstCell),self.parent.getCellAddress(self.lastCell),self.parent.getCellText(self.lastCell))

	def _get_description(self):
		if not self.lastCell and self.parent.cellHasFormula(self.firstCell):
			return _("has formula")

	def script_editCell(self,keyPress):
		cellEditDialog=CellEditDialog(self.parent.getActiveCell())
		cellEditDialog.run()

ExcelCell.bindKey("f2","editCell")
