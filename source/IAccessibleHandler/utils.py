# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


"""Utility functions for IAccessibleHander.
Kept here so they can be re-used without having to worry about circular imports.
"""

import appModuleHandler
from comInterfaces import IAccessible2Lib as IA2
import config
import winUser


_winEventNameCache = {}


def getWinEventName(eventID):
	""" Looks up the name of an EVENT_* winEvent constant. """
	global _winEventNameCache
	if not _winEventNameCache:
		_winEventNameCache = {y: x for x, y in vars(winUser).items() if x.startswith('EVENT_')}
		_winEventNameCache.update({y: x for x, y in vars(IA2).items() if x.startswith('IA2_EVENT_')})
	name = _winEventNameCache.get(eventID)
	if not name:
		name = "unknown event ({eventID})"
	return name


_objectIDNameCache = {}


def getObjectIDName(objectID):
	""" Looks up the name of an OBJID_* winEvent constant. """
	global _objectIDNameCache
	if not _objectIDNameCache:
		_objectIDNameCache = {y: x for x, y in vars(winUser).items() if x.startswith('OBJID_')}
	name = _objectIDNameCache.get(objectID)
	if not name:
		name = str(objectID)
	return name


def getWinEventLogInfo(window, objectID, childID, eventID=None, threadID=None):
	"""
	Formats the given winEvent parameters into a printable string.
	window, objectID and childID are mandatory,
	but eventID and threadID are optional.
	"""
	windowClassName = winUser.getClassName(window) or "unknown"
	objectIDName = getObjectIDName(objectID)
	processID = winUser.getWindowThreadProcessID(window)[0]
	if processID:
		processName = appModuleHandler.getAppModuleFromProcessID(processID).appName
	else:
		processName = "unknown application"
	messageList = []
	if eventID is not None:
		eventName = getWinEventName(eventID)
		messageList.append(f"{eventName}")
	messageList.append(
		f"window {window} ({windowClassName}), objectID {objectIDName}, childID {childID}, "
		f"process {processID} ({processName})"
	)
	if threadID is not None:
		messageList.append(f"thread {threadID}")
	return ", ".join(messageList)


def isMSAADebugLoggingEnabled():
	""" Whether the user has configured NVDA to log extra information about MSAA events. """
	return config.conf["debugLog"]["MSAA"]
