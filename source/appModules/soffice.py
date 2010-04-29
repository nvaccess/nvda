#appModules/soffice.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

import _default
import controlTypes
from compoundDocuments import CompoundDocument
from NVDAObjects.JAB import JAB
from NVDAObjects.IAccessible import IAccessible, IA2TextTextInfo
from NVDAObjects.behaviors import EditableText

class SymphonyTextInfo(IA2TextTextInfo):
	pass

class SymphonyText(IAccessible, EditableText):
	TextInfo = SymphonyTextInfo

	def _get_positionInfo(self):
		level = self.IA2Attributes.get("heading-level")
		if level:
			return {"level": int(level)}
		return super(SymphonyText, self).positionInfo

class AppModule(_default.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, IAccessible) and obj.windowClassName == "SALTMPSUBFRAME" and hasattr(obj, "IAccessibleTextObject"):
			clsList.insert(0, SymphonyText)

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
