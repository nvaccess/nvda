#NVDAObjects/IAccessible/SysMonthCal32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from keyUtils import sendKey
import controlTypes
from . import IAccessible

class SysMonthCal32(IAccessible):

	def _get_role(self):
		return controlTypes.ROLE_CALENDAR

	def _get_name(self):
		return ""

	def _get_value(self):
		return super(SysMonthCal32,self).name

	def script_valueChange(self,keyPress):
		sendKey(keyPress)
		self.event_valueChange()

[SysMonthCal32.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","valueChange"),
	("ExtendedDown","valueChange"),
	("ExtendedLeft","valueChange"),
	("ExtendedRight","valueChange"),
	("extendedHome","valueChange"),
	("extendedEnd","valueChange"),
	("control+extendedHome","valueChange"),
	("control+extendedEnd","valueChange"),
	("extendedNext","valueChange"),
	("extendedPrior","valueChange"),
	]
]

