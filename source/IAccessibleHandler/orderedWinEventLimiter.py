from typing import Optional, List
import heapq
import itertools

import winUser
from .types import IAccessibleObjectIdentifierType
from logHandler import log
from .utils import getWinEventLogInfo, isMSAADebugLoggingEnabled


MAX_WINEVENTS_PER_THREAD = 10

MENU_EVENTIDS = (
	winUser.EVENT_SYSTEM_MENUSTART,
	winUser.EVENT_SYSTEM_MENUEND,
	winUser.EVENT_SYSTEM_MENUPOPUPSTART,
	winUser.EVENT_SYSTEM_MENUPOPUPEND
)


class OrderedWinEventLimiter(object):
	"""Collects and limits winEvents based on whether they are focus changes,
	or just generic (all other ones).

	Only allow a max of L{maxFocusItems}:
	- if more are added then the oldest focus event is removed to make room.
	Only allow one event for one specific object at a time:
	- though push it further forward in time if a duplicate tries to get added.
	- This is true for both generic and focus events.
	"""

	def __init__(self, maxFocusItems=4):
		"""
		@param maxFocusItems: the amount of focus changed events allowed to be queued.
		@type maxFocusItems: integer
		"""
		self.maxFocusItems = maxFocusItems
		self._focusEventCache = {}
		self._genericEventCache = {}
		self._eventHeap = []
		self._eventCounter = itertools.count()
		self._lastMenuEvent = None

	def addEvent(
			self,
			eventID: int,
			window: int,
			objectID: int,
			childID: int,
			threadID: int
	) -> bool:
		"""Adds a winEvent to the limiter.
		@param eventID: the winEvent type
		@param window: the window handle of the winEvent
		@param objectID: the objectID of the winEvent
		@param childID: the childID of the winEvent
		@param threadID: the threadID of the winEvent
		@return: C{True} if the event was added, C{False} if it was discarded.
		"""
		if eventID == winUser.EVENT_OBJECT_FOCUS:
			if objectID in (winUser.OBJID_SYSMENU, winUser.OBJID_MENU) and childID == 0:
				# This is a focus event on a menu bar itself, which is just silly. Ignore it.
				return False
			self._focusEventCache[(eventID, window, objectID, childID, threadID)] = next(self._eventCounter)
			return True
		elif eventID == winUser.EVENT_SYSTEM_FOREGROUND:
			self._focusEventCache.pop((winUser.EVENT_OBJECT_FOCUS, window, objectID, childID, threadID), None)
			self._focusEventCache[(eventID, window, objectID, childID, threadID)] = next(self._eventCounter)
		elif eventID == winUser.EVENT_OBJECT_SHOW:
			k = (winUser.EVENT_OBJECT_HIDE, window, objectID, childID, threadID)
			if k in self._genericEventCache:
				del self._genericEventCache[k]
		elif eventID == winUser.EVENT_OBJECT_HIDE:
			k = (winUser.EVENT_OBJECT_SHOW, window, objectID, childID, threadID)
			if k in self._genericEventCache:
				del self._genericEventCache[k]
		elif eventID in MENU_EVENTIDS:
			self._lastMenuEvent = (next(self._eventCounter), eventID, window, objectID, childID, threadID)
			return True
		self._genericEventCache[(eventID, window, objectID, childID, threadID)] = next(self._eventCounter)
		return True

	def flushEvents(
			self,
			alwaysAllowedObjects: Optional[List[IAccessibleObjectIdentifierType]] = None
	) -> List:
		"""Returns a list of winEvents that have been added.
		Due to limiting, it will not necessarily be all the winEvents that were originally added.
		They are definitely guaranteed to be in the correct order though.
		winEvents for objects listed in alwaysAllowedObjects will always be emitted,
		Even if the winEvent limit for that thread has been exceeded.
		@return Tuple[eventID,window,objectID,childID]
		"""
		if self._lastMenuEvent is not None:
			heapq.heappush(self._eventHeap, self._lastMenuEvent)
			self._lastMenuEvent = None
		g = self._genericEventCache
		self._genericEventCache = {}
		threadCounters = {}
		for k, v in sorted(g.items(), key=lambda item: item[1], reverse=True):
			# Increase the event count for this thread by 1.
			threadCount = threadCounters.get(k[-1], 0)
			threadCounters[k[-1]] = threadCount + 1
			if isMSAADebugLoggingEnabled():
				if threadCount == MAX_WINEVENTS_PER_THREAD:
					log.debug(f"winEvent limit for thread {k[-1]} hit for this core cycle")
			# Find out if this event is for an object whos events are always allowed.
			eventsForObjectAlwaysAllowed = alwaysAllowedObjects and k[1:-1] in alwaysAllowedObjects
			if threadCount >= MAX_WINEVENTS_PER_THREAD and not eventsForObjectAlwaysAllowed:
				# Skip this event if too many events have already been emitted for this thread
				# and this event is not for an object whos events are always allowed.
				continue
			heapq.heappush(self._eventHeap, (v,) + k)
		f = self._focusEventCache
		self._focusEventCache = {}
		for k, v in sorted(f.items(), key=lambda item: item[1])[0 - self.maxFocusItems:]:
			heapq.heappush(self._eventHeap, (v,) + k)
		e = self._eventHeap
		self._eventHeap = []
		r = []
		for count in range(len(e)):
			event = heapq.heappop(e)[1:]
			if isMSAADebugLoggingEnabled():
				eventID, window, objectID, childID, threadID = event
				log.debug(
					f"Emitting winEvent {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}"
				)
			r.append(event[:-1])
		return r
