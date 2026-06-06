# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

import typing
from typing import (
	Dict,
	Any,
	Optional,
	Set,
	Union,
)

import config
import controlTypes
import textInfos
from annotation import _AnnotationRolesT
from config.configFlags import ReportTableHeaders
from config.featureFlagEnums import FontFormattingBrailleModeFlag
from controlTypes.state import State
from logHandler import log

from ..constants import TEXT_SEPARATOR
from ..formatting import (
	_getFormattingTags,
	getParagraphStartMarker,
)
from ..labels import (
	landmarkLabels,
	negativeStateLabels,
	positiveStateLabels,
	roleLabels,
)


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
