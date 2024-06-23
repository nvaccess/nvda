/*
This file is a part of the NVDA project.
URL: http://github.com/nvaccess/nvda/
Copyright 2023 NV Access Limited.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <vector>
#include <UIAutomation.h>
#include <comutil.h>
#include "utils.h"

std::vector<int> SafeArrayToVector(SAFEARRAY* pSafeArray) {
	std::vector<int> vec;
	int* data;
	HRESULT hr = SafeArrayAccessData(pSafeArray, (void**)&data);
	if (SUCCEEDED(hr)) {
		LONG lowerBound, upperBound;
		SafeArrayGetLBound(pSafeArray, 1, &lowerBound);
		SafeArrayGetUBound(pSafeArray, 1, &upperBound);
		vec.assign(data, data + (upperBound - lowerBound + 1));
		SafeArrayUnaccessData(pSafeArray);
	}
	return vec;
}

std::vector<int> getRuntimeIDFromElement(IUIAutomationElement* pElement) {
	SAFEARRAY* runtimeIdArray;
	HRESULT hr = pElement->GetRuntimeId(&runtimeIdArray);
	if (FAILED(hr)) {
		return {};
	}
	std::vector<int> runtimeID = SafeArrayToVector(runtimeIdArray);
	SafeArrayDestroy(runtimeIdArray);
	return runtimeID;
}
