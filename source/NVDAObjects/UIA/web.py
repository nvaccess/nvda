# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2015-2020 NV Access Limited, Babbage B.V., Leonard de Ruijter

from comtypes import COMError
from comtypes.automation import VARIANT
from ctypes import byref
import winVersion
from logHandler import log
import eventHandler
import config
import controlTypes
import cursorManager
import re
import aria
import textInfos
import UIAHandler
from UIABrowseMode import UIABrowseModeDocument, UIABrowseModeDocumentTextInfo, UIATextRangeQuickNavItem,UIAControlQuicknavIterator
from UIAUtils import *
from . import UIA, UIATextInfo


def splitUIAElementAttribs(attribsString):
	"""Split an UIA Element attributes string into a dict of attribute keys and values.
	An invalid attributes string does not cause an error, but strange results may be returned.
	@param attribsString: The UIA Element attributes string to convert.
	@type attribsString: str
	@return: A dict of the attribute keys and values, where values are strings
	@rtype: {str: str}
	"""
	attribsDict = {}
	tmp = ""
	key = ""
	inEscape = False
	for char in attribsString:
		if inEscape:
			tmp += char
			inEscape = False
		elif char == "\\":
			inEscape = True
		elif char == "=":
			# We're about to move on to the value, so save the key and clear tmp.
			key = tmp
			tmp = ""
		elif char == ";":
			# We're about to move on to a new attribute.
			if key:
				# Add this key/value pair to the dict.
				attribsDict[key] = tmp
			key = ""
			tmp = ""
		else:
			tmp += char
	# If there was no trailing semi-colon, we need to handle the last attribute.
	if key:
		# Add this key/value pair to the dict.
		attribsDict[key] = tmp
	return attribsDict

class UIAWeb(UIA):

	def _get_role(self):
		role = super().role
		from .edge import EdgeHTMLRoot
		if not isinstance(self, EdgeHTMLRoot) and role==controlTypes.ROLE_PANE and self.UIATextPattern:
			return controlTypes.ROLE_INTERNALFRAME
		ariaRole=self._getUIACacheablePropertyValue(UIAHandler.UIA_AriaRolePropertyId).lower()
		# #7333: It is valid to provide multiple, space separated aria roles in HTML
		# The role used is the first role in the list that has an associated NVDA role in aria.ariaRolesToNVDARoles
		for ariaRole in ariaRole.split():
			newRole=aria.ariaRolesToNVDARoles.get(ariaRole)
			if newRole:
				role=newRole
				break
		return role

	def _get_states(self):
		states = super().states
		if self.role in (controlTypes.ROLE_STATICTEXT, controlTypes.ROLE_GROUPING, controlTypes.ROLE_SECTION, controlTypes.ROLE_GRAPHIC) and self.UIAInvokePattern:
			states.add(controlTypes.STATE_CLICKABLE)
		return states

	def _get_ariaProperties(self):
		return splitUIAElementAttribs(self.UIAElement.currentAriaProperties)

	# RegEx to get the value for the aria-current property. This will be looking for a the value of 'current'
	# in a list of strings like "something=true;current=date;". We want to capture one group, after the '='
	# character and before the ';' character.
	# This could be one of: "false", "true", "page", "step", "location", "date", "time"
	# "false" is ignored by the regEx and will not produce a match
	RE_ARIA_CURRENT_PROP_VALUE = re.compile("current=(?!false)(\w+);")

	def _get_isCurrent(self):
		ariaProperties=self._getUIACacheablePropertyValue(UIAHandler.UIA_AriaPropertiesPropertyId)
		match = self.RE_ARIA_CURRENT_PROP_VALUE.search(ariaProperties)
		log.debug("aria props = %s" % ariaProperties)
		if match:
			valueOfAriaCurrent = match.group(1)
			log.debug("aria current value = %s" % valueOfAriaCurrent)
			return valueOfAriaCurrent
		return None

	def _get_roleText(self):
		roleText = self.ariaProperties.get('roledescription', None)
		if roleText:
			return roleText
		return super().roleText

	def _get_placeholder(self):
		ariaPlaceholder = self.ariaProperties.get('placeholder', None)
		return ariaPlaceholder

	def _get_landmark(self):
		landmarkId=self._getUIACacheablePropertyValue(UIAHandler.UIA_LandmarkTypePropertyId)
		if not landmarkId: # will be 0 for non-landmarks
			return None
		landmarkRole = UIAHandler.UIALandmarkTypeIdsToLandmarkNames.get(landmarkId)
		if landmarkRole:
			return landmarkRole
		ariaRoles=self._getUIACacheablePropertyValue(UIAHandler.UIA_AriaRolePropertyId).lower()
		# #7333: It is valid to provide multiple, space separated aria roles in HTML
		# If multiple roles or even multiple landmark roles are provided, the first one is used
		ariaRole = ariaRoles.split(" ")[0]
		if ariaRole in aria.landmarkRoles and (ariaRole != 'region' or self.name):
			return ariaRole
		return None


class List(UIAWeb):

	# non-focusable lists are readonly lists (ensures correct NVDA presentation category)
	def _get_states(self):
		states = super().states
		if controlTypes.STATE_FOCUSABLE not in states:
			states.add(controlTypes.STATE_READONLY)
		return states


class UIAWebTreeInterceptor(cursorManager.ReviewCursorManager,UIABrowseModeDocument):

	TextInfo=UIABrowseModeDocumentTextInfo

	def shouldPassThrough(self,obj,reason=None):
		# Enter focus mode for selectable list items (<select> and role=listbox)
		if reason==controlTypes.REASON_FOCUS and obj.role==controlTypes.ROLE_LISTITEM and controlTypes.STATE_SELECTABLE in obj.states:
			return True
		return super().shouldPassThrough(obj,reason=reason)
