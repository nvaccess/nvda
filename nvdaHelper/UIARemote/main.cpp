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
winrt::guid guid_msWord_moveEndpointBySentence{ 0x368e89a2, 0x1bc2, 0x4402, { 0x8c, 0x58, 0x33, 0xc6, 0x3e, 0xcf, 0xfa, 0x3b } };
winrt::guid guid_msWord_moveBySentence{ 0xf39655ac, 0x133a, 0x435b, { 0xa3, 0x18, 0xc1, 0x97, 0xf0, 0xd3, 0xd2, 0x3 } };
winrt::guid guid_msWord_expandToEnclosingSentence { 0x98fe8b34, 0xf317, 0x459a, { 0x96, 0x27, 0x21, 0x12, 0x3e, 0xa9, 0x5b, 0xea } };
winrt::guid guid_msWord_getMathText{ 0x380198e5, 0xa51f, 0x4618, { 0xa7, 0x8d, 0x57, 0xe9, 0x56, 0x8a, 0x38, 0x62 } };

extern "C" __declspec(dllexport) IUIAutomationTextRange* __stdcall msWord_expandToEnclosingSentence(IUIAutomationTextRange* pTextRangeArg) {
	try {
		auto scope=UiaOperationScope::StartNew();
		UiaBool isPatternSupported{false};
		UiaTextRange textRange{pTextRangeArg};
		auto element = textRange.GetEnclosingElement();
		isPatternSupported = element.IsExtensionSupported(guid_msWord_extendedTextRangePattern);
		scope.If(isPatternSupported,[&]() {
			UiaElement patternElement{nullptr};
			element.CallExtension(guid_msWord_extendedTextRangePattern, patternElement);
			patternElement.CallExtension(guid_msWord_expandToEnclosingSentence, textRange);
		});
		scope.BindResult(isPatternSupported, textRange);
		auto res = scope.ResolveHr();
		if(res != S_OK) {
			LOG_ERROR(L"Error in scope.Resolve: code "<<res);
		}
		if(isPatternSupported) {
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

