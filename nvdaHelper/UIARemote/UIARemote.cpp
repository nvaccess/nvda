/*
This file is a part of the NVDA project.
URL: http://www.nvaccess.org/
Copyright 2021-2022 NV Access Limited
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <memory>
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

#include "remoteLog.h"

wchar_t dllDirectory[MAX_PATH];

// Several custom extension GUIDs specific to Microsoft Word
winrt::guid guid_msWord_extendedTextRangePattern{ 0x93514122, 0xff04, 0x4b2c, { 0xa4, 0xad, 0x4a, 0xb0, 0x45, 0x87, 0xc1, 0x29 } };
winrt::guid guid_msWord_getCustomAttributeValue{ 0x81aca91, 0x32f2, 0x46f0, { 0x9f, 0xb9, 0x1, 0x70, 0x38, 0xbc, 0x45, 0xf8 } };

bool _isInitialized {false};

// Fetches a custom attribute value from a range of text in Microsoft Word.
// this function uses the UI automation Operation Abstraction API to call the Microsoft Word specific custom extension
extern "C" __declspec(dllexport) bool __stdcall msWord_getCustomAttributeValue(IUIAutomationElement* docElementArg, IUIAutomationTextRange* pTextRangeArg, int customAttribIDArg, VARIANT* pCustomAttribValueArg) {
	if(!_isInitialized) {
		LOG_ERROR(L"UIARemote not initialized!");
		return false;
	}
	try {
		auto scope=UiaOperationScope::StartNew();
		RemoteableLogger logger{scope};
		// Here starts declarative code which will be executed remotely
		logger<<L"Remoting msWord_getCustomAttributeValue"<<endl;
		UiaBool isExtensionSupported{false};
		UiaElement docElement{docElementArg};
		UiaTextRange textRange{pTextRangeArg};
		UiaInt customAttribID{customAttribIDArg};
		UiaVariant customAttribValue;
		scope.If(
			/* condition */ docElement.IsExtensionSupported(guid_msWord_extendedTextRangePattern),
			/* body */ [&]() {
				logger<<L"guid_msWord_extendedTextRangePattern is supported extension"<<endl;
				UiaElement patternElement{nullptr};
				docElement.CallExtension(guid_msWord_extendedTextRangePattern, patternElement);
				scope.If(
					/* condition */ patternElement,
					/* body */ [&]() {
						logger<<L"Got custom pattern element "<<endl;
						scope.If(
							/* condition */ patternElement.IsExtensionSupported(guid_msWord_getCustomAttributeValue),
							/* body */ [&]() {
								isExtensionSupported = true;
								logger<<L"guid_msWord_getCustomAttributeValue extension supported on pattern"<<endl;
								patternElement.CallExtension(guid_msWord_getCustomAttributeValue, textRange, customAttribID, customAttribValue);
								logger<<L"Called guid_msWord_getCustomAttributeValue extension"<<endl;
							},
							/* else */ [&]() {
								logger<<L"No guid_msWord_getCustomAttributeValue extension supported"<<endl;
							}
						);
					},
					/* else */ [&]() {
						logger<<L"Could not fetch guid_msWord_extendedTextRangePattern pattern"<<endl;
					}
				);
			},
			/* else */ [&]() {
				logger<<L"No guid_msWord_extendedTextRangePattern extension supported"<<endl;
			}
		);
		// Request that certain variables be made available locally after execution remotely
		scope.BindResult(isExtensionSupported, customAttribValue);
		// Actually execute the remote code
		auto res = scope.ResolveHr();
		if(res != S_OK) {
			LOG_ERROR(L"Error in scope.Resolve: code "<<res);
			return false;
		}
		logger.dumpLog();
		// We are back to local again 
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
			LOG_DEBUG(L"Extension not supported");
		}
	} catch (std::exception& e) {
		auto wideWhat = stringToWstring(e.what());
	LOG_ERROR(L"msWord_getCustomAttributeValue exception: "<<wideWhat);
	} catch(...) {
		LOG_ERROR(L"msWord_getCustomAttributeValue exception: unknown");
	}
	return false;
}

// Registers and initializes the Microsoft-ui-UIAutomation remote operations library.
extern "C" __declspec(dllexport) bool __stdcall initialize(bool doRemote, IUIAutomation* client) {
	std::wstring manifestPath = dllDirectory;
	manifestPath += L"\\Microsoft.UI.UIAutomation.dll.manifest";
	ACTCTX actCtx{};
	actCtx.cbSize=sizeof(actCtx);
	actCtx.lpSource = L"Microsoft.UI.UIAutomation.dll.manifest";
	actCtx.lpAssemblyDirectory = dllDirectory;
	actCtx.dwFlags = ACTCTX_FLAG_ASSEMBLY_DIRECTORY_VALID;
	HANDLE hActCtx=CreateActCtx(&actCtx);
	if(hActCtx == nullptr) {
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
	_isInitialized = true;
	return true;
}

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		GetModuleFileName(hModule,dllDirectory,MAX_PATH);
		PathRemoveFileSpec(dllDirectory);
	}
	return true;
}

