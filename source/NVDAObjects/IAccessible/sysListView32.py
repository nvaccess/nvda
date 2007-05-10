#NVDAObjects/sysListView32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winUser
from . import IAccessible

class ListItem(IAccessible):

	def _get_positionString(self):
		totalCount=winUser.sendMessage(self.windowHandle,0x1004,0,0)
		return _("%s of %s")%(self.IAccessibleChildID,totalCount)
