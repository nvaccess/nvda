import re
import comtypes.client
import comtypes.automation
import ctypes
import audio
import debug
from constants import *
from keyEventHandler import sendKey, key
from config import conf
import NVDAObjects
import _MSOffice

re_dollaredAddress=re.compile(r"^\$?([a-zA-Z]+)\$?([0-9]+)")

class appModule(_MSOffice.appModule):

	def __init__(self):
		_MSOffice.appModule.__init__(self)
		NVDAObjects.registerNVDAObjectClass("EXCEL6",ROLE_SYSTEM_CLIENT,NVDAObject_excelCell)
		NVDAObjects.registerNVDAObjectClass("EXCEL7",ROLE_SYSTEM_CLIENT,NVDAObject_excelTable)

	def __del__(self):
		NVDAObjects.unregisterNVDAObjectClass("EXCEL6",ROLE_SYSTEM_CLIENT)
		NVDAObjects.unregisterNVDAObjectClass("EXCEL7",ROLE_SYSTEM_CLIENT)
		_MSOffice.appModule.__del__(self)

class NVDAObject_excelCell(NVDAObjects.NVDAObject_edit):

	def getRole(self):
		return ROLE_SYSTEM_TEXT

class NVDAObject_excelTable(NVDAObjects.NVDAObject):

	def __init__(self,accObject):
		NVDAObjects.NVDAObject.__init__(self,accObject)
		ptr=ctypes.c_void_p()
		ctypes.windll.oleacc.AccessibleObjectFromWindow(self.getWindowHandle(),-16,ctypes.byref(comtypes.automation.IUnknown._iid_),ctypes.byref(ptr))
		ptr=ctypes.cast(ptr,ctypes.POINTER(comtypes.automation.IUnknown))
		self.excelObject=comtypes.client.wrap(ptr).Application
		self.keyMap.update({
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
})

	def stripAddress(self,address):
		return re_dollaredAddress.sub(r"\1\2",address)

	def getRole(self):
		return ROLE_SYSTEM_TABLE

	def getSelectedCells(self):
		addr=self.excelObject.Selection.Address()
		addrRange=addr.split(':')
		addrRange=map(lambda x: self.stripAddress(x),addrRange)
		if len(addrRange)==2:
			return addrRange
		else:
			return None

	def getCurrentCell(self):
		return self.stripAddress(self.excelObject.ActiveCell.Address())

	def getCellText(self,cell):
		return self.excelObject.Range(cell).Text

	def getCurrentCellText(self):
		return self.getCellText(self.getCurrentCell())

	def hasFormula(self,cell):
		return self.excelObject.Range(cell).HasFormula

	def speakCell(self,cell):
		audio.speakMessage("%s"%cell)
		audio.speakText("%s"%self.getCellText(cell))
		if self.hasFormula(cell):
			audio.speakMessage("has formula")

	def speakCurrentCell(self):
		return self.speakCell(self.getCurrentCell())

	def event_focusObject(self):
		if self.doneFocus:
			return
		NVDAObjects.NVDAObject.event_focusObject(self)
		self.speakCurrentCell()

	def script_moveByCell(self,keyPress):
		"""Moves to a cell and speaks its coordinates and content"""
		sendKey(keyPress)
		self.speakCurrentCell() 
