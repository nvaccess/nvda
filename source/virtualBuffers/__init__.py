import NVDAObjects
import MSAA

def getVirtualBuffer(obj):
		if isinstance(obj,NVDAObjects.MSAA.NVDAObject_MSAA):
			return MSAA.getVirtualBuffer(obj)
