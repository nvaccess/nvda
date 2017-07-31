#appModules/notepad++.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Notepad++
"""

import appModuleHandler
from NVDAObjects import NVDAObject

class NotepadPlusPlusScintillaEdit(NVDAObject):

	def initOverlayClass(self):
		pass

	def shouldAcceptShowHideCaretEvent(self):
		return False

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		pass

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		clsList.insert(0, NotepadPlusPlusScintillaEdit)
