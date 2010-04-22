#appModules/soffice.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

import _default
import controlTypes
from compoundDocuments import CompoundDocument
from NVDAObjects.JAB import JAB

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self, obj):
		windowClass = obj.windowClassName
		if isinstance(obj, JAB) and windowClass == "SALFRAME":
			# OpenOffice.org has some strange role mappings due to its use of JAB.
			if obj.role == controlTypes.ROLE_CANVAS:
				obj.role = controlTypes.ROLE_DOCUMENT
			elif obj.role == controlTypes.ROLE_LABEL:
				parent = obj.parent
				if parent and parent.role == controlTypes.ROLE_TABLE:
					obj.role = controlTypes.ROLE_TABLECELL

		if windowClass in ("SALTMPSUBFRAME", "SALFRAME") and obj.role == controlTypes.ROLE_DOCUMENT and obj.description:
			# This is a word processor document.
			obj.description = None
			obj.treeInterceptorClass = CompoundDocument
