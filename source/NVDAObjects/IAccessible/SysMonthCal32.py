#NVDAObjects/IAccessible/SysMonthCal32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import controlTypes
from . import IAccessible

class SysMonthCal32(IAccessible):

	def _get_role(self):
		return controlTypes.Role.CALENDAR

	def _get_name(self):
		return ""

	def _get_value(self):
		return super(SysMonthCal32,self).name

	def script_valueChange(self,gesture):
		gesture.send()
		self.event_valueChange()

	__valueChangeGestures = (
		"kb:upArrow",
		"kb:downArrow",
		"kb:leftArrow",
		"kb:rightArrow",
		"kb:home",
		"kb:end",
		"kb:control+home",
		"kb:control+end",
		"kb:pageDown",
		"kb:pageUp",
	)

	def initOverlayClass(self):
		for gesture in self.__valueChangeGestures:
			self.bindGesture(gesture, "valueChange")
