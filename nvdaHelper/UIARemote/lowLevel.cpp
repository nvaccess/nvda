#include <uiAutomationClient.h>
#include <winrt/windows.foundation.h>
#include <winrt/windows.foundation.collections.h>
#include <winrt/windows.ui.uiautomation.core.h>

using namespace winrt::Windows::Foundation;
using namespace winrt::Windows::UI::UIAutomation;
using namespace winrt::Windows::UI::UIAutomation::Core;

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOp_create(void** ppRemoteOp) {
	*ppRemoteOp = winrt::detach_abi(CoreAutomationRemoteOperation());
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOp_free(void* arg_pRemoteOp) {
	CoreAutomationRemoteOperation operation {nullptr};
	winrt::attach_abi(operation, arg_pRemoteOp);
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOp_importElement(void* arg_pRemoteOp, int arg_registerID, IUIAutomationElement* arg_pElement) {
	CoreAutomationRemoteOperation operation {nullptr};
	winrt::copy_from_abi(operation, arg_pRemoteOp);
	if(!operation) {
		return E_FAIL;
	}
	AutomationElement element {nullptr};
	winrt::copy_from_abi(element, arg_pElement);
	if(!element) {
		return E_FAIL;
	}
	operation.ImportElement(AutomationRemoteOperationOperandId{arg_registerID}, element);
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOp_importTextRange(void* arg_pRemoteOp, int arg_registerID, IUIAutomationTextRange* arg_pTextRange) {
	CoreAutomationRemoteOperation operation {nullptr};
	winrt::copy_from_abi(operation, arg_pRemoteOp);
	if(!operation) {
		return E_FAIL;
	}
	AutomationTextRange textRange {nullptr};
	winrt::copy_from_abi(textRange, arg_pTextRange);
	if(!textRange) {
		return E_FAIL;
	}
	operation.ImportTextRange(AutomationRemoteOperationOperandId{arg_registerID}, textRange);
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOp_addToResults(void* arg_pRemoteOp, int arg_registerID) {
	CoreAutomationRemoteOperation operation {nullptr};
	winrt::copy_from_abi(operation, arg_pRemoteOp);
	if(!operation) {
		return E_FAIL;
	}
	operation.AddToResults(AutomationRemoteOperationOperandId{arg_registerID});
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOp_isOpcodeSupported(void* arg_pRemoteOp, uint32_t arg_opcode, bool* pIsSupported) {
	CoreAutomationRemoteOperation operation {nullptr};
	winrt::copy_from_abi(operation, arg_pRemoteOp);
	if(!operation) {
		return E_FAIL;
	}
	*pIsSupported = operation.IsOpcodeSupported(arg_opcode);
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOp_execute(void* arg_pRemoteOp, uint8_t arg_byteCodeBuffer[], int arg_byteCodeBufferLength, void** ppResults) {
	CoreAutomationRemoteOperation operation {nullptr};
	winrt::copy_from_abi(operation, arg_pRemoteOp);
	if(!operation) {
		return E_FAIL;
	}
	auto results = operation.Execute(winrt::array_view<uint8_t>(arg_byteCodeBuffer, arg_byteCodeBufferLength));
	*ppResults = winrt::detach_abi(results);
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOpResult_getErrorLocation(void* arg_pResults, int* pErrorLocation) {
	AutomationRemoteOperationResult results {nullptr};
	winrt::copy_from_abi(results, arg_pResults);
	if(!results) {
		return E_INVALIDARG;
	}
	*pErrorLocation = results.ErrorLocation();
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOpResult_getExtendedError(void* arg_pResults, HRESULT* pExtendedError) {
	AutomationRemoteOperationResult results {nullptr};
	winrt::copy_from_abi(results, arg_pResults);
	if(!results) {
		return E_INVALIDARG;
	}
	*pExtendedError = results.ExtendedError();
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOpResult_getStatus(void* arg_pResults, int* pStatus) {
	AutomationRemoteOperationResult results {nullptr};
	winrt::copy_from_abi(results, arg_pResults);
	if(!results) {
		return E_INVALIDARG;
	}
	auto status = results.Status();
	*pStatus = static_cast<int>(status);
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOpResult_hasOperand(void* arg_pResults, int arg_registerID, bool* pHasOperand) {
	AutomationRemoteOperationResult results {nullptr};
	winrt::copy_from_abi(results, arg_pResults);
	if(!results) {
		return E_INVALIDARG;
	}
	*pHasOperand = results.HasOperand(AutomationRemoteOperationOperandId{arg_registerID});
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOpResult_free(void* arg_pResults) {
	AutomationRemoteOperationResult results {nullptr};
	winrt::attach_abi(results, arg_pResults);
	return S_OK;
}

HRESULT IInspectableToVariant(winrt::Windows::Foundation::IInspectable result, VARIANT* arg_pVariant) {
	if(!result) {
		// operand is NULL.
		return S_OK;
	}
	auto propVal = result.try_as<IPropertyValue>();
	if(propVal) {
		// Unbox property value into VARIANT
		auto propType = propVal.Type();
		switch(propVal.Type()) {
			case PropertyType::Int32:
				arg_pVariant->vt = VT_I4;
				arg_pVariant->lVal = propVal.GetInt32();
				break;
			case PropertyType::String:
				arg_pVariant->vt = VT_BSTR;
				arg_pVariant->bstrVal = SysAllocString(propVal.GetString().c_str());
				break;
			case PropertyType::Boolean:
				arg_pVariant->vt = VT_BOOL;
				arg_pVariant->boolVal = propVal.GetBoolean() ? VARIANT_TRUE : VARIANT_FALSE;
				break;
			case PropertyType::Inspectable:
				arg_pVariant->vt = VT_UNKNOWN;
				arg_pVariant->punkVal = static_cast<::IUnknown*>(winrt::detach_abi(propVal.as<winrt::Windows::Foundation::IUnknown>()));
				break;
			default:
				return E_NOTIMPL;
		}
		return S_OK;
	}
	auto vec = result.try_as<winrt::Windows::Foundation::Collections::IVector<winrt::Windows::Foundation::IInspectable>>();
	if(vec) {
		// Unbox vector into VARIANT array.
		auto vecSize = vec.Size();
		arg_pVariant->vt = VT_ARRAY | VT_VARIANT;
		arg_pVariant->parray = SafeArrayCreateVector(VT_VARIANT, 0, vecSize);
		if(!arg_pVariant->parray) {
			return E_OUTOFMEMORY;
		}
		for(ULONG i = 0; i < vecSize; i++) {
			auto vecItem = vec.GetAt(i);
			auto hr = IInspectableToVariant(vecItem, &static_cast<VARIANT*>(arg_pVariant->parray->pvData)[i]);
			if(FAILED(hr)) {
				return hr;
			}
		}
		return S_OK;
	}
	// Just treat it as an IUnknown.
	arg_pVariant->vt = VT_UNKNOWN;
	arg_pVariant->punkVal = static_cast<::IUnknown*>(winrt::detach_abi(result.as<winrt::Windows::Foundation::IUnknown>()));
	return S_OK;
}

extern "C" __declspec(dllexport) HRESULT __stdcall remoteOpResult_getOperand(void* arg_pResults, int arg_registerID, VARIANT* arg_pVariant) {
	AutomationRemoteOperationResult results {nullptr};
	winrt::copy_from_abi(results, arg_pResults);
	if(!results) {
		return E_INVALIDARG;
	}
	auto result = results.GetOperand(AutomationRemoteOperationOperandId{arg_registerID});
	return IInspectableToVariant(result, arg_pVariant);
}
