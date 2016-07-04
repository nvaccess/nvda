#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import appModuleHandler
import speech
import sayAllHandler
import eventHandler
import api
from scriptHandler import willSayAllResume, isScriptWaiting
import controlTypes
import treeInterceptorHandler
import IAccessibleHandler
from cursorManager import ReviewCursorManager
from browseMode import BrowseModeDocumentTreeInterceptor
import textInfos
from textInfos import DocumentWithPageTurns
from NVDAObjects.IAccessible import IAccessible, IA2TextTextInfo, getNVDAObjectFromEvent

class BookPageViewTreeInterceptor(DocumentWithPageTurns,ReviewCursorManager,BrowseModeDocumentTreeInterceptor):

	TextInfo=treeInterceptorHandler.RootProxyTextInfo

	def turnPage(self,previous=False):
		return self.rootNVDAObject.turnPage(previous=previous)

	def isAlive(self):
		if not winUser.isWindow(self.rootNVDAObject.windowHandle):
			return False
		return True

	def __contains__(self,obj):
		return obj==self.rootNVDAObject

	def _changePageScriptHelper(self,gesture,previous=False):
		if isScriptWaiting():
			return
		try:
			self.turnPage(previous=previous)
		except RuntimeError:
			return
		info=self.makeTextInfo(textInfos.POSITION_FIRST)
		self.selection=info
		info.expand(textInfos.UNIT_LINE)
		if not willSayAllResume(gesture): speech.speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)

	def script_moveByPage_forward(self,gesture):
		self._changePageScriptHelper(gesture)
	script_moveByPage_forward.resumeSayAllMode=sayAllHandler.CURSOR_CARET

	def script_moveByPage_back(self,gesture):
		self._changePageScriptHelper(gesture,previous=True)
	script_moveByPage_back.resumeSayAllMode=sayAllHandler.CURSOR_CARET

	def _tabOverride(self,direction):
		return False

class BookPageViewTextInfo(IA2TextTextInfo):

	def _get_locationText(self):
		curLocation=self.obj.IA2Attributes.get('kindle-first-visible-location-number')
		maxLocation=self.obj.IA2Attributes.get('kindle-max-location-number')
		pageNumber=self.obj.pageNumber
		# Translators: A position in a Kindle book
		# xgettext:no-python-format
		text=_("{bookPercentage}%, location {curLocation} of {maxLocation}").format(bookPercentage=int((float(curLocation)/float(maxLocation))*100),curLocation=curLocation,maxLocation=maxLocation)
		if pageNumber:
			# Translators: a page in a Kindle book
			text+=", "+_("Page {pageNumber}").format(pageNumber=pageNumber)
		return text

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		formatField,offsets=super(BookPageViewTextInfo,self)._getFormatFieldAndOffsets(offset,formatConfig,calculateOffsets=calculateOffsets)
		if formatConfig['reportPage']:
			formatField['page-number']=self.obj.pageNumber
		return formatField,offsets

class BookPageView(DocumentWithPageTurns,IAccessible):
	"""Allows navigating page text content with the arrow keys."""

	treeInterceptorClass=BookPageViewTreeInterceptor
	TextInfo=BookPageViewTextInfo
	shouldAllowIAccessibleFocusEvent=True

	def _get_pageNumber(self):
		try:
			first=self.IA2Attributes['kindle-first-visible-physical-page-label']
			last=self.IA2Attributes['kindle-last-visible-physical-page-label']
		except KeyError:
			try:
				first=self.IA2Attributes['kindle-first-visible-physical-page-number']
				last=self.IA2Attributes['kindle-last-visible-physical-page-number']
			except KeyError:
				return None
		if first!=last:
			return "%s to %s"%(first,last)
		else:
			return first

	def turnPage(self,previous=False):
		try:
			self.IAccessibleActionObject.doAction(1 if previous else 0)
		except COMError:
			raise RuntimeError("no more pages")
		startTime=curTime=time.time()
		while (curTime-startTime)<0.5:
			api.processPendingEvents(processEventQueue=False)
			# should  only check for pending pageChange for this object specifically, but object equality seems to fail sometimes?
			if eventHandler.isPendingEvents("pageChange"):
				self.invalidateCache()
				break
			time.sleep(0.05)
			curTime=time.time()
		else:
			raise RuntimeError("no more pages")

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj,IAccessible) and hasattr(obj,'IAccessibleTextObject') and obj.name=="Book Page View":
			clsList.insert(0,BookPageView)
		return clsList
