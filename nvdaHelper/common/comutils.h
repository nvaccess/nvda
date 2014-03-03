#ifndef NVDAHELPER_COMUTILS_H
#define NVDAHELPER_COMUTILS_H

#include <comdef.h>
#include <common/log.h>

/**
	* A utility template function to queryService from a given IUnknown to the given service with the given service ID and interface eing returned.
	* @param siid the service iid
	*/
template<typename toInterface> inline HRESULT com_queryService(IUnknown* pUnknown, const IID& siid, toInterface** pIface) {
	HRESULT hRes;
	IServiceProvider* pServProv=NULL;
	hRes=pUnknown->QueryInterface(IID_IServiceProvider,(void**)&pServProv);
	if(hRes!=S_OK||!pServProv) {
		LOG_DEBUG(L"Could not queryInterface to IServiceProvider");
		return hRes;
	}
	hRes=pServProv->QueryService(siid,__uuidof(toInterface),(void**)pIface);
	pServProv->Release();
	if(hRes!=S_OK||!pIface) {
		LOG_DEBUG(L"Could not get requested interface");
		*pIface=NULL;
		return hRes;
	}
	return hRes;
}

#endif
