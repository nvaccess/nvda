# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2024 NV Access Limited, Leonard de Ruijter, Cary-Rowen
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Visual Studio Code."""

import appModuleHandler
import controlTypes
from NVDAObjects.IAccessible.ia2Web import Editor
from NVDAObjects.IAccessible.chromium import Document
from NVDAObjects.IAccessible.ia2TextMozilla import MozillaCompoundTextInfo
from NVDAObjects import NVDAObject, NVDAObjectTextInfo


class VSCodeEditorTextInfo(MozillaCompoundTextInfo):
	def _isCaretAtEndOfLine(self, caretObj) -> bool:
		# #17039: IAccessibleText::textAtOffset with IA2_OFFSET_CARET is way too costly in VSCode.
		# And doesn't actually work correctly in Chromium yet anyway.
		# So it is best not to try detecting for now.
		return False


class VSCodeEditor(Editor):
	TextInfo = VSCodeEditorTextInfo


class VSCodeDocument(Document):
	"""The only content in the root document node of Visual Studio code is the application object.
	Creating a tree interceptor on this object causes a major slow down of Code.
	Therefore, forcefully block tree interceptor creation.
	"""

	textInfo = VSCodeEditorTextInfo

	_get_treeInterceptorClass = NVDAObject._get_treeInterceptorClass


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if Document in clsList and obj.IA2Attributes.get("tag") == "#document":
			clsList.insert(0, VSCodeDocument)
		elif Editor in clsList:
			clsList.insert(0, VSCodeEditor)

	def event_NVDAObject_init(self, obj: NVDAObject):
		# This is a specific fix for Visual Studio Code,
		# However, the root cause of the issue is issue #15159.
		# Once issue #15159 is fixed,
		# The PR #16248 that introduced this code can be immediately reverted.
		# (see issue #15159 for full description)
		if obj.role != controlTypes.Role.EDITABLETEXT:
			obj.TextInfo = NVDAObjectTextInfo
