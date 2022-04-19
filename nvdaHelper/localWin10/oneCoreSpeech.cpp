/*
Code for C dll bridge to Windows OneCore voices.
This file is a part of the NVDA project.
URL: http://www.nvaccess.org/
Copyright 2016-2022 Tyler Spivey, NV Access Limited, Leonard de Ruijter.
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
#include <iostream>
#include <vector>
#include <algorithm>
#include <atomic>
#include <thread>
#include <functional>
#include <shared_mutex>
#include <ranges>
#include <condition_variable>
#include <winrt/Windows.Media.SpeechSynthesis.h>
#include <winrt/Windows.Storage.Streams.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Foundation.Collections.h>
#include <winrt/Windows.Foundation.Metadata.h>
#include <common/log.h>
#include "oneCoreSpeech.h"

using namespace winrt::Windows::Media::SpeechSynthesis;
using namespace winrt::Windows::Storage::Streams;
using namespace winrt::Windows::Media;
using namespace winrt::Windows::Foundation::Collections;
using winrt::Windows::Foundation::Metadata::ApiInformation;
using winrtSynth = winrt::Windows::Media::SpeechSynthesis::SpeechSynthesizer;
using SharedLock = std::shared_lock<std::shared_timed_mutex>;
using UniqueLock = std::unique_lock<std::shared_timed_mutex>;


enum class ApiState {
	reset, // init not yet called, no pending callbacks
	active, // synth created, callback set, ready to call speak
	terminated // token no longer valid, pending callbacks
};

std::ostream& operator<< (std::ostream& os, ApiState state)
{
	switch (state)
	{
	case ApiState::reset: return os << "reset";
	case ApiState::active: return os << "active";
	case ApiState::terminated: return os << "terminated";
		// omit default case to trigger compiler warning for missing cases
	};
	return os << static_cast<std::uint16_t>(state);
}

std::wostream& operator<< (std::wostream& os, ApiState state)
{
	switch (state)
	{
	case ApiState::reset: return os << L"reset";
	case ApiState::active: return os << L"active";
	case ApiState::terminated: return os << L"terminated";
		// omit default case to trigger compiler warning for missing cases
	};
	return os << static_cast<std::uint16_t>(state);
}

class OcSpeechState {
public:
	bool isInState(ApiState checkState) {
		if (m_state != checkState) {
			std::wstringstream ss;
			ss << L"OcSpeechState not (" << checkState << L") is instead: " << m_state;
			LOG_INFO(ss.str());
			return false;
		}
		switch (m_state) {
		case ApiState::reset:
				return areResetRequirementsMet();
			case ApiState::active:
				return areActiveRequirementsMet();
			case ApiState::terminated:
				return areTerminatedRequirementsMet();
		}
		return false;
	}

	void assertInState(ApiState expected) {
		if (!isInState(expected)) {
			std::wstringstream ss;
			ss << L"Not in expected state: " << expected;
			LOG_ERROR(ss.str());
			//throw std::runtime_error(ss.str());
		}
	}

	std::shared_ptr<winrtSynth> getSynth(void* token) {
		if (isTokenValid(token)){
			return m_synth;
		}
		return std::shared_ptr<winrtSynth>();
	}

	std::function<ocSpeech_CallbackT> getCB() {
		return m_callback;
	}

	bool isTokenValid(void* token) {
		if (
			!isInState(ApiState::active)
			|| token == nullptr
			|| token != m_synth.get()
			|| isTokenTerminated_(token)
		) {
			LOG_INFO(L"Token not active: " << token);
			logTermTokens();
			return false;
		}
		return true;
	}

	bool isTokenTerminated_(void* token) {
		return token != nullptr
			&& m_terminatedTokens.end() != std::ranges::find(m_terminatedTokens, token);
	}

	void logTermTokens() {
		std::wstringstream ss;
		ss << L"terminated tokens: ";
		for (const auto t : m_terminatedTokens) {
			ss << t << L", ";
		}
		LOG_INFO(ss.str());
	}

	void reset() {
		assertInState(ApiState::terminated);
		m_synth.reset();
		m_lastSynth.reset();
		m_state = ApiState::reset;
		assertInState(ApiState::reset);
	}

	void* activate(std::function<ocSpeech_CallbackT> cb) {
		LOG_INFO(L"activate");
		assertInState(ApiState::reset);
		auto synth = std::make_shared<winrtSynth>();
		LOG_INFO(L"synth valid:" << std::boolalpha << bool(synth));
		void* token = synth.get();
		LOG_INFO(L"token val: " << token);
		removeTokenFromTerminated(token);
		LOG_INFO(L"setting cb");
		m_callback = cb;
		LOG_INFO(L"setting synth");
		m_synth = synth;
		LOG_INFO(L"setting active state");
		m_state = ApiState::active;
		LOG_INFO(L"setting active state");
		assertInState(ApiState::active);
		LOG_INFO(L"return");
		return token;
	}

	void terminate() {
		assertInState(ApiState::active);
		auto token = m_synth.get();
		m_terminatedTokens.push_back(token);
		logTermTokens();
		m_lastSynth = m_synth;
		m_synth.reset();
		m_callback = std::function<ocSpeech_CallbackT>();
		m_state = ApiState::terminated;
		assertInState(ApiState::terminated);
	}

	std::shared_ptr<winrtSynth> m_synth;
	std::weak_ptr<winrtSynth> m_lastSynth;

private:
	bool areResetRequirementsMet() {
		if (!m_synth && !m_callback && m_lastSynth.expired()) {
			return true;
		}
		LOG_ERROR("oneCoreSpeech in unexpected state.");
		return false;
	}
	bool areActiveRequirementsMet() {
		if (m_synth && m_callback && m_lastSynth.expired()) {
			return true;
		}
		LOG_ERROR("oneCoreSpeech in unexpected state.");
		return false;
	}
	bool areTerminatedRequirementsMet() {
		if (!m_synth && !m_callback) {
			return true;
		}
		LOG_ERROR("oneCoreSpeech in unexpected state.");
		return false;
	}
	void removeTokenFromTerminated(void* token) {
		LOG_INFO(L"removing from terminated");
		auto num = std::erase(m_terminatedTokens, token);
		LOG_INFO(L"erased count: " << num);
	}

	std::atomic<ApiState> m_state{ ApiState::reset };
	std::function < ocSpeech_CallbackT> m_callback;
	std::vector<void*> m_terminatedTokens;
};


OcSpeechState g_state;
std::shared_timed_mutex g_OcSpeechStateMutex{};
std::chrono::duration g_maxWaitForLock(std::chrono::seconds(3));

bool isUniversalApiContractVersion_(const int major, const int minor);
void preventEndUtteranceSilence_(std::shared_ptr<winrtSynth> synth);


void* __stdcall ocSpeech_initialize(ocSpeech_Callback fn) {
	LOG_INFO(L"ocSpeech_initialize");
	// Ensure there are no pending shared locks, all async speak calls must be finished
	UniqueLock lock(g_OcSpeechStateMutex, std::defer_lock);
	bool owned = lock.try_lock();
	if (!owned) {
		LOG_INFO(L"ocSpeech_initialize locking will block, try for timeout:");
		owned = lock.try_lock_for(g_maxWaitForLock);
	}
	if (!owned) {
		LOG_ERROR(L"Unable to lock for init. ptr count: " << g_state.m_lastSynth.use_count());
		return nullptr;
	}
	LOG_INFO(L"ocSpeech_initialize lock owned");
	if (g_state.isInState(ApiState::terminated)) {
		LOG_INFO(L"do reset");
		g_state.reset();
	}
	
	auto token = g_state.activate(fn);
	LOG_INFO(L"get synth");
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"Unable to initialize.");
		//throw std::runtime_error("Unable to initialize.");
		return nullptr;
	}
	preventEndUtteranceSilence_(synth);
	return token;
}

void __stdcall ocSpeech_terminate(void* token) {
	LOG_INFO(L"ocSpeech_terminate, token: " << token);
	SharedLock lock(g_OcSpeechStateMutex, std::defer_lock);
	const bool owned = lock.try_lock();
	if (!owned) {
		LOG_ERROR(L"ocSpeech_terminate - Unable to lock. token: " << token);
		return;
	}
	if (!g_state.isTokenValid(token) ){
		LOG_ERROR(L"Terminate error");
		//throw std::runtime_error("Logic error on terminate, token not active.");
		return;
	}
	LOG_INFO(L"setting terminate state");
	g_state.terminate();
}


struct SpeakResult {
	Buffer buffer;
	std::wstring markersStr;
};


void protectedCallback_(
	void* token,
	std::optional<SpeakResult> result
) {
	LOG_INFO(L"protectedCallback, token: " << token);
	if (!g_state.isInState(ApiState::active)
		|| !g_state.isTokenValid(token)
	) {
		LOG_INFO(L"not calling CB, token: " << token);
		return;
	}
	LOG_INFO(L"calling CB, token: " << token);
	auto cb = g_state.getCB();
	if (result.has_value()) {
		cb(result->buffer.data(), result->buffer.Length(), result->markersStr.c_str());
	}
	else {
		cb(nullptr, 0, nullptr);
	}
	LOG_INFO(L"Finished CB, token: " << token);
}


bool __stdcall ocSpeech_supportsProsodyOptions() {
	return isUniversalApiContractVersion_(5, 0);
}

std::wstring createMarkersString_(IVectorView<IMediaMarker> markers) {
	std::wstring markersStr;  // for large strings, reserving would speed this up.
	bool firstComplete = false;
	for (auto const& marker : markers) {
		if (firstComplete) {
			markersStr += L"|";
		}
		else {
			firstComplete = false;
		}
		markersStr += marker.Text();
		markersStr += L":";
		markersStr += std::to_wstring(marker.Time().count());
	}
	return markersStr;
}

/*
Send speech to OneCore.
Will block OneCore from being re-initialized until speech callbacks have completed.
*/
winrt::fire_and_forget
speak(
	winrt::hstring text,
	std::shared_ptr<winrtSynth> synth,
	void* originToken,
	// Prevent any unique locks being acquired.
	SharedLock lock
) {
	if (!lock.owns_lock()) {
		LOG_ERROR(L"speak lock not owned, exiting. Token: " << originToken);
		co_return;
	}
	// Ensure we catch all exceptions in this method,
	// as an unhandled exception causes std::terminate to get called, resulting in a crash.
	// See https://devblogs.microsoft.com/oldnewthing/20190320-00/?p=102345
	try {
		// Ensure that work is performed on a background thread.
		co_await winrt::resume_background();

		SpeechSynthesisStream speechStream{ nullptr };
		try {
			speechStream = co_await synth->SynthesizeSsmlToStreamAsync(text);
		}
		catch (winrt::hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			protectedCallback_(originToken, std::optional<SpeakResult>());
			co_return;
		}
		// speechStream.Size() is 64 bit, but Buffer can only take 32 bit.
		// We shouldn't get values above 32 bit in reality.
		const std::uint32_t size = static_cast<std::uint32_t>(speechStream.Size());
		std::optional<SpeakResult> result(SpeakResult{
			Buffer(size),
			createMarkersString_(speechStream.Markers())
			}
		);
		try {
			co_await speechStream.ReadAsync(result->buffer, size, InputStreamOptions::None);
			// Data has been read from the speech stream.
			// Pass it to the callback.
			protectedCallback_(originToken, result);
			co_return;
		}
		catch (winrt::hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			protectedCallback_(originToken, std::optional<SpeakResult>());
			co_return;
		}
	}
	catch (winrt::hresult_error const& e) {
		LOG_ERROR(L"hresult error in OcSpeech::speak: " << e.code() << L": " << e.message().c_str());
	}
	catch (std::exception const& e) {
		LOG_ERROR(L"Exception in OcSpeech::speak: " << e.what());
	}
	catch (...) {
		LOG_ERROR(L"Unexpected error in speak");
	}
}

void __stdcall ocSpeech_speak(void* token, wchar_t* text) {
	// Prevent any unique locks being acquired.
	SharedLock lock(g_OcSpeechStateMutex, std::defer_lock);
	const bool owned = lock.try_lock();
	if (!owned) {
		LOG_ERROR(L"ocSpeech_speak - Unable to lock. Token: " << token);
		return;
	}
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"speak error");
		//throw std::runtime_error("Token not valid");
		return;
	}
	speak(text, synth, token, std::move(lock));
}

// We use BSTR because we need the string to stay around until the caller is done with it
// but the caller then needs to free it.
// We can't just use malloc because the caller might be using a different CRT
// and calling malloc and free from different CRTs isn't safe.
BSTR __stdcall ocSpeech_getVoices(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"voices error");
		//throw std::runtime_error("Token not valid");
		return SysAllocString(L"");
	}
	std::wstring voices;
	auto const& allVoices = synth->AllVoices();
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
	return SysAllocString(voices.c_str());
}


bool isUniversalApiContractVersion_(const int major, const int minor) {
	constexpr auto contract_name{ L"Windows.Foundation.UniversalApiContract" };
	return ApiInformation::IsApiContractPresent(
		winrt::hstring{ contract_name },
		major,
		minor
	);
}


void preventEndUtteranceSilence_(std::shared_ptr<winrtSynth> synth) {
	// By default, OneCore speech appends a  large annoying chunk of silence at the end of every utterance.
	// Newer versions of OneCore speech allow disabling this feature, so turn it off where possible.
	const bool isAppendSilenceAvailable = isUniversalApiContractVersion_(6, 0);
	if (isAppendSilenceAvailable) {
		synth->Options().AppendedSilence(SpeechAppendedSilence::Min);
	}
	else {
		LOG_INFO(L"AppendedSilence not supported");
	}
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceId(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		//throw std::runtime_error("Token not valid");
		LOG_ERROR(L"ocSpeech_getCurrentVoiceId error");
		return L"";
	}
	winrt::hstring voiceId = synth->Voice().Id();
	return voiceId.c_str();
}

void __stdcall ocSpeech_setVoice(void* token, int index) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		//throw std::runtime_error("Token not valid");
		LOG_ERROR(L"ocSpeech_setVoice error");
		return;
	}
	synth->Voice(synth->AllVoices().GetAt(index));
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceLanguage(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		//throw std::runtime_error("Token not valid");
		LOG_ERROR(L"ocSpeech_getCurrentVoiceLanguage error");
		return L"";
	}
	return synth->Voice().Language().c_str();
}

double __stdcall ocSpeech_getPitch(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		//throw std::runtime_error("Token not valid");
		LOG_ERROR(L"ocSpeech_getPitch error");
		return 0.0;
	}
	return synth->Options().AudioPitch();
}

void __stdcall ocSpeech_setPitch(void* token, double pitch) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		//throw std::runtime_error("Token not valid");
		LOG_ERROR(L"ocSpeech_setPitch error");
		return;
	}
	synth->Options().AudioPitch(pitch);
}

double __stdcall ocSpeech_getVolume(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		//throw std::runtime_error("Token not valid");
		LOG_ERROR(L"ocSpeech_getVolume error");
		return 0.0;
	}
	return synth->Options().AudioVolume();
}

void __stdcall ocSpeech_setVolume(void* token, double volume) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		//throw std::runtime_error("Token not valid");
		LOG_ERROR(L"ocSpeech_setVolume error");
		return;
	}
	synth->Options().AudioVolume(volume);
}

double __stdcall ocSpeech_getRate(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		//throw std::runtime_error("Token not valid");
		LOG_ERROR(L"ocSpeech_getRate error");
		return 0.0;
	}
	return synth->Options().SpeakingRate();
}

void __stdcall ocSpeech_setRate(void* token, double rate) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		//throw std::runtime_error("Token not valid");
		LOG_ERROR(L"ocSpeech_setRate error");
		return;
	}
	synth->Options().SpeakingRate(rate);
}
