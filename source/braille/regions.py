# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau,
# Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt

from __future__ import annotations

import bisect
import typing
from typing import (
	TYPE_CHECKING,
	Any,
	Dict,
	Optional,
	Set,
	Union,
)

from annotation import _AnnotationRolesT
import time
import languageHandler
import louisHelper
import louis
from controlTypes.state import State
import config
from config.configFlags import (
	TetherTo,
	ReportTableHeaders,
	OutputMode,
)
from config.featureFlagEnums import (
	FontFormattingBrailleModeFlag,
	ReviewRoutingMovesSystemCaretFlag,
)
from logHandler import log
import controlTypes
import api
import textInfos
import collections
from utils.security import objectBelowLockScreenAndWindowsIsLocked
from textUtils import isUnicodeNormalized, UnicodeNormalizationOffsetConverter
from editableText import EditableText

if TYPE_CHECKING:
	from NVDAObjects import NVDAObject

from .labels import (
	roleLabels,
	positiveStateLabels,
	negativeStateLabels,
	landmarkLabels,
	SELECTION_SHAPE,
	INPUT_START_IND,
	INPUT_END_IND,
	TEXT_SEPARATOR,
	FormatTagDelimiter,
	fontAttributeFormattingMarkers,
	FormattingMarker,
)

import braille

#: Named tuple for a region with start and end positions in a buffer
RegionWithPositions = collections.namedtuple("RegionWithPositions", ("region", "start", "end"))


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


class Region(object):
	"""A region of braille to be displayed.
	Each portion of braille to be displayed is represented by a region.
	The region is responsible for retrieving its text and the cursor and selection positions, translating it into braille cells and handling cursor routing requests relative to its braille cells.
	The :class:`BrailleBuffer` containing this region will call :meth:`update` and expect that :attr:`brailleCells`, :attr:`brailleCursorPos`, :attr:`brailleSelectionStart` and :attr:`brailleSelectionEnd` will be set appropriately.
	:meth:`routeTo` will be called to handle a cursor routing request.
	"""

	rawText: str = ""
	"""The original, raw text of this region."""
	cursorPos: int | None = None
	"""The position of the cursor in :attr:`rawText`, ``None`` if the cursor is not in this region."""
	selectionStart: int | None = None
	"""The start of the selection in :attr:`rawText` (inclusive), ``None`` if there is no selection in this region."""
	selectionEnd: int | None = None
	"""The end of the selection in :attr:`rawText` (exclusive), ``None`` if there is no selection in this region."""
	rawTextTypeforms: list[int] | None = None
	"""liblouis typeform flags for each character in :attr:`rawText`, ``None`` if no typeform info."""
	brailleCursorPos: int | None = None
	"""The position of the cursor in :attr:`brailleCells`, ``None`` if the cursor is not in this region."""
	brailleSelectionStart: int | None = None
	"""The position of the selection start in :attr:`brailleCells`, ``None`` if there is no selection in this region."""
	brailleSelectionEnd: int | None = None
	"""The position of the selection end in :attr:`brailleCells`, ``None`` if there is no selection in this region."""
	hidePreviousRegions: bool = False
	"""Whether to hide all previous regions."""
	focusToHardLeft: bool = False
	"""Whether this region should be positioned at the absolute left of the display when focused."""

	def __init__(self):
		self._languageIndexes: dict[int, str] = {0: self._getDefaultRegionLanguage()}
		"""Language indexes in :attr:`rawText`. The last language is assumed to be the final language in the region."""
		self.brailleCells: list[int] = []
		"""The translated braille representation of this region."""
		self.rawToBraillePos: list[int] = []
		"""A list mapping positions in :attr:`rawText` to positions in :attr:`brailleCells`."""
		self.brailleToRawPos: list[int] = []
		"""A list mapping positions in :attr:`brailleCells` to positions in :attr:`rawText`."""

	def _getDefaultRegionLanguage(self) -> str:
		"""Get the default language for a region."""
		return louisHelper.getTableLanguage(braille.handler.table.fileName) or languageHandler.getLanguage()

	def _getLanguageAtPos(self, pos: int) -> str:
		"""Get the language at a given position in :attr:`rawText` based on :attr:`_languageIndexes`."""
		keys = sorted(self._languageIndexes)
		i = bisect.bisect_right(keys, pos) - 1
		return self._languageIndexes[keys[i]]

	def update(self):
		"""Update this region.
		Subclasses should extend this to update L{rawText}, L{cursorPos}, L{selectionStart} and L{selectionEnd} if necessary.
		The base class method handles translation of L{rawText} into braille, placing the result in L{brailleCells}.
		Typeform information from L{rawTextTypeforms} is used, if any.
		L{rawToBraillePos} and L{brailleToRawPos} are updated according to the translation.
		L{brailleCursorPos}, L{brailleSelectionStart} and L{brailleSelectionEnd} are similarly updated based on L{cursorPos}, L{selectionStart} and L{selectionEnd}, respectively.
		@postcondition: L{brailleCells}, L{brailleCursorPos}, L{brailleSelectionStart} and L{brailleSelectionEnd} are updated and ready for rendering.
		"""
		mode = louis.dotsIO
		if config.conf["braille"]["expandAtCursor"] and self.cursorPos is not None:
			mode |= louis.compbrlAtCursor

		converter: UnicodeNormalizationOffsetConverter | None = None
		textToTranslate = self.rawText
		textToTranslateTypeforms = self.rawTextTypeforms
		cursorPos = self.cursorPos
		if config.conf["braille"]["unicodeNormalization"] and not isUnicodeNormalized(textToTranslate):
			converter = UnicodeNormalizationOffsetConverter(textToTranslate)
			textToTranslate = converter.encoded
			if textToTranslateTypeforms is not None:
				# Typeforms must be adapted to represent normalized characters.
				textToTranslateTypeforms = [
					textToTranslateTypeforms[strOffset] for strOffset in converter.computedEncodedToStrOffsets
				]
			if cursorPos is not None:
				# Convert the cursor position to a normalized offset.
				cursorPos = converter.strToEncodedOffsets(cursorPos)
		self.brailleCells, brailleToRawPos, rawToBraillePos, self.brailleCursorPos = louisHelper.translate(
			[braille.handler.table.fileName, "braille-patterns.cti"],
			textToTranslate,
			typeform=textToTranslateTypeforms,
			mode=mode,
			cursorPos=cursorPos,
		)

		if converter:
			# The received brailleToRawPos contains braille to normalized positions.
			# Process them to represent real raw positions by converting them from normalized ones.
			brailleToRawPos = [converter.encodedToStrOffsets(i) for i in brailleToRawPos]
			# The received rawToBraillePos contains normalized to braille positions.
			# Create a new list based on real raw positions.
			rawToBraillePos = [rawToBraillePos[i] for i in converter.computedStrToEncodedOffsets]
		self.brailleToRawPos = brailleToRawPos
		self.rawToBraillePos = rawToBraillePos

		if (
			self.selectionStart is not None
			and self.selectionEnd is not None
			and config.conf["braille"]["showSelection"]
		):
			try:
				# Mark the selection.
				self.brailleSelectionStart = self.rawToBraillePos[self.selectionStart]
				if self.selectionEnd >= len(self.rawText):
					self.brailleSelectionEnd = len(self.brailleCells)
				else:
					self.brailleSelectionEnd = self.rawToBraillePos[self.selectionEnd]
				for pos in range(self.brailleSelectionStart, self.brailleSelectionEnd):
					self.brailleCells[pos] |= SELECTION_SHAPE
			except IndexError:
				pass

	def routeTo(self, braillePos):
		"""Handle a cursor routing request.
		For example, this might activate an object or move the cursor to the requested position.
		@param braillePos: The routing position in L{brailleCells}.
		@type braillePos: int
		@note: If routing the cursor, L{brailleToRawPos} can be used to translate L{braillePos} into a position in L{rawText}.
		"""

	def nextLine(self):
		"""Move to the next line if possible."""

	def previousLine(self, start=False):
		"""Move to the previous line if possible.
		@param start: C{True} to move to the start of the line, C{False} to move to the end.
		@type start: bool
		"""

	def __repr__(self):
		return f"{self.__class__.__name__} ({self.rawText!r})"


class TextRegion(Region):
	"""A simple region containing a string of text."""

	def __init__(self, text):
		super(TextRegion, self).__init__()
		self.rawText = text


def _getAnnotationProperty(
	propertyValues: Dict[str, Any],
) -> str:
	# Translators: Braille when there are further details/annotations that can be fetched manually.
	genericDetailsRole = _("details")
	detailsRoles: _AnnotationRolesT = propertyValues.get("detailsRoles", tuple())
	if not detailsRoles:
		log.debugWarning(
			"There should always be detailsRoles (at least a single None value) when hasDetails is true.",
		)
		return genericDetailsRole
	else:
		# Translators: Braille when there are further details/annotations that can be fetched manually.
		# %s specifies the type of details (e.g. "has comment suggestion")
		hasDetailsRoleTemplate = _("has %s")
		rolesLabels = list(
			(
				hasDetailsRoleTemplate % roleLabels.get(role, role.displayString)
				for role in detailsRoles
				if role  # handle None case without the "has X" grammar.
			)
		)
		if None in detailsRoles:
			rolesLabels.insert(0, genericDetailsRole)
		return " ".join(rolesLabels)  # no comma to save cells on braille display


# C901 'getPropertiesBraille' is too complex
# Note: when working on getPropertiesBraille, look for opportunities to simplify
# and move logic out into smaller helper functions.
def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
	textList = []
	name = propertyValues.get("name")
	if name:
		textList.append(name)
	role: Optional[Union[controlTypes.Role, int]] = propertyValues.get("role")
	roleText = propertyValues.get("roleText")
	states = propertyValues.get("states")
	positionInfo = propertyValues.get("positionInfo")
	level = positionInfo.get("level") if positionInfo else None
	childControlCount = positionInfo.get("childControlCount") if positionInfo else None
	cellCoordsText = propertyValues.get("cellCoordsText")
	rowNumber = propertyValues.get("rowNumber")
	columnNumber = propertyValues.get("columnNumber")
	# When fetching row and column span
	# default the values to 1 to make further checks a lot simpler.
	# After all, a table cell that has no rowspan implemented is assumed to span one row.
	rowSpan = propertyValues.get("rowSpan") or 1
	columnSpan = propertyValues.get("columnSpan") or 1
	includeTableCellCoords = propertyValues.get("includeTableCellCoords", True)
	if role is not None and not roleText:
		role = controlTypes.Role(role)
		if role == controlTypes.Role.HEADING and level:
			# Translators: Displayed in braille for a heading with a level.
			# %s is replaced with the level.
			roleText = _("h%s") % level
			level = None
		elif role == controlTypes.Role.LINK and states and controlTypes.State.VISITED in states:
			states = states.copy()
			states.discard(controlTypes.State.VISITED)
			# Translators: Displayed in braille for a link which has been visited.
			roleText = _("vlnk")
		elif role == controlTypes.Role.LIST:
			if (
				states
				and controlTypes.State.MULTISELECTABLE in states
				and config.conf["presentation"]["reportMultiSelect"]
			):
				# Collapse the list role and multiselectable state into a single role text.
				# Note that for other cases where this state is found, regular processing with
				# controlTypes.processAndLabelStates will discard the state if necessary.
				states = states.copy()
				states.discard(controlTypes.State.MULTISELECTABLE)
				# Translators: Displayed in braille for a multi select list.
				roleText = _("mslst")
			else:
				roleText = roleLabels.get(role, role.displayString)
			if childControlCount:
				roleText += childControlCount
				childControlCount = None

		elif (
			name or cellCoordsText or rowNumber or columnNumber
		) and role in controlTypes.silentRolesOnFocus:
			roleText = None
		else:
			roleText = roleLabels.get(role, role.displayString)
	elif role is None:
		role = propertyValues.get("_role")
	value = propertyValues.get("value")
	if value and role not in controlTypes.silentValuesForRoles:
		textList.append(value)
	if states is not None:
		textList.extend(
			controlTypes.processAndLabelStates(
				role,
				states,
				controlTypes.OutputReason.FOCUS,
				states,
				None,
				positiveStateLabels,
				negativeStateLabels,
			),
		)
	if roleText:
		textList.append(roleText)

	errorMessage = propertyValues.get("errorMessage")
	if errorMessage:
		textList.append(errorMessage)

	description = propertyValues.get("description")
	if description:
		textList.append(description)
	hasDetails = propertyValues.get("hasDetails")
	if hasDetails:
		textList.append(_getAnnotationProperty(propertyValues))
	keyboardShortcut = propertyValues.get("keyboardShortcut")
	if keyboardShortcut:
		textList.append(keyboardShortcut)
	if positionInfo:
		indexInGroup = positionInfo.get("indexInGroup")
		similarItemsInGroup = positionInfo.get("similarItemsInGroup")
		if indexInGroup and similarItemsInGroup:
			# Translators: Brailled to indicate the position of an item in a group of items (such as a list).
			# {number} is replaced with the number of the item in the group.
			# {total} is replaced with the total number of items in the group.
			textList.append(_("{number} of {total}").format(number=indexInGroup, total=similarItemsInGroup))

		if level is not None:
			# Translators: Displayed in braille when an object (e.g. a tree view item) has a hierarchical level.
			# %s is replaced with the level.
			textList.append(_("lv %s") % positionInfo["level"])

	if rowNumber:
		if includeTableCellCoords and not cellCoordsText:
			if rowSpan > 1:
				# Translators: Displayed in braille for the table cell row numbers when a cell spans multiple rows.
				# Occurences of %s are replaced with the corresponding row numbers.
				rowStr = _("r{rowNumber}-{rowSpan}").format(
					rowNumber=rowNumber,
					rowSpan=rowNumber + rowSpan - 1,
				)
			else:
				# Translators: Displayed in braille for a table cell row number.
				# %s is replaced with the row number.
				rowStr = _("r{rowNumber}").format(rowNumber=rowNumber)
			textList.append(rowStr)
	if columnNumber:
		columnHeaderText = propertyValues.get("columnHeaderText")
		if columnHeaderText:
			textList.append(columnHeaderText)
		if includeTableCellCoords and not cellCoordsText:
			if columnSpan > 1:
				# Translators: Displayed in braille for the table cell column numbers when a cell spans multiple columns.
				# Occurences of %s are replaced with the corresponding column numbers.
				columnStr = _("c{columnNumber}-{columnSpan}").format(
					columnNumber=columnNumber,
					columnSpan=columnNumber + columnSpan - 1,
				)
			else:
				# Translators: Displayed in braille for a table cell column number.
				# %s is replaced with the column number.
				columnStr = _("c{columnNumber}").format(columnNumber=columnNumber)
			textList.append(columnStr)
	isCurrent = propertyValues.get("current", controlTypes.IsCurrent.NO)
	if isCurrent != controlTypes.IsCurrent.NO:
		textList.append(isCurrent.displayString)
	placeholder = propertyValues.get("placeholder", None)
	if placeholder:
		textList.append(placeholder)
	if includeTableCellCoords and cellCoordsText:
		textList.append(cellCoordsText)
	return TEXT_SEPARATOR.join([x for x in textList if x])


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


def getControlFieldBraille(
	info: textInfos.TextInfo,
	field: textInfos.Field,
	ancestors: typing.List[textInfos.Field],
	reportStart: bool,
	formatConfig: config.AggregatedSection,
) -> Optional[str]:
	presCat = field.getPresentationCategory(ancestors, formatConfig)
	# Cache this for later use.
	field._presCat = presCat
	role = field.get("role", controlTypes.Role.UNKNOWN)
	if reportStart:
		# If this is a container, only report it if this is the start of the node.
		if presCat == field.PRESCAT_CONTAINER and not field.get("_startOfNode"):
			return None
	else:
		# We only report ends for containers that are not landmarks/regions
		# and only if this is the end of the node.
		if (
			presCat != field.PRESCAT_CONTAINER
			or not field.get("_endOfNode")
			or role == controlTypes.Role.LANDMARK
		):
			return None

	description = None
	_descriptionFrom: controlTypes.DescriptionFrom = field.get("_description-from")
	_descriptionIsContent: bool = field.get("descriptionIsContent", False)
	if (
		not _descriptionIsContent
		# Note "reportObjectDescriptions" is not a reason to include description,
		# "Object" implies focus/object nav, getControlFieldBraille calculates text for Browse mode.
		# There is no way to identify getControlFieldBraille being called for reason focus, as is done in speech.
		and (
			config.conf["annotations"]["reportAriaDescription"]
			and _descriptionFrom == controlTypes.DescriptionFrom.ARIA_DESCRIPTION
		)
	):
		description = field.get("description", None)

	states = field.get("states", set())
	value = field.get("value", None)
	current = field.get("current", controlTypes.IsCurrent.NO)
	placeholder = field.get("placeholder", None)
	errorMessage = None
	if errorMessage and State.INVALID_ENTRY in states:
		errorMessage = field.get("errorMessage", None)

	hasDetails = field.get("hasDetails", False) and config.conf["annotations"]["reportDetails"]
	if config.conf["annotations"]["reportDetails"]:
		detailsRoles: Set[Union[None, controlTypes.Role]] = field.get("detailsRoles")
	else:
		detailsRoles = set()

	roleText = field.get("roleTextBraille", field.get("roleText"))
	landmark = field.get("landmark")
	if not roleText and role == controlTypes.Role.LANDMARK and landmark:
		roleText = f"{roleLabels[controlTypes.Role.LANDMARK]} {landmarkLabels[landmark]}"

	content = field.get("content")

	if presCat == field.PRESCAT_LAYOUT:
		return _getControlFieldForLayoutPresentation(
			description=description,
			current=current,
			hasDetails=hasDetails,
			detailsRoles=detailsRoles,
			role=role,
			content=content,
		)

	elif role in (
		controlTypes.Role.TABLECELL,
		controlTypes.Role.TABLECOLUMNHEADER,
		controlTypes.Role.TABLEROWHEADER,
	) and field.get("table-id"):
		return _getControlFieldForTableCell(
			description=description,
			current=current,
			hasDetails=hasDetails,
			detailsRoles=detailsRoles,
			field=field,
			formatConfig=formatConfig,
			states=states,
		)

	elif reportStart:
		return _getControlFieldForReportStart(
			description=description,
			current=current,
			hasDetails=hasDetails,
			detailsRoles=detailsRoles,
			field=field,
			role=role,
			states=states,
			content=content,
			info=info,
			value=value,
			roleText=roleText,
			placeholder=placeholder,
			errorMessage=errorMessage,
		)

	else:
		# Translators: Displayed in braille at the end of a control field such as a list or table.
		# %s is replaced with the control's role.
		return _("%s end") % getPropertiesBraille(
			role=role,
			roleText=roleText,
		)


def _getControlFieldForLayoutPresentation(
	description: Optional[str],
	current: controlTypes.IsCurrent,
	hasDetails: bool,
	detailsRoles: _AnnotationRolesT,
	role: controlTypes.Role,
	content: Optional[str],
) -> Optional[str]:
	text = []
	if description:
		text.append(getPropertiesBraille(description=description))
	if current:
		text.append(getPropertiesBraille(current=current))
	if hasDetails:
		text.append(getPropertiesBraille(hasDetails=hasDetails, detailsRoles=detailsRoles))
	if role == controlTypes.Role.GRAPHIC and content:
		text.append(content)

	if text:
		return TEXT_SEPARATOR.join(text)
	return None


def _getControlFieldForTableCell(
	description: Optional[str],
	current: controlTypes.IsCurrent,
	hasDetails: bool,
	detailsRoles: _AnnotationRolesT,
	field: textInfos.Field,
	formatConfig: config.AggregatedSection,
	states: Set[controlTypes.State],
) -> str:
	reportTableHeaders = formatConfig["reportTableHeaders"]
	reportTableCellCoords = formatConfig["reportTableCellCoords"]
	props = {
		"states": states,
		"rowNumber": (field.get("table-rownumber-presentational") or field.get("table-rownumber")),
		"columnNumber": (field.get("table-columnnumber-presentational") or field.get("table-columnnumber")),
		"rowSpan": field.get("table-rowsspanned"),
		"columnSpan": field.get("table-columnsspanned"),
		"includeTableCellCoords": reportTableCellCoords,
		"current": current,
		"description": description,
		"hasDetails": hasDetails,
		"detailsRoles": detailsRoles,
	}
	if reportTableHeaders in (ReportTableHeaders.ROWS_AND_COLUMNS, ReportTableHeaders.COLUMNS):
		props["columnHeaderText"] = field.get("table-columnheadertext")
	return getPropertiesBraille(**props)


def _getControlFieldForReportStart(
	description: Optional[str],
	current: controlTypes.IsCurrent,
	hasDetails: bool,
	detailsRoles: _AnnotationRolesT,
	field: textInfos.Field,
	role: controlTypes.Role,
	states: Set[controlTypes.State],
	content: Optional[str],
	info: textInfos.TextInfo,
	value: Optional[str],
	roleText: str,
	placeholder: Optional[str],
	errorMessage: str | None,
) -> str:
	props = {
		"states": states,
		"value": value,
		"current": current,
		"placeholder": placeholder,
		"roleText": roleText,
		"description": description,
		"hasDetails": hasDetails,
		"detailsRoles": detailsRoles,
		"errorMessage": errorMessage,
	}

	if role == controlTypes.Role.MATH:
		# Don't report the role for math here.
		# However, we still need to pass it (hence "_role").
		props["_role"] = role
	else:
		props["role"] = role

	if field.get("alwaysReportName", False):
		# Ensure that the name of the field gets presented even if normally it wouldn't.
		name = field.get("name")
		if name:
			props["name"] = name

	if config.conf["presentation"]["reportKeyboardShortcuts"]:
		kbShortcut = field.get("keyboardShortcut")
		if kbShortcut:
			props["keyboardShortcut"] = kbShortcut

	level = field.get("level")
	if level:
		props["positionInfo"] = {"level": level}
	if role == controlTypes.Role.LIST and (int(childControlCount := field.get("_childcontrolcount", 0))) > 0:
		props["positionInfo"] = {"childControlCount": childControlCount}

	text = getPropertiesBraille(**props)
	if content:
		if text:
			text += TEXT_SEPARATOR
		text += content
	elif role == controlTypes.Role.MATH:
		import mathPres

		if mathPres.brailleProvider:
			try:
				if text:
					text += TEXT_SEPARATOR
				text += mathPres.brailleProvider.getBrailleForMathMl(
					info.getMathMl(field),
				)
			except (NotImplementedError, LookupError):
				pass
	return text


def getFormatFieldBraille(field, fieldCache, isAtStart, formatConfig):
	"""Generates the braille text for the given format field.
	@param field: The format field to examine.
	@type field: {str : str, ...}
	@param fieldCache: The format field of the previous run; i.e. the cached format field.
	@type fieldCache: {str : str, ...}
	@param isAtStart: True if this format field precedes any text in the line/paragraph.
	This is useful to restrict display of information which should only appear at the start of the line/paragraph;
	e.g. the line number or line prefix (list bullet/number).
	@type isAtStart: bool
	@param formatConfig: The formatting config.
	@type formatConfig: {str : bool, ...}
	"""
	textList = []
	if isAtStart:
		paragraphStartMarker = getParagraphStartMarker()
		if paragraphStartMarker:
			textList.append(paragraphStartMarker)
		if formatConfig["reportLineNumber"]:
			lineNumber = field.get("line-number")
			if lineNumber:
				textList.append("%s" % lineNumber)
		linePrefix = field.get("line-prefix")
		if linePrefix:
			textList.append(linePrefix)
		if formatConfig["reportHeadings"]:
			headingLevel = field.get("heading-level")
			if headingLevel:
				# Translators: Displayed in braille for a heading with a level.
				# %s is replaced with the level.
				textList.append(_("h%s") % headingLevel)
		collapsed = field.get("collapsed")
		if collapsed:
			textList.append(positiveStateLabels[controlTypes.State.COLLAPSED])
	if formatConfig["reportLinks"]:
		link = field.get("link")
		oldLink = fieldCache.get("link")
		if link and link != oldLink:
			textList.append(roleLabels[controlTypes.Role.LINK])
	if formatConfig["reportComments"]:
		comment = field.get("comment")
		oldComment = fieldCache.get("comment") if fieldCache is not None else None
		if (comment or oldComment is not None) and comment != oldComment:
			if comment:
				if comment is textInfos.CommentType.DRAFT:
					# Translators: Brailled when text contains a draft comment.
					text = _("drft cmnt")
				elif comment is textInfos.CommentType.RESOLVED:
					# Translators: Brailled when text contains a resolved comment.
					text = _("rslvd cmnt")
				else:  # generic
					# Translators: Brailled when text contains a generic comment.
					text = _("cmnt")
				textList.append(text)
	if formatConfig["reportBookmarks"]:
		bookmark = field.get("bookmark")
		oldBookmark = fieldCache.get("bookmark") if fieldCache is not None else None
		if (bookmark or oldBookmark is not None) and bookmark != oldBookmark:
			if bookmark:
				# Translators: brailled when text contains a bookmark
				text = _("bkmk")
				textList.append(text)

	if (
		config.conf["braille"]["fontFormattingDisplay"].calculated() == FontFormattingBrailleModeFlag.TAGS
		and (formattingTags := _getFormattingTags(field, fieldCache)) is not None
	):
		textList.append(formattingTags)

	fieldCache.clear()
	fieldCache.update(field)
	return TEXT_SEPARATOR.join([x for x in textList if x])


def getParagraphStartMarker() -> str | None:
	brailleConfig = config.conf["braille"]
	if brailleConfig["readByParagraph"]:
		paragraphStartMarker = brailleConfig["paragraphStartMarker"]
		if paragraphStartMarker == "¶":
			# Translators: This is a paragraph start marker used in braille.
			# The default symbol is the pilcrow,
			# a symbol also known as "paragraph symbol" or "paragraph marker".
			# This symbol should translate in braille via LibLouis automatically.
			# If there is a more appropriate character for your locale,
			# consider overwriting this (e.g. for Ge'ez ፨).
			# You can also use Unicode Braille such as ⠘⠏.
			# Ensure this is consistent with other strings with the context "paragraphMarker".
			paragraphStartMarker = pgettext("paragraphMarker", "¶")
	else:
		paragraphStartMarker = None
	return paragraphStartMarker


def _getFormattingTags(
	field: dict[str, str],
	fieldCache: dict[str, str],
) -> str | None:
	"""Get the formatting tags for the given field and cache.

	Formatting tags are calculated according to the preferences passed in formatConfig.

	:param field: The format current field.
	:param fieldCache: The previous format field.
	:param formatConfig: The user's formatting preferences.
	:return: The braille formatting tag as a string, or None if no pertinant formatting is applied.
	"""
	textList: list[str] = []
	for fontAttribute, formattingMarker in fontAttributeFormattingMarkers.items():
		if formattingMarker.shouldBeUsed(fontAttribute):
			_appendFormattingMarker(fontAttribute, formattingMarker, textList, field, fieldCache)
	if len(textList) > 0:
		return f"{FormatTagDelimiter.START}{''.join(textList)}{FormatTagDelimiter.END}"


def _appendFormattingMarker(
	attribute: str,
	marker: FormattingMarker,
	textList: list[str],
	field: dict[str, str],
	fieldCache: dict[str, str],
) -> None:
	"""Append a formatting marker to the text list if the attribute has changed.

	:param attribute: The attribute to check.
	:param marker: The formatting marker to use.
	:param textList: The list of marker strings to append to.
	:param field: The current format field.
	:param fieldCache: The previous format field.
	"""
	newVal = field.get(attribute, False)
	oldVal = fieldCache.get(attribute, False) if fieldCache is not None else False
	if newVal and not oldVal:
		textList.append(marker.start)
	elif oldVal and not newVal:
		textList.append(marker.end)


class TextInfoRegion(Region):
	pendingCaretUpdate = False  #: True if the cursor should be updated for this region on the display
	allowPageTurns = True  #: True if a page turn should be tried when a TextInfo cannot move anymore and the object supports page turns.

	def __init__(self, obj: "NVDAObject"):
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			raise RuntimeError("NVDA object is secure and should not be initialized as a braille region")
		super().__init__()
		self.obj = obj

	def _isMultiline(self):
		# A region's object can either be an NVDAObject or a tree interceptor.
		# Tree interceptors should always be multiline.
		from treeInterceptorHandler import TreeInterceptor

		if isinstance(self.obj, TreeInterceptor):
			return True
		# Terminals and documents are inherently multiline, so they don't have the multiline state.
		return (
			self.obj.role in (controlTypes.Role.TERMINAL, controlTypes.Role.DOCUMENT)
			or controlTypes.State.MULTILINE in self.obj.states
		)

	def _getSelection(self):
		"""Retrieve the selection.
		If there is no selection, retrieve the collapsed cursor.
		@return: The selection.
		@rtype: L{textInfos.TextInfo}
		"""
		try:
			return self.obj.makeTextInfo(textInfos.POSITION_SELECTION)
		except:  # noqa: E722
			return self.obj.makeTextInfo(textInfos.POSITION_FIRST)

	def _setCursor(self, info: textInfos.TextInfo):
		"""Set the cursor.
		@param info: The range to which the cursor should be moved.
		"""
		try:
			info.updateCaret()
		except NotImplementedError:
			log.debugWarning("", exc_info=True)

	def _getTypeformFromFormatField(self, field, formatConfig):
		typeform = louis.plain_text
		if not (
			(formatConfig["fontAttributeReporting"] & OutputMode.BRAILLE)
			and (
				config.conf["braille"]["fontFormattingDisplay"].calculated()
				== FontFormattingBrailleModeFlag.LIBLOUIS
			)
		):
			return typeform
		if field.get("bold", False):
			typeform |= louis.bold
		if field.get("italic", False):
			typeform |= louis.italic
		if field.get("underline", False):
			typeform |= louis.underline
		return typeform

	def _addFieldText(
		self,
		text: str,
		contentPos: int,
		separate: bool = True,
	):
		if separate and self.rawText:
			# Separate this field text from the rest of the text.
			text = TEXT_SEPARATOR + text
		textLen = len(text)
		# Fields are reported in NVDA's language
		fieldLanguage = languageHandler.getLanguage()
		rawTextLen = len(self.rawText)
		lastLanguage = self._getLanguageAtPos(rawTextLen)
		if fieldLanguage != lastLanguage:
			self._languageIndexes[rawTextLen] = fieldLanguage
			self._languageIndexes[rawTextLen + textLen] = lastLanguage
		self.rawText += text
		self.rawTextTypeforms.extend((louis.plain_text,) * textLen)
		self._rawToContentPos.extend((contentPos,) * textLen)

	def _addTextWithFields(self, info, formatConfig, isSelection=False):
		shouldMoveCursorToFirstContent = not isSelection and self.cursorPos is not None
		ctrlFields = []
		typeform = louis.plain_text
		formatFieldAttributesCache = getattr(info.obj, "_brailleFormatFieldAttributesCache", {})
		# When true, we are inside a clickable field, and should therefore not report any more new clickable fields
		inClickable = False
		# Collapsed ranges should never produce text and fields,
		# But later on we may still need to draw the cursor at this position.
		if not info.isCollapsed:
			commands = info.getTextWithFields(formatConfig=formatConfig)
		else:
			commands = []
		for command in commands:
			if isinstance(command, str):
				# Text should break a run of clickables
				inClickable = False
				self._isFormatFieldAtStart = False
				if not command:
					continue
				if self._endsWithField:
					# The last item added was a field,
					# so add a space before the content.
					self.rawText += TEXT_SEPARATOR
					self.rawTextTypeforms.append(louis.plain_text)
					self._rawToContentPos.append(self._currentContentPos)
				if isSelection and self.selectionStart is None:
					# This is where the content begins.
					self.selectionStart = len(self.rawText)
				elif shouldMoveCursorToFirstContent:
					# This is the first piece of content after the cursor.
					# Position the cursor here, as it may currently be positioned on control field text.
					self.cursorPos = len(self.rawText)
					shouldMoveCursorToFirstContent = False
				self.rawText += command
				commandLen = len(command)
				self.rawTextTypeforms.extend((typeform,) * commandLen)
				endPos = self._currentContentPos + commandLen
				self._rawToContentPos.extend(range(self._currentContentPos, endPos))
				self._currentContentPos = endPos
				if isSelection:
					# The last time this is set will be the end of the content.
					self.selectionEnd = len(self.rawText)
				self._endsWithField = False
			elif isinstance(command, textInfos.FieldCommand):
				cmd = command.command
				field = command.field
				if cmd == "formatChange":
					typeform = self._getTypeformFromFormatField(field, formatConfig)
					language = field.get("language")
					text = getFormatFieldBraille(
						field,
						formatFieldAttributesCache,
						self._isFormatFieldAtStart,
						formatConfig,
					)
					if text:
						# Map this field text to the start of the field's content.
						self._addFieldText(text, self._currentContentPos)
					rawTextLen = len(self.rawText)
					if language and self._getLanguageAtPos(rawTextLen) != language:
						self._languageIndexes[rawTextLen] = language
					if not text:
						continue
				elif cmd == "controlStart":
					if self._skipFieldsNotAtStartOfNode and not field.get("_startOfNode"):
						text = None
					else:
						textList = []
						if not inClickable and formatConfig["reportClickable"]:
							states = field.get("states")
							if states and controlTypes.State.CLICKABLE in states:
								# We have entered an outer most clickable or entered a new clickable after exiting a previous one
								# Report it if there is nothing else interesting about the field
								field._presCat = presCat = field.getPresentationCategory(
									ctrlFields,
									formatConfig,
								)
								if not presCat or presCat is field.PRESCAT_LAYOUT:
									textList.append(positiveStateLabels[controlTypes.State.CLICKABLE])
								inClickable = True
						text = info.getControlFieldBraille(field, ctrlFields, True, formatConfig)
						if text:
							textList.append(text)
						text = " ".join(textList)
					# Place this field on a stack so we can access it for controlEnd.
					ctrlFields.append(field)
					if not text:
						continue
					if getattr(field, "_presCat") == field.PRESCAT_MARKER:
						# In this case, the field text is what the user cares about,
						# not the actual content.
						fieldStart = len(self.rawText)
						if fieldStart > 0:
							# There'll be a space before the field text.
							fieldStart += 1
						if isSelection and self.selectionStart is None:
							self.selectionStart = fieldStart
						elif shouldMoveCursorToFirstContent:
							self.cursorPos = fieldStart
							shouldMoveCursorToFirstContent = False
					# Map this field text to the start of the field's content.
					self._addFieldText(text, self._currentContentPos)
				elif cmd == "controlEnd":
					# Exiting a controlField should break a run of clickables
					inClickable = False
					field = ctrlFields.pop()
					text = info.getControlFieldBraille(field, ctrlFields, False, formatConfig)
					if not text:
						continue
					# Map this field text to the end of the field's content.
					self._addFieldText(text, self._currentContentPos - 1)
				self._endsWithField = True
		if isSelection and self.selectionStart is None:
			# There is no selection. This is a cursor.
			self.cursorPos = len(self.rawText)
		if not self._skipFieldsNotAtStartOfNode:
			# We only render fields that aren't at the start of their nodes for the first part of the reading unit.
			# Otherwise, we'll render fields that have already been rendered.
			self._skipFieldsNotAtStartOfNode = True
		info.obj._brailleFormatFieldAttributesCache = formatFieldAttributesCache

	def _getReadingUnit(self):
		return textInfos.UNIT_PARAGRAPH if config.conf["braille"]["readByParagraph"] else textInfos.UNIT_LINE

	def update(self):
		formatConfig = config.conf["documentFormatting"]
		unit = self._getReadingUnit()
		self.rawText = ""
		self.rawTextTypeforms = []
		self.cursorPos = None
		self._languageIndexes: dict[int, str] = {0: self._getDefaultRegionLanguage()}
		# The output includes text representing fields which isn't part of the real content in the control.
		# Therefore, maintain a map of positions in the output to positions in the content.
		self._rawToContentPos = []
		self._currentContentPos = 0
		self.selectionStart = self.selectionEnd = None
		self._isFormatFieldAtStart = True
		self._skipFieldsNotAtStartOfNode = False
		self._endsWithField = False

		# Selection has priority over cursor.
		# HACK: Some TextInfos only support UNIT_LINE properly if they are based on POSITION_CARET,
		# and copying the TextInfo breaks this ability.
		# So use the original TextInfo for line and a copy for cursor/selection.
		self._readingInfo = readingInfo = self._getSelection()
		sel = readingInfo.copy()
		if not sel.isCollapsed:
			# There is a selection.
			if self.obj.isTextSelectionAnchoredAtStart:
				# The end of the range is exclusive, so make it inclusive first.
				readingInfo.move(textInfos.UNIT_CHARACTER, -1, "end")
			# Collapse the selection to the unanchored end.
			readingInfo.collapse(end=self.obj.isTextSelectionAnchoredAtStart)
			# Get the reading unit at the selection.
			readingInfo.expand(unit)
			# Restrict the selection to the reading unit.
			if sel.compareEndPoints(readingInfo, "startToStart") < 0:
				sel.setEndPoint(readingInfo, "startToStart")
			if sel.compareEndPoints(readingInfo, "endToEnd") > 0:
				sel.setEndPoint(readingInfo, "endToEnd")
		else:
			# There is a cursor.
			# Get the reading unit at the cursor.
			readingInfo.expand(unit)

		# Not all text APIs support offsets, so we can't always get the offset of the selection relative to the start of the reading unit.
		# Therefore, grab the reading unit in three parts.
		# First, the chunk from the start of the reading unit to the start of the selection.
		chunk = readingInfo.copy()
		chunk.collapse()
		chunk.setEndPoint(sel, "endToStart")
		self._addTextWithFields(chunk, formatConfig)
		# If the user is entering braille, place any untranslated braille before the selection.
		# Import late to avoid circular import.
		import brailleInput

		text = brailleInput.handler.untranslatedBraille
		if text:
			rawInputIndStart = len(self.rawText)
			# _addFieldText adds text to self.rawText and updates other state accordingly.
			self._addFieldText(INPUT_START_IND + text + INPUT_END_IND, None, separate=False)
			rawInputIndEnd = len(self.rawText)
		else:
			rawInputIndStart = None
		# Now, the selection itself.
		self._addTextWithFields(sel, formatConfig, isSelection=True)
		# Finally, get the chunk from the end of the selection to the end of the reading unit.
		chunk.setEndPoint(readingInfo, "endToEnd")
		chunk.setEndPoint(sel, "startToEnd")
		self._addTextWithFields(chunk, formatConfig)

		# Strip line ending characters.
		self.rawText = self.rawText.rstrip("\r\n\0\v\f")
		rawTextLen = len(self.rawText)
		if rawTextLen < len(self._rawToContentPos):
			# The stripped text is shorter than the original.
			self._currentContentPos = self._rawToContentPos[rawTextLen]
			del self.rawTextTypeforms[rawTextLen:]
			# Trimming _rawToContentPos doesn't matter,
			# because we'll only ever ask for indexes valid in rawText.
			# del self._rawToContentPos[rawTextLen:]
		if rawTextLen == 0 or not self._endsWithField:
			# There is no text left after stripping line ending characters,
			# or the last item added can be navigated with a cursor.
			# Add a space in case the cursor is at the end of the reading unit.
			self.rawText += TEXT_SEPARATOR
			rawTextLen += 1
			self.rawTextTypeforms.append(louis.plain_text)
			self._rawToContentPos.append(self._currentContentPos)
		if self.cursorPos is not None and self.cursorPos >= rawTextLen:
			self.cursorPos = rawTextLen - 1
		# The selection end doesn't have to be checked, Region.update() makes sure brailleSelectionEnd is valid.

		# If this is not the start of the object, hide all previous regions.
		start = readingInfo.obj.makeTextInfo(textInfos.POSITION_FIRST)
		self.hidePreviousRegions = start.compareEndPoints(readingInfo, "startToStart") < 0
		# Don't touch focusToHardLeft if it is already true
		# For example, it can be set to True in getFocusContextRegions when this region represents the first new focus ancestor
		# Alternatively, BrailleHandler._doNewObject can set this to True when this region represents the focus object and the focus ancestry didn't change
		if not self.focusToHardLeft:
			# If this is a multiline control, position it at the absolute left of the display when focused.
			self.focusToHardLeft = self._isMultiline()
		super(TextInfoRegion, self).update()

		if rawInputIndStart is not None:
			assert rawInputIndEnd is not None, "rawInputIndStart set but rawInputIndEnd isn't"
			# These are the start and end of the untranslated input area,
			# including the start and end indicators.
			self._brailleInputIndStart = self.rawToBraillePos[rawInputIndStart]
			self._brailleInputIndEnd = self.rawToBraillePos[rawInputIndEnd]
			# These are the start and end of the actual untranslated input, excluding indicators.
			self._brailleInputStart = self._brailleInputIndStart + len(INPUT_START_IND)
			self._brailleInputEnd = self._brailleInputIndEnd - len(INPUT_END_IND)
			self.brailleCursorPos = self._brailleInputStart + brailleInput.handler.untranslatedCursorPos
		else:
			self._brailleInputIndStart = None

	def getTextInfoForBraillePos(self, braillePos: int) -> textInfos.TextInfo:
		"""Fetches a collapsed TextInfo at the specified braille position in the region.
		:param braillePos: The braille position.
			If no textInfo could be found at braillePos,
			try to find one at braillePos - 1 until a position has been found.
		"""
		pos = self._rawToContentPos[self.brailleToRawPos[braillePos]]
		# pos is relative to the start of the reading unit.
		maxIterations = 10
		startTime = time.time()
		for i, curPos in enumerate(range(pos, max(-1, pos - maxIterations), -1)):
			if curPos == 0:
				# Not necessary to find offset.
				break
			# Move curPos code points from the start.
			# Note that, as liblouis uses 32 bit encoding internally,
			# it is really safe to assume that one code point offset is equal to one character within liblouis.
			# If an attempt fails, we try to move to the previous character
			try:
				return self._readingInfo.moveToCodepointOffset(curPos)
			except RuntimeError:
				msg = f"Error in moveToCodepointOffset in iteration {i + 1} (position {curPos}"
				if i + 1 >= maxIterations or (exceeded := time.time() - startTime > 0.5):
					logFunc = log.exception
					curPos = pos
					if exceeded:
						msg += ", exceeded time limit of 0.5 seconds"
				else:
					logFunc = log.debug
				logFunc(msg)
		dest = self._readingInfo.copy()
		dest.collapse()
		if curPos > 0:
			dest.move(textInfos.UNIT_CHARACTER, curPos)
		return dest

	def routeTo(self, braillePos: int):
		if (
			self._brailleInputIndStart is not None
			and self._brailleInputIndStart <= braillePos < self._brailleInputIndEnd
		):
			# The user is moving within untranslated braille input.
			if braillePos < self._brailleInputStart:
				# The user routed to the start indicator. Route to the start of the input.
				braillePos = self._brailleInputStart
			elif braillePos > self._brailleInputEnd:
				# The user routed to the end indicator. Route to the end of the input.
				braillePos = self._brailleInputEnd
			# Import late to avoid circular import.
			import brailleInput

			brailleInput.handler.untranslatedCursorPos = braillePos - self._brailleInputStart
			self.brailleCursorPos = self._brailleInputStart + brailleInput.handler.untranslatedCursorPos
			brailleInput.handler.updateDisplay()
			return

		dest = self.getTextInfoForBraillePos(braillePos)
		self._routeToTextInfo(dest)

	def _routeToTextInfo(self, info: textInfos.TextInfo):
		# When there is a selection, brailleCursorPos will be None
		# Don't activate, but move the cursor to the new cell (dropping the
		# selection). An alternative behavior may be to activate on the selection.
		# Moving the cursor was considered more intuitive.
		if self.brailleCursorPos is not None:
			cursor = self.getTextInfoForBraillePos(self.brailleCursorPos)
			if info.compareEndPoints(cursor, "startToStart") == 0:
				# The cursor is already at this position,
				# so activate the position.
				try:
					self._getSelection().activate()
				except NotImplementedError:
					pass
				return
		self._setCursor(info)
		_speakOnRouting(info.copy())

	def nextLine(self):
		dest = self._readingInfo.copy()
		shouldCollapseToEnd = False
		moved = dest.move(self._getReadingUnit(), 1)
		if not moved:
			if self.allowPageTurns and isinstance(dest.obj, textInfos.DocumentWithPageTurns):
				try:
					dest.obj.turnPage()
				except RuntimeError:
					braille.handler.autoScroll(enable=False)
				else:
					dest = dest.obj.makeTextInfo(textInfos.POSITION_FIRST)
			else:  # no page turn support
				braille.handler.autoScroll(enable=False)
				shouldCollapseToEnd = True
		dest.collapse(shouldCollapseToEnd)
		self._setCursor(dest)
		_speakOnNavigatingByUnit(dest, self._getReadingUnit())

	def previousLine(self, start=False):
		dest = self._readingInfo.copy()
		dest.collapse()
		if start:
			unit = self._getReadingUnit()
		else:
			# If the end of the reading unit is desired, move to the last character.
			unit = textInfos.UNIT_CHARACTER
		moved = dest.move(unit, -1)
		if not moved:
			if self.allowPageTurns and isinstance(dest.obj, textInfos.DocumentWithPageTurns):
				try:
					dest.obj.turnPage(previous=True)
				except RuntimeError:
					pass
				else:
					dest = dest.obj.makeTextInfo(textInfos.POSITION_LAST)
					dest.expand(unit)
			else:
				# no page turn support
				return
		dest.collapse()
		self._setCursor(dest)
		_speakOnNavigatingByUnit(dest, self._getReadingUnit())


class CursorManagerRegion(TextInfoRegion):
	def _isMultiline(self):
		return True

	def _getSelection(self):
		return self.obj.selection

	def _setCursor(self, info: textInfos.TextInfo):
		self.obj.selection = info


class ReviewTextInfoRegion(TextInfoRegion):
	allowPageTurns = False

	def _getSelection(self):
		return api.getReviewPosition().copy()

	def _routeToTextInfo(self, info: textInfos.TextInfo):
		super()._routeToTextInfo(info)
		if not _routingShouldMoveSystemCaret():
			return
		from displayModel import DisplayModelTextInfo, EditableTextDisplayModelTextInfo

		if isinstance(info, DisplayModelTextInfo) and not isinstance(info, EditableTextDisplayModelTextInfo):
			# This region either reviews the screen or an object that has
			# DisplayModelTextInfo without a caret, e.g. IAccessible.ContentGenericClient.
			# In this case, we can at least emulate a kind of caret
			# by trying to focus the object at start of the range.
			obj = info.NVDAObjectAtStart
			if not objectBelowLockScreenAndWindowsIsLocked(obj) and obj.isFocusable and not obj.hasFocus:
				obj.setFocus()
		else:
			# Update the physical caret using the super class.
			super()._setCursor(info)

	def _setCursor(self, info: textInfos.TextInfo):
		api.setReviewPosition(info)


class ReviewCursorManagerRegion(ReviewTextInfoRegion, CursorManagerRegion): ...


def _routingShouldMoveSystemCaret() -> bool:
	"""Returns whether pressing a braille routing key should move the system caret."""
	reviewRoutingMovesSystemCaret = config.conf["braille"]["reviewRoutingMovesSystemCaret"].calculated()
	configuredTether = config.conf["braille"]["tetherTo"]
	shouldMoveCaretTetheredReview = (
		configuredTether == TetherTo.REVIEW.value
		and reviewRoutingMovesSystemCaret == ReviewRoutingMovesSystemCaretFlag.ALWAYS
	)
	shouldMoveCaretTetheredAuto = (
		configuredTether == TetherTo.AUTO.value
		and reviewRoutingMovesSystemCaret != ReviewRoutingMovesSystemCaretFlag.NEVER
	)
	return shouldMoveCaretTetheredAuto or shouldMoveCaretTetheredReview


def rindex(seq, item, start, end):
	for index in range(end - 1, start - 1, -1):
		if seq[index] == item:
			return index
	raise ValueError("%r is not in sequence" % item)


def _speakOnRouting(info: textInfos.TextInfo):
	"""Speaks the character at the cursor position after routing.

	:param info: The TextInfo at the cursor position after routing.
	"""
	if not config.conf["braille"]["speakOnRouting"]:
		return
	# Import late to avoid circular import.
	from speech.speech import spellTextInfo

	info.expand(textInfos.UNIT_CHARACTER)
	spellTextInfo(info)


def _speakOnNavigatingByUnit(info: textInfos.TextInfo, readingUnit: str) -> None:
	"""Speaks the reading unit after navigating by it with braille.

	This only has an effect if the user has enabled "Speak when navigating by line or paragraph" in braille settings.

	:param info: The TextInfo at the cursor position after navigating.
	:param readingUnit: The reading unit to expand TextInfo.
	"""
	if not config.conf["braille"]["speakOnNavigatingByUnit"]:
		return
	# Import late to avoid circular import.
	from speech.speech import cancelSpeech, speakTextInfo

	copy = info.copy()
	copy.expand(readingUnit)
	cancelSpeech()
	speakTextInfo(copy, unit=readingUnit, reason=controlTypes.OutputReason.CARET)
