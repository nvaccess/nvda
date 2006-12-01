import ctypes
import comtypesClient
import comtypes.automation
from constants import *
import debug
import winUser
import MSAAHandler
import audio
import NVDAObjects
import baseType

NAVRELATION_EMBEDS=0x1009 

class virtualBuffer_gecko(baseType.virtualBuffer):

	def __init__(self,NVDAObject):
		baseType.virtualBuffer.__init__(self,NVDAObject)
		debug.writeMessage("virtualBuffer gecko")
		if not self.NVDAObject.states&STATE_SYSTEM_BUSY:
			self.loadDocument()

	def event_stateChange(self,hwnd,objectID,childID):
		NVDAObject=NVDAObjects.getNVDAObjectByLocator(hwnd,objectID,childID)
		if (NVDAObject.role==ROLE_SYSTEM_DOCUMENT):
			if NVDAObject.states&STATE_SYSTEM_BUSY:
				audio.speakMessage(_("Busy")+"...")
			else:
				self.NVDAObject=NVDAObject
				self.loadDocument()

	def loadDocument(self):
		if winUser.getAncestor(self.NVDAObject.hwnd,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			audio.speakMessage(_("Loading document")+" "+self.NVDAObject.name+"...")
		self.fillBuffer(self.NVDAObject)
		self.caretPosition=0
		if winUser.getAncestor(self.NVDAObject.hwnd,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			audio.speakText(self.text)

	def getIDMessage(self,ID):
		NVDAObject=NVDAObjects.getNVDAObjectByLocator(self.NVDAObject.hwnd,OBJID_CLIENT,ID)
		return "%s %s"%(NVDAObject.typeString,NVDAObject.getStateNames(NVDAObject.states))

	def getIDText(self,ID):
		NVDAObject=NVDAObjects.getNVDAObjectByLocator(self.NVDAObject.hwnd,OBJID_CLIENT,ID)
		return "%s %s\n"%(NVDAObject.name,NVDAObject.value)

	def getIDAncestors(self,ID):
		NVDAObject=NVDAObjects.getNVDAObjectByLocator(self.NVDAObject.hwnd,OBJID_CLIENT,ID)
		l=[]
		while NVDAObject and (ID<0):
			l.append(ID)
 			NVDAObject=NVDAObject.parent
		l.reverse()
		return l
 
	def getIDFromNVDAObject(self,NVDAObject):
		guid=comtypes.GUID()
		guid.Data1=0x0c539790
		guid.Data2=0x12e4
		guid.data3=0x11cf
		guid.Data4=(ctypes.c_byte*8)(0xb6,0x61,0x00,0xaa,0x00,0x4c,0xd6,0xd8)
		#guid=comtypes.GUID('{0c539790-12e4-11cf-b661-00aa004cd6d8}')
		disp=NVDAObject.ia.QueryInterface(comtypesClient.GetModule('./servprov.tlb').IServiceProvider)
		debug.writeMessage("IDFromNVDAObject: %s"%disp)
		disp=disp.RemoteQueryService(guid,comtypes.GUID('{1814ceeb-49e2-407f-af99-fa755a7d2607}'))
		debug.writeMessage("IDFromNVDAObject: %s"%disp)
		disp=comtypesClient.wrap(disp)
		debug.writeMessage("IDFromNVDAObject: %s"%disp)
		try:
			res=disp.nodeInfo
			debug.writeMessage("IDFromNVDAObject: %s"%res)
			return res
		except:
			debug.writeException("Not an ISimpleDomNode")
			return None



	def fillBuffer(self,NVDAObject):
		ID=self.getIDFromNVDAObject(NVDAObject)
		self.appendText(ID,self.getIDText(ID))
		child=NVDAObject.firstChild
		while child:
			self.fillBuffer(child)
			child=child.next
