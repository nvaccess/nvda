# This file is a part of pycaw library (https://github.com/AndreMiras/pycaw).
# Please note that it is distributed under MIT license:
# https://github.com/AndreMiras/pycaw#MIT-1-ov-file

from ctypes import HRESULT, POINTER, c_float
from ctypes.wintypes import BOOL, DWORD, UINT

from comtypes import COMMETHOD, GUID, IUnknown

from .depend import PAUDIO_VOLUME_NOTIFICATION_DATA


class IAudioEndpointVolumeCallback(IUnknown):
    _iid_ = GUID("{b1136c83-b6b5-4add-98a5-a2df8eedf6fa}")
    _methods_ = (
        # HRESULT OnNotify(
        # [in] PAUDIO_VOLUME_NOTIFICATION_DATA pNotify);
        COMMETHOD(
            [],
            HRESULT,
            "OnNotify",
            (["in"], PAUDIO_VOLUME_NOTIFICATION_DATA, "pNotify"),
        ),
    )


class IAudioEndpointVolume(IUnknown):
    _iid_ = GUID("{5CDF2C82-841E-4546-9722-0CF74078229A}")
    _methods_ = (
        # HRESULT RegisterControlChangeNotify(
        # [in] IAudioEndpointVolumeCallback *pNotify);
        COMMETHOD(
            [],
            HRESULT,
            "RegisterControlChangeNotify",
            (["in"], POINTER(IAudioEndpointVolumeCallback), "pNotify"),
        ),
        # HRESULT UnregisterControlChangeNotify(
        # [in] IAudioEndpointVolumeCallback *pNotify);
        COMMETHOD(
            [],
            HRESULT,
            "UnregisterControlChangeNotify",
            (["in"], POINTER(IAudioEndpointVolumeCallback), "pNotify"),
        ),
        # HRESULT GetChannelCount([out] UINT *pnChannelCount);
        COMMETHOD(
            [], HRESULT, "GetChannelCount", (["out"], POINTER(UINT), "pnChannelCount")
        ),
        # HRESULT SetMasterVolumeLevel(
        # [in] float fLevelDB, [in] LPCGUID pguidEventContext);
        COMMETHOD(
            [],
            HRESULT,
            "SetMasterVolumeLevel",
            (["in"], c_float, "fLevelDB"),
            (["in"], POINTER(GUID), "pguidEventContext"),
        ),
        # HRESULT SetMasterVolumeLevelScalar(
        # [in] float fLevel, [in] LPCGUID pguidEventContext);
        COMMETHOD(
            [],
            HRESULT,
            "SetMasterVolumeLevelScalar",
            (["in"], c_float, "fLevel"),
            (["in"], POINTER(GUID), "pguidEventContext"),
        ),
        # HRESULT GetMasterVolumeLevel([out] float *pfLevelDB);
        COMMETHOD(
            [],
            HRESULT,
            "GetMasterVolumeLevel",
            (["out"], POINTER(c_float), "pfLevelDB"),
        ),
        # HRESULT GetMasterVolumeLevelScalar([out] float *pfLevel);
        COMMETHOD(
            [],
            HRESULT,
            "GetMasterVolumeLevelScalar",
            (["out"], POINTER(c_float), "pfLevelDB"),
        ),
        # HRESULT SetChannelVolumeLevel(
        # [in] UINT nChannel,
        # [in] float fLevelDB,
        # [in] LPCGUID pguidEventContext);
        COMMETHOD(
            [],
            HRESULT,
            "SetChannelVolumeLevel",
            (["in"], UINT, "nChannel"),
            (["in"], c_float, "fLevelDB"),
            (["in"], POINTER(GUID), "pguidEventContext"),
        ),
        # HRESULT SetChannelVolumeLevelScalar(
        # [in] UINT nChannel,
        # [in] float fLevel,
        # [in] LPCGUID pguidEventContext);
        COMMETHOD(
            [],
            HRESULT,
            "SetChannelVolumeLevelScalar",
            (["in"], DWORD, "nChannel"),
            (["in"], c_float, "fLevelDB"),
            (["in"], POINTER(GUID), "pguidEventContext"),
        ),
        # HRESULT GetChannelVolumeLevel(
        # [in]  UINT nChannel,
        # [out] float *pfLevelDB);
        COMMETHOD(
            [],
            HRESULT,
            "GetChannelVolumeLevel",
            (["in"], UINT, "nChannel"),
            (["out"], POINTER(c_float), "pfLevelDB"),
        ),
        # HRESULT GetChannelVolumeLevelScalar(
        # [in]  UINT nChannel,
        # [out] float *pfLevel);
        COMMETHOD(
            [],
            HRESULT,
            "GetChannelVolumeLevelScalar",
            (["in"], DWORD, "nChannel"),
            (["out"], POINTER(c_float), "pfLevelDB"),
        ),
        # HRESULT SetMute([in] BOOL bMute, [in] LPCGUID pguidEventContext);
        COMMETHOD(
            [],
            HRESULT,
            "SetMute",
            (["in"], BOOL, "bMute"),
            (["in"], POINTER(GUID), "pguidEventContext"),
        ),
        # HRESULT GetMute([out] BOOL *pbMute);
        COMMETHOD([], HRESULT, "GetMute", (["out"], POINTER(BOOL), "pbMute")),
        # HRESULT GetVolumeStepInfo(
        # [out] UINT *pnStep,
        # [out] UINT *pnStepCount);
        COMMETHOD(
            [],
            HRESULT,
            "GetVolumeStepInfo",
            (["out"], POINTER(DWORD), "pnStep"),
            (["out"], POINTER(DWORD), "pnStepCount"),
        ),
        # HRESULT VolumeStepUp([in] LPCGUID pguidEventContext);
        COMMETHOD(
            [], HRESULT, "VolumeStepUp", (["in"], POINTER(GUID), "pguidEventContext")
        ),
        # HRESULT VolumeStepDown([in] LPCGUID pguidEventContext);
        COMMETHOD(
            [], HRESULT, "VolumeStepDown", (["in"], POINTER(GUID), "pguidEventContext")
        ),
        # HRESULT QueryHardwareSupport([out] DWORD *pdwHardwareSupportMask);
        COMMETHOD(
            [],
            HRESULT,
            "QueryHardwareSupport",
            (["out"], POINTER(DWORD), "pdwHardwareSupportMask"),
        ),
        # HRESULT GetVolumeRange(
        # [out] float *pfLevelMinDB,
        # [out] float *pfLevelMaxDB,
        # [out] float *pfVolumeIncrementDB);
        COMMETHOD(
            [],
            HRESULT,
            "GetVolumeRange",
            (["out"], POINTER(c_float), "pfMin"),
            (["out"], POINTER(c_float), "pfMax"),
            (["out"], POINTER(c_float), "pfIncr"),
        ),
    )


class IAudioMeterInformation(IUnknown):
    _iid_ = GUID("{C02216F6-8C67-4B5B-9D00-D008E73E0064}")
    _methods_ = (
        # HRESULT GetPeakValue([out] c_float *pfPeak);
        COMMETHOD([], HRESULT, "GetPeakValue", (["out"], POINTER(c_float), "pfPeak")),
    )

