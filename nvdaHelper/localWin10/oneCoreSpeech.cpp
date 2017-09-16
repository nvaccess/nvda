/*
Code for C dll bridge to Windows OneCore voices.
This file is a part of the NVDA project.
URL: http://www.nvaccess.org/
Copyright 2016-2017 Tyler Spivey, NV Access Limited.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <string>
#include <collection.h>
#include <ppltasks.h>
#include <wrl.h>
#include <robuffer.h>
#include <common/log.h>
#include "utils.h"
#include "oneCoreSpeech.h"

using namespace std;
using namespace Platform;
using namespace Windows::Media::SpeechSynthesis;
using namespace concurrency;
using namespace Windows::Storage::Streams;
using namespace Microsoft::WRL;
using namespace Windows::Media;
using namespace Windows::Foundation::Collections;

OcSpeech* __stdcall ocSpeech_initialize() {
	auto instance = new OcSpeech;
	instance->synth = ref new SpeechSynthesizer();
	return instance;
}

void __stdcall ocSpeech_terminate(OcSpeech* instance) {
	delete instance;
}

void __stdcall ocSpeech_setCallback(OcSpeech* instance, ocSpeech_Callback fn) {
	instance->callback = fn;
}

void __stdcall ocSpeech_speak(OcSpeech* instance, char16 *text) {
	String^ textStr = ref new String(text);
	auto markersStr = make_shared<wstring>();
	task<SpeechSynthesisStream ^>  speakTask;
	try {
		speakTask = create_task(instance->synth->SynthesizeSsmlToStreamAsync(textStr));
	} catch (Platform::Exception ^e) {
		LOG_ERROR(L"Error " << e->HResult << L": " << e->Message->Data());
		instance->callback(NULL, 0, NULL);
		return;
	}
	speakTask.then([markersStr] (SpeechSynthesisStream^ speechStream) {
		// speechStream->Size is 64 bit, but Buffer can only take 32 bit.
		// We shouldn't get values above 32 bit in reality.
		const unsigned int size = static_cast<unsigned int>(speechStream->Size);
		Buffer^ buffer = ref new Buffer(size);
		IVectorView<IMediaMarker^>^ markers = speechStream->Markers;
		for (auto&& marker : markers) {
			if (markersStr->length() > 0) {
				*markersStr += L"|";
			}
			*markersStr += marker->Text->Data();
			*markersStr += L":";
			*markersStr += to_wstring(marker->Time.Duration);
		}
		auto t = create_task(speechStream->ReadAsync(buffer, size, Windows::Storage::Streams::InputStreamOptions::None));
		return t;
	}).then([instance, markersStr] (IBuffer^ buffer) {
		// Data has been read from the speech stream.
		// Pass it to the callback.
		byte* bytes = getBytes(buffer);
		instance->callback(bytes, buffer->Length, markersStr->c_str());
	}).then([instance] (task<void> previous) {
		// Catch any unhandled exceptions that occurred during these tasks.
		try {
			previous.get();
		} catch (Platform::Exception^ e) {
			LOG_ERROR(L"Error " << e->HResult << L": " << e->Message->Data());
			instance->callback(NULL, 0, NULL);
		}
	});
}

// We use BSTR because we need the string to stay around until the caller is done with it
// but the caller then needs to free it.
// We can't just use malloc because the caller might be using a different CRT
// and calling malloc and free from different CRTs isn't safe.
BSTR __stdcall ocSpeech_getVoices(OcSpeech* instance) {
	wstring voices;
	for (unsigned int i = 0; i < instance->synth->AllVoices->Size; ++i) {
		VoiceInformation^ info = instance->synth->AllVoices->GetAt(i);
		voices += info->Id->Data();
		voices += L":";
		voices += info->DisplayName->Data();
		if (i != instance->synth->AllVoices->Size - 1) {
			voices += L"|";
		}
	}
	return SysAllocString(voices.c_str());
}

const char16* __stdcall ocSpeech_getCurrentVoiceId(OcSpeech* instance) {
	return instance->synth->Voice->Id->Data();
}

void __stdcall ocSpeech_setVoice(OcSpeech* instance, int index) {
	instance->synth->Voice = instance->synth->AllVoices->GetAt(index);
}

const char16 * __stdcall ocSpeech_getCurrentVoiceLanguage(OcSpeech* instance) {
	return instance->synth->Voice->Language->Data();
}
