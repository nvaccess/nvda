/*
Code for C dll bridge to UWP OCR.
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

#include <winrt/Windows.Storage.Streams.h>
#include <winrt/Windows.Media.Ocr.h>
#include <winrt/Windows.Foundation.Collections.h>
#include <winrt/Windows.Globalization.h>
#include <winrt/Windows.Graphics.Imaging.h>
#include <winrt/Windows.Data.Json.h>
#include <windows.h>
#include <cstring>
#include <common/log.h>
#include "uwpOcr.h"

using namespace std;
using namespace winrt;
using namespace winrt::Windows::Storage::Streams;
using namespace winrt::Windows::Media::Ocr;
using namespace winrt::Windows::Foundation::Collections;
using namespace winrt::Windows::Globalization;
using namespace winrt::Windows::Graphics::Imaging;
using namespace winrt::Windows::Data::Json;

UwpOcr::UwpOcr(OcrEngine const& engine, uwpOcr_Callback callback) : engine(engine), callback(callback) { }

UwpOcr* __stdcall uwpOcr_initialize(const wchar_t* language, uwpOcr_Callback callback) {
	auto engine = OcrEngine::TryCreateFromLanguage(Language{ language });
	if (!engine) {
		return nullptr;
	}
	auto instance = new UwpOcr{ engine, callback };
	return instance;
}

void __stdcall uwpOcr_terminate(UwpOcr* instance) {
	delete instance;
}

fire_and_forget UwpOcr::recognize(SoftwareBitmap bitmap) {
	// Ensure we catch all exceptions in this method,

	// as an unhandled exception causes std::terminate to get called, resulting in a crash.
	// See https://devblogs.microsoft.com/oldnewthing/20190320-00/?p=102345
	try {
		// Ensure that work is performed on a background thread.
		co_await resume_background();

		auto result = co_await engine.RecognizeAsync(bitmap);
		auto lines = result.Lines();
		JsonArray jLines {};

		for (auto const& line : lines) {
			auto words = line.Words();
			JsonArray jWords {};

			for (auto const& word : words) {
				JsonObject jWord {};

				auto rect = word.BoundingRect();
				jWord.Insert(L"x", JsonValue::CreateNumberValue(rect.X));
				jWord.Insert(L"y", JsonValue::CreateNumberValue(rect.Y));
				jWord.Insert(L"width", JsonValue::CreateNumberValue(rect.Width));
				jWord.Insert(L"height", JsonValue::CreateNumberValue(rect.Height));
				jWord.Insert(L"text", JsonValue::CreateStringValue(word.Text()));
				jWords.Append(jWord);
			}
			jLines.Append(jWords);
		}
		callback(jLines.Stringify().c_str());
	} catch (hresult_error const& e) {
		LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
		callback(nullptr);
	} catch (...) {
		LOG_ERROR(L"Unexpected error in UwpOcr::recognize");
		callback(nullptr);
	}
}

void __stdcall uwpOcr_recognize(UwpOcr* instance, const RGBQUAD* image, unsigned int width, unsigned int height) {
	unsigned int numBytes = sizeof(RGBQUAD) * width * height;
	Buffer buf { numBytes };
	buf.Length(numBytes);
	BYTE* bytes = buf.data();
	memcpy(bytes, image, numBytes);
	auto sbmp = SoftwareBitmap::CreateCopyFromBuffer(buf, BitmapPixelFormat::Bgra8, width, height, BitmapAlphaMode::Ignore);
	instance->recognize(sbmp);
}

// We use BSTR because we need the string to stay around until the caller is done with it
// but the caller then needs to free it.
// We can't just use malloc because the caller might be using a different CRT
// and calling malloc and free from different CRTs isn't safe.
BSTR __stdcall uwpOcr_getLanguages() {
	wstring langsStr;
	auto langs = OcrEngine::AvailableRecognizerLanguages();
	for (auto const& lang : langs) {
		langsStr += lang.LanguageTag();
		langsStr += L";";
	}
	return SysAllocString(langsStr.c_str());
}
