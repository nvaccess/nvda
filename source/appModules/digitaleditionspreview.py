#appModules/digitaleditionspreview.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011 NV Access Inc

"""App module for Adobe Digital Editions
"""

import appModuleHandler
import controlTypes
from textInfos import DocumentWithPageTurns
from NVDAObjects.UIA import UIA
from keyboardHandler import KeyboardInputGesture

class BookContent(DocumentWithPageTurns, UIA):

	def turnPage(self, previous=False):
		KeyboardInputGesture.fromName("pageUp" if previous else "pageDown").send()

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_DOCUMENT:
			clsList.insert(0, BookContent)
