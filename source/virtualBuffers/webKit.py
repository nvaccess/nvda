#virtualBuffers/webKit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2011 NV Access Inc
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
from . import VirtualBuffer, VirtualBufferTextInfo, VBufRemote_nodeHandle_t
import controlTypes
import NVDAObjects.IAccessible
import winUser
import IAccessibleHandler
import oleacc
from logHandler import log
import textInfos
import NVDAHelper

class WebKit_TextInfo(VirtualBufferTextInfo):

	def _normalizeControlField(self,attrs):
		accRole=attrs['IAccessible::role']
		role = level = None
		if accRole.isdigit():
			accRole = int(accRole)
		else:
			if "H1" <= accRole <= "H6":
				role = controlTypes.ROLE_HEADING
				level = int(accRole[1])
			else:
				accRole = accRole.lower()

		if not role:
			role = IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole, controlTypes.ROLE_UNKNOWN)

		states = set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1 << y for y in xrange(32)] if int(attrs.get('IAccessible::state_%s' % x, 0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)

		attrs["role"] = role
		attrs["states"] = states
		if level:
			attrs["level"] = level
		return super(WebKit_TextInfo, self)._normalizeControlField(attrs)

class WebKit(VirtualBuffer):
	TextInfo = WebKit_TextInfo

	def __init__(self,rootNVDAObject):
		super(WebKit,self).__init__(rootNVDAObject,backendName="webKit")

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
		node=VBufRemote_nodeHandle_t()
		NVDAHelper.localLib.VBuf_getControlFieldNodeWithIdentifier(self.VBufHandle, docHandle, ID,ctypes.byref(node))
		if not node:
			return None
		lresult = NVDAHelper.localLib.VBuf_getNativeHandleForNode(self.VBufHandle, node)
		if not lresult:
			return None
		return NVDAObjects.IAccessible.IAccessible(
			IAccessibleObject=oleacc.ObjectFromLresult(lresult, 0, oleacc.IAccessible),
			IAccessibleChildID=0, windowHandle=self.rootDocHandle)

	def getIdentifierFromNVDAObject(self,obj):
		if obj == self.rootNVDAObject:
			return obj.windowHandle, 0
		if not self.isReady or not obj.event_childID:
			# We can only retrieve the node for objects obtained from events.
			raise LookupError
		node=VBufRemote_nodeHandle_t()
		NVDAHelper.localLib.VBuf_getNodeForNativeHandle(self.VBufHandle, obj.event_childID,ctypes.byref(node))
		docHandle=ctypes.c_int()
		ID=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getIdentifierFromControlFieldNode(self.VBufHandle, node, ctypes.byref(docHandle), ctypes.byref(ID))
		return docHandle.value, ID.value

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType=="formField":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_PUSHBUTTON,oleacc.ROLE_SYSTEM_RADIOBUTTON,oleacc.ROLE_SYSTEM_CHECKBUTTON,oleacc.ROLE_SYSTEM_COMBOBOX,oleacc.ROLE_SYSTEM_LIST,oleacc.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="list":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LIST]}
		elif nodeType=="listItem":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LISTITEM]}
		elif nodeType=="button":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_PUSHBUTTON]}
		elif nodeType=="edit":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
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
		elif nodeType.startswith("heading") and nodeType[7:].isdigit():
			attrs={"IAccessible::role":["H"+nodeType[7:]]}
		elif nodeType=="heading":
			attrs={"IAccessible::role":["H1","H2","H3","H4","H5","H6"]}
		elif nodeType=="link":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_LINKED:[1]}
		elif nodeType=="table":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_TABLE]}
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

	def _shouldSetFocusToObj(self,obj):
		return obj.role!=controlTypes.ROLE_GROUPING and super(WebKit,self)._shouldSetFocusToObj(obj)
