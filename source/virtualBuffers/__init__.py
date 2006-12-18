import NVDAObjects
import IAccessible

def getVirtualBuffer(obj):
		if isinstance(obj,NVDAObjects.IAccessible.NVDAObject_IAccessible):
			return IAccessible.getVirtualBuffer(obj)
