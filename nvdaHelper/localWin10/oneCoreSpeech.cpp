/*
Code for C dll bridge to Windows OneCore voices.
This file is a part of the NVDA project.
URL: http://www.nvaccess.org/
Copyright 2016-2020 Tyler Spivey, NV Access Limited, Leonard de Ruijter.
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
#include <winrt/Windows.Media.SpeechSynthesis.h>
#include <winrt/Windows.Storage.Streams.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Foundation.Collections.h>
#include <winrt/Windows.Foundation.Metadata.h>
#include <common/log.h>
#include "oneCoreSpeech.h"

using namespace std;
using namespace winrt;
using namespace winrt::Windows::Media::SpeechSynthesis;
using namespace winrt::Windows::Storage::Streams;
using namespace winrt::Windows::Media;
using namespace winrt::Windows::Foundation::Collections;
using winrt::Windows::Foundation::Metadata::ApiInformation;

bool __stdcall ocSpeech_supportsProsodyOptions() {
	return ApiInformation::IsApiContractPresent(hstring{L"Windows.Foundation.UniversalApiContract"}, 5, 0);
}

OcSpeech::OcSpeech() : synth(SpeechSynthesizer{}) {
	// By default, OneCore speech appends a  large annoying chunk of silence at the end of every utterance.
	// Newer versions of OneCore speech allow disabling this feature, so turn it off where possible.
	if (ApiInformation::IsApiContractPresent(hstring{L"Windows.Foundation.UniversalApiContract"}, 6, 0)) {
		synth.Options().AppendedSilence(SpeechAppendedSilence::Min);
	} else {
		LOG_DEBUGWARNING(L"AppendedSilence not supported");
	}
}

OcSpeech* __stdcall ocSpeech_initialize() {
	auto instance = new OcSpeech;
	return instance;
}

void __stdcall ocSpeech_terminate(OcSpeech* instance) {
	delete instance;
}

void __stdcall ocSpeech_setCallback(OcSpeech* instance, ocSpeech_Callback fn) {
	instance->setCallback(fn);
}

void OcSpeech::setCallback(ocSpeech_Callback fn) {
	callback = fn;
}

fire_and_forget OcSpeech::speak(hstring text) {
	try {
		// Ensure that work is performed on a background thread.
		co_await resume_background();

		auto markersStr = make_shared<wstring>();
		SpeechSynthesisStream speechStream{ nullptr };
		try {
			speechStream = co_await synth.SynthesizeSsmlToStreamAsync(text);
		} catch (hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			callback(nullptr, 0, nullptr);
			co_return;
		}
		// speechStream.Size() is 64 bit, but Buffer can only take 32 bit.
		// We shouldn't get values above 32 bit in reality.
		const unsigned int size = static_cast<unsigned int>(speechStream.Size());
		Buffer buffer { size };

		IVectorView<IMediaMarker> markers = speechStream.Markers();
		for (auto const& marker : markers) {
			if (markersStr->length() > 0) {
				*markersStr += L"|";
			}
			*markersStr += marker.Text();
			*markersStr += L":";
			*markersStr += to_wstring(marker.Time().count());
		}
		try {
			co_await speechStream.ReadAsync(buffer, size, InputStreamOptions::None);
			// Data has been read from the speech stream.
			// Pass it to the callback.
			BYTE* bytes = buffer.data();
			callback(bytes, buffer.Length(), markersStr->c_str());
		} catch (hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			callback(nullptr, 0, nullptr);
		}
	} catch (...) {
		LOG_ERROR(L"Unexpected error in OcSpeech::speak");
	}
}

void __stdcall ocSpeech_speak(OcSpeech* instance, wchar_t* text) {
	instance->speak(text);
}

wstring OcSpeech::getVoices() {
	wstring voices;
	auto const& allVoices = synth.AllVoices();
	for (unsigned int i = 0; i < allVoices.Size(); ++i) {
		VoiceInformation const& voiceInfo = allVoices.GetAt(i);
		voices += voiceInfo.Id();
		voices += L":";
		voices += voiceInfo.Language();
		voices += L":";
		voices += voiceInfo.DisplayName();
		if (i != allVoices.Size() - 1) {
			voices += L"|";
		}
	}
	return voices;
}

// We use BSTR because we need the string to stay around until the caller is done with it
// but the caller then needs to free it.
// We can't just use malloc because the caller might be using a different CRT
// and calling malloc and free from different CRTs isn't safe.
BSTR __stdcall ocSpeech_getVoices(OcSpeech* instance) {
	return SysAllocString(instance->getVoices().c_str());
}

hstring OcSpeech::getCurrentVoiceId() {
	return synth.Voice().Id();
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceId(OcSpeech* instance) {
	return instance->getCurrentVoiceId().c_str();
}

void OcSpeech::setVoice(int index) {
	synth.Voice(synth.AllVoices().GetAt(index));
}

void __stdcall ocSpeech_setVoice(OcSpeech* instance, int index) {
	instance->setVoice(index);
}

hstring OcSpeech::getCurrentVoiceLanguage() {
	return synth.Voice().Language();
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceLanguage(OcSpeech* instance) {
	return instance->getCurrentVoiceLanguage().c_str();
}

double OcSpeech::getPitch() {
	return synth.Options().AudioPitch();
}

double __stdcall ocSpeech_getPitch(OcSpeech* instance) {
	return instance->getPitch();
}

void OcSpeech::setPitch(double pitch) {
	synth.Options().AudioPitch(pitch);
}

void __stdcall ocSpeech_setPitch(OcSpeech* instance, double pitch) {
	instance->setPitch(pitch);
}

double OcSpeech::getVolume() {
	return synth.Options().AudioVolume();
}

double __stdcall ocSpeech_getVolume(OcSpeech* instance) {
	return instance->getVolume();
}

void OcSpeech::setVolume(double volume) {
	synth.Options().AudioVolume(volume);
}

void __stdcall ocSpeech_setVolume(OcSpeech* instance, double volume) {
	instance->setVolume(volume);
}

double OcSpeech::getRate() {
	return synth.Options().SpeakingRate();
}

double __stdcall ocSpeech_getRate(OcSpeech* instance) {
	return instance->getRate();
}

void OcSpeech::setRate(double rate) {
	synth.Options().SpeakingRate(rate);
}

void __stdcall ocSpeech_setRate(OcSpeech* instance, double rate) {
	instance->setRate(rate);
}
