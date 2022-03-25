# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2021 NV Access Limited, Peter Vágner

import IAccessibleHandler
from comInterfaces import IAccessible2Lib as IA2
import oleacc
import winUser
import controlTypes
from . import IAccessible, WindowRoot
from logHandler import log
from NVDAObjects.behaviors import RowWithFakeNavigation
from . import ia2Web
from typing import (
	Optional,
)


class Mozilla(ia2Web.Ia2Web):

	def _get_states(self):
		states = super(Mozilla, self).states
		if self.IAccessibleStates & oleacc.STATE_SYSTEM_MARQUEED:
			states.add(controlTypes.State.CHECKABLE)
		return states

	def _get_descriptionFrom(self) -> controlTypes.DescriptionFrom:
		"""Firefox does not yet support 'description-from' attribute (which informs
		NVDA of the source of accDescription after the name/description computation
		is complete. However, a primary use-case can be supported via the IA2attribute
		'description' which is exposed by Firefox and tells us the value of the "aria-description"
		attribute. If the value of accDescription matches, we can infer that the source
		of accDescription is 'aria-description'.
		Note:
			At the time of development some 'generic HTML elements' (E.G. 'span') may not be exposed by Firefox,
			even if the element has an aria-description attribute.
			Other more significant ARIA attributes such as role may cause the element to be exposed.
		"""
		log.debug("Getting mozilla descriptionFrom")
		ariaDesc = self.IA2Attributes.get("description", "")
		log.debug(f"description IA2Attribute is: {ariaDesc}")
		if (
			ariaDesc == ""  # aria-description is missing or empty
			# Ensure that aria-description is actually the value used.
			# I.E. accDescription is sourced from the aria-description attribute as a result of the
			# name/description computation.
			# If the values don't match, some other source must have been used.
			or self.description != ariaDesc
		):
			return controlTypes.DescriptionFrom.UNKNOWN
		else:
			return controlTypes.DescriptionFrom.ARIA_DESCRIPTION

	def _get_presentationType(self):
		presType=super(Mozilla,self).presentationType
		if presType==self.presType_content:
			if self.role==controlTypes.Role.TABLE and self.IA2Attributes.get('layout-guess')=='true':
				presType=self.presType_layout
			elif self.table and self.table.presentationType==self.presType_layout:
				presType=self.presType_layout
		return presType

	def _get_detailsSummary(self) -> Optional[str]:
		# Unlike base Ia2Web implementation, the details-roles
		# IA2 attribute is not exposed in FireFox.
		# Although slower, we have to fetch the details relations instead.
		detailsRelations = self.detailsRelations
		if not detailsRelations:
			return None
		for target in detailsRelations:
			# just take the first for now.
			return target.summarizeInProcess()

	@property
	def hasDetails(self) -> bool:
		# Unlike base Ia2Web implementation, the details-roles
		# IA2 attribute is not exposed in FireFox.
		# Although slower, we have to fetch the details relations instead.
		return bool(self.detailsRelations)


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
		if controlTypes.State.EDITABLE not in self.states:
			import virtualBuffers.gecko_ia2
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

class GeckoPluginWindowRoot(WindowRoot):
	parentUsesSuperOnWindowRootIAccessible = False

	def _get_parent(self):
		parent=super(GeckoPluginWindowRoot,self).parent
		if parent.IAccessibleRole==oleacc.ROLE_SYSTEM_CLIENT:
			# Skip the window wrapping the plugin window,
			# which doesn't expose a Gecko accessible in Gecko >= 11.
			parent=parent.parent.parent
		res = IAccessibleHandler.accNavigate(parent.IAccessibleObject, 0, IAccessibleHandler.NAVRELATION_EMBEDS)
		if res:
			obj = IAccessible(IAccessibleObject=res[0], IAccessibleChildID=res[1])
			if obj:
				if controlTypes.State.OFFSCREEN not in obj.states:
					return obj
				else:
					log.debugWarning("NAVRELATION_EMBEDS returned an offscreen document, name %r" % obj.name)
			else:
				log.debugWarning("NAVRELATION_EMBEDS returned an invalid object")
		else:
			log.debugWarning("NAVRELATION_EMBEDS failed")
		return parent

class TextLeaf(Mozilla):
	role = controlTypes.Role.STATICTEXT
	beTransparentToMouse = True

def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class if this is a Mozilla object.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	if not isinstance(obj.IAccessibleObject, IA2.IAccessible2):
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
			if not (obj.IA2States & IA2.IA2_STATE_EDITABLE):
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

	ia2Web.findExtraOverlayClasses(obj, clsList,
		baseClass=Mozilla, documentClass=Document)

#: Maps IAccessible roles to NVDAObject overlay classes.
_IAccessibleRolesToOverlayClasses = {
	IA2.IA2_ROLE_EMBEDDED_OBJECT: EmbeddedObject,
	"embed": EmbeddedObject,
	"object": EmbeddedObject,
}
