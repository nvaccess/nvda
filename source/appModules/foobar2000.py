# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2023 NV Access Limited, Aleksey Sadovoy, James Teh, Joseph Lee, Tuukka Ojala,
# Bram Duvigneau, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from datetime import datetime
import re
from typing import (
	Dict,
	NamedTuple,
	Optional,
	TYPE_CHECKING,
)

import appModuleHandler
import api
from datetime import timedelta
from logHandler import log
import ui
from utils.localisation import TimeOutputFormat
from scriptHandler import script

if TYPE_CHECKING:
	from inputCore import InputGesture  # noqa: F401
	from NVDAObjects import NVDAObject  # noqa: F401


_timeOutputToParsingFormats: Dict[TimeOutputFormat, str] = {
	TimeOutputFormat.SECONDS: r"%S",
	TimeOutputFormat.MINUTES: r"%M:%S",
	TimeOutputFormat.HOURS: r"%H:%M:%S",
	TimeOutputFormat.DAY: r"%dd %H:%M:%S",
	# Handles D <= 31
	TimeOutputFormat.DAYS: r"%dd %H:%M:%S",
}


def _getTimeOutputFormat(timeStr: str) -> Optional[TimeOutputFormat]:
	"""
	Attempts to find a suitable output format for a
	D HH:MM:SS, HH:MM:SS, MM:SS or SS -style interval.
	"""
	timeStr = timeStr.strip()
	timestampRe = re.compile(
		r"^"
		r"(?:(?P<D>[0-9]+)d )?"
		r"(?:(?P<HH_MM>[0-9]{1,2}):)?"  # if both HH_MM and MM match, the time is HH_MM:MM:SS in HH:MM:SS format
		r"(?:(?P<MM>[0-9]{1,2}):)?"  # if HH_MM matches and not MM, the time is HH_MM:SS in MM:SS format
		r"(?P<SS>[0-9]{1,2})"
		r"$",
	)
	match = timestampRe.match(timeStr)
	if match is None:
		return None
	matchDict = match.groupdict()
	if matchDict["D"] == "1":
		return TimeOutputFormat.DAY
	elif matchDict["D"]:
		return TimeOutputFormat.DAYS
	elif matchDict["HH_MM"] and matchDict["MM"]:
		return TimeOutputFormat.HOURS
	elif matchDict["HH_MM"] and not matchDict["MM"]:
		return TimeOutputFormat.MINUTES
	elif matchDict["SS"]:
		return TimeOutputFormat.SECONDS
	else:
		log.error(f"Unexpected parsing format {timeStr}")
		return None


def _parseTimeStrToTimeDelta(timeStr: str) -> Optional[timedelta]:
	"""
	Attempts to convert a time string to a timedelta for a
	D HH:MM:SS, HH:MM:SS, MM:SS or SS -style interval.

	Note days D must be less than or equal to 31.
	"""
	timeStr = timeStr.strip()
	outputFormat = _getTimeOutputFormat(timeStr)
	if outputFormat is None:
		return None
	try:
		parsedTime = datetime.strptime(
			timeStr,
			_timeOutputToParsingFormats[outputFormat]
		)
	except ValueError:
		# Note if D > 31, strptime does not recognise that value for d.
		log.exception(f"Unexpected time format {timeStr}.")
		return None
	if outputFormat in (TimeOutputFormat.DAY, TimeOutputFormat.DAYS):
		parsedDay = parsedTime.day
	else:
		parsedDay = 0
	return timedelta(
		days=parsedDay,
		hours=parsedTime.hour,
		minutes=parsedTime.minute,
		seconds=parsedTime.second
	)


def _parseTimeStrToOutputFormatted(timeStr: str) -> Optional[str]:
	td = _parseTimeStrToTimeDelta(timeStr)
	if td is None:
		return td
	return TimeOutputFormat.parseTimeDeltaToFormatted(td)


class _StatusBarTimes(NamedTuple):
	"""
	A named tuple for holding the elapsed and total playing times from Foobar2000's status bar
	"""
	elapsed: Optional[str]
	total: Optional[str]


class AppModule(appModuleHandler.AppModule):
	_statusBar: Optional["NVDAObject"] = None

	def event_gainFocus(self, obj, nextHandler):
		if not self._statusBar:
			self._statusBar = api.getStatusBar()
		nextHandler()

	def getElapsedAndTotal(self) -> _StatusBarTimes:
		empty = _StatusBarTimes(None, None)
		if not self._statusBar:
			return empty
		statusBarContents = self._statusBar.firstChild.name
		try:
			playingTimes = statusBarContents.split("|")[4].split("/")
		except IndexError:
			return empty
		elapsed = playingTimes[0]
		if len(playingTimes) > 1:
			total = playingTimes[1]
		else:
			total = None
		return _StatusBarTimes(elapsed, total)

	def getElapsedAndTotalIfPlaying(self) -> _StatusBarTimes:
		elapsedAndTotalTime = self.getElapsedAndTotal()
		if elapsedAndTotalTime.elapsed is None and elapsedAndTotalTime.total is None:
			# Translators: Reported when no track is playing in Foobar 2000.
			ui.message(_("No track playing"))
		return elapsedAndTotalTime

	@script(
		# Translators: The description of an NVDA command for reading the remaining time of the currently playing
		# track in Foobar 2000.
		description=_("Reports the remaining time of the currently playing track, if any"),
		gesture="kb:control+shift+r",
		speakOnDemand=True,
	)
	def script_reportRemainingTime(self, gesture: "InputGesture"):
		elapsedTime, totalTime = self.getElapsedAndTotalIfPlaying()
		parsedElapsedTime = None
		parsedTotalTime = None
		if elapsedTime is not None and totalTime is not None:
			parsedElapsedTime = _parseTimeStrToTimeDelta(elapsedTime)
			parsedTotalTime = _parseTimeStrToTimeDelta(totalTime)

		if parsedElapsedTime is not None and parsedTotalTime is not None:
			remainingTime = parsedTotalTime - parsedElapsedTime
			remainingTimeFormatted = TimeOutputFormat.parseTimeDeltaToFormatted(remainingTime)
			# Translators: Reported remaining time in Foobar2000
			ui.message(_("{remainingTimeFormatted} remaining").format(remainingTimeFormatted=remainingTimeFormatted))
		else:
			# Translators: Reported if the remaining time can not be calculated in Foobar2000
			ui.message(_("Remaining time not available"))

	@script(
		# Translators: The description of an NVDA command for reading the elapsed time of the currently playing
		# track in Foobar 2000.
		description=_("Reports the elapsed time of the currently playing track, if any"),
		gesture="kb:control+shift+e",
		speakOnDemand=True,
	)
	def script_reportElapsedTime(self, gesture: "InputGesture"):
		elapsedTime = self.getElapsedAndTotalIfPlaying().elapsed
		if elapsedTime:
			elapsedTime = _parseTimeStrToOutputFormatted(elapsedTime)
		if elapsedTime is not None:
			# Translators: Reported elapsed time in Foobar2000
			ui.message(_("{elapsedTime} elapsed").format(elapsedTime=elapsedTime))
		else:
			# Translators: Reported if the elapsed time is not available in Foobar2000
			ui.message(_("Elapsed time not available"))

	@script(
		# Translators: The description of an NVDA command for reading the length of the currently playing track in
		# Foobar 2000.
		description=_("Reports the length of the currently playing track, if any"),
		gesture="kb:control+shift+t",
		speakOnDemand=True,
	)
	def script_reportTotalTime(self, gesture: "InputGesture"):
		totalTime = self.getElapsedAndTotalIfPlaying().total
		if totalTime:
			totalTime = _parseTimeStrToOutputFormatted(totalTime)
		if totalTime is not None:
			# Translators: Reported remaining time in Foobar2000
			ui.message(_("{totalTime} total").format(totalTime=totalTime))
		else:
			# Translators: Reported if the total time is not available in Foobar2000
			ui.message(_("Total time not available"))
