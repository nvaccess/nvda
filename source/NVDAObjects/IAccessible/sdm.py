#NVDAObjects/IAccessible/sdm.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import IAccessibleHandler
import controlTypes
import api
from . import IAccessible

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

class RichEditSDMChild(IAccessible):

	def _get_parent(self):
		parent=super(RichEditSDMChild,self).parent
		return parent.parent

	def _get_name(self):
		left,top,width,height=self.location
		obj=api.getDesktopObject().objectFromPoint(left+(width/2),top+(height/2))
		if obj:
			return obj.name

