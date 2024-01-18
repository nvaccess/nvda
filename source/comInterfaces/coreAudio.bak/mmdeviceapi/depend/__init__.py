# This file is a part of pycaw library (https://github.com/AndreMiras/pycaw).
# Please note that it is distributed under MIT license:
# https://github.com/AndreMiras/pycaw#MIT-1-ov-file

from ctypes import HRESULT, POINTER
from ctypes.wintypes import DWORD

from comtypes import COMMETHOD, GUID, IUnknown

from .structures import PROPERTYKEY, PROPVARIANT


class IPropertyStore(IUnknown):
    _iid_ = GUID("{886d8eeb-8cf2-4446-8d02-cdba1dbdcf99}")
    _methods_ = (
        # HRESULT GetCount([out] DWORD *cProps);
        COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(DWORD), "cProps")),
        # HRESULT GetAt(
        # [in] DWORD iProp,
        # [out] PROPERTYKEY *pkey);
        COMMETHOD(
            [],
            HRESULT,
            "GetAt",
            (["in"], DWORD, "iProp"),
            (["out"], POINTER(PROPERTYKEY), "pkey"),
        ),
        # HRESULT GetValue(
        # [in] REFPROPERTYKEY key,
        # [out] PROPVARIANT *pv);
        COMMETHOD(
            [],
            HRESULT,
            "GetValue",
            (["in"], POINTER(PROPERTYKEY), "key"),
            (["out"], POINTER(PROPVARIANT), "pv"),
        ),
        # HRESULT SetValue(
        #   [in] REFPROPERTYKEY key,
        #   [in] REFPROPVARIANT propvar
        # );
        COMMETHOD(
            [],
            HRESULT,
            "SetValue",
            (["in"], POINTER(PROPERTYKEY), "key"),
            (["in"], POINTER(PROPVARIANT), "propvar"),
        ),
        # HRESULT Commit();
        COMMETHOD([], HRESULT, "Commit"),
    )

