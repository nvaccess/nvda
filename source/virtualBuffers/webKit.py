# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2011-2021 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import ctypes
import typing

from . import VirtualBuffer, VirtualBufferTextInfo, VBufRemote_nodeHandle_t
import controlTypes
import NVDAObjects.IAccessible
import winUser
import mouseHandler
import IAccessibleHandler
import oleacc
from logHandler import log
import textInfos
import NVDAHelper

class WebKit_TextInfo(VirtualBufferTextInfo):

	def _normalizeControlField(self, attrs: textInfos.ControlField):
		accRole=attrs['IAccessible::role']
		role = level = None
		if accRole.isdigit():
			accRole = int(accRole)
		else:
			if "H1" <= accRole <= "H6":
				role = controlTypes.Role.HEADING
				level = int(accRole[1])
			else:
				accRole = accRole.lower()

		if not role:
			role = IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole, controlTypes.Role.UNKNOWN)
		states = IAccessibleHandler.getStatesSetFromIAccessibleAttrs(attrs)
		role, states = controlTypes.transformRoleStates(role, states)

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
		if not winUser.isWindow(root.windowHandle) or root.role == controlTypes.Role.UNKNOWN:
			return False
		return True

	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		if ID > 0:
			# WebKit returns a positive value for uniqueID,
			# but we need to pass a negative value when retrieving objects.
			ID = -ID
		return NVDAObjects.IAccessible.getNVDAObjectFromEvent(docHandle, winUser.OBJID_CLIENT, ID)

	def getIdentifierFromNVDAObject(self, obj):
		docHandle = obj.windowHandle
		ID = obj.IA2UniqueID
		return docHandle, ID

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
		oldX,oldY=winUser.getCursorPos()
		winUser.setCursorPos(*l.center)
		mouseHandler.doPrimaryClick()
		winUser.setCursorPos(oldX,oldY)

	def _shouldSetFocusToObj(self,obj):
		return obj.role!=controlTypes.Role.GROUPING and super(WebKit,self)._shouldSetFocusToObj(obj)
