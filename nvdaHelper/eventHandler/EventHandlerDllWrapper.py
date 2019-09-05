import ctypes
from ctypes import wintypes
from ctypes import c_uint

class EventData(ctypes.Structure):
	_fields_ = [
		("idEvent", wintypes.DWORD),
		("hwnd", wintypes.HWND),
		("idObject", wintypes.LONG),
		("idChild", wintypes.LONG),
		("dwEventThread", wintypes.DWORD),
		("dwmsEventTime", wintypes.DWORD),
	]
	idEvent: wintypes.DWORD
	hwnd: wintypes.HWND
	idObject: wintypes.LONG
	idChild: wintypes.LONG
	dwEventThread: wintypes.DWORD
	dwmsEventTime: wintypes.DWORD


NotifyCallback = ctypes.CFUNCTYPE(restype=None)
ObjectDestroyedCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(EventData))


class EventHandlerDll:
	def GetEventCount(self) -> c_uint: ...

	def GetEvents(
			self,
			index: c_uint,
			maxEvents: c_uint,
			data: ctypes.POINTER(EventData)
	) -> ctypes.c_uint: ...

	def FlushEvents(self) -> None: ...

	def RegisterAndPump_Async(
			self,
			notifyOfNewEvents: NotifyCallback,
			objDestroyCallback: ObjectDestroyedCallback
	) -> ctypes.c_int: ...

	def RegisterAndPump_Join(self) -> None: ...


def getEventHandlerDll() -> EventHandlerDll:
	from NVDAHelper import getEventHandlerDllPath
	dll = ctypes.cdll.LoadLibrary(getEventHandlerDllPath())

	dll.GetEvents.restype = ctypes.c_uint
	dll.GetEvents.argtypes = ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(EventData),

	dll.GetEventCount.restype = ctypes.c_uint
	dll.GetEventCount.argtypes = None

	dll.FlushEvents.restype = None
	dll.FlushEvents.argtypes = None

	dll.RegisterAndPump_Async.restype = ctypes.c_int
	dll.RegisterAndPump_Async.argtypes = NotifyCallback, ObjectDestroyedCallback,

	dll.RegisterAndPump_Join.restype = ctypes.c_int
	dll.RegisterAndPump_Join.argtypes = None
	return dll
