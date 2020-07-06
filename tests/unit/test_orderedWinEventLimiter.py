# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited

"""Unit tests for the orderedWinEventLimiter module.
"""

import unittest
import winUser
from IAccessibleHandler.orderedWinEventLimiter import OrderedWinEventLimiter

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


class TestOrderedWinEventLimiter(unittest.TestCase):

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
		expectedIds = [26, 24, 19, 18, 16, 11, 10, 9, 8, 8, 4, 3, 2, 1, 0, 0]
		self.assertEqual(expectedIds, windowIds)
		# TODO:
		#  Why isn't this equal to MAX_WINEVENTS_PER_THREAD=10
		#  There are also 4 focus events.
		#  But the total is 16 not 10+4=14?
		self.assertEqual(len(windowIds), 16)
