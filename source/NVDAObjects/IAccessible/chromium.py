# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2010-2022 NV Access Limited

"""NVDAObjects for the Chromium browser project
"""
import typing
from typing import Dict, Optional
from comtypes import COMError

import config
import controlTypes
from NVDAObjects.IAccessible import IAccessible
from virtualBuffers.gecko_ia2 import Gecko_ia2 as GeckoVBuf, Gecko_ia2_TextInfo as GeckoVBufTextInfo
from . import ia2Web
from logHandler import log

if typing.TYPE_CHECKING:
	# F401 imported but unused, actually used as a string within type annotation (to avoid having to import
	# at run time)
	from treeInterceptorHandler import TreeInterceptor  # noqa: F401

supportedAriaDetailsRoles: Dict[str, Optional[controlTypes.Role]] = {
	"unknown": None,  # no explicit role, should be reported as "details"
	"comment": controlTypes.Role.COMMENT,
	"doc-footnote": controlTypes.Role.FOOTNOTE,
	# These roles are current unsupported by IAccessible2,
	# and as such, have not been fully implemented in NVDA.
	# They can only be fetched via the IA2Attribute "details-roles",
	# which is only supported in Chrome.
	# Currently maps to the IA2 role ROLE_LIST_ITEM
	"doc-endnote": None,  # controlTypes.Role.ENDNOTE
	# Currently maps to the IA2 role ROLE_PARAGRAPH
	"definition": None,  # controlTypes.Role.DEFINITION
}
"""
details-roles attribute is only defined in Chrome as of May 2022.
Refer to ComputeDetailsRoles:
https://chromium.googlesource.com/chromium/src/+/main/ui/accessibility/platform/ax_platform_node_base.cc#2419
"""


class ChromeVBufTextInfo(GeckoVBufTextInfo):

	def _calculateDescriptionFrom(self, attrs) -> controlTypes.DescriptionFrom:
		"""Overridable calculation of DescriptionFrom
		@param attrs: source attributes for the TextInfo
		@return: the origin for accDescription.
		@note: Chrome provides 'IAccessible2::attribute_description-from' which declares the origin used for
			accDescription. Chrome also provides `IAccessible2::attribute_description` to maintain compatibility
			with FireFox.
		"""
		ia2attrDescriptionFrom = attrs.get("IAccessible2::attribute_description-from")
		try:
			return controlTypes.DescriptionFrom(ia2attrDescriptionFrom)
		except ValueError:
			if ia2attrDescriptionFrom:
				log.debugWarning(f"Unknown 'description-from' IA2Attribute value: {ia2attrDescriptionFrom}")
		# fallback to Firefox approach
		return super()._calculateDescriptionFrom(attrs)

	def _normalizeControlField(self, attrs):
		attrs = super()._normalizeControlField(attrs)
		if attrs['role'] == controlTypes.Role.TOGGLEBUTTON and controlTypes.State.CHECKABLE in attrs['states']:
			# In Chromium, the checkable state is exposed erroneously on toggle buttons.
			attrs['states'].discard(controlTypes.State.CHECKABLE)
		return attrs


class ChromeVBuf(GeckoVBuf):
	TextInfo = ChromeVBufTextInfo

	# selecting with IAccessibleTextSelectionContainer is currently broken in Chromium.
	# Please refer to comments on Chromium issue where this was implemented:
	# https://bugs.chromium.org/p/chromium/issues/detail?id=1298144
	_nativeAppSelectionModeSupported = False

	def __contains__(self, obj):
		if obj.windowHandle != self.rootNVDAObject.windowHandle:
			return False
		if not isinstance(obj,ia2Web.Ia2Web):
			# #4080: Input composition NVDAObjects are the same window but not IAccessible2!
			return False
		accId = obj.IA2UniqueID
		if accId == self.rootID:
			return True
		try:
			self.rootNVDAObject.IAccessibleObject.accChild(accId)
		except COMError:
			return False
		return not self._isNVDAObjectInApplication(obj)


class Document(ia2Web.Document):

	def _get_treeInterceptorClass(self) -> typing.Type["TreeInterceptor"]:
		shouldLoadVBufOnBusyFeatureFlag = bool(
			config.conf["virtualBuffers"]["loadChromiumVBufOnBusyState"]
		)
		vBufUnavailableStates = {  # if any of these are in states, don't return ChromeVBuf
			controlTypes.State.EDITABLE,
		}
		if not shouldLoadVBufOnBusyFeatureFlag:
			log.debug(
				f"loadChromiumVBufOnBusyState feature flag is {shouldLoadVBufOnBusyFeatureFlag},"
				" vBuf WILL NOT be loaded when state of the document is busy."
			)
			vBufUnavailableStates.add(controlTypes.State.BUSY)
		else:
			log.debug(
				f"loadChromiumVBufOnBusyState feature flag is {shouldLoadVBufOnBusyFeatureFlag},"
				" vBuf WILL be loaded when state of the document is busy."
			)
		if self.states.intersection(vBufUnavailableStates):
			return super().treeInterceptorClass
		return ChromeVBuf


class ComboboxListItem(IAccessible):
	"""
	Represents a list item inside a combo box.
	"""

	def _get_focusRedirect(self):
		# Chrome 68 and below fires focus on the active list item of combo boxes even when the combo box is collapsed.
		# We get around this by redirecting focus back up to the combo box itself if the list inside is invisible (I.e. the combo box is collapsed).
		if self.parent and controlTypes.State.INVISIBLE in self.parent.states:
			return self.parent.parent


class ToggleButton(ia2Web.Ia2Web):

	def _get_states(self):
		# In Chromium, the checkable state is exposed erroneously on toggle buttons.
		states = super().states
		states.discard(controlTypes.State.CHECKABLE)
		return states


class PresentationalList(ia2Web.Ia2Web):
	"""
	Ensures that lists like UL, DL and OL always have the readonly state.
	A work-around for issue #7562
	allowing us to differentiate presentational lists from interactive lists
	(such as of size greater 1 and ARIA list boxes).
	In firefox, this is possible by the presence of a read-only state,
	even in a content editable.
	"""

	def _get_states(self):
		states = super().states
		states.add(controlTypes.State.READONLY)
		return states


def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class(es) for Chromium objects.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	if obj.role==controlTypes.Role.LISTITEM and obj.parent and obj.parent.parent and obj.parent.parent.role==controlTypes.Role.COMBOBOX:
		clsList.append(ComboboxListItem)
	elif obj.role == controlTypes.Role.TOGGLEBUTTON:
		clsList.append(ToggleButton)
	elif obj.role == controlTypes.Role.LIST and obj.IA2Attributes.get('tag') in ('ul', 'dl', 'ol'):
		clsList.append(PresentationalList)
	ia2Web.findExtraOverlayClasses(obj, clsList,
		documentClass=Document)
