from logHandler import log
from virtualBuffers import VirtualBuffer
import IAccessibleHandler
import controlTypes
import NVDAObjects.IAccessible
import winUser

class Example(VirtualBuffer):

	def __init__(self,rootNVDAObject):
		super(Example,self).__init__(rootNVDAObject,backendLibPath=r"lib\VBufBackend_example.dll")

	def isNVDAObjectInVirtualBuffer(self,obj):
		#Special code to handle Mozilla combobox lists
		if obj.windowClassName.startswith('Mozilla') and winUser.getWindowStyle(obj.windowHandle)&winUser.WS_POPUP:
			parent=obj.parent
			while parent and parent.windowHandle==obj.windowHandle:
				parent=parent.parent
			if parent:
				obj=parent.parent
		if not (isinstance(obj,NVDAObjects.IAccessible.IAccessible) and isinstance(obj.IAccessibleObject,IAccessibleHandler.IAccessible2)) or not obj.windowClassName.startswith('Mozilla') or not winUser.isDescendantWindow(self.rootNVDAObject.windowHandle,obj.windowHandle):
			return False
		if self.rootNVDAObject.windowHandle==obj.windowHandle:
			ID=obj.IAccessibleObject.uniqueID
			try:
				self.rootNVDAObject.IAccessibleObject.accChild(ID)
			except:
				return False
			return True
		else:
			return True

	def isAlive(self):
		root=self.rootNVDAObject
		if not root:
			return False
		states=root.states
		if not winUser.isWindow(root.windowHandle) or controlTypes.STATE_DEFUNCT in states or controlTypes.STATE_READONLY not in states:
			return False
		try:
			if not NVDAObjects.IAccessible.getNVDAObjectFromEvent(root.windowHandle,IAccessibleHandler.OBJID_CLIENT,root.IAccessibleObject.uniqueID):
				return False
		except:
			log.error("bla",exc_info=True)
			return False
		import winsound
		winsound.Beep(440,30)
		return True

	def getIdentifierFromNVDAObject(self,obj):
		return self.rootNVDAObject.windowHandle, self.rootNVDAObject.IAccessibleObject.uniqueID

	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		return self.rootNVDAObject
