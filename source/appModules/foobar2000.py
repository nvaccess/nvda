# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2020 NV Access Limited, Aleksey Sadovoy, James Teh, Joseph Lee, Tuukka Ojala,
# Bram Duvigneau
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import appModuleHandler
import calendar
import collections
import time
import api
import ui

# A named tuple for holding the elapsed and total playing times from Foobar2000's status bar
statusBarTimes = collections.namedtuple('StatusBarTimes', ['elapsed', 'total'])

def getParsingFormat(interval):
	"""Attempts to find a suitable parsing format string for a HH:MM:SS, MM:SS or SS -style time interval."""
	timeParts = len(interval.split(":"))
	if timeParts == 1:
		return "%S"
	elif timeParts == 2:
		return "%M:%S"
	elif timeParts == 3:
		return "%H:%M:%S"
	else:
		return None

def getOutputFormat(seconds):
	"""Returns a format string for the given number of seconds with the least leading zeros."""
	if seconds < 60:
		return "%S"
	elif seconds < 3600:
		return "%M:%S"
	else:
		return "%H:%M:%S"

def parseIntervalToTimestamp(interval):
	"""Parses a HH:MM:SS, MM:SS or SS -style interval to a timestamp."""
	format = getParsingFormat(interval)
	return calendar.timegm(time.strptime(interval.strip(), format))

class AppModule(appModuleHandler.AppModule):
	_statusBar = None

	def event_gainFocus(self, obj, nextHandler):
		if not self._statusBar:
			self._statusBar = api.getStatusBar()
		nextHandler()

	def getElapsedAndTotal(self):
		empty = statusBarTimes(None, None)
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
		return statusBarTimes(elapsed, total)

	def getElapsedAndTotalIfPlaying(self):
		elapsedAndTotalTime = self.getElapsedAndTotal()
		if elapsedAndTotalTime.elapsed is None and elapsedAndTotalTime.total is None:
			# Translators: Reported when no track is playing in Foobar 2000.
			ui.message(_("No track playing"))
		return elapsedAndTotalTime

	def script_reportRemainingTime(self,gesture):
		elapsedTime, totalTime = self.getElapsedAndTotalIfPlaying()
		if elapsedTime is None or totalTime is None:
			# Translators: Reported if the remaining time can not be calculated in Foobar2000
			msg = _("Unable to determine remaining time")
		else:
			parsedElapsedTime = parseIntervalToTimestamp(elapsedTime)
			parsedTotalTime = parseIntervalToTimestamp(totalTime)
			remainingTime = parsedTotalTime - parsedElapsedTime
			msg = time.strftime(getOutputFormat(remainingTime), time.gmtime(remainingTime))
		ui.message(msg)
	# Translators: The description of an NVDA command for reading the remaining time of the currently playing track in Foobar 2000.
	script_reportRemainingTime.__doc__ = _("Reports the remaining time of the currently playing track, if any")

	def script_reportElapsedTime(self,gesture):
		elapsedTime = self.getElapsedAndTotalIfPlaying()[0]
		if elapsedTime is not None:
			ui.message(elapsedTime)
	# Translators: The description of an NVDA command for reading the elapsed time of the currently playing track in Foobar 2000.
	script_reportElapsedTime.__doc__ = _("Reports the elapsed time of the currently playing track, if any")

	def script_reportTotalTime(self,gesture):
		totalTime = self.getElapsedAndTotalIfPlaying()[1]
		if totalTime is not None:
			ui.message(totalTime)
		else:
			# Translators: Reported if the total time is not available in Foobar2000
			ui.message(_("Total time not available"))
	# Translators: The description of an NVDA command for reading the length of the currently playing track in Foobar 2000.
	script_reportTotalTime.__doc__ = _("Reports the length of the currently playing track, if any")

	__gestures = {
		"kb:control+shift+r": "reportRemainingTime",
		"kb:control+shift+e": "reportElapsedTime",
		"kb:control+shift+t": "reportTotalTime",
	}
