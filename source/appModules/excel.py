import time
import re
import ctypes
import comtypesClient
import comtypes.automation
import audio
import debug
from constants import *
from keyboardHandler import sendKey, key
from config import conf
import NVDAObjects
import lang
import _MSOffice

re_dollaredAddress=re.compile(r"^\$?([a-zA-Z]+)\$?([0-9]+)")

class appModule(_MSOffice.appModule):

	def __init__(self,*args):
		_MSOffice.appModule.__init__(self,*args)
		NVDAObjects.registerNVDAObjectClass(self.processID,"EXCEL6",ROLE_SYSTEM_CLIENT,NVDAObject_excelEditableCell)
		NVDAObjects.registerNVDAObjectClass(self.processID,"EXCEL7",ROLE_SYSTEM_CLIENT,NVDAObject_excelTable)

	def __del__(self):
		NVDAObjects.unregisterNVDAObjectClass("EXCEL6",ROLE_SYSTEM_CLIENT)
		NVDAObjects.unregisterNVDAObjectClass("EXCEL7",ROLE_SYSTEM_CLIENT)
		_MSOffice.appModule.__del__(self)

class NVDAObject_excelEditableCell(NVDAObjects.MSAA.NVDAObject_edit):

	def getRole(self):
		return ROLE_SYSTEM_TEXT
	role=property(fget=getRole)

class NVDAObject_excelTable(NVDAObjects.MSAA.NVDAObject_MSAA):

	def __init__(self,*args):
		NVDAObjects.MSAA.NVDAObject_MSAA.__init__(self,*args)
		ptr=ctypes.POINTER(comtypes.automation.IDispatch)()
		if ctypes.windll.oleacc.AccessibleObjectFromWindow(self.hwnd,OBJID_NATIVEOM,ctypes.byref(ptr._iid_),ctypes.byref(ptr))!=0:
			raise OSError("No native object model")
		self.excelObject=comtypesClient.wrap(ptr)
		self.registerScriptKeys({
			key("Insert+f"):self.script_formatInfo,
			key("ExtendedUp"):self.script_moveByCell,
			key("ExtendedDown"):self.script_moveByCell,
			key("ExtendedLeft"):self.script_moveByCell,
			key("ExtendedRight"):self.script_moveByCell,
			key("Control+ExtendedUp"):self.script_moveByCell,
			key("Control+ExtendedDown"):self.script_moveByCell,
			key("Control+ExtendedLeft"):self.script_moveByCell,
			key("Control+ExtendedRight"):self.script_moveByCell,
			key("ExtendedHome"):self.script_moveByCell,
			key("ExtendedEnd"):self.script_moveByCell,
			key("Control+ExtendedHome"):self.script_moveByCell,
			key("Control+ExtendedEnd"):self.script_moveByCell,
			key("Shift+ExtendedUp"):self.script_moveByCell,
			key("Shift+ExtendedDown"):self.script_moveByCell,
			key("Shift+ExtendedLeft"):self.script_moveByCell,
			key("Shift+ExtendedRight"):self.script_moveByCell,
			key("Shift+Control+ExtendedUp"):self.script_moveByCell,
			key("Shift+Control+ExtendedDown"):self.script_moveByCell,
			key("Shift+Control+ExtendedLeft"):self.script_moveByCell,
			key("Shift+Control+ExtendedRight"):self.script_moveByCell,
			key("Shift+ExtendedHome"):self.script_moveByCell,
			key("Shift+ExtendedEnd"):self.script_moveByCell,
			key("Shift+Control+ExtendedHome"):self.script_moveByCell,
			key("Shift+Control+ExtendedEnd"):self.script_moveByCell,
		})

	def getRole(self):
		return ROLE_SYSTEM_TABLE
	role=property(fget=getRole)

	def getSelectedRange(self):
		return self.excelObject.Selection
	selectedRange=property(fget=getSelectedRange)

	def getActiveCell(self):
		time.sleep(0.01)
		return self.excelObject.ActiveCell
	activeCell=property(fget=getActiveCell)

	def getCellAddress(self,cell):
		return re_dollaredAddress.sub(r"\1\2",cell.Address())

	def getCellText(self,cell):
		return cell.Text

	def cellHasFormula(self,cell):
		return cell.HasFormula

	def speakSelection(self):
		cells=self.getSelectedRange()
		if cells.Count>1:
			first=cells.Item(1)
			last=cells.Item(cells.Count)
			audio.speakMessage((lang.messages["selected"]+" %s %s "+lang.messages["through"]+" %s %s")%(self.getCellAddress(first),self.getCellText(first),self.getCellAddress(last),self.getCellText(last)))
		else:
			text=self.getCellAddress(self.getActiveCell())
			if self.cellHasFormula(self.getActiveCell()):
				text+=" "+lang.messages["hasFormula"]
			text+=" %s"%self.getCellText(self.getActiveCell())
			audio.speakMessage(text)

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
		self.speakObject()
		self.speakSelection()

	def script_moveByCell(self,keyPress):
		"""Moves to a cell and speaks its coordinates and content"""
		sendKey(keyPress)
		self.speakSelection()

	def script_formatInfo(self,keyPress):
		"""Reports the current font name, font size, font attributes of the active cell"""
		audio.speakMessage(lang.messages["font"]+": %s"%self.getFontName(self.getActiveCell()))
		audio.speakMessage("%s %s"%(self.getFontSize(self.getActiveCell()),lang.messages["point"]))
		if self.isBold(self.getActiveCell()):
			audio.speakMessage(lang.messages["bold"])
		if self.isItalic(self.getActiveCell()):
			audio.speakMessage(lang.messages["italic"])
		if self.isUnderline(self.getActiveCell()):
			audio.speakMessage(lang.messages["underline"])
