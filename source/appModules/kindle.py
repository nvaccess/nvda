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
from cursorManager import ReviewCursorManager
from browseMode import BrowseModeDocumentTreeInterceptor
import textInfos
from textInfos import DocumentWithPageTurns
from NVDAObjects.IAccessible import IAccessible, IA2TextTextInfo
from globalCommands import SCRCAT_SYSTEMCARET

class BookPageViewTreeInterceptor(DocumentWithPageTurns,ReviewCursorManager,BrowseModeDocumentTreeInterceptor):

	TextInfo=treeInterceptorHandler.RootProxyTextInfo

	def turnPage(self,previous=False):
		# When in a page turn, Kindle  fires focus on the new page in the table of contents treeview.
		# We must ignore this focus event as it is a hinderance to a screen reader user while reading the book.
		try:
			self.rootNVDAObject.appModule.inPageTurn=True
			return self.rootNVDAObject.turnPage(previous=previous)
		finally:
			self.rootNVDAObject.appModule.inPageTurn=False

	def isAlive(self):
		return winUser.isWindow(self.rootNVDAObject.windowHandle)

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

	def script_finalizeSelection(self, gesture):
		fakeSel = self.makeTextInfo(textInfos.POSITION_SELECTION)
		if fakeSel.isCollapsed:
			# Translators: Reported when there is no text selection.
			ui.message(_("No selection"))
			return
		# Update the selection in Kindle.
		fakeSel.innerTextInfo.updateSelection()
		# The selection might have been adjusted to meet word boundaries, so update our fake selection.
		# we can't just use self.makeTextInfo, as that will use our fake selection.
		realSel = self.rootNVDAObject.makeTextInfo(textInfos.POSITION_SELECTION)
		fakeSel.innerTextInfo = realSel
		self.selection = fakeSel
		# Translators: Announces selected text. %s is replaced with the text.
		speech.speakSelectionMessage(_("selected %s"), fakeSel.text)
	# Translators: Describes a command.
	script_finalizeSelection.__doc__ = _("Finalizes selection of text and presents a menu from which you can choose what to do with the selection")
	script_finalizeSelection.category = SCRCAT_SYSTEMCARET

	__gestures = {
		"kb:control+c": "finalizeSelection",
		"kb:applications": "finalizeSelection",
		"kb:shift+f10": "finalizeSelection",
	}

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

class PageTurnFocusIgnorer(IAccessible):

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# When in a page turn, Kindle  fires focus on the new page in the table of contents treeview.
		# We must ignore this focus event as it is a hinderance to a screen reader user while reading the book.
		if self.appModule.inPageTurn:
			return False
		return super(PageTurnFocusIgnorer,self).shouldAllowIAccessibleFocusEvent

class AppModule(appModuleHandler.AppModule):

	inPageTurn=False

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj,IAccessible):
			clsList.insert(0,PageTurnFocusIgnorer)
			if hasattr(obj,'IAccessibleTextObject') and obj.name=="Book Page View":
				clsList.insert(0,BookPageView)
		return clsList
