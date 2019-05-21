#NVDAObjects/UIA/ConsoleUIA.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2019 Bill Dengler

import textInfos
import UIAHandler

from winVersion import winVersion
from . import UIATextInfo
from ..behaviors import Terminal


class consoleUIATextInfo(UIATextInfo):
	def __init__(self,obj,position,_rangeObj=None):
		super(consoleUIATextInfo, self).__init__(obj,position,_rangeObj)
		if position==textInfos.POSITION_CARET:
			if winVersion.build >= 18362: #Windows 10 version 1903
				# The UIA implementation in 1903 causes the caret to be off-by-one, so move it one position to the right to compensate.
				self._rangeObj.MoveEndpointByUnit(UIAHandler.TextPatternRangeEndpoint_Start,UIAHandler.NVDAUnitsToUIAUnits['character'],1)


class consoleUIA(Terminal):
	_TextInfo=consoleUIATextInfo
	def event_textChanged(self):
		# fire textChange for liveText
		#Todo: this is probably a good place to filter out extraneous events from user input
		self.event_textChange()
	def _getTextLines(self):
		# Filter out extraneous empty lines from UIA
		#Todo: do this (also) somewhere else so they aren't in document review either
		return self.makeTextInfo(textInfos.POSITION_ALL).text.strip().split("\r\n")