# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2018 NV Access Limited, Aleksey Sadovoy, James Teh, Joseph Lee, Tuukka Ojala
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.htmlimport appModuleHandler

import calendar
import time

import api
import appModuleHandler
import ui

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
	statusBar=None

	def event_gainFocus(self, obj, nextHandler):
		if not self.statusBar: self.statusBar=api.getStatusBar()
		nextHandler()

	def getElapsedAndTotal(self):
		if not self.statusBar: return None
		statusBarContents = self.statusBar.firstChild.name
		try:
			playingTimes = statusBarContents.split("|")[4].split("/")
			return playingTimes[0], playingTimes[1]
		except IndexError:
			return None

	def getElapsedAndTotalIfPlaying(self):
		times = self.getElapsedAndTotal()
		if not times:
			# Translators: Reported when no track is playing in Foobar 2000.
			ui.message(_("No track playing"))
		return times

	def script_reportRemainingTime(self,gesture):
		elapsedTime, totalTime = self.getElapsedAndTotalIfPlaying()
		if elapsedTime is not None and totalTime is not None:
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
	# Translators: The description of an NVDA command for reading the length of the currently playing track in Foobar 2000.
	script_reportTotalTime.__doc__ = _("Reports the length of the currently playing track, if any")

	__gestures = {
		"kb:control+shift+r": "reportRemainingTime",
		"kb:control+shift+e": "reportElapsedTime",
		"kb:control+shift+t": "reportTotalTime",
	}
