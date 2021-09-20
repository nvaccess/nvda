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

#include <collection.h>
#include <ppltasks.h>
#include <wrl.h>
#include <robuffer.h>
#include <windows.h>
#include <cstring>
#include <common/log.h>
#include "utils.h"
#include "uwpOcr.h"

using namespace std;
using namespace Platform;
using namespace concurrency;
using namespace Windows::Storage::Streams;
using namespace Microsoft::WRL;
using namespace Windows::Media::Ocr;
using namespace Windows::Foundation::Collections;
using namespace Windows::Globalization;
using namespace Windows::Graphics::Imaging;
using namespace Windows::Data::Json;

UwpOcr* __stdcall uwpOcr_initialize(const char16* language, uwpOcr_Callback callback) {
	auto engine = OcrEngine::TryCreateFromLanguage(ref new Language(ref new String(language)));
	if (!engine)
		return nullptr;
	auto instance = new UwpOcr;
	instance->engine = engine;
	instance->callback = callback;
	return instance;
}

void __stdcall uwpOcr_terminate(UwpOcr* instance) {
	delete instance;
}

void __stdcall uwpOcr_recognize(UwpOcr* instance, const RGBQUAD* image, unsigned int width, unsigned int height) {
	unsigned int numBytes = sizeof(RGBQUAD) * width * height;
	auto buf = ref new Buffer(numBytes);
	buf->Length = numBytes;
	BYTE* bytes = getBytes(buf);
	memcpy(bytes, image, numBytes);
	auto sbmp = SoftwareBitmap::CreateCopyFromBuffer(buf, BitmapPixelFormat::Bgra8, width, height, BitmapAlphaMode::Ignore);
	task<OcrResult^> ocrTask = create_task(instance->engine->RecognizeAsync(sbmp));
	ocrTask.then([instance, sbmp] (OcrResult^ result) {
		auto lines = result->Lines;
		auto jLines = ref new JsonArray();
		for (unsigned short l = 0; l < lines->Size; ++l) {
			auto words = lines->GetAt(l)->Words;
			auto jWords = ref new JsonArray();
			for (unsigned short w = 0; w < words->Size; ++w) {
				auto word = words->GetAt(w);
				auto jWord = ref new JsonObject();
				auto rect = word->BoundingRect;
				jWord->Insert("x", JsonValue::CreateNumberValue(rect.X));
				jWord->Insert("y", JsonValue::CreateNumberValue(rect.Y));
				jWord->Insert("width", JsonValue::CreateNumberValue(rect.Width));
				jWord->Insert("height", JsonValue::CreateNumberValue(rect.Height));
				jWord->Insert("text", JsonValue::CreateStringValue(word->Text));
				jWords->Append(jWord);
			}
			jLines->Append(jWords);
		}
		instance->callback(jLines->Stringify()->Data());
	}).then([instance] (task<void> previous) {
		// Catch any unhandled exceptions that occurred during these tasks.
		try {
			previous.get();
		} catch (Platform::Exception^ e) {
			LOG_ERROR(L"Error " << e->HResult << L": " << e->Message->Data());
			instance->callback(NULL);
		}
	});
}

// We use BSTR because we need the string to stay around until the caller is done with it
// but the caller then needs to free it.
// We can't just use malloc because the caller might be using a different CRT
// and calling malloc and free from different CRTs isn't safe.
BSTR __stdcall uwpOcr_getLanguages() {
	wstring langsStr;
	auto langs = OcrEngine::AvailableRecognizerLanguages ;
	for (unsigned int i = 0; i < langs->Size; ++i) {
		langsStr += langs->GetAt(i)->LanguageTag->Data();
		langsStr += L";";
	}
	return SysAllocString(langsStr.c_str());
}
