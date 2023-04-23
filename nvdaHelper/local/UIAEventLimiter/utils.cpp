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
