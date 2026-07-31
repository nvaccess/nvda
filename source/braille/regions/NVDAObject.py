# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

from typing import TYPE_CHECKING

import config
import controlTypes
from controlTypes.state import State
from editableText import EditableText
from utils.security import objectBelowLockScreenAndWindowsIsLocked

if TYPE_CHECKING:
	from NVDAObjects import NVDAObject

from .base import Region
from ..constants import TEXT_SEPARATOR
from .properties import getPropertiesBraille
from ._routing import _routingShouldMoveSystemCaret


def NVDAObjectHasUsefulText(obj: "NVDAObject") -> bool:
	"""Does obj contain useful text to display in braille

	:param obj: object to check
	:return: True if there is useful text, False if not
	"""
	if objectBelowLockScreenAndWindowsIsLocked(obj):
		return False
	import displayModel

	if issubclass(obj.TextInfo, displayModel.DisplayModelTextInfo):
		# #1711: Flat review (using displayModel) should always be presented on the braille display
		return True
	if obj._hasNavigableText or isinstance(obj, EditableText):
		return True
	return False


class NVDAObjectRegion(Region):
	"""A region to provide a braille representation of an NVDAObject.
	This region will update based on the current state of the associated NVDAObject.
	A cursor routing request will activate the object's default action.
	"""

	def __init__(self, obj: "NVDAObject", appendText: str = ""):
		"""Constructor.
		@param obj: The associated NVDAObject.
		@param appendText: Text which should always be appended to the NVDAObject text, useful if this region will always precede other regions.
		"""
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			raise RuntimeError("NVDA object is secure and should not be initialized as a braille region")
		super().__init__()
		self.obj = obj
		self.appendText = appendText

	def update(self):
		obj = self.obj
		presConfig = config.conf["presentation"]
		role = obj.role
		name = obj.name
		placeholderValue = obj.placeholder
		if placeholderValue and not obj._isTextEmpty:
			placeholderValue = None
		errorMessage = obj.errorMessage
		if errorMessage and State.INVALID_ENTRY not in obj.states:
			errorMessage = None

		# determine if description should be read
		_shouldUseDescription = (
			obj.description  # is there a description
			and obj.description
			!= name  # the description must not be a duplicate of name, prevent double braille
			and (
				presConfig["reportObjectDescriptions"]  # report description always
				or (
					# aria description provides more relevant information than other sources of description such as
					# a 'title' attribute.
					# It should be used for extra details that would be obvious visually.
					config.conf["annotations"]["reportAriaDescription"]
					and obj.descriptionFrom == controlTypes.DescriptionFrom.ARIA_DESCRIPTION
				)
			)
		)
		description = obj.description if _shouldUseDescription else None
		detailsRoles = obj.annotations.roles if obj.annotations else None
		text = getPropertiesBraille(
			name=name,
			role=role,
			roleText=obj.roleTextBraille,
			current=obj.isCurrent,
			placeholder=placeholderValue,
			hasDetails=bool(obj.annotations),
			detailsRoles=detailsRoles,
			value=obj.value if not NVDAObjectHasUsefulText(obj) else None,
			states=obj.states,
			description=description,
			keyboardShortcut=obj.keyboardShortcut if presConfig["reportKeyboardShortcuts"] else None,
			positionInfo=obj.positionInfo if presConfig["reportObjectPositionInformation"] else None,
			cellCoordsText=obj.cellCoordsText
			if config.conf["documentFormatting"]["reportTableCellCoords"]
			else None,
			errorMessage=errorMessage,
		)
		if role == controlTypes.Role.MATH:
			import mathPres

			if mathPres.brailleProvider:
				try:
					text += TEXT_SEPARATOR + mathPres.brailleProvider.getBrailleForMathMl(
						obj.mathMl,
					)
				except (NotImplementedError, LookupError):
					pass
		self.rawText = text + self.appendText
		super(NVDAObjectRegion, self).update()

	def routeTo(self, braillePos):
		try:
			self.obj.doAction()
		except NotImplementedError:
			pass


class ReviewNVDAObjectRegion(NVDAObjectRegion):
	"""A region to provide a braille representation of an NVDAObject when braille is tethered to review.
	This region behaves very similar to its base class.
	However, when the move system caret when routing review cursor braille setting is active,
	pressing a routing key will first focus the object before executing the default action.
	"""

	def routeTo(self, braillePos: int):
		if _routingShouldMoveSystemCaret() and self.obj.isFocusable and not self.obj.hasFocus:
			self.obj.setFocus()
		super().routeTo(braillePos)
