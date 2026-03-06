// wgcCapture.h
// Windows Graphics Capture integration for NVDA.
// Captures window content via CreateForWindow, bypassing
// Magnification API color transforms (screen curtain).

#pragma once
#include <windows.h>

#ifdef __cplusplus
extern "C" {
#endif

// Callback receiving JSON OCR results (nullptr on failure).
// Format: [[{"x","y","width","height","text"}, ...], ...]
typedef void (*wgcCapture_Callback)(const wchar_t*);

// Opaque handle to a WGC capture + OCR instance.
typedef void* WgcCapture_H;

// True if Windows.Graphics.Capture is available (Win10 1903+).
bool __stdcall wgcCapture_isSupported();

// Create a WGC capture + OCR instance.
// language: BCP-47 tag (e.g. L"en-US"), or nullptr for user profile language.
// Returns handle, or nullptr on failure.
WgcCapture_H __stdcall wgcCapture_initialize(
	const wchar_t* language,
	wgcCapture_Callback callback
);

// Capture entire window by HWND and run OCR asynchronously.
// Works even when screen curtain is active (captures from compositor).
void __stdcall wgcCapture_recognizeWindow(
	WgcCapture_H handle,
	HWND hwnd
);

// Capture a sub-region of a window and run OCR asynchronously.
// Coordinates are relative to the window's client area.
void __stdcall wgcCapture_recognizeWindowRegion(
	WgcCapture_H handle,
	HWND hwnd,
	unsigned int x,
	unsigned int y,
	unsigned int width,
	unsigned int height
);

// Terminate and free a WGC capture + OCR instance.
void __stdcall wgcCapture_terminate(WgcCapture_H handle);

#ifdef __cplusplus
}
#endif
