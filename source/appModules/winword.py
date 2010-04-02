#appModules/winword.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import comtypes.client
import comtypes.automation
import controlTypes
import textInfos
import winUser
import speech
import _default
from NVDAObjects.window.winword import WordDocument

class AppModule(_default.AppModule):

	def findExtraNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName=="_WwN" and obj.role==controlTypes.ROLE_EDITABLETEXT:
			clsList.insert(0, SpellCheckErrorField)

class SpellCheckErrorField(WordDocument):

	def _get_WinwordWindowObject(self):
		if not hasattr(self,'_WinwordWindowObject'):
			try:
				self._WinwordWindowObject=comtypes.client.dynamic.Dispatch(comtypes.client.GetActiveObject('word.application',interface=comtypes.automation.IDispatch)).activeWindow.activePane
			except:
				return None
		return self._WinwordWindowObject

	def _get_name(self):
		return super(SpellCheckErrorField,self).description

	def _get_description(self):
		return ""

	def reportFocus(self):
		speech.speakObjectProperties(self,name=True,role=True)
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.move(textInfos.UNIT_WORD,-1,endPoint="start")
		try:
			error=info._rangeObj.spellingErrors[1].text
		except:
			info.expand(textInfos.UNIT_STORY)
			speech.speakText(info.text)
			return
		speech.speakText(error)
		speech.speakSpelling(error)
