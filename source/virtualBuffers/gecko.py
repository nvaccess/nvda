import time
import ctypes
import comtypesClient
import comtypes.automation
from constants import *
import debug
import winUser
import MSAAHandler
import audio
import api
import NVDAObjects
from baseType import *

NAVRELATION_EMBEDS=0x1009 

class virtualBuffer_gecko(virtualBuffer):

	def __init__(self,NVDAObject):
		virtualBuffer.__init__(self,NVDAObject)
		audio.speakMessage("gecko virtualBuffer %s %s"%(self.NVDAObject.name,self.NVDAObject.typeString))
		#(pacc,child)=MSAAHandler.accessibleObjectFromEvent(self.NVDAObject.windowHandle,0,0)
		#(pacc,child)=MSAAHandler.accNavigate(pacc,child,NAVRELATION_EMBEDS)
		#self.NVDAObject=NVDAObjects.MSAA.NVDAObject_MSAA(pacc,child)
		audio.speakMessage("gecko virtualBuffer %s %s"%(self.NVDAObject.name,self.NVDAObject.typeString))
		if self.isDocumentComplete():
			self.loadDocument()

	def event_MSAA_gainFocus(self,hwnd,objectID,childID):
		obj=NVDAObjects.MSAA.getNVDAObjectFromEvent(hwnd,objectID,childID)
		if not obj:
			return False
		role=obj.role
		states=obj.states
		if (role==ROLE_SYSTEM_DOCUMENT) and not (states&STATE_SYSTEM_BUSY) and (states&STATE_SYSTEM_READONLY) and ((self.NVDAObject.role !=ROLE_SYSTEM_DOCUMENT) or self.neverLoaded):
			self.NVDAObject=obj
			self.loadDocument()
			return False
		if (role not in [ROLE_SYSTEM_TEXT,ROLE_SYSTEM_CHECKBUTTON,ROLE_SYSTEM_RADIOBUTTON,ROLE_SYSTEM_COMBOBOX]) and api.isVirtualBufferPassThrough():
  			api.toggleVirtualBufferPassThrough()
		if not self._allowCaretMovement:
			return False
		ID=self.getNVDAObjectID(obj)
		r=self.getRangeFromID(ID)
		if (r is not None) and (len(r)==2) and ((self.caretPosition<r[0]) or (self.caretPosition>=r[1])):
			self.caretPosition=r[0]
			if conf["virtualBuffers"]["reportVirtualPresentationOnFocusChanges"]:
				self.reportCaretIDMessages()
				audio.speakText(self.getTextRange(r[0],r[1]))
				api.setFocusObject(obj)
				api.setNavigatorObject(obj)
				return True
		return False

	def event_MSAA_scrollingStart(self,hwnd,objectID,childID):
		audio.speakMessage("scroll")
		obj=NVDAObjects.MSAA.getNVDAObjectFromEvent(hwnd,objectID,childID)
		if not obj:
			return False
		role=obj.role
		states=obj.states
		if not self._allowCaretMovement:
			return False
		ID=self.getNVDAObjectID(obj)
		audio.speakMessage("ID: %s, obj: %s"%(ID,obj.role))
		r=self.getRangeFromID(ID)
		if (r is not None) and (len(r)==2) and ((self.caretPosition<r[0]) or (self.caretPosition>=r[1])):
			self.caretPosition=r[0]
			self.reportCaretIDMessages()
			audio.speakText(self.getTextRange(r[0],r[1]))

	def event_MSAA_stateChange(self,hwnd,objectID,childID):
		obj=NVDAObjects.MSAA.getNVDAObjectFromEvent(hwnd,objectID,childID)
		if (obj.role==ROLE_SYSTEM_DOCUMENT) and (obj.states&STATE_SYSTEM_BUSY):
			audio.speakMessage(MSAAHandler.getStateName(STATE_SYSTEM_BUSY))
		return False

	def event_MSAA_valueChange(self,hwnd,objectID,childID):
		audio.speakMessage('value')
		return False

	def activatePosition(self,pos):
		IDs=self.getIDsFromPosition(pos)
		if (IDs is None) or (len(IDs)<1):
			return
		obj=self._IDs[IDs[-1]]["node"]
		if obj is None:
			return
		role=obj.role
		states=obj.states
		nodeInfo=self.getNVDAObjectInfo(obj)
		if role in [ROLE_SYSTEM_TEXT,ROLE_SYSTEM_COMBOBOX]:
			if not api.isVirtualBufferPassThrough():
				api.toggleVirtualBufferPassThrough()
			obj.doDefaultAction()
		if role in [ROLE_SYSTEM_CHECKBUTTON,ROLE_SYSTEM_RADIOBUTTON]:
			obj.doDefaultAction()
			audio.speakMessage("%s"%(MSAAHandler.getStateName(STATE_SYSTEM_CHECKED) if obj.states&STATE_SYSTEM_CHECKED else _("not")+" "+MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)))
		elif role==ROLE_SYSTEM_PUSHBUTTON:
			obj.doDefaultAction()
		elif role in [ROLE_SYSTEM_LINK,ROLE_SYSTEM_GRAPHIC]:
			obj.doDefaultAction()

	def isDocumentComplete(self):
		role=self.NVDAObject.role
		states=self.NVDAObject.states
		if (role==ROLE_SYSTEM_DOCUMENT) and not (states&STATE_SYSTEM_BUSY) and (states&STATE_SYSTEM_READONLY):
			return True
		else:
			return False

	def loadDocument(self):
		if winUser.getAncestor(self.NVDAObject.windowHandle,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			if api.isVirtualBufferPassThrough():
				api.toggleVirtualBufferPassThrough()
			audio.speakMessage(_("Loading document")+" "+self.NVDAObject.name+"...")
		self.resetBuffer()
		self.fillBuffer(self.NVDAObject)
		self.caretPosition=0
		self.neverLoaded=False
		if winUser.getAncestor(self.NVDAObject.windowHandle,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			self.caretPosition=0
			self._allowCaretMovement=False #sayAllGenerator will set this back to true when done
			time.sleep(0.01)
			audio.speakMessage(_("done"))
			core.newThread(self.sayAllGenerator())

	def fillBuffer(self,obj,IDAncestors=(),position=None):
		debug.writeMessage("virtualBuffers.gecko.fillBuffer: %s %s %s %s"%(obj.name,MSAAHandler.getRoleName(obj.role),obj.value,obj.description))
		info=self.getNVDAObjectInfo(obj)
		ID=self.getNVDAObjectID(obj)
		if ID and ID not in IDAncestors:
			IDAncestors=tuple(list(IDAncestors)+[ID])
		if ID and not self._IDs.has_key(ID):
			self.addID(ID,**info)
		text=self.getNVDAObjectText(obj)
		if text:
			position=self.addText(IDAncestors,text,position=position)
		#We don't want to render objects inside comboboxes
		if obj.role==ROLE_SYSTEM_COMBOBOX:
			return position
		#For everything else we keep walking the tree
		else:
			child=obj.firstChild
			while child:
				position=self.fillBuffer(child,IDAncestors,position=position)
				child=child.next
			return position

	def getNVDAObjectID(self,obj):
		if obj.role!=ROLE_SYSTEM_STATICTEXT:
			return ctypes.cast(obj._pacc,ctypes.c_void_p).value

	def getNVDAObjectText(self,obj):
		role=obj.role
		states=obj.states
		if role==ROLE_SYSTEM_STATICTEXT:
			data=obj.value
			if data and not data.isspace():
				return "%s "%data
		if role==ROLE_SYSTEM_DOCUMENT:
			return "%s\n "%obj.name
		elif role==ROLE_SYSTEM_GRAPHIC:
			return obj.name+" " 
		elif role==ROLE_SYSTEM_COMBOBOX:
			return obj.value+" "
		elif role==ROLE_SYSTEM_CHECKBUTTON:
			return obj.name+" "
		elif role==ROLE_SYSTEM_RADIOBUTTON:
			return obj.name+" "
		elif role==ROLE_SYSTEM_TEXT:
			return obj.value+"\0"
		elif role==ROLE_SYSTEM_PUSHBUTTON:
			return obj.name+" "
		elif role=="white space":
			return obj.name.replace('\r\n','\n')

	def getNVDAObjectInfo(self,obj):
		info=fieldInfo.copy()
		info["node"]=obj
		role=obj.role
		states=obj.states
		if role=="frame":
			info["fieldType"]=fieldType_frame
			info["typeString"]=fieldNames[fieldType_frame]
		elif role==ROLE_SYSTEM_DOCUMENT:
			info["fieldType"]=fieldType_document
			info["typeString"]=fieldNames[fieldType_document]
		elif role==ROLE_SYSTEM_LINK:
			info["fieldType"]=fieldType_link
			info["typeString"]=fieldNames[fieldType_link]
		elif role=="p":
			info["fieldType"]=fieldType_paragraph
			info["typeString"]=fieldNames[fieldType_paragraph]
		elif role==ROLE_SYSTEM_TABLE:
			info["fieldType"]=fieldType_table
			info["typeString"]=fieldNames[fieldType_table]
		elif role==ROLE_SYSTEM_LIST:
			info["fieldType"]=fieldType_list
			info["typeString"]=fieldNames[fieldType_list]
			info["descriptionFunc"]=lambda x: "with %s items"%x.childCount
		elif role==ROLE_SYSTEM_LISTITEM:
			info["fieldType"]=fieldType_listItem
			info["typeString"]=_("bullit item")
		elif role=="dl":
			info["fieldType"]=fieldType_list
			info["typeString"]=_("definition")+" "+fieldNames[fieldType_list]
			info["descriptionFunc"]=lambda x: "with %s items"%x.childCount
		elif role=="dt":
			info["fieldType"]=fieldType_listItem
			info["typeString"]=_("bullit item")
		elif role=="dd":
			info["fieldType"]=fieldType_listItem
			info["typeString"]=_("definition")
		elif role==ROLE_SYSTEM_GRAPHIC:
			info["fieldType"]=fieldType_graphic
			info["typeString"]=fieldNames[fieldType_graphic]
		elif role in ["h1","h2","h3","h4","h5","h6"]:
			info["fieldType"]=fieldType_heading
			info["typeString"]=fieldNames[fieldType_heading]+" %s"%role[1]
		elif role=="blockQuote":
			info["fieldType"]=fieldType_blockQuote
			info["typeString"]=fieldNames[fieldType_blockQuote]
		elif role==ROLE_SYSTEM_PUSHBUTTON:
			info["fieldType"]=fieldType_button
			info["typeString"]=fieldNames[fieldType_button]
		elif role==ROLE_SYSTEM_RADIOBUTTON:
			info["fieldType"]=fieldType_radioButton
			info["typeString"]=fieldNames[fieldType_radioButton]
			info["stateTextFunc"]=lambda x: MSAAHandler.getStateName(STATE_SYSTEM_CHECKED) if x.states&STATE_SYSTEM_CHECKED else _("not")+" "+MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)
		elif role==ROLE_SYSTEM_CHECKBUTTON:
			info["fieldType"]=fieldType_checkBox
			info["typeString"]=fieldNames[fieldType_checkBox]
			info["stateTextFunc"]=lambda x: MSAAHandler.getStateName(STATE_SYSTEM_CHECKED) if x.states&STATE_SYSTEM_CHECKED else _("not")+" "+MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)
		elif role==ROLE_SYSTEM_TEXT:
			info["fieldType"]=fieldType_edit
			info["typeString"]=fieldNames[fieldType_edit]
		elif role==ROLE_SYSTEM_COMBOBOX:
			info["fieldType"]=fieldType_comboBox
			info["typeString"]=fieldNames[fieldType_comboBox]
		else:
			info["typeString"]=MSAAHandler.getRoleName(role) if isinstance(role,int) else role
		accessKey=obj.keyboardShortcut
		if accessKey:
			info["accessKey"]=accessKey
		return info
 
