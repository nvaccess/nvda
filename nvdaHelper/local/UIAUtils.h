#ifndef NVDAHELPERLOCAL_UIAUTILS_H
#define NVDAHELPERLOCAL_UIAUTILS_H

// The following header included to allow winrt::guid to be converted to GUID
#include <unknwn.h>

#include <winrt/windows.ui.uiautomation.core.h>
#include <uiAutomationCore.h>

PROPERTYID registerUIAProperty(GUID* guid, LPCWSTR programmaticName, UIAutomationType propertyType);
int registerUIAAnnotationType(GUID* guid);


#endif

