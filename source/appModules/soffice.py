#appModules/soffice.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

import _default
import controlTypes
from compoundDocuments import CompoundDocument

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self, obj):
		if (obj.windowClassName == "SALTMPSUBFRAME" and obj.role == controlTypes.ROLE_DOCUMENT) or (obj.windowClassName == "SALFRAME" and obj.role == controlTypes.ROLE_CANVAS):
			obj.description = None
			obj.treeInterceptorClass = CompoundDocument
