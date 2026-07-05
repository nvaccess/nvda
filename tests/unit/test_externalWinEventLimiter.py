# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Unit tests for the external winEventLimiter integration in IAccessibleHandler."""

import unittest
from unittest import mock

import api
import config
import eventHandler
import IAccessibleHandler
from IAccessibleHandler import internalWinEventHandler
from NVDAHelper import winEventLimiter as winEventLimiterLib
import NVDAObjects.IAccessible
import winUser


def _makeFakeDll(
	events: list[tuple[int, int | None, int, int]] | None = None,
	destroyEvents: list[tuple[int | None, int, int]] | None = None,
	startRet: int = 0,
	flushDeferred: bool = False,
	lostDestroys: bool = False,
) -> mock.MagicMock:
	"""Create a stand-in for the loaded winEventLimiter dll.

	:param events: The ``(eventID, window, objectID, childID)`` tuples, oldest first,
		that winEventLimiter_getEvents should produce.
	:param destroyEvents: The ``(window, objectID, childID)`` tuples that
		winEventLimiter_getDestroyEvents should produce.
	:param startRet: The return value of winEventLimiter_start.
	:param flushDeferred: Whether winEventLimiter_flushEvents reports the flush as
		deferred for a pending foreground change (#3831).
	:param lostDestroys: Whether winEventLimiter_takeLostDestroys reports that destroy
		events were discarded under a sustained flood.
	"""
	events = events if events is not None else []
	destroyEvents = destroyEvents if destroyEvents is not None else []
	dll = mock.MagicMock()
	dll.winEventLimiter_start.return_value = startRet
	dll.winEventLimiter_flushEvents.return_value = 1 if flushDeferred else 0
	dll.winEventLimiter_flushDestroyEvents.return_value = None
	dll.winEventLimiter_getEventCount.side_effect = lambda: len(events)
	dll.winEventLimiter_getDestroyEventCount.side_effect = lambda: len(destroyEvents)
	lostDestroysPending = lostDestroys

	def fakeTakeLostDestroys() -> int:
		nonlocal lostDestroysPending
		res = 1 if lostDestroysPending else 0
		lostDestroysPending = False
		return res

	dll.winEventLimiter_takeLostDestroys.side_effect = fakeTakeLostDestroys

	def fakeAddEvent(
		eventID: int,
		window: int,
		objectID: int,
		childID: int,
		threadID: int,
	) -> int:
		events.append((eventID, window, objectID, childID))
		return 0

	def fakeGetEvents(index: int, maxEvents: int, data) -> int:
		numberFetched = min(len(events) - index, maxEvents)
		for i in range(numberFetched):
			eventID, window, objectID, childID = events[index + i]
			data[i].idEvent = eventID
			data[i].hwnd = window
			data[i].idObject = objectID
			data[i].idChild = childID
		return numberFetched

	def fakeGetDestroyEvents(index: int, maxEvents: int, data) -> int:
		numberFetched = min(len(destroyEvents) - index, maxEvents)
		for i in range(numberFetched):
			window, objectID, childID = destroyEvents[index + i]
			data[i].idEvent = winUser.EVENT_OBJECT_DESTROY
			data[i].hwnd = window
			data[i].idObject = objectID
			data[i].idChild = childID
		return numberFetched

	dll.winEventLimiter_addEvent.side_effect = fakeAddEvent
	dll.winEventLimiter_getEvents.side_effect = fakeGetEvents
	dll.winEventLimiter_getDestroyEvents.side_effect = fakeGetDestroyEvents
	return dll


class _FakeDllTestCase(unittest.TestCase):
	"""Base class installing a fake winEventLimiter dll for the duration of each test."""

	def setUp(self) -> None:
		super().setUp()
		internalWinEventHandler._limiterSelectionComplete.set()

	def installFakeDll(self, fakeDll: mock.MagicMock) -> None:
		patcher = mock.patch.object(
			internalWinEventHandler,
			"_externalWinEventLimiterDll",
			fakeDll,
		)
		patcher.start()
		self.addCleanup(patcher.stop)


class Test_fetchExternalEvents(_FakeDllTestCase):
	def test_fetchYieldsChronologicalOrder(self):
		"""Events are played back in chronological order, like the in-process limiter's
		flushEvents (pumpAll relies on this to use the most recent possible focus event),
		and the dll calls happen in the right order.
		"""
		events = [
			(winUser.EVENT_OBJECT_SHOW, 1, 11, 0),
			(winUser.EVENT_OBJECT_HIDE, 2, 22, 0),
			(winUser.EVENT_OBJECT_NAMECHANGE, 3, 33, 0),
		]
		fakeDll = _makeFakeDll(events=events)
		self.installFakeDll(fakeDll)
		deferred, fetched = internalWinEventHandler._fetchExternalEvents()
		self.assertFalse(deferred)
		self.assertEqual(fetched, events)
		callNames = [name for name, args, kwargs in fakeDll.mock_calls]
		self.assertEqual(
			callNames,
			[
				"winEventLimiter_setAlwaysAllowedObject",
				"winEventLimiter_flushEvents",
				"winEventLimiter_getEventCount",
				"winEventLimiter_getEvents",
			],
		)

	def test_fetchAllPendingEvents(self):
		"""All flushed events are fetched, matching the in-process limiter since #11520
		removed its 500 event truncation; the dll bounds its backlog itself.
		"""
		eventCount = 600
		events = [(winUser.EVENT_OBJECT_NAMECHANGE, n, n, n) for n in range(eventCount)]
		fakeDll = _makeFakeDll(events=events)
		self.installFakeDll(fakeDll)
		_deferred, fetched = internalWinEventHandler._fetchExternalEvents()
		self.assertEqual(fetched, events)
		startIndexArg, maxEventsArg = fakeDll.winEventLimiter_getEvents.call_args.args[:2]
		self.assertEqual(startIndexArg, 0)
		self.assertEqual(maxEventsArg, eventCount)

	def test_fetchHwndNoneBecomesZero(self):
		fakeDll = _makeFakeDll(events=[(winUser.EVENT_OBJECT_SHOW, None, 1, 2)])
		self.installFakeDll(fakeDll)
		_deferred, fetched = internalWinEventHandler._fetchExternalEvents()
		self.assertEqual(fetched, [(winUser.EVENT_OBJECT_SHOW, 0, 1, 2)])

	def test_fetchReportsDeferredWithoutFetching(self):
		"""#3831: when the dll defers the flush for a pending foreground change, nothing
		was flushed and nothing is fetched; the dll has already requested another pump.
		"""
		fakeDll = _makeFakeDll(
			events=[(winUser.EVENT_OBJECT_NAMECHANGE, 3, 33, 0)],
			flushDeferred=True,
		)
		self.installFakeDll(fakeDll)
		deferred, fetched = internalWinEventHandler._fetchExternalEvents()
		self.assertTrue(deferred)
		self.assertEqual(fetched, [])
		fakeDll.winEventLimiter_getEventCount.assert_not_called()
		fakeDll.winEventLimiter_getEvents.assert_not_called()

	def test_fetchReturnsRawDestroys(self):
		"""Destroys come back as raw (window, objectID, childID) tuples (hwnd None
		becoming 0), snapshotted independently of the regular flush so they can be
		processed before this cycle's focus is captured.
		"""
		fakeDll = _makeFakeDll(destroyEvents=[(42, 0, 0), (None, -4, 1)])
		self.installFakeDll(fakeDll)
		destroysLost, destroys = internalWinEventHandler._fetchExternalDestroyEvents()
		self.assertFalse(destroysLost)
		self.assertEqual(destroys, [(42, 0, 0), (0, -4, 1)])
		callNames = [name for name, args, kwargs in fakeDll.mock_calls]
		self.assertEqual(
			callNames,
			[
				"winEventLimiter_flushDestroyEvents",
				"winEventLimiter_getDestroyEventCount",
				"winEventLimiter_getDestroyEvents",
				"winEventLimiter_takeLostDestroys",
			],
		)

	def test_fetchReportsLostDestroys(self):
		"""When the dll had to shed destroys under a sustained flood, the fetch reports
		it, so pumpAll can treat every cached object as potentially destroyed; the
		destroys that did survive are still delivered.
		"""
		fakeDll = _makeFakeDll(destroyEvents=[(42, 0, 0)], lostDestroys=True)
		self.installFakeDll(fakeDll)
		destroysLost, destroys = internalWinEventHandler._fetchExternalDestroyEvents()
		self.assertTrue(destroysLost)
		self.assertEqual(destroys, [(42, 0, 0)])

	def test_fetchDestroysWithInternalLimiter(self):
		"""The internal limiter processes destroys at hook-callback time: nothing is
		fetched, and nothing can have been lost.
		"""
		with mock.patch.object(
			internalWinEventHandler,
			"_externalWinEventLimiterDll",
			None,
		):
			destroysLost, destroys = internalWinEventHandler.fetchDestroyEvents()
		self.assertFalse(destroysLost)
		self.assertEqual(destroys, [])

	def test_setAlwaysAllowedObjectPassed(self):
		fakeDll = _makeFakeDll()
		self.installFakeDll(fakeDll)
		internalWinEventHandler._fetchExternalEvents((123, -4, 1))
		fakeDll.winEventLimiter_setAlwaysAllowedObject.assert_called_once_with(123, -4, 1)

	def test_setAlwaysAllowedObjectCleared(self):
		fakeDll = _makeFakeDll()
		self.installFakeDll(fakeDll)
		internalWinEventHandler._fetchExternalEvents(None)
		fakeDll.winEventLimiter_setAlwaysAllowedObject.assert_called_once_with(0, 0, 0)

	def test_unchangedAlwaysAllowedObjectIsSentAgain(self):
		"""Each flush updates the DLL without relying on cross-lifecycle cached state."""
		fakeDll = _makeFakeDll()
		self.installFakeDll(fakeDll)
		alwaysAllowedObject = (123, winUser.OBJID_CLIENT, 1)
		internalWinEventHandler._fetchExternalEvents(alwaysAllowedObject)
		internalWinEventHandler._fetchExternalEvents(alwaysAllowedObject)
		self.assertEqual(
			fakeDll.winEventLimiter_setAlwaysAllowedObject.call_args_list,
			[mock.call(*alwaysAllowedObject), mock.call(*alwaysAllowedObject)],
		)


class Test_addEvent(_FakeDllTestCase):
	def test_internalLimiterUsedWhenExternalInactive(self):
		with (
			mock.patch.object(
				internalWinEventHandler,
				"_externalWinEventLimiterDll",
				None,
			),
			mock.patch.object(
				internalWinEventHandler.winEventLimiter,
				"addEvent",
				return_value=True,
			) as internalAddEvent,
		):
			accepted = internalWinEventHandler.addEvent(
				winUser.EVENT_OBJECT_FOCUS,
				42,
				winUser.OBJID_CLIENT,
				0,
				7,
			)
		self.assertTrue(accepted)
		internalAddEvent.assert_called_once_with(
			winUser.EVENT_OBJECT_FOCUS,
			42,
			winUser.OBJID_CLIENT,
			0,
			7,
		)

	def test_externalLimiterUsedWhenActive(self):
		events: list[tuple[int, int | None, int, int]] = []
		fakeDll = _makeFakeDll(events=events)
		self.installFakeDll(fakeDll)
		with (
			mock.patch.object(
				internalWinEventHandler.winEventLimiter,
				"addEvent",
			) as internalAddEvent,
		):
			accepted = internalWinEventHandler.addEvent(
				winUser.EVENT_OBJECT_FOCUS,
				42,
				winUser.OBJID_CLIENT,
				0,
				7,
			)
		self.assertTrue(accepted)
		fakeDll.winEventLimiter_addEvent.assert_called_once_with(
			winUser.EVENT_OBJECT_FOCUS,
			42,
			winUser.OBJID_CLIENT,
			0,
			7,
		)
		internalAddEvent.assert_not_called()
		self.assertEqual(
			events,
			[(winUser.EVENT_OBJECT_FOCUS, 42, winUser.OBJID_CLIENT, 0)],
		)


class Test_newEventsCallback(unittest.TestCase):
	def test_immediatePumpForFocus(self):
		"""#14928: focus events are pumped immediately rather than after a delay,
		matching the in-process winEventCallback.
		"""
		import core

		with mock.patch.object(core, "requestPump") as requestPump:
			internalWinEventHandler._newEventsCallback(0)
			requestPump.assert_called_once_with(immediate=False)
			requestPump.reset_mock()
			internalWinEventHandler._newEventsCallback(1)
			requestPump.assert_called_once_with(immediate=True)


class Test_getConsoleWindowThreadID(unittest.TestCase):
	def test_externalModeQueriesDll(self):
		fakeDll = mock.MagicMock()
		fakeDll.winEventLimiter_getConsoleThreadID.return_value = 1234
		with mock.patch.object(
			internalWinEventHandler,
			"_externalWinEventLimiterDll",
			fakeDll,
		):
			self.assertEqual(internalWinEventHandler.getConsoleWindowThreadID(42), 1234)
		fakeDll.winEventLimiter_getConsoleThreadID.assert_called_once_with(42)

	def test_internalModeUsesMap(self):
		with (
			mock.patch.object(
				internalWinEventHandler,
				"_externalWinEventLimiterDll",
				None,
			),
			mock.patch.dict(internalWinEventHandler.consoleWindowsToThreadIDs, {42: 5678}),
		):
			self.assertEqual(internalWinEventHandler.getConsoleWindowThreadID(42), 5678)
			self.assertEqual(internalWinEventHandler.getConsoleWindowThreadID(43), 0)


class Test_destroyEvents(_FakeDllTestCase):
	def test_destroysProcessedBeforeEventsInPump(self):
		"""Destroys are processed synchronously at the start of the pump, before any of
		the cycle's other events and with the raw (unremapped) objectID, mirroring the
		in-process implementation which handles them immediately on receipt (#2695).
		"""
		fakeDll = _makeFakeDll(
			events=[(winUser.EVENT_OBJECT_NAMECHANGE, 3, 33, 0)],
			destroyEvents=[(42, 0, 0)],
		)
		self.installFakeDll(fakeDll)
		processed = []

		def fakeShouldAcceptEvent(eventName, windowHandle=None):
			processed.append(("event", eventName))
			return False

		with (
			mock.patch.object(
				internalWinEventHandler,
				"_processDestroyWinEvent",
				side_effect=lambda *args: processed.append(("destroy", args)),
			),
			mock.patch.object(eventHandler, "shouldAcceptEvent", fakeShouldAcceptEvent),
		):
			IAccessibleHandler.pumpAll()
		self.assertEqual(
			processed,
			[
				("destroy", (42, 0, 0)),
				("event", "nameChange"),
			],
		)

	def test_destroysProcessedBeforeFocusCapture(self):
		"""Processing a destroy may correct the focus (#2695: a destroyed IME candidate is
		corrected to its container). The corrected focus must be the one this cycle captures
		and exempts from limiting, matching the in-process implementation which handles
		destroys at hook-callback time, always before pumpAll captures the focus.
		"""
		fakeDll = _makeFakeDll(destroyEvents=[(42, 0, 0)])
		self.installFakeDll(fakeDll)
		correctedFocus = mock.MagicMock(spec=NVDAObjects.IAccessible.IAccessible)
		correctedFocus.event_windowHandle = 77
		correctedFocus.event_objectID = winUser.OBJID_CLIENT
		correctedFocus.event_childID = 0

		def fakeProcessDestroy(*args):
			eventHandler.lastQueuedFocusObject = correctedFocus

		with (
			mock.patch.object(eventHandler, "lastQueuedFocusObject", None),
			mock.patch.object(
				internalWinEventHandler,
				"_processDestroyWinEvent",
				side_effect=fakeProcessDestroy,
			),
		):
			IAccessibleHandler.pumpAll()
		fakeDll.winEventLimiter_setAlwaysAllowedObject.assert_called_once_with(
			77,
			winUser.OBJID_CLIENT,
			0,
		)

	def test_destroyHandlerFailureDoesNotAbortPump(self):
		"""A raising destroy handler is isolated per destroy, as in the in-process
		winEventCallback: the remaining destroys are still processed, and the cycle still
		reaches the dll flush, which rearms the dll's coalesced notifier so future events
		keep requesting pumps.
		"""
		fakeDll = _makeFakeDll(destroyEvents=[(1, 0, 0), (2, 0, 0)])
		self.installFakeDll(fakeDll)
		processed = []

		def failingProcessDestroy(window, objectID, childID):
			processed.append((window, objectID, childID))
			if window == 1:
				raise RuntimeError("destroy handler failure")

		with (
			mock.patch.object(
				internalWinEventHandler,
				"_processDestroyWinEvent",
				side_effect=failingProcessDestroy,
			),
		):
			IAccessibleHandler.pumpAll()
		self.assertEqual(processed, [(1, 0, 0), (2, 0, 0)])
		fakeDll.winEventLimiter_flushEvents.assert_called_once()

	def test_lossAfterRegularFlushEvictsCacheBeforeEventProcessing(self):
		"""Loss is sampled again after the regular flush, before its events can use
		objects whose destroy notifications might have been discarded.
		"""
		cacheKey = (42, winUser.OBJID_CLIENT, 0)
		cachedObject = mock.MagicMock(spec=NVDAObjects.IAccessible.IAccessible)
		IAccessibleHandler.liveNVDAObjectTable[cacheKey] = cachedObject
		fakeDll = _makeFakeDll(
			events=[(winUser.EVENT_OBJECT_NAMECHANGE, *cacheKey)],
		)
		# No loss at the destroy snapshot; a destroy is discarded before the
		# later regular event enters the DLL flush.
		fakeDll.winEventLimiter_takeLostDestroys.side_effect = [0, 1]
		self.installFakeDll(fakeDll)
		cacheWasEvicted = []

		def fakeShouldAcceptEvent(eventName, windowHandle=None):
			cacheWasEvicted.append(
				cacheKey not in IAccessibleHandler.liveNVDAObjectTable,
			)
			return False

		with (
			mock.patch.object(api, "getFocusObject", return_value=None),
			mock.patch.object(eventHandler, "shouldAcceptEvent", fakeShouldAcceptEvent),
		):
			IAccessibleHandler.pumpAll()
		self.assertEqual(cacheWasEvicted, [True])
		self.assertEqual(fakeDll.winEventLimiter_takeLostDestroys.call_count, 2)

	def test_lostCandidateWindowDestroyCorrectsFocus(self):
		"""A discarded destroy applies the #2695 IME candidate focus correction
		when the focused candidate window no longer exists.
		"""
		from NVDAObjects.IAccessible.mscandui import BaseCandidateItem

		fakeDll = _makeFakeDll(lostDestroys=True)
		self.installFakeDll(fakeDll)
		candidate = mock.MagicMock(spec=BaseCandidateItem)
		candidate.windowHandle = 42
		container = candidate.container
		with (
			mock.patch.object(api, "getFocusObject", return_value=candidate),
			mock.patch.object(winUser, "isWindow", return_value=False),
			mock.patch.object(eventHandler, "isPendingEvents", return_value=False),
			mock.patch.object(eventHandler, "lastQueuedFocusObject", None),
			mock.patch.object(eventHandler, "queueEvent") as queueEvent,
		):
			IAccessibleHandler.pumpAll()
		queueEvent.assert_called_once_with("gainFocus", container)

	def test_unrelatedLostDestroyDoesNotCorrectCandidateFocus(self):
		"""A discarded destroy for an unknown object must not move focus away
		from a candidate window that still exists.
		"""
		from NVDAObjects.IAccessible.mscandui import BaseCandidateItem

		fakeDll = _makeFakeDll(lostDestroys=True)
		self.installFakeDll(fakeDll)
		candidate = mock.MagicMock(spec=BaseCandidateItem)
		candidate.windowHandle = 42
		with (
			mock.patch.object(api, "getFocusObject", return_value=candidate),
			mock.patch.object(winUser, "isWindow", return_value=True),
			mock.patch.object(eventHandler, "lastQueuedFocusObject", None),
			mock.patch.object(eventHandler, "queueEvent") as queueEvent,
		):
			IAccessibleHandler.pumpAll()
		queueEvent.assert_not_called()


class Test_initializeFallback(unittest.TestCase):
	"""Initialization honours the externalWinEventLimiter feature flag,
	and falls back to internal hooks when the external limiter cannot be used.
	"""

	def setUp(self):
		self.hooks = []
		self.unhooked = []
		patchers = [
			mock.patch.object(
				winUser,
				"setWinEventHook",
				side_effect=lambda *args: (self.hooks.append(args), len(self.hooks))[1],
			),
			mock.patch.object(
				winUser,
				"unhookWinEvent",
				side_effect=self.unhooked.append,
			),
		]
		for patcher in patchers:
			patcher.start()
			self.addCleanup(patcher.stop)
		self.addCleanup(internalWinEventHandler.terminate)

	def enableExternalLimiterFlag(self):
		config.conf["IAccessible"]["externalWinEventLimiter"] = "enabled"
		self.addCleanup(
			config.conf["IAccessible"].__setitem__,
			"externalWinEventLimiter",
			"default",
		)

	def test_flagDisabledByDefaultUsesInternalHooks(self):
		with mock.patch.object(winEventLimiterLib, "getWinEventLimiterDll") as loader:
			internalWinEventHandler.initialize(lambda *args: None)
		loader.assert_not_called()
		self.assertIsNone(internalWinEventHandler._externalWinEventLimiterDll)
		self.assertEqual(
			len(self.hooks),
			len(internalWinEventHandler.winEventIDsToNVDAEventNames),
		)

	def test_fallsBackWhenDllMissing(self):
		self.enableExternalLimiterFlag()
		with mock.patch.object(
			winEventLimiterLib,
			"getWinEventLimiterDll",
			side_effect=OSError("dll not found"),
		):
			internalWinEventHandler.initialize(lambda *args: None)
		self.assertIsNone(internalWinEventHandler._externalWinEventLimiterDll)
		self.assertEqual(
			len(self.hooks),
			len(internalWinEventHandler.winEventIDsToNVDAEventNames),
		)

	def test_fallsBackWhenDllExportMissing(self):
		"""A loadable but stale dll raises AttributeError while its function prototypes
		are configured; NVDA must fall back to internal hooks rather than fail to start.
		"""
		self.enableExternalLimiterFlag()
		with mock.patch.object(
			winEventLimiterLib,
			"getWinEventLimiterDll",
			side_effect=AttributeError("function 'winEventLimiter_getDestroyEvents' not found"),
		):
			internalWinEventHandler.initialize(lambda *args: None)
		self.assertIsNone(internalWinEventHandler._externalWinEventLimiterDll)
		self.assertIsNone(internalWinEventHandler._externalWinEventLimiterDll)
		self.assertEqual(
			len(self.hooks),
			len(internalWinEventHandler.winEventIDsToNVDAEventNames),
		)

	def test_fallsBackWhenStartFails(self):
		self.enableExternalLimiterFlag()
		fakeDll = _makeFakeDll(startRet=-2)
		with mock.patch.object(
			winEventLimiterLib,
			"getWinEventLimiterDll",
			return_value=fakeDll,
		):
			internalWinEventHandler.initialize(lambda *args: None)
		self.assertIsNone(internalWinEventHandler._externalWinEventLimiterDll)
		self.assertIsNone(internalWinEventHandler._externalWinEventLimiterDll)
		self.assertEqual(
			len(self.hooks),
			len(internalWinEventHandler.winEventIDsToNVDAEventNames),
		)

	def test_fallsBackWhenStartRaises(self):
		self.enableExternalLimiterFlag()
		fakeDll = _makeFakeDll()
		fakeDll.winEventLimiter_start.side_effect = OSError("start fault")
		with mock.patch.object(
			winEventLimiterLib,
			"getWinEventLimiterDll",
			return_value=fakeDll,
		):
			internalWinEventHandler.initialize(lambda *args: None)
		self.assertIsNone(internalWinEventHandler._externalWinEventLimiterDll)
		self.assertEqual(
			len(self.hooks),
			len(internalWinEventHandler.winEventIDsToNVDAEventNames),
		)

	def test_externalModeDisabledBeforeDllStops(self):
		self.enableExternalLimiterFlag()
		fakeDll = _makeFakeDll()
		modeWhileStopping: list[bool] = []
		fakeDll.winEventLimiter_stop.side_effect = lambda: modeWhileStopping.append(
			internalWinEventHandler._externalWinEventLimiterDll is not None,
		)
		with mock.patch.object(
			winEventLimiterLib,
			"getWinEventLimiterDll",
			return_value=fakeDll,
		):
			internalWinEventHandler.initialize(lambda *args: None)
		self.assertIs(
			internalWinEventHandler._externalWinEventLimiterDll,
			fakeDll,
		)
		self.assertEqual(self.hooks, [])
		internalWinEventHandler.terminate()
		fakeDll.winEventLimiter_stop.assert_called_once()
		self.assertEqual(modeWhileStopping, [False])
		self.assertIsNone(internalWinEventHandler._externalWinEventLimiterDll)

	def test_initializationFailureReleasesWaitingCallbacks(self):
		with (
			mock.patch.object(
				internalWinEventHandler,
				"_registerInternalHooks",
				side_effect=RuntimeError("hook failure"),
			),
			self.assertRaises(RuntimeError),
		):
			internalWinEventHandler.initialize(lambda *args: None)
		self.assertTrue(internalWinEventHandler._limiterSelectionComplete.is_set())

	def test_startReceivesEventIdsTable(self):
		"""The dll hooks exactly the events NVDA's table defines: the Python table is the
		single source of truth for the winEvents to receive.
		"""
		self.enableExternalLimiterFlag()
		fakeDll = _makeFakeDll()
		with mock.patch.object(
			winEventLimiterLib,
			"getWinEventLimiterDll",
			return_value=fakeDll,
		):
			internalWinEventHandler.initialize(lambda *args: None)
		args = fakeDll.winEventLimiter_start.call_args.args
		self.assertEqual(len(args), 3)
		expectedIds = sorted(internalWinEventHandler.winEventIDsToNVDAEventNames)
		self.assertEqual(args[2], len(expectedIds))
		self.assertEqual(list(args[1]), expectedIds)

	def test_terminateUnhooksInternalHooks(self):
		self.enableExternalLimiterFlag()
		with mock.patch.object(
			winEventLimiterLib,
			"getWinEventLimiterDll",
			side_effect=OSError("dll not found"),
		):
			internalWinEventHandler.initialize(lambda *args: None)
		internalWinEventHandler.terminate()
		self.assertEqual(len(self.unhooked), len(self.hooks))
		self.assertEqual(internalWinEventHandler.winEventHookIDs, [])

	def test_terminateResetsDestroyHandler(self):
		"""terminate() must clear the destroy handler installed by initialize(), so a
		stale handler can never leak into a later initialize (or another test).
		"""

		def sentinel(*args):
			return None

		internalWinEventHandler.initialize(sentinel)
		self.assertIs(internalWinEventHandler._processDestroyWinEvent, sentinel)
		internalWinEventHandler.terminate()
		self.assertIsNone(internalWinEventHandler._processDestroyWinEvent)

	def test_terminateClearsConsoleWindowThreadIds(self):
		internalWinEventHandler.consoleWindowsToThreadIDs[42] = 5678
		internalWinEventHandler.terminate()
		self.assertEqual(internalWinEventHandler.consoleWindowsToThreadIDs, {})


class Test_pumpAll(_FakeDllTestCase):
	def test_pumpAllFetchesFromExternalWhenActive(self):
		fakeDll = _makeFakeDll()
		self.installFakeDll(fakeDll)
		IAccessibleHandler.pumpAll()
		fakeDll.winEventLimiter_flushEvents.assert_called_once()

	def test_pumpAllIgnoresExternalWhenInactive(self):
		fakeDll = _makeFakeDll()
		self.installFakeDll(fakeDll)
		with (
			mock.patch.object(internalWinEventHandler, "_externalWinEventLimiterDll", None),
			mock.patch.object(internalWinEventHandler, "_shouldGetEvents", return_value=False),
		):
			IAccessibleHandler.pumpAll()
		fakeDll.winEventLimiter_flushEvents.assert_not_called()

	def test_realFocusAfterAddedFocusWins(self):
		"""A later hooked focus event must remain newer than an explicitly added focus."""
		events: list[tuple[int, int | None, int, int]] = []
		fakeDll = _makeFakeDll(events=events)
		self.installFakeDll(fakeDll)
		with (
			mock.patch.object(eventHandler, "shouldAcceptEvent", return_value=True),
			mock.patch.object(
				internalWinEventHandler.winEventLimiter,
				"flushEvents",
			) as flushInternal,
			mock.patch.object(
				IAccessibleHandler,
				"processFocusWinEvent",
				return_value=True,
			) as processFocus,
		):
			internalWinEventHandler.addEvent(
				winUser.EVENT_OBJECT_FOCUS,
				42,
				winUser.OBJID_CLIENT,
				0,
				7,
			)
			# This represents a real MSAA focus arriving after the added Word focus.
			events.append(
				(winUser.EVENT_OBJECT_FOCUS, 84, winUser.OBJID_CLIENT, 0),
			)
			IAccessibleHandler.pumpAll()
		processFocus.assert_called_once_with(84, winUser.OBJID_CLIENT, 0)
		flushInternal.assert_not_called()

	def test_addedFocusAfterRealFocusWins(self):
		"""An explicitly added focus must remain newer than an earlier hooked focus."""
		events: list[tuple[int, int | None, int, int]] = [
			(winUser.EVENT_OBJECT_FOCUS, 84, winUser.OBJID_CLIENT, 0),
		]
		fakeDll = _makeFakeDll(events=events)
		self.installFakeDll(fakeDll)
		with (
			mock.patch.object(eventHandler, "shouldAcceptEvent", return_value=True),
			mock.patch.object(
				IAccessibleHandler,
				"processFocusWinEvent",
				return_value=True,
			) as processFocus,
		):
			internalWinEventHandler.addEvent(
				winUser.EVENT_OBJECT_FOCUS,
				42,
				winUser.OBJID_CLIENT,
				0,
				7,
			)
			IAccessibleHandler.pumpAll()
		processFocus.assert_called_once_with(42, winUser.OBJID_CLIENT, 0)

	def test_deferredCycleHoldsAddedEvents(self):
		"""#3831: while the dll defers the flush for a pending foreground change, the whole
		cycle is held, including explicitly added events. Destroys are still processed,
		matching the in-process implementation which handles them at hook-callback time
		regardless of the defer.
		"""
		events: list[tuple[int, int | None, int, int]] = []
		fakeDll = _makeFakeDll(
			events=events,
			destroyEvents=[(42, 0, 0)],
			flushDeferred=True,
		)
		self.installFakeDll(fakeDll)
		with (
			mock.patch.object(eventHandler, "shouldAcceptEvent", return_value=True),
			mock.patch.object(
				internalWinEventHandler,
				"_processDestroyWinEvent",
			) as processDestroy,
			mock.patch.object(
				IAccessibleHandler,
				"processFocusWinEvent",
				return_value=True,
			) as processFocus,
		):
			internalWinEventHandler.addEvent(
				winUser.EVENT_OBJECT_FOCUS,
				42,
				winUser.OBJID_CLIENT,
				0,
				7,
			)
			IAccessibleHandler.pumpAll()
		processDestroy.assert_called_once_with(42, 0, 0)
		processFocus.assert_not_called()
		fakeDll.winEventLimiter_getEvents.assert_not_called()
		self.assertEqual(
			events,
			[(winUser.EVENT_OBJECT_FOCUS, 42, winUser.OBJID_CLIENT, 0)],
		)

	def test_lostDestroysEvictWholeObjectCache(self):
		"""When the dll had to shed destroys under a sustained flood, a destroy may have
		been missed for any window, so pumpAll evicts the whole object cache rather than
		relying on per window destroy processing.
		"""
		fakeDll = _makeFakeDll(lostDestroys=True)
		self.installFakeDll(fakeDll)
		cachedObject = mock.MagicMock(spec=NVDAObjects.IAccessible.IAccessible)
		IAccessibleHandler.liveNVDAObjectTable[(42, 0, 0)] = cachedObject
		IAccessibleHandler.pumpAll()
		self.assertNotIn((42, 0, 0), IAccessibleHandler.liveNVDAObjectTable)
