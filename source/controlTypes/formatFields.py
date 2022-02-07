# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited, Cyrille Bougot

from typing import Dict

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
