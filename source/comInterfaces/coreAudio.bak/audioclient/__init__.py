# This file is a part of pycaw library (https://github.com/AndreMiras/pycaw).
# Please note that it is distributed under MIT license:
# https://github.com/AndreMiras/pycaw#MIT-1-ov-file

from ctypes import HRESULT, POINTER, c_float
from ctypes import c_longlong as REFERENCE_TIME
from ctypes import c_uint32 as UINT32
from ctypes.wintypes import BOOL, DWORD, HANDLE

from comtypes import COMMETHOD, GUID, IUnknown

from .depend import WAVEFORMATEX


class ISimpleAudioVolume(IUnknown):
    _iid_ = GUID("{87CE5498-68D6-44E5-9215-6DA47EF883D8}")
    _methods_ = (
        # HRESULT SetMasterVolume(
        # [in] float fLevel,
        # [in] LPCGUID EventContext);
        COMMETHOD(
            [],
            HRESULT,
            "SetMasterVolume",
            (["in"], c_float, "fLevel"),
            (["in"], POINTER(GUID), "EventContext"),
        ),
        # HRESULT GetMasterVolume([out] float *pfLevel);
        COMMETHOD(
            [], HRESULT, "GetMasterVolume", (["out"], POINTER(c_float), "pfLevel")
        ),
        # HRESULT SetMute(
        # [in] BOOL bMute,
        # [in] LPCGUID EventContext);
        COMMETHOD(
            [],
            HRESULT,
            "SetMute",
            (["in"], BOOL, "bMute"),
            (["in"], POINTER(GUID), "EventContext"),
        ),
        # HRESULT GetMute([out] BOOL *pbMute);
        COMMETHOD([], HRESULT, "GetMute", (["out"], POINTER(BOOL), "pbMute")),
    )


class IAudioClient(IUnknown):
    _iid_ = GUID("{1cb9ad4c-dbfa-4c32-b178-c2f568a703b2}")
    _methods_ = (
        # HRESULT Initialize(
        # [in] AUDCLNT_SHAREMODE ShareMode,
        # [in] DWORD StreamFlags,
        # [in] REFERENCE_TIME hnsBufferDuration,
        # [in] REFERENCE_TIME hnsPeriodicity,
        # [in] const WAVEFORMATEX *pFormat,
        # [in] LPCGUID AudioSessionGuid);
        COMMETHOD(
            [],
            HRESULT,
            "Initialize",
            (["in"], DWORD, "ShareMode"),
            (["in"], DWORD, "StreamFlags"),
            (["in"], REFERENCE_TIME, "hnsBufferDuration"),
            (["in"], REFERENCE_TIME, "hnsPeriodicity"),
            (["in"], POINTER(WAVEFORMATEX), "pFormat"),
            (["in"], POINTER(GUID), "AudioSessionGuid"),
        ),
        # HRESULT GetBufferSize(
        # [out] UINT32 *pNumBufferFrames);
        COMMETHOD(
            [], HRESULT, "GetBufferSize", (["out"], POINTER(UINT32), "pNumBufferFrames")
        ),
        # HRESULT GetStreamLatency(
        # [out] REFERENCE_TIME *phnsLatency);
        COMMETHOD(
            [],
            HRESULT,
            "GetStreamLatency",
            (["out"], POINTER(REFERENCE_TIME), "phnsLatency"),
        ),
        # HRESULT GetCurrentPadding(
        # [out] UINT32 *pNumPaddingFrames);
        COMMETHOD(
            [],
            HRESULT,
            "GetCurrentPadding",
            (["out"], POINTER(UINT32), "pNumPaddingFrames"),
        ),
        # HRESULT IsFormatSupported(
        # [in] AUDCLNT_SHAREMODE ShareMode,
        # [in] const WAVEFORMATEX *pFormat,
        # [out,unique] WAVEFORMATEX **ppClosestMatch);
        COMMETHOD(
            [],
            HRESULT,
            "IsFormatSupported",
            (["in"], DWORD, "ShareMode"),
            (["in"], POINTER(WAVEFORMATEX), "pFormat"),
            (["out"], POINTER(POINTER(WAVEFORMATEX)), "ppClosestMatch"),
        ),
        # HRESULT GetMixFormat(
        # [out] WAVEFORMATEX **ppDeviceFormat
        # );
        COMMETHOD(
            [],
            HRESULT,
            "GetMixFormat",
            (["out"], POINTER(POINTER(WAVEFORMATEX)), "ppDeviceFormat"),
        ),
        # HRESULT GetDevicePeriod(
        # [out] REFERENCE_TIME *phnsDefaultDevicePeriod,
        # [out] REFERENCE_TIME *phnsMinimumDevicePeriod);
        COMMETHOD(
            [],
            HRESULT,
            "GetDevicePeriod",
            (["out"], POINTER(REFERENCE_TIME), "phnsDefaultDevicePeriod"),
            (["out"], POINTER(REFERENCE_TIME), "phnsMinimumDevicePeriod"),
        ),
        # HRESULT Start(void);
        COMMETHOD([], HRESULT, "Start"),
        # HRESULT Stop(void);
        COMMETHOD([], HRESULT, "Stop"),
        # HRESULT Reset(void);
        COMMETHOD([], HRESULT, "Reset"),
        # HRESULT SetEventHandle([in] HANDLE eventHandle);
        COMMETHOD(
            [],
            HRESULT,
            "SetEventHandle",
            (["in"], HANDLE, "eventHandle"),
        ),
        # HRESULT GetService(
        # [in] REFIID riid,
        # [out] void **ppv);
        COMMETHOD(
            [],
            HRESULT,
            "GetService",
            (["in"], POINTER(GUID), "iid"),
            (["out"], POINTER(POINTER(IUnknown)), "ppv"),
        ),
    )


class IChannelAudioVolume (IUnknown):
    _iid_ = GUID('{1c158861-b533-4b30-b1cf-e853e51c59b8}')
    _methods_ = (
                COMMETHOD([], HRESULT, 'GetChannelCount',
                            (['out'], POINTER(UINT), 'pnChannelCount')),
                COMMETHOD([], HRESULT, 'SetChannelVolume',
                        (['in'], UINT, 'dwIndex'),
                        (['in'], c_float, 'fLevel'),
                        (['in'], POINTER(GUID), 'EventContext')),
    )
