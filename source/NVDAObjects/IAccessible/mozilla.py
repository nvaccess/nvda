#NVDAObjects/IAccessible/mozilla.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

import IAccessibleHandler
import oleacc
import winUser
from comtypes import IServiceProvider, COMError
import eventHandler
import controlTypes
from . import IAccessible, Dialog
from logHandler import log

class Mozilla(IAccessible):

	IAccessibleTableUsesTableCellIndexAttrib=True

	def _get_beTransparentToMouse(self):
		if not hasattr(self,'IAccessibleTextObject') and self.role==controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_READONLY in self.states:
			return True
		return super(Mozilla,self).beTransparentToMouse

	def _get_parent(self):
		#Special code to support Mozilla node_child_of relation (for comboboxes)
		res=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVRELATION_NODE_CHILD_OF)
		if res and res!=(self.IAccessibleObject,self.IAccessibleChildID):
			newObj=IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
			if newObj:
				return newObj
		return super(Mozilla,self).parent

	def _get_states(self):
		states = super(Mozilla, self).states
		if self.IAccessibleStates & oleacc.STATE_SYSTEM_MARQUEED:
			states.add(controlTypes.STATE_CHECKABLE)
		return states

class Gecko1_9(Mozilla):

	def _get_description(self):
		rawDescription=super(Mozilla,self).description
		if isinstance(rawDescription,basestring) and rawDescription.startswith('Description: '):
			return rawDescription[13:]
		else:
			return ""

	def event_scrollingStart(self):
		#Firefox 3.6 fires scrollingStart on leaf nodes which is not useful to us.
		#Bounce the event up to the node's parent so that any possible virtualBuffers will detect it.
		if self.role==controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_READONLY in self.states:
			eventHandler.queueEvent("scrollingStart",self.parent)

class BrokenFocusedState(Mozilla):
	shouldAllowIAccessibleFocusEvent=True

class RootApplication(Mozilla):
	"""Mozilla exposes a root application accessible as the parent of all top level frames.
	See MozillaBug:555861.
	This is non-standard; the top level accessible should be the top level window.
	NVDA expects the standard behaviour, so we never want to see this object.
	"""

	def __nonzero__(self):
		# As far as NVDA is concerned, this is a useless object.
		return False

class Document(Mozilla):

	value=None

	def _get_treeInterceptorClass(self):
		states=self.states
		ver=_getGeckoVersion(self)
		if (not ver or ver.startswith('1.9')) and self.windowClassName!="MozillaContentWindowClass":
			return super(Document,self).treeInterceptorClass
		if controlTypes.STATE_READONLY in states:
			import virtualBuffers.gecko_ia2
			return virtualBuffers.gecko_ia2.Gecko_ia2
		return super(Document,self).treeInterceptorClass

class ListItem(Mozilla):

	def _get_name(self):
		name=super(ListItem,self)._get_name()
		if self.IAccessibleStates&oleacc.STATE_SYSTEM_READONLY:
			children=super(ListItem,self)._get_children()
			if len(children)>0 and (children[0].IAccessibleRole in ["bullet",oleacc.ROLE_SYSTEM_STATICTEXT]):
				name=children[0].value
		return name

	def _get_children(self):
		children=super(ListItem,self)._get_children()
		if self.IAccessibleStates&oleacc.STATE_SYSTEM_READONLY and len(children)>0 and (children[0].IAccessibleRole in ("bullet",oleacc.ROLE_SYSTEM_STATICTEXT)):
			del children[0]
		return children

class EmbeddedObject(Mozilla):

	def _get_shouldAllowIAccessibleFocusEvent(self):
		focusWindow = winUser.getGUIThreadInfo(self.windowThreadID).hwndFocus
		if self.windowHandle != focusWindow:
			# This window doesn't have the focus, which means the embedded object's window probably already has the focus.
			# We don't want to override the focus event fired by the embedded object.
			return False
		return super(EmbeddedObject, self).shouldAllowIAccessibleFocusEvent

def _getGeckoVersion(obj):
	appMod = obj.appModule
	try:
		return appMod._geckoVersion
	except AttributeError:
		pass
	try:
		ver = obj.IAccessibleObject.QueryInterface(IServiceProvider).QueryService(IAccessibleHandler.IAccessibleApplication._iid_, IAccessibleHandler.IAccessibleApplication).toolkitVersion
	except COMError:
		return None
	appMod._geckoVersion = ver
	return ver

class GeckoPluginWindowRoot(IAccessible):

	def _get_parent(self):
		parent=super(GeckoPluginWindowRoot,self).parent
		ver=_getGeckoVersion(parent)
		if ver and not ver.startswith('1.'):
			res=IAccessibleHandler.accNavigate(parent.IAccessibleObject,0,IAccessibleHandler.NAVRELATION_EMBEDS)
			if res:
				obj=IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
				if obj and controlTypes.STATE_OFFSCREEN not in obj.states:
					return obj
		return parent

 
def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class if this is a Mozilla object.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	if not isinstance(obj.IAccessibleObject, IAccessibleHandler.IAccessible2):
		# We require IAccessible2; i.e. Gecko >= 1.9.
		return

	iaRole = obj.IAccessibleRole
	cls = None
	if iaRole == oleacc.ROLE_SYSTEM_APPLICATION:
		try:
			if not obj.IAccessibleObject.windowHandle:
				cls = RootApplication
		except COMError:
			pass
	if not cls:
		cls = _IAccessibleRolesToOverlayClasses.get(iaRole)
	if cls:
		clsList.append(cls)
	if iaRole in _IAccessibleRolesWithBrokenFocusedState:
		clsList.append(BrokenFocusedState)

	ver = _getGeckoVersion(obj)
	if ver and ver.startswith("1.9"):
		clsList.append(Gecko1_9)

	clsList.append(Mozilla)

#: Maps IAccessible roles to NVDAObject overlay classes.
_IAccessibleRolesToOverlayClasses = {
	oleacc.ROLE_SYSTEM_ALERT: Dialog,
	oleacc.ROLE_SYSTEM_LISTITEM: ListItem,
	oleacc.ROLE_SYSTEM_DOCUMENT: Document,
	IAccessibleHandler.IA2_ROLE_EMBEDDED_OBJECT: EmbeddedObject,
	"embed": EmbeddedObject,
	"object": EmbeddedObject,
}

#: Roles that mightn't set the focused state when they are focused.
_IAccessibleRolesWithBrokenFocusedState = frozenset((
	oleacc.ROLE_SYSTEM_COMBOBOX,
	oleacc.ROLE_SYSTEM_LIST,
	oleacc.ROLE_SYSTEM_LISTITEM,
	oleacc.ROLE_SYSTEM_DOCUMENT,
	oleacc.ROLE_SYSTEM_APPLICATION,
	oleacc.ROLE_SYSTEM_TABLE,
	oleacc.ROLE_SYSTEM_OUTLINE,
))
