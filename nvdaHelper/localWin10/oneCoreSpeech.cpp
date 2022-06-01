/*
Copyright (C) 2016-2022 NV Access Limited, Tyler Spivey, Leonard de Ruijter
This file may be used under the terms of the GNU General Public License, version 2 or later.
For more details see: https://www.gnu.org/licenses/gpl-2.0.html
*/

#include <string>
#include <iostream>
#include <vector>
#include <algorithm>
#include <atomic>
#include <thread>
#include <functional>
#include <shared_mutex>
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

/*
* See design notes in oneCoreSpeech.h
*/

using ocSpeech_CallbackT = void(BYTE* data, int length, const wchar_t* markers);

class OcSpeechState {
public:
	std::shared_ptr<winrtSynth> getSynth(void* token) {
		if (isTokenValid(token)) {
			return m_synth;
		}
		return std::shared_ptr<winrtSynth>();
	}

	std::function<ocSpeech_CallbackT> getCB() {
		return m_callback;
	}

	bool isTokenValid(void* token) {
		if (
			!isActive()  // token can't be valid if one core is not active
			|| token == nullptr  // indicates this was never a valid token
			|| token != m_synth.get()  // only a token matching the synth pointer are active
			|| isTokenTerminated_(token)
		) {
			LOG_DEBUG(
				L"Token not active: " << token
				<< L" Terminated tokens: " << getTerminatedTokensString()
			);
			return false;
		}
		return true;
	}

	bool isTokenTerminated_(void* token) {
		if (token == nullptr) {
			LOG_ERROR(L"token is nullptr, it was never valid.");
		}
		for (const auto& t : m_terminatedTokens) {
			if (t.first == token) {
				return true;
			}
		}
		return false;
	}

	std::wstring getTerminatedTokensString() {
		std::wstringstream ss;
		for (const auto t : m_terminatedTokens) {
			ss << t.first << L"(use: " << t.second.use_count() << L"), ";
		}
		return ss.str();
	}

	void* activate(std::function<ocSpeech_CallbackT> cb) {
		LOG_INFO(L"Activating");
		if(!isTerminated()){
			LOG_ERROR(L"Unable to activate if not terminated.");
			return nullptr;
		}
		auto synth = std::make_shared<winrtSynth>();
		LOG_DEBUG(L"new token val: " << synth.get());
		removeTokenFromTerminated(synth.get());
		m_callback = cb;
		m_synth = synth;
		if (!isActive()){
			LOG_ERROR(L"Activating failed");
		}
		return m_synth.get();
	}

	void terminate() {
		LOG_INFO(L"Terminating");
		if (!isActive()) {
			LOG_ERROR(L"Unable to terminate if not active");
			return;
		}
		m_terminatedTokens.push_back({ m_synth.get(), m_synth });  // record weak_ptr for debugging.
		LOG_DEBUG(L" Terminated tokens: " << getTerminatedTokensString());

		m_synth.reset();
		m_callback = std::function<ocSpeech_CallbackT>();

		if (!isTerminated()) {
			LOG_ERROR(L"Terminating failed");
		}
	}

	/* Get the usage count of the last synth to be terminated.
	* Useful for debugging.
	*/
	int getLastSynthUsageCount() {
		if (m_terminatedTokens.size() > 0) {
			return m_terminatedTokens.rbegin()->second.use_count();
		}
		return 0;
	}

private:
	bool isActive() {
		const bool isSynthActive = bool(m_synth);
		const bool isCallbackActive = bool(m_callback);
		if (isSynthActive && isCallbackActive) {  // don't care about last synth. Status only useful for debugging.
			return true;
		}
		LOG_DEBUG(
			"oneCoreSpeech not Active. "
			<< createStateString(isSynthActive, isCallbackActive)
		);
		return false;
	}

	bool isTerminated() {
		const bool isSynthActive = bool(m_synth);
		const bool isCallbackActive = bool(m_callback);
		if (!isSynthActive && !isCallbackActive) {  // don't care about last synth. Status only useful for debugging.
			return true;
		}
		LOG_DEBUG(
			L"oneCoreSpeech not Terminated. "
			<< createStateString(isSynthActive, isCallbackActive)
		);
		return false;
	}

	void removeTokenFromTerminated(void* token) {
		auto numErased = std::erase_if(m_terminatedTokens, [token](auto& tokenPair) {
			return tokenPair.first == token;
		});
		if (numErased != 0) {
			LOG_DEBUG("Remove from terminated erased count: " << numErased << " while removing: " << token);
		}
	}

	std::wstring createStateString(const bool isSynthActive, const bool isCallbackActive) {
		std::wstringstream ss;
		ss << std::boolalpha
			<< L"m_synth: " << isSynthActive
			<< L" m_callback: " << isCallbackActive
			<< L" terminated tokens: " << getTerminatedTokensString();
		return ss.str();
	}

	std::shared_ptr<winrtSynth> m_synth;  // Held until terminate is called

	// Async code holds a shared_ptr keeping m_lastSynth active, this weak_ptr lets us check
	// when / if it expires and confirm the usage count.
	std::function < ocSpeech_CallbackT > m_callback;

	// m_terminatedTokens allows explicitly confirming that a token has been terminated.
	// order of termination is maintained.
	std::vector<std::pair<void*, std::weak_ptr<winrtSynth>>> m_terminatedTokens; // Only for debugging.
};


OcSpeechState g_state;

// Mutex to protect against state changes (of g_state).
// Allows shared read access (protectedCallback_)
// and exclusive write access (ocSpeech_initialize, ocSpeech_terminate)
std::shared_timed_mutex g_OcSpeechStateMutex{};

// The max wait time for to acquire a lock. Exceeding this likely indicates a deadlock.
std::chrono::duration g_maxWaitForLock(std::chrono::seconds(3));

UniqueLock getUniqueLock_(std::wstring forPurpose) {
	UniqueLock lock(g_OcSpeechStateMutex, std::defer_lock);
	bool owned = lock.try_lock();
	if (!owned) {
		LOG_DEBUG(L"Locking will block, try for timeout: " << forPurpose);
		owned = lock.try_lock_for(g_maxWaitForLock);
	}
	if (!owned) {
		LOG_ERROR(L"Unable to lock after timeout: " << forPurpose);
	}
	return lock;
}

void preventEndUtteranceSilence_(std::shared_ptr<winrtSynth> synth);

void* __stdcall ocSpeech_initialize(ocSpeech_Callback fn) {
	LOG_INFO(L"ocSpeech_initialize");
	// Ensure there are no pending shared locks, all async speak calls must be finished
	auto lock = getUniqueLock_(L"ocSpeech_initialize");
	if (!lock) {
		return nullptr;
	}
	LOG_DEBUG(L"ocSpeech_initialize lock acquired");

	auto token = g_state.activate(fn);
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"Unable to initialize.");
		return nullptr;
	}
	preventEndUtteranceSilence_(synth);
	return token;
}

void __stdcall ocSpeech_terminate(void* token) {
	std::wstringstream ss;
	ss << L"ocSpeech_terminate, token: " << token;
	LOG_INFO(ss.str());
	// Acquire a unique lock to ensure that no callbacks can happen while changing state.
	// Changing state must be atomic.
	auto lock = getUniqueLock_(ss.str());
	if (!lock) {
		return;
	}
	if (!g_state.isTokenValid(token)) {
		LOG_ERROR(L"ocSpeech_terminate error");
		return;
	}
	g_state.terminate();
}


/* Internal convenience pairing for a winRT synth result.
*/
struct SpeakResult {
	Buffer buffer;
	std::wstring markersStr;
};

/*Call the external callback.
* This requires a shared lock on the callback / g_OcSpeechStateMutex.
* This shared ownership prevents (blocks) unique locks from being acquired, thus blocking
* ocSpeech_initialize and ocSpeech_terminate.
* If the given token is no longer valid, the callback will not be called.
*/
void protectedCallback_(
	void* token,
	std::optional<SpeakResult> result,
	std::function<ocSpeech_CallbackT> cb
) {
	// Prevent any unique locks being acquired.
	SharedLock lock(g_OcSpeechStateMutex, std::defer_lock);
	const bool owned = lock.try_lock();
	if (!owned) {
		LOG_DEBUG(L"protectedCallback_ - Unable to lock. Token: " << token);
		return;
	}
	LOG_DEBUG(L"protectedCallback, token: " << token);
	if (!g_state.isTokenValid(token)) {
		LOG_INFO(L"not calling CB, token: " << token);
		return;
	}
	LOG_DEBUG(L"calling CB, token: " << token);
	if (result.has_value()) {
		cb(result->buffer.data(), result->buffer.Length(), result->markersStr.c_str());
	}
	else {
		cb(nullptr, 0, nullptr);
	}
	LOG_DEBUG(L"Finished CB, token: " << token);
}

bool isUniversalApiContractVersion_(const int major, const int minor);

bool __stdcall ocSpeech_supportsProsodyOptions() {
	return isUniversalApiContractVersion_(5, 0);
}

std::wstring createMarkersString_(IVectorView<IMediaMarker> markers) {
	std::wstring markersStr;  // for large strings, preallocating / reserving may speed this up.
	bool firstComplete = false;
	for (auto const& marker : markers) {
		if (firstComplete) {
			markersStr += L"|";
		}
		else {
			firstComplete = true;
		}
		markersStr += marker.Text();
		markersStr += L":";
		markersStr += std::to_wstring(marker.Time().count());
	}
	return markersStr;
}

/*
Send speech text to OneCore, call back to NVDA with synthesized speech.
This is an async function, it runs in the background via the Windows thread pool.
@param originToken Used to track the origin init of this call. Allows detection of synchronization errors.
@param text The text to synthesize.
@param synth A copy of the shared pointer to the winRT Synth.
This is safe to use from another thread (a reference to the same shared pointer is not).
@param cb The function associated with originToken. To be called when a result is available.
*/
winrt::fire_and_forget
speak(
	void* originToken,
	winrt::hstring text,
	std::shared_ptr<winrtSynth> synth,
	std::function<ocSpeech_CallbackT> cb
) {
	// Ensure we catch all exceptions in this method,
	// as an unhandled exception causes std::terminate to get called, resulting in a crash.
	// See https://devblogs.microsoft.com/oldnewthing/20190320-00/?p=102345
	try {
		// Ensure that work is performed on a background thread.
		// Note only use local var, not vars by ref.
		// See Microsoft docs:
		// https://docs.microsoft.com/en-us/windows/uwp/cpp-and-winrt-apis/concurrency#parameter-passing
		co_await winrt::resume_background();

		SpeechSynthesisStream speechStream{ nullptr };
		try {
			speechStream = co_await synth->SynthesizeSsmlToStreamAsync(text);
		}
		catch (winrt::hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			protectedCallback_(originToken, std::optional<SpeakResult>(), cb);
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
			protectedCallback_(originToken, result, cb);
			co_return;
		}
		catch (winrt::hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			protectedCallback_(originToken, std::optional<SpeakResult>(), cb);
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
	if (!g_state.isTokenValid(token)) {
		LOG_ERROR(L"speak error: invalid token" << token);
		return;
	}
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"speak error: synth not valid.");
		return;
	}
	auto cb = g_state.getCB();
	if (!cb) {
		LOG_ERROR(L"speak error: call back not valid");
		return;
	}
	speak(token, text, synth, cb);
}

// We use BSTR because we need the string to stay around until the caller is done with it
// but the caller then needs to free it.
// We can't just use malloc because the caller might be using a different CRT
// and calling malloc and free from different CRTs isn't safe.
BSTR __stdcall ocSpeech_getVoices(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"voices error");
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
	// By default, OneCore speech appends a large annoying chunk of silence at the end of every utterance.
	// Newer versions of OneCore speech allow disabling this feature, so turn it off where possible.
	const bool isAppendSilenceAvailable = isUniversalApiContractVersion_(6, 0);
	if (isAppendSilenceAvailable) {
		synth->Options().AppendedSilence(SpeechAppendedSilence::Min);
		LOG_INFO(L"AppendedSilence supported");
	}
	else {
		LOG_INFO(L"AppendedSilence not supported");
	}
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceId(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"ocSpeech_getCurrentVoiceId error");
		return L"";
	}
	winrt::hstring voiceId = synth->Voice().Id();
	return voiceId.c_str();
}

void __stdcall ocSpeech_setVoice(void* token, int index) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"ocSpeech_setVoice error");
		return;
	}
	synth->Voice(synth->AllVoices().GetAt(index));
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceLanguage(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"ocSpeech_getCurrentVoiceLanguage error");
		return L"";
	}
	return synth->Voice().Language().c_str();
}

double __stdcall ocSpeech_getPitch(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"ocSpeech_getPitch error");
		return 0.0;
	}
	return synth->Options().AudioPitch();
}

void __stdcall ocSpeech_setPitch(void* token, double pitch) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"ocSpeech_setPitch error");
		return;
	}
	synth->Options().AudioPitch(pitch);
}

double __stdcall ocSpeech_getVolume(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"ocSpeech_getVolume error");
		return 0.0;
	}
	return synth->Options().AudioVolume();
}

void __stdcall ocSpeech_setVolume(void* token, double volume) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"ocSpeech_setVolume error");
		return;
	}
	synth->Options().AudioVolume(volume);
}

double __stdcall ocSpeech_getRate(void* token) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"ocSpeech_getRate error");
		return 0.0;
	}
	return synth->Options().SpeakingRate();
}

void __stdcall ocSpeech_setRate(void* token, double rate) {
	auto synth = g_state.getSynth(token);
	if (!synth) {
		LOG_ERROR(L"ocSpeech_setRate error");
		return;
	}
	synth->Options().SpeakingRate(rate);
}
