#appModules/digitaleditions.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011-2012 NV Access Limited

"""App module for Adobe Digital Editions
"""

import appModuleHandler
import controlTypes
from textInfos import DocumentWithPageTurns
from NVDAObjects.UIA import UIA, UIATextInfo
from keyboardHandler import KeyboardInputGesture
import UIAHandler

class BookContentTextInfo(UIATextInfo):
	# #5264: Adobe Digital editions classes ranges expanded to character as degenerate.
	# Therefore we must force UIATextInfo to still fetch formatting and text for these ranges.
	allowGetFormatFieldsAndTextOnDegenerateUIARanges=True

class BookContent(DocumentWithPageTurns, UIA):

	def _get_TextInfo(self):
		TextInfo=super(BookContent,self).TextInfo
		if TextInfo is UIATextInfo:
			TextInfo=BookContentTextInfo
		return TextInfo

	def turnPage(self, previous=False):
		try:
			# Find the slider which indicates the current position.
			posSlider = self.parent.parent.next.lastChild
		except AttributeError:
			raise RuntimeError
		# We need the raw value, not the percentage.
		oldPos = posSlider.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_RangeValueValuePropertyId, True)
		KeyboardInputGesture.fromName("pageUp" if previous else "pageDown").send()
		if posSlider.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_RangeValueValuePropertyId, True) == oldPos:
			# No more pages.
			raise RuntimeError

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, UIA) and obj.role == controlTypes.Role.DOCUMENT:
			clsList.insert(0, BookContent)
