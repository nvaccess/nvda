#virtualBuffers/gecko.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import ctypes
import debug
import core
import tones
import winUser
import IAccessibleHandler
import speech
import api
import config
import controlTypes
import NVDAObjects
from .. import virtualBuffer

NAVRELATION_EMBEDS=0x1009 

lastLoadTime=0

def getMozillaRole(role):
	if isinstance(role,basestring):
		split=role.split(', ')
		return split[0]
	else:
		return role

class Gecko(virtualBuffer):

	def __init__(self,NVDAObject):
		virtualBuffer.__init__(self,NVDAObject)
		#(pacc,child)=IAccessibleHandler.accessibleObjectFromEvent(self.NVDAObject.windowHandle,0,0)
		#(pacc,child)=IAccessibleHandler.accNavigate(NVDAObject.IAccessibleObject,NVDAObject._accChild,NAVRELATION_EMBEDS)
		#newObj=NVDAObjects.IAccessible.IAccessible(pacc,child)
		#if newObj:
		#	self.NVDAObject=newObj
		speech.speakMessage("gecko virtualBuffer %s %s"%(self.NVDAObject.name,_("document")))
		if self.isDocumentComplete():
			self.loadDocument()

	def event_gainFocus(self,obj,nextHandler):
		role=getMozillaRole(obj.IAccessibleRole)
		states=obj.IAccessibleStates
		if (role==IAccessibleHandler.ROLE_SYSTEM_DOCUMENT) and (states&IAccessibleHandler.STATE_SYSTEM_READONLY):
			if (states&IAccessibleHandler.STATE_SYSTEM_BUSY):
				speech.speakMessage(IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_BUSY))
			elif self.getNVDAObjectID(obj)!=self.getNVDAObjectID(self.NVDAObject): 
				self.NVDAObject=obj
				self.loadDocument()
			return True
		ID=self.getNVDAObjectID(obj)
		if not self._IDs.has_key(ID):
			return nextHandler()
		r=self.getFullRangeFromID(ID)
		if ((self.text_reviewOffset<r[0]) or (self.text_reviewOffset>=r[1])):
			self.text_reviewOffset=r[0]
		if not api.isVirtualBufferPassThrough() and config.conf["virtualBuffers"]["reportVirtualPresentationOnFocusChanges"]:
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			speech.speakText(self.text_getText(r[0],r[1]))
			api.setFocusObject(obj)
			api.setNavigatorObject(obj)
			return True
		return nextHandler()

	def event_scrollingStart(self,obj,nextHandler):
		ID=self.getNVDAObjectID(obj)
		if not self._IDs.has_key(ID):
			return nextHandler()
		r=self._IDs[ID]['range']
		if ((self.text_reviewOffset<r[0]) or (self.text_reviewOffset>=r[1])):
			self.text_reviewOffset=r[0]
			self.text_reportNewPresentation(self.text_reviewOffset)
			speech.speakText(self.text_getText(r[0],r[1]))

	def event_stateChange(self,obj,nextHandler):
		role=getMozillaRole(obj.IAccessibleRole)
		states=obj.IAccessibleStates
		if (role==IAccessibleHandler.ROLE_SYSTEM_DOCUMENT) and (states&IAccessibleHandler.STATE_SYSTEM_READONLY):
			if states&IAccessibleHandler.STATE_SYSTEM_BUSY:
				speech.speakMessage(IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_BUSY))
				return True
			elif self.getNVDAObjectID(obj)!=self.getNVDAObjectID(self.NVDAObject):
				self.NVDAObject=obj
				self.loadDocument()
				return True
		return nextHandler()

	def event_reorder(self,obj,nextHandler):
		if not config.conf["virtualBuffers"]["updateContentDynamically"]:
			return nextHandler() 
		if self.NVDAObject.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_BUSY:
			return nextHandler()
		#obj.speakObject()
		ID=self.getNVDAObjectID(obj)
		debug.writeMessage("virtualBuffers.gecko.event_IAccessible_reorder: ID %s"%ID)
		if ID not in self._IDs:
			return nextHandler()
		parentID=self._IDs[ID]['parent']
		r=self._IDs[ID]['range']
		zOrder=self.getIDZOrder(ID)
		if len(zOrder)>0:
			childNum=zOrder[-1]
		else:
			childNum=0
		debug.writeMessage("virtualBuffers.gecko.event_IAccessible_reorder: range %s"%str(r))
		self.removeID(ID)
		if parentID is not None:
			self._IDs[parentID]['children'].insert(childNum,ID)
		self.fillBuffer(obj,parentID,position=r[0])
		textLen=self.text_characterCount
		if self.text_reviewOffset>=textLen:
			self.text_reviewOffset=textLen-1

	def activatePosition(self,pos):
		ID=self.getIDFromPosition(pos)
		obj=self._IDs[ID]["node"]
		if obj is None:
			return
		role=getMozillaRole(obj.IAccessibleRole)
		states=obj.IAccessibleStates
		if (role==IAccessibleHandler.ROLE_SYSTEM_TEXT and not states&IAccessibleHandler.STATE_SYSTEM_READONLY) or role==IAccessibleHandler.ROLE_SYSTEM_COMBOBOX:
			if not api.isVirtualBufferPassThrough():
				api.toggleVirtualBufferPassThrough()
			obj.setFocus()
		else:
			obj.doDefaultAction()
			obj.setFocus()
			return
		if role in [IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON,IAccessibleHandler.ROLE_SYSTEM_RADIOBUTTON]:
			obj.doDefaultAction()
			obj.setFocus()
		elif role==IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON:
			obj.doDefaultAction()
		elif role in [IAccessibleHandler.ROLE_SYSTEM_LINK,IAccessibleHandler.ROLE_SYSTEM_GRAPHIC]:
			obj.doDefaultAction()
			obj.setFocus()

	def isDocumentComplete(self):
		role=self.NVDAObject.role
		states=self.NVDAObject.IAccessibleStates
		if (role==controlTypes.ROLE_DOCUMENT) and not (states&IAccessibleHandler.STATE_SYSTEM_BUSY) and (states&IAccessibleHandler.STATE_SYSTEM_READONLY):
			return True
		else:
			return False

	def loadDocument(self):
		global lastLoadTime
		if winUser.getAncestor(self.NVDAObject.windowHandle,winUser.GA_ROOT)==winUser.getForegroundWindow():
			speech.cancelSpeech()
			if api.isVirtualBufferPassThrough():
				api.toggleVirtualBufferPassThrough()
			speech.speakMessage(_("loading document %s")%self.NVDAObject.name+"...")
		self.resetBuffer()
		debug.writeMessage("virtualBuffers.gecko.loadDocument: load start") 
		self.fillBuffer(self.NVDAObject)
		debug.writeMessage("virtualBuffers.gecko.loadDocument: load end")
		lastLoadTime=time.time()
		if winUser.getAncestor(self.NVDAObject.windowHandle,winUser.GA_ROOT)==winUser.getForegroundWindow():
			speech.cancelSpeech()
			self.text_reviewOffset=0
			speech.speakMessage(_("done"))
			time.sleep(0.001)
			self.text_speakLine(0)

	def fillBuffer(self,obj,parentID=None,position=None):
		getNVDAObjectID=self.getNVDAObjectID
		role=getMozillaRole(obj.IAccessibleRole)
		states=obj.IAccessibleStates
		text=""
		if position is None:
			position=self.text_characterCount
		ID=getNVDAObjectID(obj)
		if ID is None:
			ID=parentID
		#Collect the children
		#Use IAccessible directly to save time
		#Don't get children of combo boxes or embed objects
		if obj.childCount>0 and role not in [IAccessibleHandler.ROLE_SYSTEM_COMBOBOX,"embed",IAccessibleHandler.ROLE_SYSTEM_LINK]:
			windowHandle=obj.windowHandle
			IAccessible=NVDAObjects.IAccessible.IAccessible
			hwnd=obj.windowHandle
			children=[IAccessible(x[0],x[1],windowHandle=hwnd) for x in IAccessibleHandler.accessibleChildren(obj.IAccessibleObject,0,obj.childCount)]
		else:
			children=[]
		#Get rid of the bullet object if this was a list item's children (its in the name)
		if (role==IAccessibleHandler.ROLE_SYSTEM_LISTITEM) and (len(children)>0) and (children[0].role in [IAccessibleHandler.ROLE_SYSTEM_STATICTEXT,'bullet']):
			del children[0]
		#Get the info and text depending on the node type
		info=self.fieldInfoTemplate.copy()
		info["node"]=obj
		info['range']=[position,position]
		info['parent']=parentID
		info['children']=[x for x in [getNVDAObjectID(y) for y in children ] if x is not None]
		info['labeledBy']=getNVDAObjectID(obj.labeledBy)
		if role==IAccessibleHandler.ROLE_SYSTEM_TEXT and states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			data=obj.name
			if data and not data.isspace():
				text="%s"%data
		elif role=="white space":
			text=obj.name.replace('\r\n','\n')
		elif role=="frame":
			info["role"]=controlTypes.ROLE_FRAME
		if role=="iframe":
			info["role"]=controlTypes.ROLE_FRAME
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_FRAME]
		elif role==IAccessibleHandler.ROLE_SYSTEM_DOCUMENT:
			text="%s \n "%obj.name
			info["role"]=controlTypes.ROLE_DOCUMENT
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_DOCUMENT]
		elif role==IAccessibleHandler.ROLE_SYSTEM_LINK and states&IAccessibleHandler.STATE_SYSTEM_LINKED:
			info["role"]=controlTypes.ROLE_LINK
			if True:
				text=obj.name
				if not text or text.isspace():
					text=obj.description
				if not text or text.isspace():
					text=obj.value
				if text:
					text=text.strip()
		elif role=="p":
			info["role"]=controlTypes.ROLE_PARAGRAPH
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_PARAGRAPH]
		elif role==IAccessibleHandler.ROLE_SYSTEM_CELL:
			info["role"]=controlTypes.ROLE_TABLECELL
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_TABLECELL]
		elif role==IAccessibleHandler.ROLE_SYSTEM_TABLE:
			info["role"]=controlTypes.ROLE_TABLE
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_TABLE]
		elif role==IAccessibleHandler.ROLE_SYSTEM_ROW:
			info["role"]=controlTypes.ROLE_TABLEROW
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_TABLEROW]
		elif role=="thead":
			info["role"]=controlTypes.ROLE_TABLEHEADER
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_TABLEHEADER]
		elif role=="tfoot":
			info["role"]=controlTypes.ROLE_TABLEFOOTER
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_TABLEFOOTER]
		elif role=="tbody":
			info["role"]=controlTypes.ROLE_TABLEBODY
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_TABLEBODY]
		elif role in [IAccessibleHandler.ROLE_SYSTEM_LIST,"ul"]:
			info["role"]=controlTypes.ROLE_LIST
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_LIST]
			info["descriptionFunc"]=lambda x: "with %s items"%x.childCount
		elif role==IAccessibleHandler.ROLE_SYSTEM_LISTITEM:
			info["role"]=controlTypes.ROLE_LISTITEM
			bullet=obj.name
			bullet=bullet.rstrip() if isinstance(bullet,basestring) else ""
			if not bullet or (len(bullet)>0 and ord(bullet[0])>127):
				bullet=_("bullet")
			info["typeString"]=bullet
		elif role=="dl":
			info["role"]=controlTypes.ROLE_LIST
			info["typeString"]=_("definition")+" "+controlTypes.speechRoleLabels[controlTypes.ROLE_LIST]
			info["descriptionFunc"]=lambda x: _("with %s items")%x.childCount
		elif role=="dt":
			info["role"]=controlTypes.ROLE_LISTITEM
			bullet=obj.name
			bullet = bullet.rstrip() if isinstance(bullet,basestring) else ""
			if not bullet:
				bullet=_("bullet")
			elif bullet.endswith('.'):
				bullet=bullet[0:-1]
			info["typeString"]=bullet
		elif role=="dd":
			info["role"]=controlTypes.ROLE_LISTITEM
			info["typeString"]=_("definition")
		elif role==IAccessibleHandler.ROLE_SYSTEM_GRAPHIC:
			text="%s"%obj.name
			if not text and states&IAccessibleHandler.STATE_SYSTEM_LINKED:
				text=" "
			info["role"]=controlTypes.ROLE_GRAPHIC
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_GRAPHIC]
		elif role in ["h1","h2","h3","h4","h5","h6"]:
			info["role"]=getattr(controlTypes,"ROLE_HEADING%s"%role[1:])
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_HEADING]+" %s"%role[1]
		elif role=="blockquote":
			info["role"]=controlTypes.ROLE_BLOCKQUOTE
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_BLOCKQUOTE]
		elif role=="q":
			info["role"]=controlTypes.ROLE_BLOCKQUOTE
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_BLOCKQUOTE]
		elif role==IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON:
			text="%s "%obj.name
			info["role"]=controlTypes.ROLE_BUTTON
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_BUTTON]
		elif role=="form":
			info["role"]=controlTypes.ROLE_FORM
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_FORM]
		elif role==IAccessibleHandler.ROLE_SYSTEM_RADIOBUTTON:
			text="%s "%obj.name
			info["role"]=controlTypes.ROLE_RADIOBUTTON
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_RADIOBUTTON]
			info["stateTextFunc"]=lambda x: IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_CHECKED) if x.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_CHECKED else _("not %s")%IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_CHECKED)
		elif role==IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON:
			text="%s "%obj.name
			info["role"]=controlTypes.ROLE_CHECKBOX
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_CHECKBOX]
			info["stateTextFunc"]=lambda x: IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_CHECKED) if x.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_CHECKED else _("not %s")%IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_CHECKED)
		elif role==IAccessibleHandler.ROLE_SYSTEM_TEXT and not states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			val=obj.value
			if val=="":
				val="\0"
			text=val
			info["role"]=controlTypes.ROLE_EDITABLETEXT
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_EDITABLETEXT]
			if obj.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_PROTECTED:
				info["typeString"]=_("protected %s")%info["typeString"]
		elif role==IAccessibleHandler.ROLE_SYSTEM_COMBOBOX:
			text="%s "%obj.value
			info["role"]=controlTypes.ROLE_COMBOBOX
			info["typeString"]=controlTypes.speechRoleLabels[controlTypes.ROLE_COMBOBOX]
		else:
			info["typeString"]=IAccessibleHandler.getRoleName(role) if isinstance(role,int) else role
		accessKey=obj.keyboardShortcut
		if accessKey:
			info["accessKey"]=accessKey
		if ID not in self._IDs:
			self.addID(ID,info)
		if text:
			position=self.addText(ID,text,position)
		#We don't want to render objects inside comboboxes
		func=self.fillBuffer
		for child in children:
			position=func(child,ID,position)
		#if role==IAccessibleHandler.ROLE_SYSTEM_DOCUMENT:
		#	position=self.addText(ID," ",position)
		return position

	def getNVDAObjectID(self,obj):
		if not obj:
			return None
		if getMozillaRole(obj.IAccessibleRole)!=IAccessibleHandler.ROLE_SYSTEM_TEXT or obj.childCount>0 or not obj.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_READONLY:
			return ctypes.cast(obj.IAccessibleObject,ctypes.c_void_p).value

