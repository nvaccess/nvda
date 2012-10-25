#virtualBuffers/lotusNotes.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2012 NV Access Limited

from . import VirtualBuffer, VirtualBufferTextInfo
import controlTypes
import NVDAObjects.IAccessible
import winUser
import IAccessibleHandler
import oleacc
from logHandler import log
import textInfos
from virtualBuffers import VirtualBufferTextInfo

class LotusNotesRichText_TextInfo(VirtualBufferTextInfo):

	def _normalizeControlField(self,attrs):
		role=controlTypes.ROLE_STATICTEXT
		states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('IAccessible::state_%s'%x,0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)
		if controlTypes.STATE_LINKED in states:
			role=controlTypes.ROLE_LINK
		attrs['role']=role
		attrs['states']=states
		return super(LotusNotesRichText_TextInfo, self)._normalizeControlField(attrs)

class LotusNotesRichText(VirtualBuffer):
	TextInfo=LotusNotesRichText_TextInfo

	def __init__(self,rootNVDAObject):
		super(LotusNotesRichText,self).__init__(rootNVDAObject,backendName="lotusNotesRichText")

	def __contains__(self,obj):
		return winUser.isDescendantWindow(self.rootNVDAObject.windowHandle, obj.windowHandle)

	def _get_isAlive(self):
		if self.isLoading:
			return True
		root=self.rootNVDAObject
		if not root:
			return False
		if not winUser.isWindow(root.windowHandle) or root.role == controlTypes.ROLE_UNKNOWN:
			return False
		return True

	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		return NVDAObjects.IAccessible.getNVDAObjectFromEvent(docHandle, winUser.OBJID_CLIENT, ID)

	def getIdentifierFromNVDAObject(self,obj):
		return obj.windowHandle, obj.event_childID

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType=="formField":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_PUSHBUTTON,oleacc.ROLE_SYSTEM_RADIOBUTTON,oleacc.ROLE_SYSTEM_CHECKBUTTON,oleacc.ROLE_SYSTEM_COMBOBOX,oleacc.ROLE_SYSTEM_LIST,oleacc.ROLE_SYSTEM_TEXT]}
		elif nodeType=="list":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LIST]}
		elif nodeType=="listItem":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LISTITEM]}
		elif nodeType=="button":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_PUSHBUTTON]}
		elif nodeType=="edit":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_TEXT]}
		elif nodeType=="radioButton":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_RADIOBUTTON]}
		elif nodeType=="comboBox":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_COMBOBOX]}
		elif nodeType=="checkBox":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_CHECKBUTTON]}
		elif nodeType=="graphic":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_GRAPHIC]}
		elif nodeType=="focusable":
			attrs={"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		else:
			return None
		return attrs

	def _activateNVDAObject(self, obj):
		try:
			obj.doAction()
			return
		except:
			pass

		log.debugWarning("could not programmatically activate field, trying mouse")
		l=obj.location
		if not l:
			log.debugWarning("no location for field")
			return
		x=(l[0]+l[2]/2)
		y=l[1]+(l[3]/2) 
		oldX,oldY=winUser.getCursorPos()
		winUser.setCursorPos(x,y)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		winUser.setCursorPos(oldX,oldY)

	def _shouldSetFocusToObj(self, obj):
		states=obj.states
		return controlTypes.STATE_FOCUSABLE in states or controlTypes.STATE_LINKED in states

	def shouldPassThrough(self,obj,reason=None):
		return False

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType=="link":
			attrs={"IAccessible::state_%s"%oleacc.STATE_SYSTEM_LINKED:[1]}
		elif nodeType=="graphic":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_GRAPHIC]}
		elif nodeType=="focusable":
			attrs={"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_LINKED:[1]}
		else:
			return None
		return attrs
