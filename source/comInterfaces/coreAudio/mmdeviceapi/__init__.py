# This file is a part of pycaw library (https://github.com/AndreMiras/pycaw).
# Please note that it is distributed under MIT license:
# https://github.com/AndreMiras/pycaw#MIT-1-ov-file

from ctypes import HRESULT, POINTER
from ctypes.wintypes import DWORD, LPCWSTR, LPWSTR, UINT

from comtypes import COMMETHOD, GUID, IUnknown

from .depend import PROPERTYKEY, IPropertyStore


class IMMDevice(IUnknown):
	_iid_ = GUID("{D666063F-1587-4E43-81F1-B948E807363F}")
	_methods_ = (
		# HRESULT Activate(
		# [in] REFIID iid,
		# [in] DWORD dwClsCtx,
		# [in] PROPVARIANT *pActivationParams,
		# [out] void **ppInterface);
		COMMETHOD(
			[],
			HRESULT,
			"Activate",
			(["in"], POINTER(GUID), "iid"),
			(["in"], DWORD, "dwClsCtx"),
			(["in"], POINTER(DWORD), "pActivationParams"),
			(["out"], POINTER(POINTER(IUnknown)), "ppInterface"),
		),
		# HRESULT OpenPropertyStore(
		# [in] DWORD stgmAccess,
		# [out] IPropertyStore **ppProperties);
		COMMETHOD(
			[],
			HRESULT,
			"OpenPropertyStore",
			(["in"], DWORD, "stgmAccess"),
			(["out"], POINTER(POINTER(IPropertyStore)), "ppProperties"),
		),
		# HRESULT GetId([out] LPWSTR *ppstrId);
		COMMETHOD([], HRESULT, "GetId", (["out"], POINTER(LPWSTR), "ppstrId")),
		# HRESULT GetState([out] DWORD *pdwState);
		COMMETHOD([], HRESULT, "GetState", (["out"], POINTER(DWORD), "pdwState")),
	)


class IMMDeviceCollection(IUnknown):
	_iid_ = GUID("{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}")
	_methods_ = (
		# HRESULT GetCount([out] UINT *pcDevices);
		COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(UINT), "pcDevices")),
		# HRESULT Item([in] UINT nDevice, [out] IMMDevice **ppDevice);
		COMMETHOD(
			[],
			HRESULT,
			"Item",
			(["in"], UINT, "nDevice"),
			(["out"], POINTER(POINTER(IMMDevice)), "ppDevice"),
		),
	)


class IMMNotificationClient(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID("{7991EEC9-7E89-4D85-8390-6C703CEC60C0}")
	_methods_ = (
		# HRESULT OnDeviceStateChanged(
		# [in] LPCWSTR pwstrDeviceId,
		# [in] DWORD   dwNewState);
		COMMETHOD(
			[],
			HRESULT,
			"OnDeviceStateChanged",
			(["in"], LPCWSTR, "pwstrDeviceId"),
			(["in"], DWORD, "dwNewState"),
		),
		# HRESULT OnDeviceAdded(
		# [in] LPCWSTR pwstrDeviceId,
		COMMETHOD(
			[],
			HRESULT,
			"OnDeviceAdded",
			(["in"], LPCWSTR, "pwstrDeviceId"),
		),
		# HRESULT OnDeviceRemoved(
		# [in] LPCWSTR pwstrDeviceId,
		COMMETHOD(
			[],
			HRESULT,
			"OnDeviceRemoved",
			(["in"], LPCWSTR, "pwstrDeviceId"),
		),
		# HRESULT OnDefaultDeviceChanged(
		# [in] EDataFlow flow,
		# [in] ERole role,
		# [in] LPCWSTR pwstrDefaultDeviceId;
		COMMETHOD(
			[],
			HRESULT,
			"OnDefaultDeviceChanged",
			(["in"], DWORD, "flow"),
			(["in"], DWORD, "role"),
			(["in"], LPCWSTR, "pwstrDefaultDeviceId"),
		),
		# HRESULT OnPropertyValueChanged(
		# [in] LPCWSTR		   pwstrDeviceId,
		# [in] const PROPERTYKEY key);
		COMMETHOD(
			[],
			HRESULT,
			"OnPropertyValueChanged",
			(["in"], LPCWSTR, "pwstrDeviceId"),
			(["in"], PROPERTYKEY, "key"),
		),
	)


class IMMDeviceEnumerator(IUnknown):
	_iid_ = GUID("{A95664D2-9614-4F35-A746-DE8DB63617E6}")
	_methods_ = (
		# HRESULT EnumAudioEndpoints(
		# [in] EDataFlow dataFlow,
		# [in] DWORD dwStateMask,
		# [out] IMMDeviceCollection **ppDevices);
		COMMETHOD(
			[],
			HRESULT,
			"EnumAudioEndpoints",
			(["in"], DWORD, "dataFlow"),
			(["in"], DWORD, "dwStateMask"),
			(["out"], POINTER(POINTER(IMMDeviceCollection)), "ppDevices"),
		),
		# HRESULT GetDefaultAudioEndpoint(
		# [in] EDataFlow dataFlow,
		# [in] ERole role,
		# [out] IMMDevice **ppDevice);
		COMMETHOD(
			[],
			HRESULT,
			"GetDefaultAudioEndpoint",
			(["in"], DWORD, "dataFlow"),
			(["in"], DWORD, "role"),
			(["out"], POINTER(POINTER(IMMDevice)), "ppDevices"),
		),
		# HRESULT GetDevice(
		# [in] LPCWSTR pwstrId,
		# [out] IMMDevice **ppDevice);
		COMMETHOD(
			[],
			HRESULT,
			"GetDevice",
			(["in"], LPCWSTR, "pwstrId"),
			(["out"], POINTER(POINTER(IMMDevice)), "ppDevice"),
		),
		# HRESULT RegisterEndpointNotificationCallback(
		# [in] IMMNotificationClient *pClient);
		COMMETHOD(
			[],
			HRESULT,
			"RegisterEndpointNotificationCallback",
			(["in"], POINTER(IMMNotificationClient), "pClient"),
		),
		# HRESULT UnregisterEndpointNotificationCallback(
		# [in] IMMNotificationClient *pClient);
		COMMETHOD(
			[],
			HRESULT,
			"UnregisterEndpointNotificationCallback",
			(["in"], POINTER(IMMNotificationClient), "pClient"),
		),
	)


class IMMEndpoint(IUnknown):
	_iid_ = GUID("{1BE09788-6894-4089-8586-9A2A6C265AC5}")
	_methods_ = (
		# HRESULT GetDataFlow(
		# [out] EDataFlow *pDataFlow);
		COMMETHOD(
			[],
			HRESULT,
			"GetDataFlow",
			(["out"], POINTER(DWORD), "pDataFlow"),
		),
	)



