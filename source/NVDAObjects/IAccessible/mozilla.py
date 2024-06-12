# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2022 NV Access Limited, Peter Vágner

from typing import (
	Generator,
	Optional,
	Tuple,
)

from annotation import (
	_AnnotationRolesT,
	AnnotationTarget,
	AnnotationOrigin,
)
import IAccessibleHandler
from comInterfaces import IAccessible2Lib as IA2
import config
import oleacc
import winUser
import controlTypes
from . import IAccessible, WindowRoot
from logHandler import log
from NVDAObjects.behaviors import RowWithFakeNavigation
from . import ia2Web


class MozAnnotationTarget(AnnotationTarget):
	def __init__(self, target: IAccessible):
		self._target: IAccessible = target

	@property
	def summary(self) -> str:
		return self._target.summarizeInProcess()

	@property
	def role(self) -> Optional[controlTypes.Role]:
		# details-roles is currently only defined in Chromium
		# this may diverge in Firefox in the future.
		from .chromium import supportedAriaDetailsRoles
		detailsRole = IAccessibleHandler.IAccessibleRolesToNVDARoles.get(
			self._target.IAccessibleRole
		)
		# return a supported details role
		if config.conf["debugLog"]["annotations"]:
			log.debug(f"detailsRole: {repr(detailsRole)}")
		if detailsRole in supportedAriaDetailsRoles.values():
			return detailsRole

		if config.conf["debugLog"]["annotations"]:
			log.warning(f"Unsupported aria details role: {detailsRole}")
		return None

	@property
	def targetObject(self) -> IAccessible:
		return self._target


class MozAnnotation(AnnotationOrigin):
	"""
	Unlike base Ia2Web implementation, the details-roles IA2 attribute is not exposed in Firefox.
	"""
	_originObj: "Mozilla"

	def __bool__(self) -> bool:
		# Unlike base Ia2Web implementation, the details-roles
		# IA2 attribute is not exposed in Firefox.
		# Although slower, we have to fetch the details relations instead.
		return bool(
			self._originObj.detailsRelations
		)

	@property
	def targets(self) -> Tuple[MozAnnotationTarget]:
		return tuple(MozAnnotationTarget(rel) for rel in self._originObj.detailsRelations)

	@property
	def roles(self) -> _AnnotationRolesT:
		return tuple(self._rolesGenerator)

	@property
	def _rolesGenerator(self) -> Generator[Optional[controlTypes.Role], None, None]:
		# Unlike base Ia2Web implementation, the details-roles
		# IA2 attribute is not exposed in Firefox.
		# Although slower, we have to fetch the details relations instead.
		for target in self.targets:
			try:
				yield target.role
			except ValueError:
				log.error("Error getting role.", exc_info=True)


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

	annotations: MozAnnotation
	"""Typing information for auto property _get_annotations
	"""

	def _get_annotations(self) -> MozAnnotation:
		annotationOrigin = MozAnnotation(self)
		return annotationOrigin

	def _get_detailsSummary(self) -> Optional[str]:
		log.warning(
			"NVDAObject.detailsSummary is deprecated. Use NVDAObject.annotations instead.",
			stack_info=True,
		)
		# just take the first for now.
		return self.annotations.targets[0].summary

	def _get_detailsRole(self) -> Optional[controlTypes.Role]:
		log.warning(
			"NVDAObject.detailsRole is deprecated. Use NVDAObject.annotations instead.",
			stack_info=True,
		)
		# just take the first target for now.
		return self.annotations.roles[0]

	@property
	def hasDetails(self) -> bool:
		log.warning(
			"NVDAObject.hasDetails is deprecated. Use NVDAObject.annotations instead.",
			stack_info=True,
		)
		return bool(self.annotations)


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
