#NVDAObjects/IAccessible/msOffice.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

import oleacc
import IAccessibleHandler
import controlTypes
import winUser
import api
from . import IAccessible, getNVDAObjectFromEvent

"""Miscellaneous support for Microsoft Office applications.
"""

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
 
class BrokenMsoCommandBar(IAccessible):
	"""Work around broken IAccessible implementation for Microsoft Office XP-2003 toolbars.
	For these IAccessibles, accNavigate is rather broken
	and retrieving only the first child with AccessibleChildren causes a crash.
	"""

	@classmethod
	def appliesTo(cls, obj):
		return obj.childCount > 0 and not IAccessibleHandler.accNavigate(obj.IAccessibleObject, obj.IAccessibleChildID, oleacc.NAVDIR_FIRSTCHILD)

	def _get_firstChild(self):
		# accNavigate incorrectly returns nothing for NAVDIR_FIRSTCHILD and requesting one child with AccessibleChildren causes a crash.
		# Therefore, we must use accChild(1).
		child = IAccessibleHandler.accChild(self.IAccessibleObject, 1)
		if not child:
			return None
		return IAccessible(IAccessibleObject=child[0], IAccessibleChildID=child[1])

	# accNavigate incorrectly returns the first child for NAVDIR_NEXT.
	next = None
	# description is redundant.
	description = None

	def _get_name(self):
		name = super(BrokenMsoCommandBar, self).name
		if name == "MSO Generic Control Container":
			return None
		return name
