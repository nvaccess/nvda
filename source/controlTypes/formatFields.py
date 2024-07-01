# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021-2023 NV Access Limited, Cyrille Bougot

import re
from typing import Dict

from logHandler import log
from utils.displayString import DisplayStringStrEnum


class TextPosition(DisplayStringStrEnum):
	"""Values to use for 'text-position' NVDA format field.
	These describe the vertical position of the text with respect to the base line.
	"""
	UNDEFINED = 'undefined'
	BASELINE = 'baseline'
	SUBSCRIPT = 'sub'
	SUPERSCRIPT = 'super'

	@property
	def _displayStringLabels(self):
		return _textPositionLabels


#: Text to use for 'text-position' format field values. These describe the vertical position of the
#: formatted text with respect to the base line.
_textPositionLabels: Dict[TextPosition, str] = {
	TextPosition.UNDEFINED: "",  # There is nothing to report if no text position is defined.
	# Translators: Reported for text which is at the baseline position;
	# i.e. not superscript or subscript.
	TextPosition.BASELINE: _("baseline"),
	# Translators: Reported for subscript text.
	TextPosition.SUBSCRIPT: _("subscript"),
	# Translators: Reported for superscript text.
	TextPosition.SUPERSCRIPT: _("superscript"),
}


class FontSize:
	_unitToTranslatableString: Dict[str, str] = {
		# Translators: Abbreviation for pixels, a measurement of font size.
		"px": pgettext("font size", "%s px"),
		# Translators: A measurement unit of font size.
		"em": pgettext("font size", "%s em"),
		# Translators: A measurement unit of font size.
		"ex": pgettext("font size", "%s ex"),
		# Translators: Abbreviation for relative em, a measurement of font size.
		"rem": pgettext("font size", "%s rem"),
		# Translators: Abbreviation for points, a measurement of font size.
		"pt": pgettext("font size", "%s pt"),
		# Translators: Font size measured as a percentage
		"%": pgettext("font size", "%s%%"),
	}

	_keywordToTranslatableString: Dict[str, str] = {
		# Translators: A measurement unit of font size.
		"xx-small": pgettext("font size", "xx-small"),
		# Translators: A measurement unit of font size.
		"x-small": pgettext("font size", "x-small"),
		# Translators: A measurement unit of font size.
		"small": pgettext("font size", "small"),
		# Translators: A measurement unit of font size.
		"medium": pgettext("font size", "medium"),
		# Translators: A measurement unit of font size.
		"large": pgettext("font size", "large"),
		# Translators: A measurement unit of font size.
		"x-large": pgettext("font size", "x-large"),
		# Translators: A measurement unit of font size.
		"xx-large": pgettext("font size", "xx-large"),
		# Translators: A measurement unit of font size.
		"xxx-large": pgettext("font size", "xxx-large"),
		# Translators: A measurement unit of font size.
		"larger": pgettext("font size", "larger"),
		# Translators: A measurement unit of font size.
		"smaller": pgettext("font size", "smaller")
	}

	_measurementRe = re.compile(r"([0-9\.]+)(px|em|ex|rem|pt|%)")

	@staticmethod
	def translateFromAttribute(fontSize: str) -> str:
		"""
		@param fontSize:
		Browsers provide the value of the font-size attribute directly,
		either as a measurement or as keywords. These aren't translated.
		https://developer.mozilla.org/en-US/docs/Web/CSS/font-size#values
		
		@return: a translated font size string.
		"""
		if fontSize in FontSize._keywordToTranslatableString:
			return FontSize._keywordToTranslatableString[fontSize]
		fontSizeMeasurement = re.match(FontSize._measurementRe, fontSize)
		if fontSizeMeasurement:
			measurement = fontSizeMeasurement.group(1)
			measurementUnit = fontSizeMeasurement.group(2)
			if measurementUnit in FontSize._unitToTranslatableString:
				return FontSize._unitToTranslatableString[measurementUnit] % measurement
		log.debugWarning(f"Unknown font-size value, can't translate '{fontSize}'")
		return fontSize


class TextAlign(DisplayStringStrEnum):
	"""Values to use for 'text-align' NVDA format field.
	These describe the horizontal paragraph position.
	"""
	UNDEFINED = 'undefined'
	LEFT = 'left'
	CENTER = 'center'
	RIGHT = 'right'
	JUSTIFY = 'justify'
	DISTRIBUTE = 'distribute'
	CENTER_ACROSS_SELECTION = 'center-across-selection'
	GENERAL = 'general'
	FILL = 'fill'

	@property
	def _displayStringLabels(self):
		return _textAlignLabels


#: Text to use for 'text-align format field values. These describe the horizontal position of a paragraph
#: or a cell's content.
_textAlignLabels: Dict[TextAlign, str] = {
	TextAlign.UNDEFINED: "",  # There is nothing to report if no alignment is defined.
	# Translators: Reported when text is left-aligned.
	TextAlign.LEFT: _("align left"),
	# Translators: Reported when text is centered.
	TextAlign.CENTER: _("align center"),
	# Translators: Reported when text is right-aligned.
	TextAlign.RIGHT: _("align right"),
	# Translators: Reported when text is justified.
	# See http://en.wikipedia.org/wiki/Typographic_alignment#Justified
	TextAlign.JUSTIFY: _("align justify"),
	# Translators: Reported when text is justified with character spacing (Japanese etc)
	# See http://kohei.us/2010/01/21/distributed-text-justification/
	TextAlign.DISTRIBUTE: _("align distributed"),
	# Translators: Reported when text is centered across multiple cells.
	TextAlign.CENTER_ACROSS_SELECTION: _("align centered across selection"),
	# Translators: Reported in Excel when text is formatted with "General" alignment, i.e. the name of the
	# alignment in Excel aligning the cell's content depending on its type: text left and numbers right.
	TextAlign.GENERAL: _("align general"),
	# Translators: Reported in Excel when text is formatted with "Fill" alignment, i.e. the name of the
	# alignment in Excel repeating the cell's content for the width of the cell.
	TextAlign.FILL: _("align fill"),
}


class VerticalTextAlign(DisplayStringStrEnum):
	"""Values to use for 'vertical-align' NVDA format field.
	These describe the vertical text position, e.g. in a table cell.
	"""
	UNDEFINED = 'undefined'
	TOP = 'top'
	CENTER = 'center'
	BOTTOM = 'bottom'
	JUSTIFY = 'justify'
	DISTRIBUTE = 'distributed'

	@property
	def _displayStringLabels(self):
		return _verticalTextAlignLabels


#: Text to use for 'vertical-align' format field values. These describe the vertical position
#: of a cell's content.
_verticalTextAlignLabels: Dict[VerticalTextAlign, str] = {
	VerticalTextAlign.UNDEFINED: "",  # There is nothing to report if no vertical alignment is defined.
	# Translators: Reported when text is vertically top-aligned.
	VerticalTextAlign.TOP: _("vertical align top"),
	# Translators: Reported when text is vertically middle aligned.
	VerticalTextAlign.CENTER: _("vertical align middle"),
	# Translators: Reported when text is vertically bottom-aligned.
	VerticalTextAlign.BOTTOM: _("vertical align bottom"),
	# Translators: Reported when text is vertically justified.
	VerticalTextAlign.JUSTIFY: _("vertical align justified"),
	# Translators: Reported when text is vertically justified but with character spacing
	# (For some Asian content).
	VerticalTextAlign.DISTRIBUTE: _("vertical align distributed"),
}
