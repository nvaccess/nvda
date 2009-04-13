#appModules/winword.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import comtypes.client
import comtypes.automation
import controlTypes
import textHandler
import winUser
import IAccessibleHandler
import NVDAObjects.IAccessible
import speech
import _default
from NVDAObjects.window.winword import WordDocument

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="_WwN" and obj.role==controlTypes.ROLE_EDITABLETEXT:
				self.overlayCustomNVDAObjectClass(obj,SpellCheckErrorField,outerMost=True)

class SpellCheckErrorField(WordDocument):

	def _get_WinwordDocumentObject(self):
		if not hasattr(self,'_WinwordDocumentObject'):
			try:
				self._WinwordDocumentObject=comtypes.client.dynamic.Dispatch(comtypes.client.GetActiveObject('word.application',interface=comtypes.automation.IDispatch)).activeWindow.activePane
			except:
				return None
		return self._WinwordDocumentObject

	def _get_name(self):
		return super(SpellCheckErrorField,self).description

	def _get_description(self):
		return ""

	def reportFocus(self):
		speech.speakObjectProperties(self,name=True,role=True)
		info=self.makeTextInfo(textHandler.POSITION_ALL)
		try:
			error=info._rangeObj.spellingErrors[0].text
		except:
			speech.speakTextInfo(info,speech.REASON_FOCUS)
		speech.speakText(error)
		speech.speakSpelling(error)
