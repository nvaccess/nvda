# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited

"""Unit tests for the orderedWinEventLimiter module.
"""
import inspect
import re
import unittest
from typing import List, Iterator, Callable
import winUser
from IAccessibleHandler import orderedWinEventLimiter
from IAccessibleHandler.orderedWinEventLimiter import OrderedWinEventLimiter


def softAssert(errorList: List[AssertionError], method: Callable, *args, **kwargs):
	try:
		method(*args, **kwargs)
	except AssertionError as e:
		errorList.append(e)


specialCaseEvents = [
	winUser.EVENT_SYSTEM_FOREGROUND,
	winUser.EVENT_OBJECT_FOCUS,
	winUser.EVENT_OBJECT_SHOW,
	winUser.EVENT_OBJECT_HIDE,
	winUser.EVENT_SYSTEM_MENUSTART,
	winUser.EVENT_SYSTEM_MENUEND,
	winUser.EVENT_SYSTEM_MENUPOPUPSTART,
	winUser.EVENT_SYSTEM_MENUPOPUPEND
]


def _getNonSpecialCaseEvents() -> Iterator[int]:
	objectOrSystemEvent = re.compile("^EVENT_(OBJECT|SYSTEM)_")
	for name, value in inspect.getmembers(winUser):
		if value not in specialCaseEvents and objectOrSystemEvent.match(name):
			yield value


nonSpecialCaseEvents: List[int] = list(_getNonSpecialCaseEvents())


class TestOrderedWinEventLimiter(unittest.TestCase):

	def test_nonSpecialCaseEvents(self):
		"""Test that the list of events without special cases matches expectations
		"""
		self.assertEqual(39, len(nonSpecialCaseEvents))

	def test_maxFocusEvents(self):
		limiter = OrderedWinEventLimiter(maxFocusItems=4)
		for n in range(0, 5):
			limiter.addEvent(
				eventID=winUser.EVENT_OBJECT_FOCUS,
				window=n, objectID=n, childID=n, threadID=n,
			)
		events = limiter.flushEvents()
		windowIds = [
			e[1]  # window
			for e in events
		]
		expectedIds = [1, 2, 3, 4]
		self.assertEqual(expectedIds, windowIds)

	# Todo: Why do we get two events matching events?
	def test_foregroundOverwritesFocus(self):
		limiter = OrderedWinEventLimiter(maxFocusItems=4)
		n = 1
		limiter.addEvent(
			eventID=winUser.EVENT_OBJECT_FOCUS,
			window=n, objectID=n, childID=n, threadID=n,
		)
		limiter.addEvent(
			eventID=winUser.EVENT_SYSTEM_FOREGROUND,
			window=n, objectID=n, childID=n, threadID=n,
		)
		events = limiter.flushEvents()
		actualEvents = [(
			e[0],  # eventID
			e[1],  # window
		) for e in events
		]
		expectedEvents = [
			(winUser.EVENT_SYSTEM_FOREGROUND, n),
			(winUser.EVENT_SYSTEM_FOREGROUND, n)
		]
		self.assertEqual(expectedEvents, actualEvents)

	def test_showOverridesHide_whenDetailsMatch(self):
		limiter = OrderedWinEventLimiter(maxFocusItems=4)
		n = 1
		limiter.addEvent(
			eventID=winUser.EVENT_OBJECT_HIDE,
			window=n, objectID=n, childID=n, threadID=n,
		)
		limiter.addEvent(
			eventID=winUser.EVENT_OBJECT_SHOW,
			window=n, objectID=n, childID=n, threadID=n,
		)
		events = limiter.flushEvents()
		actualEvents = [
			(e[0], e[1])
			for e in events
		]
		expectedEvents = [
			(winUser.EVENT_OBJECT_SHOW, n),
		]
		self.assertEqual(expectedEvents, actualEvents)

	def test_hideOverridesShow_whenDetailsMatch(self):
		limiter = OrderedWinEventLimiter(maxFocusItems=4)
		n = 1
		limiter.addEvent(
			eventID=winUser.EVENT_OBJECT_SHOW,
			window=n, objectID=n, childID=n, threadID=n,
		)
		limiter.addEvent(
			eventID=winUser.EVENT_OBJECT_HIDE,
			window=n, objectID=n, childID=n, threadID=n,
		)
		events = limiter.flushEvents()
		actualEvents = [
			(e[0], e[1])
			for e in events
		]
		expectedEvents = [
			(winUser.EVENT_OBJECT_HIDE, n),
		]
		self.assertEqual(expectedEvents, actualEvents)

	def test_showNoOverridesHide_whenDetailsDontMatch(self):
		limiter = OrderedWinEventLimiter(maxFocusItems=4)
		n = 1
		limiter.addEvent(
			eventID=winUser.EVENT_OBJECT_HIDE,
			window=n, objectID=n, childID=n, threadID=n,
		)
		n = 2
		limiter.addEvent(
			eventID=winUser.EVENT_OBJECT_SHOW,
			window=n, objectID=n, childID=n, threadID=n,
		)
		events = limiter.flushEvents()
		actualEvents = [
			(e[0], e[1])
			for e in events
		]
		expectedEvents = [
			(winUser.EVENT_OBJECT_HIDE, 1),
			(winUser.EVENT_OBJECT_SHOW, 2),
		]
		self.assertEqual(expectedEvents, actualEvents)

	def test_hideNoOverridesShow_whenDetailsDontMatch(self):
		limiter = OrderedWinEventLimiter(maxFocusItems=4)
		n = 1
		limiter.addEvent(
			eventID=winUser.EVENT_OBJECT_SHOW,
			window=n, objectID=n, childID=n, threadID=n,
		)
		n = 2
		limiter.addEvent(
			eventID=winUser.EVENT_OBJECT_HIDE,
			window=n, objectID=n, childID=n, threadID=n,
		)
		events = limiter.flushEvents()
		actualEvents = [
			(e[0], e[1])
			for e in events
		]
		expectedEvents = [
			(winUser.EVENT_OBJECT_SHOW, 1),
			(winUser.EVENT_OBJECT_HIDE, 2),
		]
		self.assertEqual(expectedEvents, actualEvents)

	def test_alwaysAllowedObjects_specialCaseEvents(self):
		# We have events from two unique objects:
		# Window, objectID, childID
		allowedSource = (1, 1, 1)

		limiter = OrderedWinEventLimiter(maxFocusItems=4)
		for n in range(2000):  # send many events, to saturate all limits.
			eventId = specialCaseEvents[n % len(specialCaseEvents)]
			limiter.addEvent(eventId, *allowedSource, threadID=0)
		events = limiter.flushEvents(alwaysAllowedObjects=[allowedSource, ])

		expected = [
			# Two Foreground events, because they are added to multiple queues.
			# Added to both _focusEventCache and _genericEventCache
			# See also test_limitEventsPerThread
			(winUser.EVENT_SYSTEM_FOREGROUND, *allowedSource),
			(winUser.EVENT_SYSTEM_FOREGROUND, *allowedSource),
			(winUser.EVENT_OBJECT_FOCUS, *allowedSource),
			(winUser.EVENT_OBJECT_HIDE, *allowedSource),  # latest out of show / hide is kept
			(winUser.EVENT_SYSTEM_MENUPOPUPEND, *allowedSource),  # Only one menu event is allowed
		]
		self.assertEqual(expected, events)

	def test_alwaysAllowedObjects_onlyLatestEventKept(self):
		# We have events from two unique objects:
		# Window, objectID, childID
		allowedSource = (1, 1, 1)
		otherSource = (2, 2, 2,)

		limiter = OrderedWinEventLimiter(maxFocusItems=4)
		for n in range(50):  # send many value changed events
			limiter.addEvent(winUser.EVENT_OBJECT_VALUECHANGE, *allowedSource, threadID=0)
			limiter.addEvent(winUser.EVENT_OBJECT_VALUECHANGE, *otherSource, threadID=0)
		events = limiter.flushEvents(alwaysAllowedObjects=[allowedSource, ])
		# only the most recent event of each object is kept, all previous duplicates are discarded
		self.assertEqual(2, len(events))

	def test_threadLimit_singleObject(self):
		"""Test that only the latest events are kept when the thread limit is exceeded
		"""
		# We have events from two unique objects:
		# Window, objectID, childID
		source = (2, 2, 2,)

		limiter = OrderedWinEventLimiter(maxFocusItems=4)

		for n in range(500):  # exceed the limit for a single thread
			eventId = nonSpecialCaseEvents[n % len(nonSpecialCaseEvents)]
			# same thread, different object. Use a second object to aid tracking.
			limiter.addEvent(eventId, *source, threadID=0)

		events = limiter.flushEvents()
		expectedEventCount = orderedWinEventLimiter.MAX_WINEVENTS_PER_THREAD
		self.assertEqual(expectedEventCount, len(events))

	def test_threadLimit_noCanary(self):
		"""Test that only the latest events are kept when the thread limit is exceeded
		"""
		limiter = OrderedWinEventLimiter(maxFocusItems=4)

		for n in range(500):  # exceed the limit for a single thread
			eventId = nonSpecialCaseEvents[n % len(nonSpecialCaseEvents)]
			# same thread, different object. Ensure there are no duplicates
			# Window, objectID, childID
			source = (2, 2, n,)
			limiter.addEvent(eventId, *source, threadID=0)

		events = limiter.flushEvents()

		errors = []
		expectedEventCount = orderedWinEventLimiter.MAX_WINEVENTS_PER_THREAD
		softAssert(errors, self.assertEqual, expectedEventCount, len(events))  # Fails with 11 actual events
		self.assertListEqual([], errors)

	def test_threadLimit_withCanaryAtStart(self):
		"""Test that only the latest events are kept when the thread limit is exceeded
		"""
		limiter = OrderedWinEventLimiter(maxFocusItems=4)

		# Window, objectID, childID
		canaryObject = (1, 1, 1)
		eventStartCanary = (winUser.EVENT_OBJECT_VALUECHANGE, *canaryObject)
		limiter.addEvent(*eventStartCanary, threadID=0)

		for n in range(500):  # exceed the limit for a single thread
			eventId = nonSpecialCaseEvents[n % len(nonSpecialCaseEvents)]
			# same thread, different object. Ensure there are no duplicates
			# Window, objectID, childID
			source = (2, 2, n,)
			limiter.addEvent(eventId, *source, threadID=0)

		events = limiter.flushEvents()

		errors = []
		expectedEventCount = orderedWinEventLimiter.MAX_WINEVENTS_PER_THREAD
		softAssert(errors, self.assertEqual, expectedEventCount, len(events))  # Fails with 11 actual events
		softAssert(errors, self.assertNotIn, eventStartCanary, events)
		self.assertListEqual([], errors)

	def test_threadLimit_canaryStartAndEnd(self):
		"""Test that only the latest events are kept when the thread limit is exceeded
		"""
		limiter = OrderedWinEventLimiter(maxFocusItems=4)

		# Window, objectID, childID
		canaryObject = (1, 1, 1)
		eventStartCanary = (winUser.EVENT_OBJECT_VALUECHANGE, *canaryObject)
		limiter.addEvent(*eventStartCanary, threadID=0)

		for n in range(500):  # exceed the limit for a single thread
			eventId = nonSpecialCaseEvents[n % len(nonSpecialCaseEvents)]
			# same thread, different object. Ensure there are no duplicates
			# Window, objectID, childID
			source = (2, 2, n,)
			limiter.addEvent(eventId, *source, threadID=0)

		# Note event type must differ from start canary to ensure they are not duplicates
		eventEndCanary = (winUser.EVENT_OBJECT_NAMECHANGE, *canaryObject)
		limiter.addEvent(*eventEndCanary, threadID=0)

		events = limiter.flushEvents()
		errors = []
		expectedEventCount = orderedWinEventLimiter.MAX_WINEVENTS_PER_THREAD
		softAssert(errors, self.assertEqual, expectedEventCount, len(events))  # Fails with 11 actual events
		softAssert(errors, self.assertIn, eventEndCanary, events)
		softAssert(errors, self.assertNotIn, eventStartCanary, events)
		self.assertListEqual([], errors)

	def test_alwaysAllowedObjects(self):
		"""Matches test_threadLimit_canaryStartAndEnd, but allows events from the first object
		"""
		limiter = OrderedWinEventLimiter(maxFocusItems=4)

		# Window, objectID, childID
		canaryObject = (1, 1, 1)
		eventStartCanary = (winUser.EVENT_OBJECT_VALUECHANGE, *canaryObject)
		limiter.addEvent(*eventStartCanary, threadID=0)

		for n in range(orderedWinEventLimiter.MAX_WINEVENTS_PER_THREAD):  # exceed the limit for a single thread
			eventId = nonSpecialCaseEvents[n % len(nonSpecialCaseEvents)]
			# same thread, different object. Ensure there are no duplicates
			# Window, objectID, childID
			source = (2, 2, n,)
			limiter.addEvent(eventId, *source, threadID=0)

		eventEndCanary = (winUser.EVENT_OBJECT_NAMECHANGE, *canaryObject)
		limiter.addEvent(*eventEndCanary, threadID=0)

		events = limiter.flushEvents(alwaysAllowedObjects=[canaryObject, ])
		# only the most recent event of each object is kept, all previous duplicates are discarded
		self.assertEqual(11, len(events))
		self.assertIn(eventStartCanary, events)
		self.assertEqual(eventStartCanary, events[0])
		self.assertIn(eventEndCanary, events)

	def test_limitEventsPerThread(self):
		limiter = OrderedWinEventLimiter(maxFocusItems=4)
		for n in reversed(range(2000)):  # send many events, to saturate all limits.
			limiter.addEvent(
				eventID=specialCaseEvents[n % len(specialCaseEvents)],
				window=n, objectID=n, childID=n,
				threadID=0,  # all events for same thread
			)
		events = limiter.flushEvents()
		windowIds = [
			e[1]  # window
			for e in events
		]
		# TODO: Note: repeated Id's (0 and 8) are EVENT_SYSTEM_FOREGROUND see test_maxFocusEvents
		expectedIds = [24, 19, 18, 16, 11, 10, 9, 8, 8, 4, 3, 2, 1, 0, 0]
		self.assertEqual(expectedIds, windowIds)
		#  equal to MAX_WINEVENTS_PER_THREAD=10
		# Plus 4 focus events,
		# Plus the last menu event.
		#  All totalling 15.
		self.assertEqual(len(windowIds), 15)
