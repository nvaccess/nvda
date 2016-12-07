# -*- coding: UTF-8 -*-
#NVDAObjects/IAccessible/mozilla.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2015 NV Access Limited, Peter Vágner

from collections import namedtuple
from ctypes import c_short
import IAccessibleHandler
import oleacc
import winUser
from comtypes import IServiceProvider, COMError, BSTR
import eventHandler
import controlTypes
from . import IAccessible, Dialog, WindowRoot
from logHandler import log
import textInfos.offsets
from NVDAObjects.behaviors import RowWithFakeNavigation
from . import IA2TextTextInfo
from . import ia2Web

class Mozilla(ia2Web.Ia2Web):

	def _get_parent(self):
		#Special code to support Mozilla node_child_of relation (for comboboxes)
		res=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVRELATION_NODE_CHILD_OF)
		if res and res!=(self.IAccessibleObject,self.IAccessibleChildID):
			#Gecko can sometimes give back a broken application node with a windowHandle of 0
			#The application node is annoying, even if it wasn't broken
			#So only use the node_child_of object if it has a valid IAccessible2 windowHandle
			try:
				windowHandle=res[0].windowHandle
			except (COMError,AttributeError):
				windowHandle=None
			if windowHandle:
				newObj=IAccessible(windowHandle=windowHandle,IAccessibleObject=res[0],IAccessibleChildID=res[1])
				if newObj:
					return newObj
		return super(Mozilla,self).parent

	def _get_states(self):
		states = super(Mozilla, self).states
		if self.IAccessibleStates & oleacc.STATE_SYSTEM_MARQUEED:
			states.add(controlTypes.STATE_CHECKABLE)
		if self.IA2Attributes.get("hidden") == "true":
			states.add(controlTypes.STATE_INVISIBLE)
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

class Document(ia2Web.Document):

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

class Math(Mozilla):

	def _get_mathMl(self):
		from comtypes.gen.ISimpleDOM import ISimpleDOMNode
		node = self.IAccessibleObject.QueryInterface(ISimpleDOMNode)
		# Try the data-mathml attribute.
		attr = node.attributesForNames(1, (BSTR * 1)("data-mathml"), (c_short * 1)(0,))
		if attr:
			import mathPres
			if not mathPres.getLanguageFromMath(attr) and self.language:
				attr = mathPres.insertLanguageIntoMath(attr, self.language)
			return attr
		if self.IA2Attributes.get("tag") != "math":
			# This isn't MathML.
			raise LookupError
		if self.language:
			attrs = ' xml:lang="%s"' % self.language
		else:
			attrs = ""
		return "<math%s>%s</math>" % (attrs, node.innerHTML)

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
	elif iaRole == oleacc.ROLE_SYSTEM_TEXT:
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
		if hasattr(parent, "IAccessibleTableObject"):
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
	oleacc.ROLE_SYSTEM_EQUATION: Math,
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
