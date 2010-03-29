from . import VirtualBuffer, VirtualBufferTextInfo
import controlTypes
import NVDAObjects.IAccessible
import winUser
import IAccessibleHandler
import oleacc
from logHandler import log
import textInfos

class MSAATest_TextInfo(VirtualBufferTextInfo):

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
		return super(MSAATest_TextInfo, self)._normalizeControlField(attrs)

class MSAATest(VirtualBuffer):
	TextInfo = MSAATest_TextInfo

	def __init__(self,rootNVDAObject):
		super(MSAATest,self).__init__(rootNVDAObject,backendName="msaaTest")

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
