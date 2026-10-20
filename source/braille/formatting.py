# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Braille font-formatting markers and the helpers that render them into format-field braille."""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple

import config
from config.configFlags import (
	OutputMode,
	ReportSpellingErrors,
)


class FormatTagDelimiter(StrEnum):
	"""Delimiters for the start and end of format tags.

	As these are shapes, they should be provided in unicode braille.
	"""

	START = "⣋"
	END = "⣙"


class FormattingMarker(NamedTuple):
	"""A pair of braille symbols that indicate the start and end of a particular type of font formatting.

	As these are shapes, they should be provided in unicode braille.
	"""

	start: str
	end: str

	def shouldBeUsed(self, key) -> bool:
		"""Determines if the formatting marker should be reported in braille.
		:param key: A key which represents an element that may be reported in braille.
		:return: `True` if the element should be reported, `False` otherwise.
		"""
		formatConfig = config.conf["documentFormatting"]
		if key in ("invalid-spelling", "invalid-grammar"):
			return bool(formatConfig["reportSpellingErrors2"] & ReportSpellingErrors.BRAILLE)
		return formatConfig["fontAttributeReporting"] & OutputMode.BRAILLE


fontAttributeFormattingMarkers: dict[str, FormattingMarker] = {
	"bold": FormattingMarker(
		# Translators: Brailled at the start of bold text.
		# This is the English letter "b" in braille.
		start=pgettext("braille formatting symbol", "⠃"),
		# Translators: Brailled at the end of bold text.
		# This is the English letter "b" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡃"),
	),
	"italic": FormattingMarker(
		# Translators: Brailled at the start of italic text.
		# This is the English letter "i" in braille.
		start=pgettext("braille formatting symbol", "⠊"),
		# Translators: Brailled at the end of italic text.
		# This is the English letter "i" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡊"),
	),
	"underline": FormattingMarker(
		# Translators: Brailled at the start of underlined text.
		# This is the English letter "u" in braille.
		start=pgettext("braille formatting symbol", "⠥"),
		# Translators: Brailled at the end of underlined text.
		# This is the English letter "u" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡥"),
	),
	"strikethrough": FormattingMarker(
		# Translators: Brailled at the start of strikethrough text.
		# This is the English letter "s" in braille.
		start=pgettext("braille formatting symbol", "⠎"),
		# Translators: Brailled at the end of strikethrough text.
		# This is the English letter "s" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡎"),
	),
	"invalid-spelling": FormattingMarker(
		# Translators: Brailled at the start of invalid spelling text.
		# This is the English letter "e" in braille.
		start=pgettext("braille formatting symbol", "⠑"),
		# Translators: Brailled at the end of invalid spelling text.
		# This is the English letter "e" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡑"),
	),
	"invalid-grammar": FormattingMarker(
		# Translators: Brailled at the start of invalid grammar text.
		# This is the English letter "g" in braille.
		start=pgettext("braille formatting symbol", "⠛"),
		# Translators: Brailled at the end of invalid grammar text.
		# This is the English letter "g" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡛"),
	),
}


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
