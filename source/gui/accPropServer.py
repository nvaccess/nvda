#IAccProcServer.py:
	#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Implementation of IAccProcServer, so that customization of a wx control can be done very fast."""

from logHandler import log
from  comtypes.automation import VT_EMPTY
from  comtypes import GUID, COMObject
from comInterfaces.Accessibility import IAccPropServer

#These are the GUIDS for IAccessible properties we can override.
#Use these to look up the GUID needed when implementing a server.
#These are taken from oleacc.h (oleacc.idl has them too).
#Number of digits Format: "{8-4-4-4-12}"
PROPID_ACC_NAME = GUID("{608d3df8-8128-4aa7-a428-f55e49267291}")
PROPID_ACC_VALUE             = GUID("{123fe443-211a-4615-9527-c45a7e93717a}")
PROPID_ACC_DESCRIPTION = GUID("{4d48dfe4-bd3f-491f-a648-492d6f20c588}")
PROPID_ACC_ROLE = GUID("{CB905FF2-7BD1-4C05-B3C8-E6C241364D70}")
PROPID_ACC_STATE = GUID("{A8D4D5B0-0A21-42D0-A5C0-514E984F457B}")
PROPID_ACC_HELP = GUID("{c831e11f-44db-4a99-9768-cb8f978b7231}")
PROPID_ACC_KEYBOARDSHORTCUT = GUID("{7d9bceee-7d1e-4979-9382-5180f4172c34}")
PROPID_ACC_DEFAULTACTION = GUID("{180c072b-c27f-43c7-9922-f63562a4632b}")
PROPID_ACC_VALUEMAP = GUID("{da1c3d79-fc5c-420e-b399-9d1533549e75}")
PROPID_ACC_ROLEMAP = GUID("{f79acda2-140d-4fe6-8914-208476328269}")
PROPID_ACC_STATEMAP = GUID("{43946c5e-0ac0-4042-b525-07bbdbe17fa7}")
PROPID_ACC_FOCUS = GUID("{6eb335df-1c29-4127-b12c-dee9fd157f2b}")
PROPID_ACC_SELECTION = GUID("{b99d073c-d731-405b-9061-d95e8f842984}")
PROPID_ACC_PARENT = GUID("{474c22b6-ffc2-467a-b1b5-e958b4657330}")
PROPID_ACC_NAV_UP = GUID("{016e1a2b-1a4e-4767-8612-3386f66935ec}")
PROPID_ACC_NAV_LEFT = GUID("{228086cb-82f1-4a39-8705-dcdc0fff92f5}")
PROPID_ACC_NAV_RIGHT = GUID("{cd211d9f-e1cb-4fe5-a77c-920b884d095b}")
PROPID_ACC_NAV_PREV = GUID("{776d3891-c73b-4480-b3f6-076a16a15af6}")
PROPID_ACC_NAV_NEXT = GUID("{1cdc5455-8cd9-4c92-a371-3939a2fe3eee}")
PROPID_ACC_NAV_FIRSTCHILD = GUID("{cfd02558-557b-4c67-84f9-2a09fce40749}")
PROPID_ACC_NAV_LASTCHILD = GUID("{302ecaa5-48d5-4f8d-b671-1a8d20a77832}")

class IAccPropServer_Impl(COMObject):
	"""Base class for implementing a COM interface for AccPropServer.
	Please override the _GetPropValue method, not GetPropValue.
	GetPropValue wraps _getPropValue to catch and log exceptions (Which for some reason NVDA's logger misses when they occur in GetPropValue).
	"""
	
	_com_interfaces_ = [
		IAccPropServer
	]

	def __init__(self, control, *args, **kwargs):
		"""Initialize the instance of AccPropServer. 
		@param control: the WX control instance, so you can look up things in the _getPropValue method.
			It's available on self.control.
		@Type control: Subclass of wx.Window
		"""
		self.control = control
		super(IAccPropServer_Impl, self).__init__(*args, **kwargs)

	def _getPropValue(self, pIDString, dwIDStringLen, idProp):
		"""use this method to implement GetPropValue. It  is wrapped by the callback GetPropValue to handle exceptions.
		See https://msdn.microsoft.com/en-us/library/windows/desktop/dd373681(v=vs.85).aspx for instructions on implementing accPropServers.
		See https://msdn.microsoft.com/en-us/library/windows/desktop/dd318495(v=vs.85).aspx for instructions specifically about this method.
		@param pIDString: Contains a string that identifies the property being requested.
		@type pIDString: A weird comtypes thing you should not mess with.
		@param dwIDStringLen: Specifies the length of the identity string specified by the pIDString parameter.
		@type dwIDStringLen: technically dwordd
		@param idProp: Specifies a GUID indicating the desired property.
		@type idProp: One of the above GUIDS
		"""
		raise NotImplementedError

	def GetPropValue(self, pIDString, dwIDStringLen, idProp):
		try:
			return self._getPropValue(pIDString, dwIDStringLen, idProp)
		except Exception:
			log.exception()
			return VT_EMPTY, 0

