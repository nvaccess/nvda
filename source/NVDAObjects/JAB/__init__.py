import ctypes
import debug
import appModuleHandler
import winUser
import JABHandler
from window import Window

class JAB(Window):

	def __init__(self,vmID,accContext,windowHandle=None):
		if windowHandle is None:
			#windowHandle=JABHandler.bridgeDll.getHWNDFromAccessibleContext(vmID,accContext)
			windowHandle=winUser.getForegroundWindow()
		debug.writeMessage("JAB windowHandle: %s"%windowHandle)
		Window.__init__(self,windowHandle)
		self.JABVmID=vmID
		self.JABAccContext=accContext
		info=JABHandler.AccessibleContextInfo()
		debug.writeMessage("JAB: about to call contextInfo")
		JABHandler.bridgeDll.getAccessibleContextInfo(vmID,accContext,ctypes.byref(info))
		self._JABAccContextInfo=info

	def __del__(self):
		JABHandler.bridgeDll.releaseJavaObject(self.JABAccContext)

	def _get_name(self):
		return self._JABAccContextInfo.name

	def _get_role(self):
		return self._JABAccContextInfo.role_en_US

	def _get_typeString(self):
		return self._JABAccContextInfo.role

	def _get_description(self):
		return self._JABAccContextInfo.description
