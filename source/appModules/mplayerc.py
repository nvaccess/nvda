#appModules/mplayerc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _default
import controlTypes

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="#32770" and obj.windowControlID==10021:
			obj.role = controlTypes.ROLE_STATUSBAR
