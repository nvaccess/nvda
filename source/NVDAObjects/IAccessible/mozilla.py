# -*- coding: UTF-8 -*-
#NVDAObjects/IAccessible/mozilla.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2017 NV Access Limited, Peter Vágner

from collections import namedtuple
import IAccessibleHandler
import oleacc
import winUser
from comtypes import IServiceProvider, COMError
import eventHandler
import controlTypes
from . import IAccessible, Dialog, WindowRoot
from logHandler import log
import textInfos.offsets
from NVDAObjects.behaviors import RowWithFakeNavigation
from virtualBuffers import VirtualBuffer
from . import IA2TextTextInfo
from . import ia2Web

class Mozilla(ia2Web.Ia2Web):

	def _get_states(self):
		states = super(Mozilla, self).states
		if self.IAccessibleStates & oleacc.STATE_SYSTEM_MARQUEED:
			states.add(controlTypes.STATE_CHECKABLE)
		return states

	def _get_presentationType(self):
		presType=super(Mozilla,self).presentationType
		if presType==self.presType_content:
			if self.role==controlTypes.ROLE_TABLE and self.IA2Attributes.get('layout-guess')=='true':
				presType=self.presType_layout
			elif self.table and self.table.presentationType==self.presType_layout:
				presType=self.presType_layout
		return presType

class Gecko1_9(Mozilla):

	def _get_description(self):
		rawDescription=super(Mozilla,self).description
		if isinstance(rawDescription,str) and rawDescription.startswith('Description: '):
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

class Document(ia2Web.Document):

	def _get_parent(self):
		res = IAccessibleHandler.accParent(
			self.IAccessibleObject, self.IAccessibleChildID
		)
		if not res:
			# accParent is broken in Firefox for same-process iframe documents.
			# Use NODE_CHILD_OF instead.
			res = IAccessibleHandler.accNavigate(
				self.IAccessibleObject, self.IAccessibleChildID,
				IAccessibleHandler.NAVRELATION_NODE_CHILD_OF
			)
		if not res:
			return None
		return IAccessible(IAccessibleObject=res[0], IAccessibleChildID=res[1])

	def _get_treeInterceptorClass(self):
		ver=getGeckoVersion(self)
		if (not ver or ver.full.startswith('1.9')) and self.windowClassName!="MozillaContentWindowClass":
			return super(Document,self).treeInterceptorClass
		if controlTypes.STATE_EDITABLE not in self.states:
			import virtualBuffers.gecko_ia2
			if ver and ver.major < 14:
				return virtualBuffers.gecko_ia2.Gecko_ia2Pre14
			else:
				return virtualBuffers.gecko_ia2.Gecko_ia2
		return super(Document,self).treeInterceptorClass

class EmbeddedObject(Mozilla):

	def _get_shouldAllowIAccessibleFocusEvent(self):
		focusWindow = winUser.getGUIThreadInfo(self.windowThreadID).hwndFocus
		if self.windowHandle != focusWindow:
			# This window doesn't have the focus, which means the embedded object's window probably already has the focus.
			# We don't want to override the focus event fired by the embedded object.
			return False
		return super(EmbeddedObject, self).shouldAllowIAccessibleFocusEvent

GeckoVersion = namedtuple("GeckoVersion", ("full", "major"))
def getGeckoVersion(obj):
	appMod = obj.appModule
	try:
		return appMod._geckoVersion
	except AttributeError:
		pass
	try:
		full = obj.IAccessibleObject.QueryInterface(IServiceProvider).QueryService(IAccessibleHandler.IAccessibleApplication._iid_, IAccessibleHandler.IAccessibleApplication).toolkitVersion
	except COMError:
		return None
	try:
		major = int(full.split(".", 1)[0])
	except ValueError:
		major = None
	ver = appMod._geckoVersion = GeckoVersion(full, major)
	return ver

class GeckoPluginWindowRoot(WindowRoot):
	parentUsesSuperOnWindowRootIAccessible = False

	def _get_parent(self):
		parent=super(GeckoPluginWindowRoot,self).parent
		if parent.IAccessibleRole==oleacc.ROLE_SYSTEM_CLIENT:
			# Skip the window wrapping the plugin window,
			# which doesn't expose a Gecko accessible in Gecko >= 11.
			parent=parent.parent.parent
		ver=getGeckoVersion(parent)
		if ver and ver.major!=1:
			res=IAccessibleHandler.accNavigate(parent.IAccessibleObject,0,IAccessibleHandler.NAVRELATION_EMBEDS)
			if res:
				obj=IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
				if obj:
					if controlTypes.STATE_OFFSCREEN not in obj.states:
						return obj
					else:
						log.debugWarning("NAVRELATION_EMBEDS returned an offscreen document, name %r" % obj.name)
				else:
					log.debugWarning("NAVRELATION_EMBEDS returned an invalid object")
			else:
				log.debugWarning("NAVRELATION_EMBEDS failed")
		return parent

class TextLeaf(Mozilla):
	role = controlTypes.ROLE_STATICTEXT
	beTransparentToMouse = True

def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class if this is a Mozilla object.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	if not isinstance(obj.IAccessibleObject, IAccessibleHandler.IAccessible2):
		# We require IAccessible2; i.e. Gecko >= 1.9.
		return

	iaRole = obj.IAccessibleRole

	cls = None
	if iaRole == oleacc.ROLE_SYSTEM_TEXT:
		# Check if this is a text leaf.
		iaStates = obj.IAccessibleStates
		# Text leaves are never focusable.
		# Not unavailable excludes disabled editable text fields (which also aren't focusable).
		if not (iaStates & oleacc.STATE_SYSTEM_FOCUSABLE or iaStates & oleacc.STATE_SYSTEM_UNAVAILABLE):
			# This excludes a non-focusable @role="textbox".
			if not (obj.IA2States & IAccessibleHandler.IA2_STATE_EDITABLE):
				cls = TextLeaf
	if not cls:
		cls = _IAccessibleRolesToOverlayClasses.get(iaRole)
	if cls:
		clsList.append(cls)

	if iaRole == oleacc.ROLE_SYSTEM_ROW:
		clsList.append(RowWithFakeNavigation)
	elif iaRole == oleacc.ROLE_SYSTEM_LISTITEM and hasattr(obj.parent, "IAccessibleTableObject"):
		clsList.append(RowWithFakeNavigation)
	elif iaRole == oleacc.ROLE_SYSTEM_OUTLINEITEM:
		# Check if the tree view is a table.
		parent = obj.parent
		# Tree view items may be nested, so skip any tree view item ancestors.
		while parent and isinstance(parent, Mozilla) and parent.IAccessibleRole == oleacc.ROLE_SYSTEM_OUTLINEITEM:
			newParent = parent.parent
			parent.parent = newParent
			parent = newParent
		if hasattr(parent, "IAccessibleTableObject") or hasattr(parent, "IAccessibleTable2Object"):
			clsList.append(RowWithFakeNavigation)

	if iaRole in _IAccessibleRolesWithBrokenFocusedState:
		clsList.append(BrokenFocusedState)

	ver = getGeckoVersion(obj)
	if ver and ver.full.startswith("1.9"):
		clsList.append(Gecko1_9)

	ia2Web.findExtraOverlayClasses(obj, clsList,
		baseClass=Mozilla, documentClass=Document)

#: Maps IAccessible roles to NVDAObject overlay classes.
_IAccessibleRolesToOverlayClasses = {
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
