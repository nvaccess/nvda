import appModuleHandler
from comtypes import COMError
import controlTypes
import oleacc
import winUser
import speech
import treeInterceptorHandler
import api
import eventHandler
import NVDAObjects.IAccessible

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		if isinstance(obj,NVDAObjects.IAccessible.IAccessible) and not isinstance(obj,WebKitWrapper):
			obj.shouldAllowIAccessibleFocusEvent=True
			if obj.windowClassName=="WebViewWindowClass":
				if obj.IAccessibleRole==oleacc.ROLE_SYSTEM_WINDOW:
					#Disable a safety mechonism in our IAccessible support as in iTunes it causes an infinit ancestry.
					obj.parentUsesSuperOnWindowRootIAccessible=False
				else:
					obj.hasEncodedAccDescription=True

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClassName=obj.windowClassName
		role=obj.role
		if windowClassName in ('iTunesList','iTunesSources','iTunesTrackList') and role in (controlTypes.ROLE_LISTITEM,controlTypes.ROLE_TREEVIEWITEM):
			clsList.insert(0, ITunesItem)
		elif windowClassName=="iTunesWebViewControl" and role==controlTypes.ROLE_DOCUMENT:
			clsList.insert(0,WebKitWrapper)

class ITunesItem(NVDAObjects.IAccessible.IAccessible):
	"""Retreaves position information encoded in the accDescription"""

	hasEncodedAccDescription=True
	value = None

	def _get_next(self):
		next=super(ITunesItem,self).next
		try:
			parentChildCount=self.IAccessibleObject.accParent.accChildCount
		except COMError:
			parentChildCount=0
		if not next and self.IAccessibleChildID>0 and self.IAccessibleChildID<parentChildCount:
			next=NVDAObjects.IAccessible.IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=self.IAccessibleChildID+1)
		return next

	def _get_previous(self):
		previous=super(ITunesItem,self).previous
		if not previous and self.IAccessibleChildID>1:
			previous=NVDAObjects.IAccessible.IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=self.IAccessibleChildID-1)
		return previous

class WebKitWrapper(NVDAObjects.IAccessible.IAccessible):
	"""An iTunes wrapper around a WebKit document.
	"""
	# This wrapper should never be seen by the user.
	shouldAllowIAccessibleFocusEvent = False
	presentationType = NVDAObjects.IAccessible.IAccessible.presType_layout

	def event_stateChange(self):
		from logHandler import log
		# iTunes has indicated that a page has died and been replaced by a new one.
		focus = api.getFocusObject()
		if not winUser.isDescendantWindow(self.windowHandle, focus.windowHandle):
			return
		# The new page has the same event params, so we must bypass NVDA's IAccessible caching.
		obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(focus.windowHandle, winUser.OBJID_CLIENT, 0)
		if not obj:
			return
		if focus.treeInterceptor:
			speech.cancelSpeech()
			treeInterceptorHandler.killTreeInterceptor(focus.treeInterceptor)
		eventHandler.queueEvent("gainFocus",obj)
