#NVDAObjects/IAccessible/sdm.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import IAccessibleHandler
import controlTypes
import winUser
import api
from . import IAccessible, getNVDAObjectFromEvent

class SDM(IAccessible):

	def _get_positionInfo(self):
		if self.role!=controlTypes.ROLE_LISTITEM:
			return {}
		return super(SDM,self).positionInfo

	def _get_parent(self):
		parent=super(SDM,self).parent
		if self.IAccessibleChildID>0 and self.role!=controlTypes.ROLE_LISTITEM:
			parent=parent.parent
		return parent

	def _get_SDMChild(self):
		if controlTypes.STATE_FOCUSED in self.states:
			hwndFocus=winUser.getGUIThreadInfo(0).hwndFocus
			if hwndFocus and hwndFocus!=self.windowHandle and not winUser.getClassName(hwndFocus).startswith('bosa_sdm'):
				obj=getNVDAObjectFromEvent(hwndFocus,winUser.OBJID_CLIENT,0)
				obj.parent=self.parent
				obj.name=self.name
				return obj
		return None

class MSOUNISTAT(IAccessible):

	def _get_role(self):
		return controlTypes.ROLE_STATICTEXT
 
