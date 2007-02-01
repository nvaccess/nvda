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
import audio
import api
import config
import NVDAObjects
from baseType import *

NAVRELATION_EMBEDS=0x1009 

lastLoadTime=0

def getMozillaRole(role):
	if isinstance(role,basestring):
		split=role.split(', ')
		return split[0]
	else:
		return role

class virtualBuffer_gecko(virtualBuffer):

	def __init__(self,NVDAObject):
		virtualBuffer.__init__(self,NVDAObject)
		#(pacc,child)=IAccessibleHandler.accessibleObjectFromEvent(self.NVDAObject.windowHandle,0,0)
		#(pacc,child)=IAccessibleHandler.accNavigate(pacc,child,NAVRELATION_EMBEDS)
		#self.NVDAObject=NVDAObjects.IAccessible.NVDAObject_IAccessible(pacc,child)
		audio.speakMessage("gecko virtualBuffer %s %s"%(self.NVDAObject.name,self.NVDAObject.typeString))
		if self.isDocumentComplete():
			self.loadDocument()

	def event_IAccessible_gainFocus(self,hwnd,objectID,childID):
		obj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(hwnd,objectID,childID)
		if not obj:
			return False
		role=getMozillaRole(obj.role)
		states=obj.states
		if (role==IAccessibleHandler.ROLE_SYSTEM_DOCUMENT) and (states&IAccessibleHandler.STATE_SYSTEM_READONLY):
			if (states&IAccessibleHandler.STATE_SYSTEM_BUSY):
				audio.speakMessage(IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_BUSY))
			elif self.getNVDAObjectID(obj)!=self.getNVDAObjectID(self.NVDAObject): 
				self.NVDAObject=obj
				self.loadDocument()
			return True
		ID=self.getNVDAObjectID(obj)
		if not self._IDs.has_key(ID):
			return False
		r=self.getFullRangeFromID(ID)
		if ((self.caretPosition<r[0]) or (self.caretPosition>=r[1])):
			self.caretPosition=r[0]
		if not api.isVirtualBufferPassThrough() and config.conf["virtualBuffers"]["reportVirtualPresentationOnFocusChanges"]:
			self.reportLabel(self.getIDFromPosition(self.caretPosition))
			self.reportCaretIDMessages()
			audio.speakText(self.getTextRange(r[0],r[1]))
			api.setFocusObject(obj)
			api.setNavigatorObject(obj)
			return True
		return False

	def event_IAccessible_scrollingStart(self,hwnd,objectID,childID):
		audio.speakMessage("scroll")
		obj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(hwnd,objectID,childID)
		if not obj:
			return False
		ID=self.getNVDAObjectID(obj)
		if not self._IDs.has_key(ID):
			return
		r=self._IDs[ID]
		if ((self.caretPosition<r[0]) or (self.caretPosition>=r[1])):
			self.caretPosition=r[0]
			self.reportCaretIDMessages()
			audio.speakText(self.getTextRange(r[0],r[1]))

	def event_IAccessible_stateChange(self,hwnd,objectID,childID):
		obj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(hwnd,objectID,childID)
		if not obj:
			return
		role=getMozillaRole(obj.role)
		states=obj.states
		if (role==IAccessibleHandler.ROLE_SYSTEM_DOCUMENT) and (states&IAccessibleHandler.STATE_SYSTEM_READONLY):
			if states&IAccessibleHandler.STATE_SYSTEM_BUSY:
				audio.speakMessage(IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_BUSY))
				return True
			elif self.getNVDAObjectID(obj)!=self.getNVDAObjectID(self.NVDAObject):
				self.NVDAObject=obj
				self.loadDocument()
				return True
		return False

	def event_IAccessible_reorder(self,hwnd,objectID,childID):
		if not config.conf["virtualBuffers"]["updateContentDynamically"]:
			return 
		if time.time()<(lastLoadTime+2):
			return
		obj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(hwnd,objectID,childID)
		if not obj:
			return
		tones.beep(440,100)
		debug.writeMessage("virtualBuffers.gecko.event_IAccessible_reorder: object (%s %s %s %s)"%(obj.name,obj.typeString,obj.value,obj.description))
		#obj.speakObject()
		ID=self.getNVDAObjectID(obj)
		debug.writeMessage("virtualBuffers.gecko.event_IAccessible_reorder: ID %s"%ID)
		if ID not in self._IDs:
			return
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
		textLen=len(self.text)
		if self.caretPosition>=textLen:
			self.caretPosition=textLen-1
		tones.beep(880,100)

	def activatePosition(self,pos):
		ID=self.getIDFromPosition(pos)
		obj=self._IDs[ID]["node"]
		if obj is None:
			return
		role=getMozillaRole(obj.role)
		states=obj.states
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
		states=self.NVDAObject.states
		if (role==IAccessibleHandler.ROLE_SYSTEM_DOCUMENT) and not (states&IAccessibleHandler.STATE_SYSTEM_BUSY) and (states&IAccessibleHandler.STATE_SYSTEM_READONLY):
			return True
		else:
			return False

	def loadDocument(self):
		global lastLoadTime
		if winUser.getAncestor(self.NVDAObject.windowHandle,winUser.GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			if api.isVirtualBufferPassThrough():
				api.toggleVirtualBufferPassThrough()
			audio.speakMessage(_("loading document %s")%self.NVDAObject.name+"...")
		self.resetBuffer()
		debug.writeMessage("virtualBuffers.gecko.loadDocument: load start") 
		self.fillBuffer(self.NVDAObject)
		debug.writeMessage("virtualBuffers.gecko.loadDocument: load end")
		lastLoadTime=time.time()
		if winUser.getAncestor(self.NVDAObject.windowHandle,winUser.GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			self.caretPosition=0
			audio.speakMessage(_("done"))
			time.sleep(0.001)
			self.speakLine(0)

	def fillBuffer(self,obj,parentID=None,position=None):
		getNVDAObjectID=self.getNVDAObjectID
		role=getMozillaRole(obj.role)
		states=obj.states
		text=""
		if position is None:
			position=len(self.text)
		ID=getNVDAObjectID(obj)
		#debug.writeMessage("virtualBuffers.gecko.fillBuffer: object (%s %s %s %s)"%(obj.name,obj.typeString,obj.value,obj.description))
		if ID is None:
			ID=parentID
		#Collect the children
		#Use IAccessible directly to save time
		#Don't get children of combo boxes or embed objects
		if obj.childCount>0 and role not in [IAccessibleHandler.ROLE_SYSTEM_COMBOBOX,"embed"]:
			hwnd=obj.windowHandle
			NVDAObject_IAccessible=NVDAObjects.IAccessible.NVDAObject_IAccessible
			children=[NVDAObject_IAccessible(x[0],x[1],hwnd=hwnd) for x in IAccessibleHandler.accessibleChildren(obj._pacc,0,obj.childCount)]
		else:
			children=[]
		#Get rid of the bullet object if this was a list item's children (its in the name)
		if (role==IAccessibleHandler.ROLE_SYSTEM_LISTITEM) and (len(children)>0) and (children[0].role in [IAccessibleHandler.ROLE_SYSTEM_STATICTEXT,'bullet']):
			del children[0]
		#Get the info and text depending on the node type
		info=fieldInfo.copy()
		info["node"]=obj
		info['range']=[position,position]
		info['parent']=parentID
		info['children']=[x for x in [getNVDAObjectID(y) for y in children ] if x is not None]
		info['labeledBy']=getNVDAObjectID(obj.labeledBy)
		if role==IAccessibleHandler.ROLE_SYSTEM_TEXT and states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			data=obj.value
			if data and not data.isspace():
				text="%s "%data
		elif role=="white space":
			text=obj.name.replace('\r\n','\n')
		elif role=="frame":
			info["fieldType"]=fieldType_frame
			info["typeString"]=fieldNames[fieldType_frame]
		if role=="iframe":
			info["fieldType"]=fieldType_frame
			info["typeString"]=fieldNames[fieldType_frame]
		elif role==IAccessibleHandler.ROLE_SYSTEM_DOCUMENT:
			text="%s\n "%obj.name
			info["fieldType"]=fieldType_document
			info["typeString"]=fieldNames[fieldType_document]
		elif role==IAccessibleHandler.ROLE_SYSTEM_LINK:
			info["fieldType"]=fieldType_link
			info["typeString"]=obj.typeString
		elif role=="p":
			info["fieldType"]=fieldType_paragraph
			info["typeString"]=fieldNames[fieldType_paragraph]
		elif role==IAccessibleHandler.ROLE_SYSTEM_CELL:
			info["fieldType"]=fieldType_cell
			info["typeString"]=fieldNames[fieldType_cell]
		elif role==IAccessibleHandler.ROLE_SYSTEM_TABLE:
			info["fieldType"]=fieldType_table
			info["typeString"]=fieldNames[fieldType_table]
		elif role==IAccessibleHandler.ROLE_SYSTEM_ROW:
			info["fieldType"]=fieldType_row
			info["typeString"]=fieldNames[fieldType_row]
		elif role=="thead":
			info["fieldType"]=fieldType_tableHeader
			info["typeString"]=fieldNames[fieldType_tableHeader]
		elif role=="tfoot":
			info["fieldType"]=fieldType_tableFooter
			info["typeString"]=fieldNames[fieldType_tableFooter]
		elif role=="tbody":
			info["fieldType"]=fieldType_tableBody
			info["typeString"]=fieldNames[fieldType_tableBody]
		elif role in [IAccessibleHandler.ROLE_SYSTEM_LIST,"ul"]:
			info["fieldType"]=fieldType_list
			info["typeString"]=fieldNames[fieldType_list]
			info["descriptionFunc"]=lambda x: "with %s items"%x.childCount
		elif role==IAccessibleHandler.ROLE_SYSTEM_LISTITEM:
			info["fieldType"]=fieldType_listItem
			bullet=obj.name.rstrip()
			if not bullet or (len(bullet)>0 and ord(bullet[0])>127):
				bullet=_("bullet")
			info["typeString"]=bullet
		elif role=="dl":
			info["fieldType"]=fieldType_list
			info["typeString"]=_("definition")+" "+fieldNames[fieldType_list]
			info["descriptionFunc"]=lambda x: _("with %s items")%x.childCount
		elif role=="dt":
			info["fieldType"]=fieldType_listItem
			bullet=obj.name.rstrip()
			if not bullet:
				bullet=_("bullet")
			elif bullet.endswith('.'):
				bullet=bullet[0:-1]
			info["typeString"]=bullet
		elif role=="dd":
			info["fieldType"]=fieldType_listItem
			info["typeString"]=_("definition")
		elif role==IAccessibleHandler.ROLE_SYSTEM_GRAPHIC:
			text="%s"%obj.name
			if not text and states&IAccessibleHandler.STATE_SYSTEM_LINKED:
				text=" "
			info["fieldType"]=fieldType_graphic
			info["typeString"]=fieldNames[fieldType_graphic]
		elif role in ["h1","h2","h3","h4","h5","h6"]:
			info["fieldType"]=fieldType_heading
			info["typeString"]=fieldNames[fieldType_heading]+" %s"%role[1]
		elif role=="blockquote":
			info["fieldType"]=fieldType_blockQuote
			info["typeString"]=fieldNames[fieldType_blockQuote]
		elif role=="q":
			info["fieldType"]=fieldType_blockQuote
			info["typeString"]=fieldNames[fieldType_blockQuote]
		elif role==IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON:
			text="%s "%obj.name
			info["fieldType"]=fieldType_button
			info["typeString"]=fieldNames[fieldType_button]
		elif role=="form":
			info["fieldType"]=fieldType_form
			info["typeString"]=fieldNames[fieldType_form]
		elif role==IAccessibleHandler.ROLE_SYSTEM_RADIOBUTTON:
			text="%s "%obj.name
			info["fieldType"]=fieldType_radioButton
			info["typeString"]=fieldNames[fieldType_radioButton]
			info["stateTextFunc"]=lambda x: IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_CHECKED) if x.states&IAccessibleHandler.STATE_SYSTEM_CHECKED else _("not %s")%IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_CHECKED)
		elif role==IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON:
			text="%s "%obj.name
			info["fieldType"]=fieldType_checkBox
			info["typeString"]=fieldNames[fieldType_checkBox]
			info["stateTextFunc"]=lambda x: IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_CHECKED) if x.states&IAccessibleHandler.STATE_SYSTEM_CHECKED else _("not %s")%IAccessibleHandler.getStateName(IAccessibleHandler.STATE_SYSTEM_CHECKED)
		elif role==IAccessibleHandler.ROLE_SYSTEM_TEXT and not states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			text="%s "%obj.value
			info["fieldType"]=fieldType_edit
			info["typeString"]=fieldNames[fieldType_edit]
			if obj.states&IAccessibleHandler.STATE_SYSTEM_PROTECTED:
				info["typeString"]=_("protected %s")%info["typeString"]
		elif role==IAccessibleHandler.ROLE_SYSTEM_COMBOBOX:
			text="%s "%obj.value
			info["fieldType"]=fieldType_comboBox
			info["typeString"]=fieldNames[fieldType_comboBox]
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
		if getMozillaRole(obj.role)!=IAccessibleHandler.ROLE_SYSTEM_TEXT or obj.childCount>0 or not obj.states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			return ctypes.cast(obj._pacc,ctypes.c_void_p).value

