/*
Header for C dll bridge to UWP OCR.
This file is a part of the NVDA project.
URL: http://www.nvaccess.org/
Copyright 2017 NV Access Limited.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#pragma once
#define export __declspec(dllexport) 

typedef void (*uwpOcr_Callback)(const char16* result);
typedef struct {
	Windows::Media::Ocr::OcrEngine^ engine;
	uwpOcr_Callback callback;
} UwpOcr;

extern "C" {
export UwpOcr* __stdcall uwpOcr_initialize(const char16* language, uwpOcr_Callback callback);
export void __stdcall uwpOcr_terminate(UwpOcr* instance);
export void __stdcall uwpOcr_recognize(UwpOcr* instance, const RGBQUAD* image, unsigned int width, unsigned int height);
// Returns a BSTR of language codes terminated by semi-colons;
// e.g. "de-de;en-us;".
export BSTR __stdcall uwpOcr_getLanguages();
}
