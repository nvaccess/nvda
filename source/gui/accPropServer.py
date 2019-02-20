#accPropServer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017-2018 NV Access Limited, Derek Riemer, Babbage B.V.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Implementation of IAccProcServer, so that customization of a wx control can be done very fast."""

from logHandler import log
from  comtypes.automation import VT_EMPTY
from  comtypes import COMObject, GUID
from comInterfaces.Accessibility import IAccPropServer, ANNO_CONTAINER, ANNO_THIS
from abc import ABCMeta, abstractmethod, abstractproperty
from six import with_metaclass
import weakref
import winUser
import wx

class IAccPropServer_Impl(with_metaclass(ABCMeta, COMObject)):
	"""Base class for implementing a COM interface for a hwnd based AccPropServer\
	to annotate a WX control.
	The AccPropServer registers itself using the window handle of the WX control.
	When the WX control is destroyed, the instance is automatically unregistered.
	This should eventually be dropped in favor of WX' own annotation support,
	blocked by wxWidgets/Phoenix#1129.
	Please override the L{_GetPropValue} method, not L{GetPropValue}.
	L{GetPropValue} wraps L{_getPropValue} to catch and log exceptions (Which for some reason NVDA's logger misses when they occur in GetPropValue).
	You must also provide the L{properties} property.
	"""

	_com_interfaces_ = [
		IAccPropServer
	]

	# Constants used with `IAccPropServer::GetPropValue` method see
	# https://msdn.microsoft.com/en-us/library/windows/desktop/dd318495(v=vs.85).aspx
	HAS_PROP = 1  # TRUE - Constant for `BOOL* pfHasProp` out param of `IAccPropServer::GetPropValue` method
	DOES_NOT_HAVE_PROP = 0  # FALSE - Constant for `BOOL* pfHasProp` out param of `IAccPropServer::GetPropValue` method
	# When returning `DOES_NOT_HAVE_PROP` or FALSE as the pfHasProp part of the return of `IAccPropServer::GetPropValue`
	# method, then `pvarValue` return value must be `VT_EMPTY`.
	# Consider using `NO_RETURN_VALUE`
	NO_RETURN_VALUE = (VT_EMPTY, DOES_NOT_HAVE_PROP)

	# An array with the GUIDs of the properties that an AccPropServer should override
	properties_GUIDPTR = []
	properties = []

	def __init__(self, control, annotateProperties, annotateChildren=False):
		"""Initialize the instance of AccPropServer. 
		@param control: the WX control instance, so you can look up things in the _getPropValue method.
			It's available on self.control.
		@Type control: Subclass of wx.Window
		@param annotateProperties The properties that should be annotated, see oleacc.py for constants.
		@type annotateProperties List of oleacc constants. Internally these are converted to GUID pointers for the server.
		@param annotateChildren: whether the WX control is a container which children should be annotated.
		@type annotateChildren: bool
		"""
		self.properties = annotateProperties
		self.properties_GUIDPTR = convertToGUIDPointerList(annotateProperties)
		self.control = weakref.ref(control)
		self.hwnd = control.GetHandle()
		super(IAccPropServer_Impl, self).__init__()
		# Import late to avoid circular import
		from IAccessibleHandler import accPropServices
		accPropServices.SetHwndPropServer(
			hwnd=self.hwnd,
			idObject=winUser.OBJID_CLIENT,
			idChild=0,
			paProps=self.properties_GUIDPTR,
			cProps=len(self.properties_GUIDPTR),
			pServer=self,
			AnnoScope=ANNO_CONTAINER if annotateChildren else ANNO_THIS
		)
		# clean up of accPropServices needs to happen when the control is destroyed. We can't rely on 
		# pythons `__del__` method to be called, and the wx framework does not call Destroy on child controls,
		# automatically. Instead we can bind to the "window destroy" event for the control to do necessary 
		# cleanup (wxWidgets/Phoenix/#630). Not performing this cleanup results in a reference to the parent
		# window, keeping it from being deleted correctly. This can cause a freeze on exit of NVDA.
		control.Bind(wx.EVT_WINDOW_DESTROY, self._onDestroyControl, source=control)

	@abstractmethod
	def _getPropValue(self, pIDString, dwIDStringLen, idProp):
		"""use this method to implement GetPropValue. It  is wrapped by the callback GetPropValue to handle exceptions.
		For instructions on implementing accPropServers, see https://msdn.microsoft.com/en-us/library/windows/desktop/dd373681(v=vs.85).aspx .
		For instructions specifically about this method, see https://msdn.microsoft.com/en-us/library/windows/desktop/dd318495(v=vs.85).aspx .
		@param pIDString: Contains a string that identifies the property being requested.
			If a single callback object is registered for annotating multiple accessible elements,
			the identity string can be used to determine which element the request refers to.
			If the accessible element is HWND-based,
			IAccessibleHandler.accPropServices.DecomposeHwndIdentityString can be used
			to extract the HWND/idObject/idChild from the identity string.
			Note that, while one IAccPropServer implementation can annotate
			multiple accessible elements, it is still bound to one wx.Control.
		@type pIDString: str
		@param dwIDStringLen: Specifies the length of the identity string specified by the pIDString parameter.
		@type dwIDStringLen: int
		@param idProp: Specifies a GUID indicating the desired property.
		@type idProp: One of the oleacc.PROPID_* GUIDS
		@return A tuple of the out params for the `IAccPropServer::GetPropValue` method: `VARIANT* pvarValue` and `BOOL*
		pfHasProp`. When the pfHasProp part is FALSE / self.DOES_NOT_HAVE_PROP, then the pvarValue part must be VT_EMPTY.
		Consider using self.NO_RETURN_VALUE instead. Returning (VT_EMPTY, HAS_PROP) IS valid, meaning the property exists
		but is empty.
		"""
		raise NotImplementedError

	def GetPropValue(self, pIDString, dwIDStringLen, idProp):
		try:
			return self._getPropValue(pIDString, dwIDStringLen, idProp)
		except Exception:
			log.exception()
			return self.NO_RETURN_VALUE

	def _onDestroyControl(self, evt):
		evt.Skip()  # Allow other handlers to process this event.
		self._cleanup()

	def _cleanup(self):
		# Import late to avoid circular import
		from IAccessibleHandler import accPropServices
		accPropServices.ClearHwndProps(
			hwnd=self.hwnd,
			idObject=winUser.OBJID_CLIENT,
			idChild=0,
			paProps=self.properties_GUIDPTR,
			cProps=len(self.properties_GUIDPTR)
		)

def convertToGUIDPointerList(propList):
	return (GUID * len(propList))(*propList)
