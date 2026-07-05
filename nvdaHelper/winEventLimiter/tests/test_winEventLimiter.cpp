/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2019-2026 NV Access Limited, Bill Dengler
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2.0, as published by
the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include "stdafx.h"
#include "CppUnitTest.h"
#include "eventDoubleBuffer.h"
#include "eventLimiterThread.h"
#include "eventNotifier.h"
#include "winEventLimiter.h"
#include <WinUser.h>
#include <atomic>
#include <chrono>
#include <future>
#include <thread>

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

std::vector<DWORD> specialCaseEvents({
	EVENT_SYSTEM_FOREGROUND,
	EVENT_OBJECT_FOCUS,
	EVENT_OBJECT_SHOW,
	EVENT_OBJECT_HIDE,
	EVENT_SYSTEM_MENUSTART,
	EVENT_SYSTEM_MENUEND,
	EVENT_SYSTEM_MENUPOPUPSTART,
	EVENT_SYSTEM_MENUPOPUPEND,
});

namespace Microsoft {
	namespace VisualStudio {
		namespace CppUnitTestFramework
		{
			template<> inline std::wstring ToString<std::vector<int>>(const std::vector<int>& t) {
				std::wstringstream ss;
				ss << "[ ";
				for (auto i : t) {
					ss << i << L", ";
				}
				ss << " ]";
				return ss.str();
			}
		}
	}
}

namespace {

	// Builds an event whose window, objectID and childID are all `id`,
	// making each id a distinct object as far as the limiter is concerned.
	EventData makeEvent(DWORD idEvent, int id, DWORD threadID = 0) {
		return EventData{
			idEvent,
			reinterpret_cast<HWND>(static_cast<INT_PTR>(id)),
			id, // idObject
			id, // idChild
			threadID,
			0, // dwmsEventTime
		};
	}

	void addEvent(WinEventLimiter& limiter, DWORD idEvent, int id, DWORD threadID = 0) {
		auto e = makeEvent(idEvent, id, threadID);
		limiter.AddEvent(e);
	}

	std::vector<int> flushIds(WinEventLimiter& limiter) {
		auto events = limiter.Flush();
		std::vector<int> ids;
		for (auto& e : events) {
			ids.push_back(e.idObject);
		}
		return ids;
	}

}

namespace WinEventLimiterTests
{
	TEST_CLASS(test_WinEventLimiter)
	{
	public:

		TEST_METHOD(test_limitEventsPerThread)
		{
			WinEventLimiter limiter;
			for (int n = 2000 - 1; n >= 0; --n) {
				EventData e = {
					specialCaseEvents[n % specialCaseEvents.size()],
					reinterpret_cast<HWND>(static_cast<INT_PTR>(n)), // window
					n, // objectID - in this test, used as an ID.
					n, // childID
					0, // threadID - all events for same thread
				};
				limiter.AddEvent(e);
			}

			auto actualEvents = limiter.Flush();
			std::vector<int> actualIds;
			for (auto& e : actualEvents) {
				actualIds.push_back(e.idObject);
			}
			// Derivation: events are added from n=1999 down to n=0, so chronological
			// order is descending n, and event type cycles through specialCaseEvents
			// by n % 8 (0=foreground, 1=focus, 2=show, 3=hide, 4-7=menu). All ids are
			// distinct, so no duplicate or show/hide cancellation applies.
			// - Focus class (n % 8 in {0, 1}): the newest MAX_FOCUS_ITEMS=4 survive:
			//   n in {9, 8, 1, 0}. Foreground events evicted from the focus cache are
			//   demoted to generic events rather than dropped (n in {16, 24, 32, ...}).
			// - Menu (n % 8 in {4..7}): only the newest survives, n=4 (menuStart).
			// - Generic (show/hide and demoted foregrounds): the per thread limit keeps
			//   the newest MAX_EVENTS_FOR_THREAD=10: n in {2,3,10,11,16,18,19,24,26,27}.
			// Output is chronological (descending n).
			std::vector<int> expectedIds({
				27, 26, 24, 19, 18, 16, 11, 10, 9, 8, 4, 3, 2, 1, 0,
				});
			Assert::AreEqual(expectedIds, actualIds);
		}

		TEST_METHOD(test_showDoesNotCancelItself)
		{
			// Regression test: _invalidateEquivEvent previously compared against the
			// event itself, so every show/hide event invalidated its own entry.
			WinEventLimiter limiter;
			addEvent(limiter, EVENT_OBJECT_SHOW, 1);
			auto out = limiter.Flush();
			Assert::AreEqual(size_t{ 1 }, out.size());
			Assert::AreEqual(static_cast<unsigned long>(EVENT_OBJECT_SHOW), out[0].idEvent);
		}

		TEST_METHOD(test_showCancelsEarlierHide)
		{
			WinEventLimiter limiter;
			addEvent(limiter, EVENT_OBJECT_HIDE, 1);
			addEvent(limiter, EVENT_OBJECT_SHOW, 1);
			auto out = limiter.Flush();
			Assert::AreEqual(size_t{ 1 }, out.size());
			Assert::AreEqual(static_cast<unsigned long>(EVENT_OBJECT_SHOW), out[0].idEvent);
		}

		TEST_METHOD(test_hideCancelsEarlierShow)
		{
			WinEventLimiter limiter;
			addEvent(limiter, EVENT_OBJECT_SHOW, 1);
			addEvent(limiter, EVENT_OBJECT_HIDE, 1);
			auto out = limiter.Flush();
			Assert::AreEqual(size_t{ 1 }, out.size());
			Assert::AreEqual(static_cast<unsigned long>(EVENT_OBJECT_HIDE), out[0].idEvent);
		}

		TEST_METHOD(test_showDoesNotCancelHideForOtherObject)
		{
			WinEventLimiter limiter;
			addEvent(limiter, EVENT_OBJECT_HIDE, 1);
			addEvent(limiter, EVENT_OBJECT_SHOW, 2);
			auto actualIds = flushIds(limiter);
			Assert::AreEqual(std::vector<int>({ 1, 2 }), actualIds);
		}

		TEST_METHOD(test_duplicateEventMovesForward)
		{
			// A duplicate replaces the original, moving it forward in time,
			// matching the in-process Python limiter.
			WinEventLimiter limiter;
			addEvent(limiter, EVENT_OBJECT_NAMECHANGE, 1);
			addEvent(limiter, EVENT_OBJECT_NAMECHANGE, 2);
			addEvent(limiter, EVENT_OBJECT_NAMECHANGE, 1);
			auto actualIds = flushIds(limiter);
			Assert::AreEqual(std::vector<int>({ 2, 1 }), actualIds);
		}

		TEST_METHOD(test_threadCapKeepsNewestTen)
		{
			WinEventLimiter limiter;
			for (int id = 1; id <= 12; ++id) {
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, id, 1);
			}
			auto actualIds = flushIds(limiter);
			Assert::AreEqual(std::vector<int>({ 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 }), actualIds);
		}

		TEST_METHOD(test_threadCapIsPerThread)
		{
			WinEventLimiter limiter;
			for (int id = 1; id <= 11; ++id) {
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, id, 1);
			}
			for (int id = 100; id <= 102; ++id) {
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, id, 2);
			}
			auto actualIds = flushIds(limiter);
			// Thread 1 loses only its oldest event; thread 2 is untouched.
			Assert::AreEqual(
				std::vector<int>({ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 100, 101, 102 }),
				actualIds
			);
		}

		TEST_METHOD(test_maxFocusEvents)
		{
			// Mirrors test_maxFocusEvents in tests/unit/test_orderedWinEventLimiter.py:
			// of 5 focus events, only the last MAX_FOCUS_ITEMS=4 survive
			// (the oldest focus event is removed to make room).
			WinEventLimiter limiter;
			for (int id = 1; id <= 5; ++id) {
				addEvent(limiter, EVENT_OBJECT_FOCUS, id);
			}
			auto actualIds = flushIds(limiter);
			Assert::AreEqual(std::vector<int>({ 2, 3, 4, 5 }), actualIds);
		}

		TEST_METHOD(test_foregroundInvalidatesMatchingFocus)
		{
			WinEventLimiter limiter;
			addEvent(limiter, EVENT_OBJECT_FOCUS, 1);
			addEvent(limiter, EVENT_SYSTEM_FOREGROUND, 1);
			auto out = limiter.Flush();
			Assert::AreEqual(size_t{ 1 }, out.size());
			Assert::AreEqual(static_cast<unsigned long>(EVENT_SYSTEM_FOREGROUND), out[0].idEvent);
		}

		TEST_METHOD(test_menuEventsKeepLast)
		{
			WinEventLimiter limiter;
			addEvent(limiter, EVENT_SYSTEM_MENUSTART, 1);
			addEvent(limiter, EVENT_SYSTEM_MENUPOPUPSTART, 2);
			addEvent(limiter, EVENT_SYSTEM_MENUEND, 3);
			auto out = limiter.Flush();
			Assert::AreEqual(size_t{ 1 }, out.size());
			Assert::AreEqual(static_cast<unsigned long>(EVENT_SYSTEM_MENUEND), out[0].idEvent);
		}

		TEST_METHOD(test_focusAndMenuNotCountedInThreadCap)
		{
			WinEventLimiter limiter;
			for (int id = 1; id <= 10; ++id) {
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, id, 7);
			}
			addEvent(limiter, EVENT_OBJECT_FOCUS, 100, 7);
			addEvent(limiter, EVENT_SYSTEM_MENUSTART, 200, 7);
			auto actualIds = flushIds(limiter);
			// All 10 generic events survive: focus and menu events are limited by their
			// own mechanisms and don't consume the thread's generic allowance.
			Assert::AreEqual(
				std::vector<int>({ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 200 }),
				actualIds
			);
		}

		TEST_METHOD(test_alwaysAllowedObjectExemptFromThreadCap)
		{
			WinEventLimiter limiter;
			for (int id = 1; id <= 12; ++id) {
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, id, 1);
			}
			// Exempt the oldest event's object, which the per thread limit
			// would otherwise drop.
			limiter.SetAlwaysAllowedObject(
				reinterpret_cast<HWND>(static_cast<INT_PTR>(1)), 1, 1);
			auto actualIds = flushIds(limiter);
			Assert::AreEqual(
				std::vector<int>({ 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 }),
				actualIds
			);
		}

		TEST_METHOD(test_alwaysAllowedObjectCleared)
		{
			WinEventLimiter limiter;
			for (int id = 1; id <= 12; ++id) {
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, id, 1);
			}
			limiter.SetAlwaysAllowedObject(
				reinterpret_cast<HWND>(static_cast<INT_PTR>(1)), 1, 1);
			limiter.SetAlwaysAllowedObject(nullptr, 0, 0);
			auto actualIds = flushIds(limiter);
			Assert::AreEqual(
				std::vector<int>({ 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 }),
				actualIds
			);
		}

		TEST_METHOD(test_alwaysAllowedObjectStillDeduplicated)
		{
			// The exemption only applies to the per thread limit;
			// duplicate collapsing still applies to the allowed object.
			WinEventLimiter limiter;
			limiter.SetAlwaysAllowedObject(
				reinterpret_cast<HWND>(static_cast<INT_PTR>(1)), 1, 1);
			addEvent(limiter, EVENT_OBJECT_NAMECHANGE, 1);
			addEvent(limiter, EVENT_OBJECT_NAMECHANGE, 1);
			auto out = limiter.Flush();
			Assert::AreEqual(size_t{ 1 }, out.size());
		}

		TEST_METHOD(test_bufferOverflowKeepsNewestHalf)
		{
			WinEventLimiter limiter;
			const auto max = static_cast<int>(WinEventLimiter::MAX_BUFFERED_EVENTS);
			// Unique thread per event, so the per thread limit stays inert.
			for (int id = 0; id <= max; ++id) {
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, id, static_cast<DWORD>(id));
			}
			auto actualIds = flushIds(limiter);
			// Compaction fired when the buffer reached MAX_BUFFERED_EVENTS (after adding
			// id max-1), keeping the newest half; one more event was added afterwards.
			Assert::AreEqual(size_t{ WinEventLimiter::MAX_BUFFERED_EVENTS / 2 + 1 }, actualIds.size());
			Assert::AreEqual(max / 2, actualIds.front());
			Assert::AreEqual(max, actualIds.back());
		}

		TEST_METHOD(test_doubleBufferOverflowKeepsNewestHalf)
		{
			// The write buffer must stay bounded even while the limiter thread is not
			// draining it (the in-process implementation was implicitly bounded by the OS
			// limit on the hooking thread's message queue); the oldest half is discarded,
			// like the queues downstream.
			EventDoubleBuffer buffer;
			const auto max = static_cast<int>(EventDoubleBuffer::MAX_BUFFERED_EVENTS);
			const auto total = max + 100;
			for (int id = 0; id < total; ++id) {
				buffer.Write(makeEvent(EVENT_OBJECT_NAMECHANGE, id));
			}
			buffer.SwapEventBuffers();
			const auto& read = buffer.Read();
			// Writing event max triggered the drop of the oldest half; everything since
			// survives, newest last.
			Assert::AreEqual(
				size_t{ EventDoubleBuffer::MAX_BUFFERED_EVENTS / 2 + 100 }, read.size());
			Assert::AreEqual(static_cast<LONG>(max / 2), read.front().idObject);
			Assert::AreEqual(static_cast<LONG>(total - 1), read.back().idObject);
		}

		TEST_METHOD(test_doubleBufferOverflowRetainsProtectedEvents)
		{
			// The overflow trim prefers generic events: focus, foreground and destroy
			// events feed the limiter's focus protections and destroy diversion, which
			// only see events that survive this buffer, so discarding them here would
			// leave NVDA on stale focus or skip a destroy correction.
			EventDoubleBuffer buffer;
			buffer.Write(makeEvent(EVENT_OBJECT_FOCUS, 9001));
			buffer.Write(makeEvent(EVENT_SYSTEM_FOREGROUND, 9002));
			buffer.Write(makeEvent(EVENT_OBJECT_DESTROY, 9003));
			const auto max = static_cast<int>(EventDoubleBuffer::MAX_BUFFERED_EVENTS);
			const auto total = max + 100;
			for (int id = 0; id < total - 3; ++id) {
				buffer.Write(makeEvent(EVENT_OBJECT_NAMECHANGE, id));
			}
			buffer.SwapEventBuffers();
			const auto& read = buffer.Read();
			// The trim dropped only the oldest generics; the three protected events were
			// the oldest in the buffer, yet survive in order.
			Assert::AreEqual(
				size_t{ EventDoubleBuffer::MAX_BUFFERED_EVENTS / 2 + 100 }, read.size());
			Assert::AreEqual(9001L, read[0].idObject);
			Assert::AreEqual(9002L, read[1].idObject);
			Assert::AreEqual(9003L, read[2].idObject);
			Assert::AreEqual(static_cast<LONG>(max / 2), read[3].idObject);
			Assert::AreEqual(static_cast<LONG>(total - 4), read.back().idObject);
			// The generics covered the excess, so no destroy was lost.
			Assert::IsFalse(buffer.TakeLostDestroys());
		}

		TEST_METHOD(test_doubleBufferMenuFloodDoesNotDisplaceFocus)
		{
			// Raw menu events are coalesced downstream, so protecting an entire menu
			// flood here must not make an older focus event pay the protected-event
			// overflow budget.
			EventDoubleBuffer buffer;
			buffer.Write(makeEvent(EVENT_OBJECT_FOCUS, 9001));
			const auto max = static_cast<int>(EventDoubleBuffer::MAX_BUFFERED_EVENTS);
			const auto genericCount = max / 2 - 1;
			for (int id = 0; id < genericCount; ++id) {
				buffer.Write(makeEvent(EVENT_OBJECT_NAMECHANGE, id));
			}
			const auto menuCount = max - genericCount - 1;
			for (int id = 0; id < menuCount; ++id) {
				buffer.Write(makeEvent(EVENT_SYSTEM_MENUSTART, 10000 + id));
			}
			buffer.Write(makeEvent(EVENT_OBJECT_NAMECHANGE, 20000));
			buffer.SwapEventBuffers();
			const auto& read = buffer.Read();
			Assert::AreEqual(
				size_t{ EventDoubleBuffer::MAX_BUFFERED_EVENTS / 2 + 1 }, read.size());
			Assert::AreEqual(9001L, read.front().idObject);
			Assert::AreEqual(
				static_cast<unsigned long>(EVENT_OBJECT_FOCUS), read.front().idEvent);
			Assert::AreEqual(10001L, read[1].idObject);
			Assert::AreEqual(20000L, read.back().idObject);
		}

		TEST_METHOD(test_doubleBufferOverflowRetainsFocusedObjectEvents)
		{
			// #11520: events for the always allowed (focused) object must survive the
			// overflow trim, or they would be lost before WinEventLimiter's exemption
			// could see them. Events in this buffer are raw, so the trim must apply the
			// same objectID remap the limiter thread's preprocessing will.
			EventDoubleBuffer buffer;
			const HWND focusedWindow = reinterpret_cast<HWND>(static_cast<INT_PTR>(9004));
			buffer.SetAlwaysAllowedObject(focusedWindow, OBJID_CLIENT, 0);
			// Raw form: a window objectID of 0 remaps to OBJID_CLIENT downstream.
			buffer.Write(EventData{
				EVENT_OBJECT_NAMECHANGE, focusedWindow, 0, 0, 7, 0,
			});
			// Already-client form matches directly.
			buffer.Write(EventData{
				EVENT_OBJECT_VALUECHANGE, focusedWindow, OBJID_CLIENT, 0, 7, 0,
			});
			const auto max = static_cast<int>(EventDoubleBuffer::MAX_BUFFERED_EVENTS);
			const auto total = max + 100;
			for (int id = 0; id < total; ++id) {
				buffer.Write(makeEvent(EVENT_OBJECT_NAMECHANGE, id));
			}
			buffer.SwapEventBuffers();
			const auto& read = buffer.Read();
			// The focused object's events were the oldest in the buffer, yet survive in
			// order; only the oldest generics were dropped.
			Assert::AreEqual(
				size_t{ EventDoubleBuffer::MAX_BUFFERED_EVENTS / 2 + 102 }, read.size());
			Assert::IsTrue(focusedWindow == read[0].hwnd);
			Assert::AreEqual(0L, read[0].idObject);
			Assert::IsTrue(focusedWindow == read[1].hwnd);
			Assert::AreEqual(static_cast<LONG>(OBJID_CLIENT), read[1].idObject);
			Assert::AreEqual(static_cast<LONG>(max / 2), read[2].idObject);
			Assert::AreEqual(static_cast<LONG>(total - 1), read.back().idObject);
		}

		TEST_METHOD(test_doubleBufferOverflowShedsDestroyFloodAndReportsLoss)
		{
			// Protection is a preference, not an exemption: when the buffer is full of
			// protected events (e.g. an application with thousands of windows closing),
			// memory boundedness wins and the oldest are dropped regardless, or every
			// write above the limit would copy an ever-growing buffer. The loss is
			// reported, so NVDA can treat every window as potentially destroyed instead
			// of relying on the dropped destroy events.
			EventDoubleBuffer buffer;
			const auto max = static_cast<int>(EventDoubleBuffer::MAX_BUFFERED_EVENTS);
			for (int id = 0; id <= max; ++id) {
				buffer.Write(makeEvent(EVENT_OBJECT_DESTROY, id));
			}
			buffer.SwapEventBuffers();
			const auto& read = buffer.Read();
			Assert::AreEqual(
				size_t{ EventDoubleBuffer::MAX_BUFFERED_EVENTS / 2 + 1 }, read.size());
			Assert::AreEqual(static_cast<LONG>(max / 2), read.front().idObject);
			Assert::AreEqual(static_cast<LONG>(max), read.back().idObject);
			Assert::IsTrue(buffer.TakeLostDestroys());
			// Reading consumed the flag.
			Assert::IsFalse(buffer.TakeLostDestroys());
		}

		TEST_METHOD(test_maxBufferSizeDiagnosticTracksHighWater)
		{
			WinEventLimiter limiter;
			const auto max = static_cast<int>(WinEventLimiter::MAX_BUFFERED_EVENTS);
			for (int id = 0; id < max; ++id) {
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, id, static_cast<DWORD>(id));
			}
			Assert::IsTrue(limiter.GetMaxBufferSize() >= WinEventLimiter::MAX_BUFFERED_EVENTS);
		}

		TEST_METHOD(test_notifierCoalescesAndUpgradesForFocus)
		{
			// The notifier fires at most once until the client flushes, but a focus
			// event still upgrades an already delivered notification once, so NVDA can
			// upgrade a pending delayed pump to an immediate one (#14928).
			std::vector<int> received;
			EventNotifier notifier(
				[&received](int includesFocusEvent) { received.push_back(includesFocusEvent); }
			);
			notifier.NotifyClientOfNewEvents(false);
			notifier.NotifyClientOfNewEvents(false);
			Assert::AreEqual(std::vector<int>({ 0 }), received);
			notifier.NotifyClientOfNewEvents(true);
			notifier.NotifyClientOfNewEvents(true);
			Assert::AreEqual(std::vector<int>({ 0, 1 }), received);
			notifier.ResetNotify();
			notifier.NotifyClientOfNewEvents(false);
			Assert::AreEqual(std::vector<int>({ 0, 1, 0 }), received);
		}

		TEST_METHOD(test_duplicateFocusDoesNotConsumeFocusBudget)
		{
			// A duplicated focus event replaces its old copy in place (like the Python
			// limiter's keyed cache) and must not consume an extra MAX_FOCUS_ITEMS slot,
			// which would wrongly evict a still valid older focus event.
			WinEventLimiter limiter;
			addEvent(limiter, EVENT_OBJECT_FOCUS, 1);
			addEvent(limiter, EVENT_OBJECT_FOCUS, 2);
			addEvent(limiter, EVENT_OBJECT_FOCUS, 2);
			addEvent(limiter, EVENT_OBJECT_FOCUS, 3);
			addEvent(limiter, EVENT_OBJECT_FOCUS, 4);
			auto actualIds = flushIds(limiter);
			Assert::AreEqual(std::vector<int>({ 1, 2, 3, 4 }), actualIds);
		}

		TEST_METHOD(test_foregroundSurvivesFocusEviction)
		{
			// A foreground event evicted from the focus cache is demoted to a generic
			// event rather than dropped, mirroring the Python limiter's generic cache
			// copy: the application switch must still be announced.
			WinEventLimiter limiter;
			addEvent(limiter, EVENT_SYSTEM_FOREGROUND, 1);
			for (int id = 2; id <= 5; ++id) {
				addEvent(limiter, EVENT_OBJECT_FOCUS, id);
			}
			auto actualIds = flushIds(limiter);
			Assert::AreEqual(std::vector<int>({ 1, 2, 3, 4, 5 }), actualIds);
		}

		TEST_METHOD(test_demotedForegroundSubjectToThreadCap)
		{
			// Once demoted to a generic event, an evicted foreground competes in the per
			// thread limit like any other generic event.
			WinEventLimiter limiter;
			addEvent(limiter, EVENT_SYSTEM_FOREGROUND, 100, 7);
			for (int id = 200; id <= 203; ++id) {
				// The fourth focus event evicts and demotes the foreground.
				addEvent(limiter, EVENT_OBJECT_FOCUS, id, 7);
			}
			for (int id = 1; id <= 10; ++id) {
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, id, 7);
			}
			auto actualIds = flushIds(limiter);
			// The 10 newer generic events push the demoted foreground over the cap.
			Assert::AreEqual(
				std::vector<int>({ 200, 201, 202, 203, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 }),
				actualIds
			);
		}

		TEST_METHOD(test_compactionPreservesExemptEvents)
		{
			// Compaction under buffer overflow must never drop focus class events, the
			// surviving menu event, or events for the always allowed (focused) object,
			// however old: the Python limiter never evicted them before a flush.
			WinEventLimiter limiter;
			limiter.SetAlwaysAllowedObject(
				reinterpret_cast<HWND>(static_cast<INT_PTR>(9003)), 9003, 9003);
			addEvent(limiter, EVENT_OBJECT_FOCUS, 9001);
			addEvent(limiter, EVENT_SYSTEM_MENUSTART, 9002);
			addEvent(limiter, EVENT_OBJECT_NAMECHANGE, 9003);
			const auto max = static_cast<int>(WinEventLimiter::MAX_BUFFERED_EVENTS);
			// Unique thread per event, so the per thread limit stays inert.
			for (int id = 0; id < max; ++id) {
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, id, static_cast<DWORD>(id + 1));
			}
			auto actualIds = flushIds(limiter);
			// The three protected events were the oldest in the buffer, yet survive.
			Assert::AreEqual(9001, actualIds[0]);
			Assert::AreEqual(9002, actualIds[1]);
			Assert::AreEqual(9003, actualIds[2]);
		}

		TEST_METHOD(test_compactionRemovesInvalidatedEntriesFirst)
		{
			// Filling the buffer with duplicates of one object leaves one valid entry and
			// thousands of invalidated ones; compaction must reclaim the invalid entries
			// without dropping any valid event.
			WinEventLimiter limiter;
			const auto max = static_cast<int>(WinEventLimiter::MAX_BUFFERED_EVENTS);
			for (int n = 0; n < max + 100; ++n) {
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, 1);
			}
			Assert::IsTrue(limiter.GetMaxBufferSize() >= WinEventLimiter::MAX_BUFFERED_EVENTS);
			auto out = limiter.Flush();
			Assert::AreEqual(size_t{ 1 }, out.size());
		}

		TEST_METHOD(test_compactionBoundsAlwaysAllowedFlood)
		{
			// The #11520 exemption is a preference, not an exemption from the absolute
			// cap: deduplication keeps one entry per distinct event ID and thread, so a
			// focused object emitting from enough distinct threads could otherwise grow
			// the buffer without bound while recompacting on every add.
			WinEventLimiter limiter;
			limiter.SetAlwaysAllowedObject(
				reinterpret_cast<HWND>(static_cast<INT_PTR>(9003)), 9003, 9003);
			const auto max = static_cast<int>(WinEventLimiter::MAX_BUFFERED_EVENTS);
			for (int n = 0; n < max + 100; ++n) {
				// Every event matches the allowed object; distinct threads defeat
				// deduplication.
				addEvent(limiter, EVENT_OBJECT_NAMECHANGE, 9003, static_cast<DWORD>(n + 1));
			}
			Assert::IsTrue(limiter.GetMaxBufferSize() <= WinEventLimiter::MAX_BUFFERED_EVENTS);
			auto out = limiter.Flush();
			// Compaction fired once at the cap, keeping the newest half; the rest were
			// added afterwards.
			Assert::AreEqual(size_t{ WinEventLimiter::MAX_BUFFERED_EVENTS / 2 + 100 }, out.size());
			Assert::AreEqual(static_cast<DWORD>(max / 2 + 1), out.front().dwEventThread);
			Assert::AreEqual(static_cast<DWORD>(max + 100), out.back().dwEventThread);
		}

		TEST_METHOD(test_destroyEventsDeliveredRawViaFetch)
		{
			// Destroy events are diverted to their own fetch queue before preprocessing:
			// NVDA's processDestroyWinEvent needs the raw objectID (#2695), and the invalid
			// window drop must not apply to a window that is being destroyed.
			std::atomic<bool> signalled = false;
			std::promise<void> notified;
			EventNotifier notifier(
				[&signalled, &notified](int) {
					if (!signalled.exchange(true)) {
						notified.set_value();
					}
				}
			);
			EventDoubleBuffer buffer;
			EventLimiterThread limiterThread(notifier, buffer);
			buffer.Write(EventData{
				EVENT_OBJECT_DESTROY,
				nullptr, // hwnd: already destroyed
				0, // idObject: raw, must not be remapped to OBJID_CLIENT
				0, // idChild
				7, // threadID
				0, // dwmsEventTime
			});
			const auto status = notified.get_future().wait_for(std::chrono::seconds(5));
			Assert::IsTrue(std::future_status::ready == status);
			auto destroys = limiterThread.TakeDestroyEvents();
			bool deferred = true;
			auto flushed = limiterThread.FlushEventLimiter(deferred);
			limiterThread.Stop();
			Assert::AreEqual(size_t{ 1 }, destroys.size());
			Assert::AreEqual(static_cast<unsigned long>(EVENT_OBJECT_DESTROY), destroys[0].idEvent);
			Assert::IsNull(destroys[0].hwnd);
			Assert::AreEqual(0L, destroys[0].idObject);
			// The destroy event must not also surface as a regular event, and a destroy
			// alone never defers the flush.
			Assert::AreEqual(size_t{ 0 }, flushed.size());
			Assert::IsFalse(deferred);
		}

		TEST_METHOD(test_injectedEventsBypassHookPreprocessing)
		{
			// Synthetic events were already selected by NVDA. External mode must match
			// direct insertion into the in-process limiter, including when a transient
			// cross-thread handoff makes the window handle fail IsWindow.
			std::atomic<bool> signalled = false;
			std::promise<void> notified;
			EventNotifier notifier(
				[&signalled, &notified](int) {
					if (!signalled.exchange(true)) {
						notified.set_value();
					}
				}
			);
			EventDoubleBuffer buffer;
			EventLimiterThread limiterThread(notifier, buffer);
			const HWND transientWindow = reinterpret_cast<HWND>(
				static_cast<INT_PTR>(42)
			);
			buffer.Write(EventData{
				EVENT_OBJECT_FOCUS,
				transientWindow,
				OBJID_CLIENT,
				0,
				7,
				0,
				true,
			});
			const std::future_status status = notified.get_future().wait_for(
				std::chrono::seconds(5)
			);
			Assert::IsTrue(std::future_status::ready == status);
			bool deferred = false;
			EventBuffer flushed = limiterThread.FlushEventLimiter(deferred);
			limiterThread.Stop();
			Assert::IsFalse(deferred);
			Assert::AreEqual(size_t{ 1 }, flushed.size());
			Assert::IsTrue(transientWindow == flushed[0].hwnd);
		}

		TEST_METHOD(test_destroyEventsBypassForegroundDefer)
		{
			// While a foreground change defers the regular flush (#3831), destroy events
			// must still reach the client: the in-process implementation processed them
			// regardless of pump gating.
			std::atomic<size_t> notifyCount = 0;
			std::promise<void> firstNotify;
			std::promise<void> secondNotify;
			EventNotifier notifier(
				[&notifyCount, &firstNotify, &secondNotify](int) {
					const auto n = notifyCount.fetch_add(1);
					if (n == 0) {
						firstNotify.set_value();
					}
					else if (n == 1) {
						secondNotify.set_value();
					}
				}
			);
			EventDoubleBuffer buffer;
			EventLimiterThread limiterThread(notifier, buffer);
			// A message-only window can never become the foreground window, so the defer
			// deterministically holds.
			const HWND messageOnlyWindow = CreateWindowExW(
				0, L"STATIC", nullptr, 0,
				0, 0, 0, 0,
				HWND_MESSAGE, nullptr, nullptr, nullptr
			);
			Assert::IsNotNull(messageOnlyWindow);
			buffer.Write(EventData{
				EVENT_SYSTEM_FOREGROUND, messageOnlyWindow, 0, 0, 7, 0,
			});
			auto status = firstNotify.get_future().wait_for(std::chrono::seconds(5));
			Assert::IsTrue(std::future_status::ready == status);
			notifier.ResetNotify();
			buffer.Write(EventData{
				EVENT_OBJECT_DESTROY, messageOnlyWindow, 0, 0, 7, 0,
			});
			status = secondNotify.get_future().wait_for(std::chrono::seconds(5));
			Assert::IsTrue(std::future_status::ready == status);
			bool deferred = false;
			auto flushed = limiterThread.FlushEventLimiter(deferred);
			auto destroys = limiterThread.TakeDestroyEvents();
			limiterThread.Stop();
			DestroyWindow(messageOnlyWindow);
			Assert::AreEqual(size_t{ 0 }, flushed.size()); // deferred
			// The deferral is reported, so the client can hold its whole cycle (#3831).
			Assert::IsTrue(deferred);
			Assert::AreEqual(size_t{ 1 }, destroys.size()); // delivered anyway
		}

		TEST_METHOD(test_destroysDivertedAfterSnapshotStillNotify)
		{
			// The client takes the destroy snapshot before FlushEventLimiter resets the
			// notifier. A destroy diverted between the two has its own notification
			// coalesced away with the one being serviced, so the flush must leave a new
			// notification behind for it; otherwise it - and any focus correction it
			// implies - would stay pending until some unrelated event caused a pump.
			std::atomic<size_t> notifyCount = 0;
			std::promise<void> firstNotify;
			std::promise<void> secondNotify;
			EventNotifier notifier(
				[&notifyCount, &firstNotify, &secondNotify](int) {
					const auto n = notifyCount.fetch_add(1);
					if (n == 0) {
						firstNotify.set_value();
					}
					else if (n == 1) {
						secondNotify.set_value();
					}
				}
			);
			EventDoubleBuffer buffer;
			EventLimiterThread limiterThread(notifier, buffer);
			buffer.Write(EventData{
				EVENT_OBJECT_DESTROY, nullptr, 0, 0, 7, 0,
			});
			auto status = firstNotify.get_future().wait_for(std::chrono::seconds(5));
			Assert::IsTrue(std::future_status::ready == status);
			// The client's cycle begins: destroys are snapshotted first, with the
			// notifier still holding the notification being serviced.
			auto destroys = limiterThread.TakeDestroyEvents();
			Assert::AreEqual(size_t{ 1 }, destroys.size());
			// Reset only so the test can observe the late destroy being diverted. Once
			// its callback runs, the notifier is held again, matching the coalesced state.
			notifier.ResetNotify();
			buffer.Write(EventData{
				EVENT_OBJECT_DESTROY, nullptr, 0, 0, 7, 0,
			});
			status = secondNotify.get_future().wait_for(std::chrono::seconds(5));
			Assert::IsTrue(std::future_status::ready == status);
			bool deferred = false;
			auto flushed = limiterThread.FlushEventLimiter(deferred);
			// The flush must replace the notification it reset so the client pumps again.
			Assert::AreEqual(size_t{ 3 }, notifyCount.load());
			flushed = limiterThread.FlushEventLimiter(deferred);
			Assert::IsTrue(deferred);
			Assert::AreEqual(size_t{ 4 }, notifyCount.load());
			flushed = limiterThread.FlushEventLimiter(deferred);
			Assert::IsFalse(deferred);
			// The cap may permit regular events only after escalating the pending
			// destroy to whole-cache recovery, and it must leave a notification for
			// the next pump.
			Assert::AreEqual(size_t{ 5 }, notifyCount.load());
			Assert::IsTrue(limiterThread.TakeLostDestroys());
			auto lateDestroys = limiterThread.TakeDestroyEvents();
			limiterThread.Stop();
			Assert::AreEqual(size_t{ 0 }, flushed.size());
			Assert::IsFalse(deferred);
			Assert::AreEqual(size_t{ 1 }, lateDestroys.size());
		}

		TEST_METHOD(test_unfetchedDestroyFloodStaysBoundedAndReportsLoss)
		{
			// If NVDA's core stalls while windows are destroyed en masse, the destroy
			// queue and the input buffer shed their oldest events rather than grow (and
			// copy) without bound; the loss is reported so NVDA can treat every window
			// as potentially destroyed.
			EventNotifier notifier([](int) {});
			EventDoubleBuffer buffer;
			EventLimiterThread limiterThread(notifier, buffer);
			// More destroys than the unfetched queue may hold: once the limiter thread
			// has drained the writes, every survivor sits in the capped queue, so some
			// stage must have shed and flagged the loss, no matter how the draining
			// interleaved with the writes.
			const auto total = static_cast<int>(
				EventLimiterThread::MAX_BUFFERED_DESTROY_EVENTS
				+ EventDoubleBuffer::MAX_BUFFERED_EVENTS
				+ 100
			);
			for (int id = 0; id < total; ++id) {
				buffer.Write(makeEvent(EVENT_OBJECT_DESTROY, id));
			}
			bool lost = false;
			for (int i = 0; i < 5000 && !lost; ++i) {
				lost = limiterThread.TakeLostDestroys() || buffer.TakeLostDestroys();
				if (!lost) {
					std::this_thread::sleep_for(std::chrono::milliseconds(1));
				}
			}
			limiterThread.Stop();
			const auto destroys = limiterThread.TakeDestroyEvents();
			Assert::IsTrue(lost);
			Assert::IsTrue(
				destroys.size() <= EventLimiterThread::MAX_BUFFERED_DESTROY_EVENTS);
		}

		TEST_METHOD(test_menuBarFocusIgnored)
		{
			WinEventLimiter limiter;
			// A focus event on a menu bar itself (objectID OBJID_MENU, childID 0).
			EventData e{
				EVENT_OBJECT_FOCUS,
				reinterpret_cast<HWND>(static_cast<INT_PTR>(1)),
				OBJID_MENU,
				0, // childID
				0, // threadID
				0, // dwmsEventTime
			};
			const bool added = limiter.AddEvent(e);
			Assert::IsFalse(added);
			Assert::AreEqual(size_t{ 0 }, limiter.Flush().size());
		}

	};
}
