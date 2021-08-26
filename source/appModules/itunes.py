#appModules/itunes.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2018 NV Access Limited, Leonard de Ruijter

"""App module for iTunes
"""

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
import NVDAObjects.UIA
from NVDAObjects.IAccessible import webKit

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		if isinstance(obj,NVDAObjects.IAccessible.IAccessible):
			if obj.windowClassName=="WebViewWindowClass":
				if obj.IAccessibleRole==oleacc.ROLE_SYSTEM_WINDOW:
					#Disable a safety mechonism in our IAccessible support as in iTunes it causes an infinit ancestry.
					obj.parentUsesSuperOnWindowRootIAccessible=False
				else:
					obj.hasEncodedAccDescription=True
			elif obj.role==controlTypes.Role.BUTTON:
				# iTunes seems to put some controls inside a button.
				# Don't report this weirdness to the user.
				obj.isPresentableFocusAncestor=False
			elif obj.windowClassName=="iTunesWebViewControl" and obj.role==controlTypes.Role.DOCUMENT:
				# This wrapper should never be seen by the user.
				obj.shouldAllowIAccessibleFocusEvent = False
				obj.presentationType = obj.presType_layout

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj,NVDAObjects.UIA.UIA):
			# iTunes 12.9 implements UIA for many controls.
			# Just leave them untouched for now.
			return
		windowClassName=obj.windowClassName
		role=obj.role
		if windowClassName in ('iTunesList','iTunesSources','iTunesTrackList') and role in (controlTypes.Role.LISTITEM,controlTypes.Role.TREEVIEWITEM):
			clsList.insert(0, ITunesItem)
		elif webKit.Document in clsList:
			clsList.insert(0, WebKitDocument)
		elif windowClassName=="iTunes" and obj.IAccessibleRole==oleacc.ROLE_SYSTEM_CLIENT:
			clsList.insert(0, TopLevelClient)

class ITunesItem(NVDAObjects.IAccessible.IAccessible):
	"""Retreaves position information encoded in the accDescription"""

	hasEncodedAccDescription=True
	value = None

	def _get_next(self):
		next=super(ITunesItem,self).next
		if next:
			return next
		try:
			parentChildCount=self.IAccessibleObject.accChildCount
		except COMError:
			parentChildCount=0
		if self.IAccessibleChildID>0 and self.IAccessibleChildID<parentChildCount:
			return NVDAObjects.IAccessible.IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=self.IAccessibleChildID+1)
		return None

	def _get_previous(self):
		previous=super(ITunesItem,self).previous
		if not previous and self.IAccessibleChildID>1:
			previous=NVDAObjects.IAccessible.IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=self.IAccessibleChildID-1)
		return previous

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# These items can fire spurious focus events; e.g. when tabbing out of the Music list.
		# The list reports that it's focused even when it isn't.
		# Thankfully, the list items don't.
		return self.hasFocus

class WebKitDocument(webKit.Document):

	def event_stateChange(self):
		# iTunes has indicated that a page has died and been replaced by a new one.
		# #5191: This is actually fired on the "iTunesWebViewControl" parent,
		# but AccessibleObjectFromEvent on this window returns the WebKit document as of iTunes 12.
		focus = api.getFocusObject()
		if self.windowHandle != focus.windowHandle:
			return
		# The new page has the same event params, so we must bypass NVDA's IAccessible caching.
		obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(focus.windowHandle, winUser.OBJID_CLIENT, 0)
		if not obj:
			return
		if focus.treeInterceptor:
			speech.cancelSpeech()
			treeInterceptorHandler.killTreeInterceptor(focus.treeInterceptor)
		eventHandler.queueEvent("gainFocus",obj)

class TopLevelClient(NVDAObjects.IAccessible.IAccessible):

	def _isEqual(self, other):
		# The location seems to be reported differently depending on how you get to this object.
		# This causes the focus ancestry to change when it really hasn't,
		# which in turn causes spurious reporting.
		if self.IAccessibleIdentity == other.IAccessibleIdentity:
			return True
		return super(TopLevelClient, self)._isEqual(other)
