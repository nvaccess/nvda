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

winrt::guid GUID_MSWORD_EXPANDTOENCLOSINGSENTENCE { 0x98fe8b34, 0xf317, 0x459a, { 0x96, 0x27, 0x21, 0x12, 0x3e, 0xa9, 0x5b, 0xea } };

extern "C" __declspec(dllexport) IUIAutomationTextRange* __stdcall msWord_expandToEnclosingSentence(IUIAutomationTextRange* pTextRangeArg) {
	try {
		auto scope=UiaOperationScope::StartNew();
		UiaBool isSupported{false};
		UiaTextRange textRange{pTextRangeArg};
		auto element = textRange.GetEnclosingElement();
		scope.If(element.IsExtensionSupported(GUID_MSWORD_EXPANDTOENCLOSINGSENTENCE),[&]() {
			isSupported = true;
			element.CallExtension(GUID_MSWORD_EXPANDTOENCLOSINGSENTENCE, textRange);
		});
		scope.BindResult(isSupported, textRange);
		auto res = scope.ResolveHr();
		if(res != S_OK) {
			LOG_ERROR(L"Error in scope.Resolve: code "<<res);
		}
		if(isSupported) {
			return (*textRange).detach();
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
	return nullptr;
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

