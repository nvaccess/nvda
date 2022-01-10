#define _SILENCE_CXX17_CODECVT_HEADER_DEPRECATION_WARNING
#include <locale>
#include <codecvt>
#include <functional>
#include <string>
#include <windows.h>
#include <atlsafe.h>
#include <atlcomcli.h>
#include <roapi.h>
#include <winstring.h>
#include <UIAutomation.h>
#include <UiaOperationAbstraction/UiaOperationAbstraction.h>
#include <UiaOperationAbstraction/SafeArrayUtil.h>
#include <common/log.h>
#include <winrt/microsoft.ui.uiautomation.h>

using namespace UiaOperationAbstraction;

wchar_t dllDirectory[MAX_PATH];

winrt::guid guid_msWord_extendedTextRangePattern{ 0x93514122, 0xff04, 0x4b2c, { 0xa4, 0xad, 0x4a, 0xb0, 0x45, 0x87, 0xc1, 0x29 } };
winrt::guid guid_msWord_getCustomAttributeValue{ 0x81aca91, 0x32f2, 0x46f0, { 0x9f, 0xb9, 0x1, 0x70, 0x38, 0xbc, 0x45, 0xf8 } };

extern "C" __declspec(dllexport) bool __stdcall msWord_getCustomAttributeValue(IUIAutomationTextRange* pTextRangeArg, int customAttribIDArg, VARIANT* pCustomAttribValueArg) {
	try {
		auto scope=UiaOperationScope::StartNew();
		UiaBool isExtensionSupported{false};
		UiaTextRange textRange{pTextRangeArg};
		UiaInt customAttribID{customAttribIDArg};
		UiaVariant customAttribValue;
		auto element = textRange.GetEnclosingElement();
		scope.If(element.IsExtensionSupported(guid_msWord_extendedTextRangePattern),[&]() {
			UiaElement patternElement{nullptr};
			element.CallExtension(guid_msWord_extendedTextRangePattern, patternElement);
			scope.If(patternElement.IsExtensionSupported(guid_msWord_getCustomAttributeValue),[&]() {
				isExtensionSupported = true;
				patternElement.CallExtension(guid_msWord_getCustomAttributeValue, textRange, customAttribID, customAttribValue);
			});
		});
		scope.BindResult(isExtensionSupported, customAttribValue);
		auto res = scope.ResolveHr();
		if(res != S_OK) {
			LOG_ERROR(L"Error in scope.Resolve: code "<<res);
		}
		if(isExtensionSupported) {
			if(customAttribValue.IsInt()) {
				pCustomAttribValueArg->vt = VT_I4;
				pCustomAttribValueArg->lVal = customAttribValue.AsInt();
				return true;
			} else if(customAttribValue.IsString()) {
				pCustomAttribValueArg->vt = VT_BSTR;
				pCustomAttribValueArg->bstrVal = customAttribValue.AsString().get();
				return true;
			} else {
				LOG_ERROR(L"Unknown data type");
				return false;
			}
		} else {
			LOG_ERROR(L"Extension not supported");
		}
	} catch (std::exception& e) {
		std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
		auto what = converter.from_bytes(e.what());
		LOG_ERROR(L"msWord_expandToEnclosingSentence exception: "<<what);
	} catch(...) {
		LOG_ERROR(L"msWord_expandToEnclosingSentence exception: unknown");
	}
	return false;
}

extern "C" __declspec(dllexport) bool __stdcall initialize(bool doRemote, IUIAutomation* client) {
	std::wstring manifestPath = dllDirectory;
	manifestPath += L"\\Microsoft.UI.UIAutomation.dll.manifest";
	ACTCTX actCtx={0};
	actCtx.cbSize=sizeof(actCtx);
	actCtx.lpSource = L"Microsoft.UI.UIAutomation.dll.manifest";
	actCtx.lpAssemblyDirectory = dllDirectory;
	actCtx.dwFlags = ACTCTX_FLAG_ASSEMBLY_DIRECTORY_VALID;
	HANDLE hActCtx=CreateActCtx(&actCtx);
	if(hActCtx==NULL) {
		LOG_ERROR(L"Could not create activation context for "<<manifestPath);
		return false;
	}
	ULONG_PTR actCtxCookie;
	if(!ActivateActCtx(hActCtx,&actCtxCookie)) {
		LOG_ERROR(L"Error activating activation context for "<<manifestPath);
		ReleaseActCtx(hActCtx);
		return false;
	}
	LOG_INFO(L"Registered "<<manifestPath);
	if(!winrt::get_activation_factory<winrt::Microsoft::UI::UIAutomation::AutomationRemoteOperation>()) {
		LOG_ERROR(L"Unable to get Microsoft.UI.UIAutomation activation factory");
		return false;
	}
	LOG_INFO(L"Microsoft.UI.UIAutomation is available");
	UiaOperationAbstraction::Initialize(doRemote,client);
	return true;
}

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		GetModuleFileName(hModule,dllDirectory,MAX_PATH);
		PathRemoveFileSpec(dllDirectory);
	}
	return true;
}

