# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Derek Riemer
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Crash handling helpers shared by watchdog and the rest of NVDA."""

from __future__ import annotations

import ctypes
import json
import os
import time
from dataclasses import asdict, dataclass

from logHandler import log
import logHandler
import core
import globalVars
import NVDAHelper
import winBindings.kernel32
from winBindings.kernel32 import UnhandledExceptionFilter


@dataclass(frozen=True)
class CrashStats:
	fileName: str = "nvda_crash_stats.txt"
	timeout: int = 120
	maxCount: int = 3

	@property
	def crashStatsPath(self) -> str:
		return os.path.join(os.path.dirname(globalVars.appArgs.logFileName), self.fileName)


CRASH_STATS = CrashStats()


@dataclass
class CrashEvent:
	timestamp: float
	version: str
	installType: str

	def json(self) -> str:
		return json.dumps(asdict(self), separators=(",", ":"))

	@staticmethod
	def from_line(line: str) -> "CrashEvent | None":
		if not line:
			return None
		try:
			data = json.loads(line)
		except json.JSONDecodeError:
			return None
		if not isinstance(data, dict):
			return None
		try:
			timestamp = float(data["timestamp"])
			version = data["version"]
			installType = data["installType"]
		except (KeyError, TypeError, ValueError):
			return None
		if not isinstance(version, str) or not version:
			return None
		if not isinstance(installType, str) or not installType:
			return None
		return CrashEvent(timestamp=timestamp, version=version, installType=installType)


def _getCurrentCrashFingerprint() -> tuple[str, str]:
	try:
		import buildVersion

		version = buildVersion.version
	except Exception:
		log.debugWarning("Failed to determine NVDA version for crash stats", exc_info=True)
		version = "unknown"

	installType = "unknown"
	try:
		import config
	except Exception:
		log.debugWarning("Failed to import config for crash stats", exc_info=True)
	else:
		try:
			if config.isInstalledCopy():
				installType = "installed"
			else:
				installType = "portable"
		except Exception:
			log.debugWarning("Failed to determine install type for crash stats", exc_info=True)

	return version, installType


def _buildCrashEvent(timestamp: float, version: str, installType: str) -> CrashEvent:
	return CrashEvent(timestamp=float(timestamp), version=version, installType=installType)


def _writeCrashStats(path: str, events: list[CrashEvent]) -> None:
	try:
		with open(path, "w", encoding="utf-8") as f:
			for event in events:
				f.write(f"{event.json()}\n")
	except OSError:
		log.debugWarning("Failed to update crash stats file", exc_info=True)


def loadRecentCrashTimestamps(now: float) -> list[float]:
	path = CRASH_STATS.crashStatsPath
	# Check existence explicitly rather than catching exceptions, as this check is far faster than catching an expected exception.
	if not os.path.exists(path):
		return []
	try:
		with open(path, "r", encoding="utf-8") as f:
			lines = f.readlines()
	except OSError:
		log.debugWarning("Failed to read crash stats file", exc_info=True)
		return []

	recentCrashes: list[float] = []
	eventsToRetain: list[CrashEvent] = []
	needsRewrite = False
	currentVersion, currentInstallType = _getCurrentCrashFingerprint()
	for line in lines:
		event = CrashEvent.from_line(line.strip())
		if event is None:
			needsRewrite = True
			continue
		timestamp = event.timestamp
		if now - timestamp <= CRASH_STATS.timeout:
			eventsToRetain.append(event)
			if event.version == currentVersion and event.installType == currentInstallType:
				recentCrashes.append(timestamp)
		else:
			# Older entries fall outside of the tracking window.
			needsRewrite = True

	if needsRewrite:
		_writeCrashStats(path, eventsToRetain)

	return recentCrashes


def _recordCrashTimestamp() -> None:
	path = CRASH_STATS.crashStatsPath
	version, installType = _getCurrentCrashFingerprint()
	try:
		with open(path, "a", encoding="utf-8") as f:
			event = _buildCrashEvent(time.time(), version, installType)
			# Append JSON lines instead of writing a list; NVDA is crashing, keep work minimal
			f.write(f"{event.json()}\n")
	except OSError:
		log.debugWarning("Failed to append crash stats", exc_info=True)


@UnhandledExceptionFilter
def crashHandler(exceptionInfo):
	threadId = winBindings.kernel32.GetCurrentThreadId()
	# An exception might have been set for this thread.
	# Clear it so that it doesn't get raised in this function.
	ctypes.pythonapi.PyThreadState_SetAsyncExc(threadId, None)

	# Write a minidump.
	dumpPath = os.path.join(os.path.dirname(globalVars.appArgs.logFileName), "nvda_crash.dmp")
	if not NVDAHelper.localLib.writeCrashDump(dumpPath, exceptionInfo):
		log.critical("NVDA crashed! Error writing minidump", exc_info=True)
	else:
		log.critical(f"NVDA crashed! Minidump written to {dumpPath}")

	# Log Python stacks for every thread.
	stacks = logHandler.getFormattedStacksForAllThreads()
	log.info(f"Listing stacks for Python threads:\n{stacks}")

	_recordCrashTimestamp()
	log.info("Restarting due to crash")
	# if NVDA has crashed we cannot rely on the queue handler to start the new NVDA instance
	core.restartUnsafely()
	return 1  # EXCEPTION_EXECUTE_HANDLER
