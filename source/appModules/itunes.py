import appModuleHandler
from comtypes import COMError
import controlTypes
import oleacc
import NVDAObjects.IAccessible

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		if isinstance(obj,NVDAObjects.IAccessible.IAccessible):
			obj.shouldAllowIAccessibleFocusEvent=True
			if obj.IAccessibleRole==oleacc.ROLE_SYSTEM_WINDOW and obj.windowClassName=="WebViewWindowClass":
				#Disable a safety mechonism in our IAccessible support as in iTunes it causes an infinit ancestry.
				obj.parentUsesSuperOnWindowRootIAccessible=False

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClassName=obj.windowClassName
		role=obj.role
		if windowClassName in ('iTunesSources','iTunesTrackList') and role in (controlTypes.ROLE_LISTITEM,controlTypes.ROLE_TREEVIEWITEM):
			clsList.insert(0, ITunesItem)

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
