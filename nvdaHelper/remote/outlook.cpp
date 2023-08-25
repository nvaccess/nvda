/*
This file is a part of the NVDA project.
Copyright 2018 NV Access Limited.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#define WIN32_LEAN_AND_MEAN

#include <memory>
#include <comdef.h>
#include <windows.h>
#include <common/log.h>
#include <common/libraryLoader.h>
#include <common/COMUtils.h>
#include "inProcess.h"
#include <remote/nvdaInProcUtils.h>

// The following declarations come from MAPIDEFS.h which is no longer included in the Windows SDK

constexpr ULONG PT_LONG=3;
constexpr ULONG MAPI_E_NOTFOUND=0x8004010f;
constexpr ULONG PROP_TYPE_MASK=0xffff;

typedef struct {
	ULONG ulPropTag;
	ULONG dwAlignPad;
	union {
		long l;
		// other types removed
	} Value;
} SPropValue;

using funcType_HrGetOneProp=HRESULT(STDAPICALLTYPE *)(IUnknown*,ULONG,SPropValue**);
using funcType_MAPIFreeBuffer=ULONG(STDAPICALLTYPE *)(SPropValue*);

// Our RPC function
error_status_t nvdaInProcUtils_outlook_getMAPIProp(handle_t bindingHandle, const long threadID, IUnknown* mapiObject, const unsigned long mapiPropTag, VARIANT* retVal) {
	if(!mapiObject) {
		LOG_ERROR(L"NULL MAPI object");
		return E_INVALIDARG;
	}
	if((mapiPropTag&PROP_TYPE_MASK)!=PT_LONG) {
		// Right now this function only supports MAPI properties with a type of long.
		// To support more types, we would need to know how to correctly pack them into a VARIANT.
		LOG_ERROR(L"Unsupported MAPI prop type");
		return E_INVALIDARG;
	}
	// Load mapi32 and manually lookup the functions we need.
	CLoadedLibrary mapi32lib=LoadLibrary(L"mapi32.dll");
	if(!mapi32lib) {
		LOG_ERROR(L"Could not load mapi32.dll");
		return E_UNEXPECTED;
	}
	auto HrGetOneProp=(funcType_HrGetOneProp)GetProcAddress(mapi32lib,"HrGetOneProp");
	if(!HrGetOneProp) {
		// Some versions of mapi32.dll name the HrGetOneProp symbol with an arguments size suffix 
		HrGetOneProp=(funcType_HrGetOneProp)GetProcAddress(mapi32lib,"HrGetOneProp@12");
	}
	if(!HrGetOneProp) {
		LOG_ERROR(L"Could not locate function HrGetOneProp in mapi32.dll");
		return E_UNEXPECTED;
	}
	auto MAPIFreeBuffer=(funcType_MAPIFreeBuffer)GetProcAddress(mapi32lib,"MAPIFreeBuffer");
	if(!MAPIFreeBuffer) {
		LOG_ERROR(L"Could not locate function MAPIFreeBuffer in mapi32.dll");
		return E_UNEXPECTED;
	}
	// NVDA gave us an IUnknown pointer representing the MAPI object from Outlook.
	// As the MAPIProp interface is not marshallable, we need to access it from its original STA thread as a real (non-proxied) raw pointer.
	// Therefore register the IUnknown in the COM global interface table so we can unmarshal it in the main GUI thread. 
	nvCOMUtils::InterfaceMarshaller im;
	HRESULT res=im.marshal(mapiObject);
	if(res!=S_OK) {
		LOG_ERROR(L"Failed to marshal MAPI object from rpc thread");
		return E_UNEXPECTED;
	}
	// Execute the following code in Outlook's GUI thread. 
	execInThread(threadID,[=,&res,&im](){
		// Unmarshal the IUnknown pointer from the COM global interface table.
		IUnknownPtr mapiObject=im.unmarshal<IUnknown>();
		if(!mapiObject) {
			LOG_ERROR(L"Failed to unmarshal MAPI object into Outlook GUI thread");
			return;
		}
		// Fetch the wanted property from the MAPI object
		std::unique_ptr<SPropValue,funcType_MAPIFreeBuffer> propValue {nullptr,MAPIFreeBuffer};
		{
			SPropValue* _propValue=nullptr;
			res=HrGetOneProp(mapiObject,mapiPropTag,&_propValue);
			propValue.reset(_propValue);
		}
		if(res!=S_OK) {
			// We should be quiet about  the error where the property does not exist as this happens most of the time.
			if(res!=MAPI_E_NOTFOUND) LOG_ERROR(L"Could not fetch MAPI property, code "<<res);
			return;
		}
		if(!propValue) {
			LOG_ERROR(L"NULL property value");
			res=E_UNEXPECTED;
			return;
		}
		// Pack the property value into the VARIANT for returning.
		// We can assume here that the type is long and nothing else.
		retVal->vt=VT_I4;
		retVal->lVal=propValue->Value.l;
	});
	return res;
}
