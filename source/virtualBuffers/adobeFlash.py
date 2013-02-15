#virtualBuffers/adobeFlash.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2013 NV Access Limited

from comtypes import COMError
from . import VirtualBuffer, VirtualBufferTextInfo
import controlTypes
import NVDAObjects.IAccessible
import winUser
import IAccessibleHandler
import oleacc
from logHandler import log
import textInfos

class AdobeFlash_TextInfo(VirtualBufferTextInfo):

	def _normalizeControlField(self,attrs):
		accRole=attrs['IAccessible::role']
		if accRole.isdigit():
			accRole=int(accRole)
		else:
			accRole = accRole.lower()
		role=IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole,controlTypes.ROLE_UNKNOWN)

		states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('IAccessible::state_%s'%x,0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)

		attrs['role']=role
		attrs['states']=states
		return super(AdobeFlash_TextInfo, self)._normalizeControlField(attrs)

class AdobeFlash(VirtualBuffer):
	TextInfo = AdobeFlash_TextInfo

	def __init__(self,rootNVDAObject):
		super(AdobeFlash,self).__init__(rootNVDAObject,backendName="adobeFlash")
		self.isWindowless = rootNVDAObject.event_objectID > 0

	def __contains__(self,obj):
		if self.isWindowless:
			if not isinstance(obj, NVDAObjects.IAccessible.IAccessible):
				return False
			if obj.windowHandle != self.rootDocHandle:
				return False
			info = obj.IAccessibleIdentity
			if not info:
				return False
			ID=info['objectID']
			try:
				self.rootNVDAObject.IAccessibleObject.accChild(ID)
				return True
			except COMError:
				return False
		return winUser.isDescendantWindow(self.rootDocHandle, obj.windowHandle)

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
		if self.isWindowless:
			objId = ID
			childId = 0
		else:
			objId = winUser.OBJID_CLIENT
			childId = ID
		return NVDAObjects.IAccessible.getNVDAObjectFromEvent(docHandle, objId, childId)

	def getIdentifierFromNVDAObject(self,obj):
		info = obj.IAccessibleIdentity
		if info:
			# Trust IAccIdentity over the event parameters.
			accId = info["objectID"]
		else:
			accId = obj.event_objectID
			if accId is None:
				# We don't have event parameters, so we can't get an ID.
				raise LookupError
			if accId <= 0:
				accId = obj.event_childID
		return obj.windowHandle, accId

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
