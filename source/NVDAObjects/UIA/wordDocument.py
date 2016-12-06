#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2016 NV Access Limited

import controlTypes
import textInfos
import eventHandler
import controlTypes
import speech
import api
from UIABrowseMode import UIABrowseModeDocument
from . import UIA, UIATextInfo

class WordDocumentTextInfo(UIATextInfo):

	# UIA text range comparison for bookmarks works okay in this MS Word implementation
	# Thus __ne__ is useful
	def __ne__(self,other):
		return not self==other

	def _getControlFieldForObject(self,obj,isEmbedded=False,startOfNode=False,endOfNode=False):
		# Ignore strange editable text fields surrounding most inner fields (links, table cells etc) 
		automationID=obj.UIAElement.cachedAutomationID
		if obj.role==controlTypes.ROLE_EDITABLETEXT and (automationID=='Body' or automationID.startswith('UIA_AutomationId_Word_Content')):
			return None
		field=super(WordDocumentTextInfo,self)._getControlFieldForObject(obj,isEmbedded=isEmbedded,startOfNode=startOfNode,endOfNode=endOfNode)
		if obj.role==controlTypes.ROLE_GRAPHIC:
			# Label graphics with a description before name as name seems to be auto-generated (E.g. "rectangle")
			field['value']=field.pop('description',None) or obj.description or field.pop('name',None) or obj.name
		return field

	def _getTextFromUIARange(self,range):
		t=super(WordDocumentTextInfo,self)._getTextFromUIARange(range)
		if t:
			# HTML emails expose a lot of vertical tab chars in their text
			# Really better as carage returns
			t=t.replace('\v','\r')
			# Remove end-of-row markers from the text - they are not useful
			t=t.replace('\x07','')
		return t

	def _isEndOfRow(self):
		""" Is this textInfo positioned on an end-of-row mark? """
		info=self.copy()
		info.expand(textInfos.UNIT_CHARACTER)
		return info._rangeObj.getText(-1)==u'\u0007'

	def move(self,unit,direction,endPoint=None):
		if endPoint is None:
			res=super(WordDocumentTextInfo,self).move(unit,direction)
			if res==0:
				return 0
			# Skip over end of Row marks
			while self._isEndOfRow():
				if self.move(unit,1 if direction>0 else -1)==0:
					break
			return res
		return super(WordDocumentTextInfo,self).move(unit,direction,endPoint)

	def _get_isCollapsed(self):
		res=super(WordDocumentTextInfo,self).isCollapsed
		if res: 
			return True
		# MS Word does not seem to be able to fully collapse ranges when on links and tables etc.
		# Therefore class a range as collapsed if it has no text
		return not bool(self.text)

	def getTextWithFields(self,formatConfig=None):
		fields=super(WordDocumentTextInfo,self).getTextWithFields(formatConfig=formatConfig)
		# MS Word can sometimes return a higher ancestor in its textRange's children.
		# E.g. a table inside a table header.
		# This does not cause a loop, but does cause information to be doubled
		# Detect these duplicates and remove them from the generated fields.
		seenStarts=set()
		pendingRemoves=[]
		index=0
		for index,field in enumerate(fields):
			if isinstance(field,textInfos.FieldCommand) and field.command=="controlStart":
				runtimeID=field.field['runtimeID']
				if runtimeID in seenStarts:
					pendingRemoves.append(field.field)
				else:
					seenStarts.add(runtimeID)
			elif seenStarts:
				seenStarts.clear()
		index=0
		while index<len(fields):
			field=fields[index]
			if isinstance(field,textInfos.FieldCommand) and any(x is field.field for x in pendingRemoves):
				del fields[index]
			else:
				index+=1
		return fields

class WordBrowseModeDocument(UIABrowseModeDocument):

	def shouldSetFocusToObj(self,obj):
		# Ignore strange editable text fields surrounding most inner fields (links, table cells etc) 
		if obj.role==controlTypes.ROLE_EDITABLETEXT and obj.UIAElement.cachedAutomationID.startswith('UIA_AutomationId_Word_Content'):
			return False
		return super(WordBrowseModeDocument,self).shouldSetFocusToObj(obj)

	def shouldPassThrough(self,obj,reason=None):
		# Ignore strange editable text fields surrounding most inner fields (links, table cells etc) 
		if obj.role==controlTypes.ROLE_EDITABLETEXT and obj.UIAElement.cachedAutomationID.startswith('UIA_AutomationId_Word_Content'):
			return False
		return super(WordBrowseModeDocument,self).shouldPassThrough(obj,reason=reason)

	def script_tab(self,gesture):
		oldBookmark=self.rootNVDAObject.makeTextInfo(textInfos.POSITION_SELECTION).bookmark
		gesture.send()
		noTimeout,newInfo=self.rootNVDAObject._hasCaretMoved(oldBookmark,timeout=1)
		if not newInfo:
			return
		info=self.makeTextInfo(textInfos.POSITION_SELECTION)
		if not info.isCollapsed:
			speech.speakTextInfo(info,reason=controlTypes.REASON_FOCUS)
	script_shiftTab=script_tab

class WordDocumentNode(UIA):
	TextInfo=WordDocumentTextInfo

class WordDocument(WordDocumentNode):
	treeInterceptorClass=WordBrowseModeDocument
	shouldCreateTreeInterceptor=False
