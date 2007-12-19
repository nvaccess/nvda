from . import VirtualBuffer
from virtualBuffer_new_wrapper import *
import controlTypes
import NVDAObjects.IAccessible
import winUser
import speech

class Gecko(VirtualBuffer):

	def _fillVBufHelper(self,NVDAObject):
		node=VBufStorage_addTagNodeToBuffer(self.VBufHandle,None,1,{'role':'bla'})
		VBufStorage_addTextNodeToBuffer(self.VBufHandle,node,0,u"test:\n%s %s %s\n"%(NVDAObject.name,controlTypes.speechRoleLabels[NVDAObject.role],NVDAObject.value))

	def fillVBuf(self):
		self._fillVBufHelper(self.rootNVDAObject)

	def isNVDAObjectInVirtualBuffer(self,obj):
		root=self.rootNVDAObject
		if root and obj and isinstance(obj,NVDAObjects.IAccessible.IAccessible) and winUser.isDescendantWindow(root.windowHandle,obj.windowHandle): 
			return True

	def isAlive(self):
		root=self.rootNVDAObject
		if root and winUser.isWindow(root.windowHandle):
			return True
