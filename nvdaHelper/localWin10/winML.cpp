/*
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
*/

#include <windows.h>
#ifndef _M_ARM64EC
#include <WindowsAppSDK-VersionInfo.h>
#include <MddBootstrap.h>
#endif
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Foundation.Collections.h>
#include <winrt/Microsoft.Windows.AI.MachineLearning.h>
#include <winml/onnxruntime_cxx_api.h>
#include "winML.h"
#include <memory>
#include <string>
#include <vector>

using namespace winrt;
using namespace winrt::Windows::Foundation;
using namespace winrt::Microsoft::Windows::AI::MachineLearning;

namespace {
	// Global state
	static std::unique_ptr<Ort::Env> g_ortEnv;
	static bool g_initialized = false;
}

extern "C" {

WINML_API int winML_initialize() {
	try {
		if (g_initialized) {
			return 0;
		}

	init_apartment();

#ifndef _M_ARM64EC
	// Initialize Windows App SDK bootstrap
	// Version 2.0 = 0x00020000 (majorMinorVersion format: 0xMMMMNNNN)
	UINT32 majorMinorVersion = 0x00020000;
	PCWSTR versionTag = nullptr;  // No version tag for experimental2
	PACKAGE_VERSION minVersion = { 0 };  // Use default minimum version
	MddBootstrapInitializeOptions options = MddBootstrapInitializeOptions_None;

	HRESULT hr = MddBootstrapInitialize2(
		majorMinorVersion,
		versionTag,
		minVersion,
		options
	);
	if (FAILED(hr)) {
		return -1;
	}
#endif
		// Create ONNX Runtime environment
		g_ortEnv = std::make_unique<Ort::Env>(ORT_LOGGING_LEVEL_ERROR, "NVDAWinML");

		// Get the default ExecutionProviderCatalog
		ExecutionProviderCatalog catalog = ExecutionProviderCatalog::GetDefault();

		// Ensure and register all compatible execution providers with ONNX Runtime
		auto operation = catalog.EnsureAndRegisterCertifiedAsync();
		operation.get();

		g_initialized = true;
		return 0;
	} catch (...) {
		return -1;
	}
}

WINML_API void* winML_createSession(const char* modelPath, int enableProfiling) {
	try {
		if (!g_initialized || !g_ortEnv) {
			return nullptr;
		}

		Ort::SessionOptions sessionOptions;
		if (enableProfiling) {
			sessionOptions.EnableProfiling(L"onnx_profile");
		}

		// Convert UTF-8 path to wide string for Windows
		int widePathLen = MultiByteToWideChar(CP_UTF8, 0, modelPath, -1, nullptr, 0);
		if (widePathLen == 0) {
			return nullptr;
		}

		std::wstring widePath(widePathLen - 1, L'\0');
		MultiByteToWideChar(CP_UTF8, 0, modelPath, -1, &widePath[0], widePathLen);

		// Create inference session
		auto session = new Ort::Session(*g_ortEnv, widePath.c_str(), sessionOptions);
		return static_cast<void*>(session);
	} catch (...) {
		return nullptr;
	}
}

WINML_API void winML_destroySession(void* session) {
	if (session) {
		delete static_cast<Ort::Session*>(session);
	}
}

WINML_API int winML_getInputCount(void* session) {
	try {
		if (!session) return 0;
		auto ortSession = static_cast<Ort::Session*>(session);
		return static_cast<int>(ortSession->GetInputCount());
	} catch (...) {
		return 0;
	}
}

WINML_API int winML_getOutputCount(void* session) {
	try {
		if (!session) return 0;
		auto ortSession = static_cast<Ort::Session*>(session);
		return static_cast<int>(ortSession->GetOutputCount());
	} catch (...) {
		return 0;
	}
}

WINML_API void winML_terminate() {
	g_ortEnv.reset();
	g_initialized = false;

#ifndef _M_ARM64EC
	// Shutdown Windows App SDK bootstrap
	MddBootstrapShutdown();
#endif

	uninit_apartment();
}

}
