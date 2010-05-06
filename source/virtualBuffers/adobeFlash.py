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

	def isNVDAObjectInVirtualBuffer(self,obj):
		return winUser.isDescendantWindow(self.rootNVDAObject.windowHandle, obj.windowHandle)

	def isAlive(self):
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
