import _default
import re
from comtypes import COMError
import controlTypes
import oleacc
import NVDAObjects.IAccessible

class AppModule(_default.AppModule):

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

	RE_POSITION_INFO = re.compile(r"L(?P<level>\d+), (?P<indexInGroup>\d+) of (?P<similarItemsInGroup>\d+)")

	# The description and value should not be user visible.
	description = None
	value = None

	def _get_positionInfo(self):
		# iTunes encodes the position info in the accDescription.
		try:
			desc = self.IAccessibleObject.accDescription(self.IAccessibleChildID)
		except COMError:
			return super(ITunesItem, self).positionInfo

		if desc:
			m = self.RE_POSITION_INFO.match(desc)
			if m:
				return m.groupdict()

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
