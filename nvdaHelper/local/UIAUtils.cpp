#include "UIAUtils.h"
#include <common/log.h>

PROPERTYID registerUIAProperty(GUID* guid, LPCWSTR programmaticName, UIAutomationType propertyType) {
	HRESULT res;
	IUIAutomationRegistrar* registrar=NULL;
	if(CoCreateInstance(CLSID_CUIAutomationRegistrar,NULL,CLSCTX_INPROC_SERVER,IID_IUIAutomationRegistrar,(void**)&registrar)!=S_OK) {
		LOG_DEBUGWARNING(L"Could not create instance of IUIAutomationRegistrar");
		return 0;
	}
	UIAutomationPropertyInfo info={*guid,programmaticName,propertyType};
	PROPERTYID propertyId=0;
	res=registrar->RegisterProperty(&info,&propertyId);
	if(res!=S_OK) {
		LOG_DEBUGWARNING(L"IUIAutomationRegistrar::RegisterProperty failed with "<<res);
		return 0;
	}
	registrar->Release();
	return propertyId;
}
