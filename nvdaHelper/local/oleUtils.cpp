/*
A part of NonVisual Desktop Access (NVDA)
Copyright (C) 2019-2025 NV Access Limited
This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
*/

#include <windows.h>
#include <wtypes.h>
#include <atlcomcli.h>
#include <common/log.h>

/*
 * Fetches a text representation of the given OLE data object
 * @param dataObject an IDataObject interface of an OLE object
 * @param text a pointer to a BSTR which will hold the resulting text
 * @return S_OK on success or an OLE error code.
 */
HRESULT getOleClipboardText(IUnknown* pUnknown, BSTR* text) {
	if (!pUnknown) {
		LOG_DEBUGWARNING(L"pUnknown is null.");
		return E_INVALIDARG;
	}
	CComQIPtr<IDataObject> pDataObject(pUnknown);
	if (!pDataObject) {
		LOG_DEBUGWARNING(L"Could not get IDataObject interface from pUnknown");
		return E_NOINTERFACE;
	}
	FORMATETC format={CF_UNICODETEXT,nullptr,DVASPECT_CONTENT,-1,TYMED_HGLOBAL};
	STGMEDIUM  medium={0};
	HRESULT res = pDataObject->GetData(&format, &medium);
	if(FAILED(res)) {
		LOG_DEBUGWARNING(L"IDataObject::getData failed with error "<<res);
		return res;
	}
	if(medium.tymed!=TYMED_HGLOBAL||!medium.hGlobal) {
		LOG_DEBUGWARNING(L"Got back invalid medium");
		return E_FAIL;
	}
	LPVOID addr=GlobalLock(medium.hGlobal);
	if(addr) {
		*text=SysAllocString((wchar_t*)addr);
	}
	GlobalUnlock(medium.hGlobal);
	ReleaseStgMedium(&medium);
	return res;
}

HRESULT getOleUserType(IUnknown* pUnknown, DWORD dwFlags, BSTR* userType) {
	if (!pUnknown) {
		LOG_DEBUGWARNING(L"pUnknown is null.");
		return E_INVALIDARG;
	}
	if (!userType) {
		LOG_DEBUGWARNING(L"userType is null.");
		return E_INVALIDARG;
	}
	CComQIPtr<IOleObject> pOleObject(pUnknown);
	if (!pOleObject) {
		LOG_DEBUGWARNING(L"Could not get IOleObject interface from pUnknown");
		return E_NOINTERFACE;
	}
	LPOLESTR pOleStr{nullptr};
	HRESULT res = pOleObject->GetUserType(dwFlags, &pOleStr);
	if (FAILED(res)) {
		LOG_DEBUGWARNING(L"IOleObject::GetUserType failed with error " << res
			<< L" for flags " << dwFlags);
		return res;
	}
	if (!pOleStr) {
		LOG_DEBUGWARNING(L"IOleObject::GetUserType returned null string for flags " << dwFlags);
		return E_FAIL;
	}
	*userType = SysAllocString(pOleStr);
	CComPtr<IMalloc> pMalloc;
	if (SUCCEEDED(CoGetMalloc(MEMCTX_TASK, &pMalloc)) && pMalloc) {
		pMalloc->Free(pOleStr);
	} else {
		LOG_ERROR(L"Failed to get IMalloc interface to free memory for pOleStr");
	}
	return S_OK;
}
