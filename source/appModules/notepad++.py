#appModules/notepad++.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Notepad++
"""

import oleacc
import appModuleHandler
from NVDAObjects import NVDAObject, IAccessible

class NotepadPlusPlusScintillaEdit(NVDAObject):

	shouldAcceptShowHideCaretEvent = False

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		isIAccessible = isinstance(obj, IAccessible.IAccessible)
		if isIAccessible and obj.windowClassName == "Scintilla" and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT:
			clsList.insert(0, NotepadPlusPlusScintillaEdit)

