# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Flags used for the configuration."""

from enum import unique
from utils.displayString import DisplayStringIntEnum


@unique
class ShowMessages(DisplayStringIntEnum):
	"""Enumeration containing the possible config values for "Show messages" option in braille settings.
	
	Use ShowMessages.MEMBER.value to compare with the config;
	use ShowMessages.MEMBER.displayString in the UI for a translatable description of this member.
	"""
	
	DISABLED = 0
	USE_TIMEOUT = 1
	SHOW_INDEFINITELY = 2
	
	@property
	def _displayStringLabels(self):
		return {
			# Translators: One of the show states of braille messages
			# (the disabled mode turns off showing of braille messages completely).
			ShowMessages.DISABLED: _("Disabled"),
			# Translators: One of the show states of braille messages
			# (the timeout mode shows messages for the specific time).
			ShowMessages.USE_TIMEOUT: _("Use timeout"),
			# Translators: One of the show states of braille messages
			# (the indefinitely mode prevents braille messages from disappearing automatically).
			ShowMessages.SHOW_INDEFINITELY: _("Show indefinitely"),
		}


@unique
class ReportLineIndentation(DisplayStringIntEnum):
	"""Enumeration containing the possible config values to report line indent.
	
	Use ReportLineIndentation.MEMBER.value to compare with the config;
	use ReportLineIndentation.MEMBER.displayString in the UI for a translatable description of this member.
	"""
	
	OFF = 0
	SPEECH = 1
	TONES = 2
	SPEECH_AND_TONES = 3
	
	@property
	def _displayStringLabels(self):
		return {
			# Translators: A choice in a combo box in the document formatting dialog to report No line Indentation.
			ReportLineIndentation.OFF: _("Off"),
			# Translators: A choice in a combo box in the document formatting dialog to report indentation
			# with Speech.
			ReportLineIndentation.SPEECH: pgettext('line indentation setting', "Speech"),
			# Translators: A choice in a combo box in the document formatting dialog to report indentation
			# with tones.
			ReportLineIndentation.TONES: _("Tones"),
			# Translators: A choice in a combo box in the document formatting dialog to report indentation with both
			# Speech and tones.
			ReportLineIndentation.SPEECH_AND_TONES: _("Both Speech and Tones"),
		}


@unique
class ReportTableHeaders(DisplayStringIntEnum):
	"""Enumeration containing the possible config values to report table headers.
	
	Use ReportTableHeaders.MEMBER.value to compare with the config;
	use ReportTableHeaders.MEMBER.displayString in the UI for a translatable description of this member.
	"""
	
	OFF = 0
	ROWS_AND_COLUMNS = 1
	ROWS = 2
	COLUMNS = 3
	
	@property
	def _displayStringLabels(self):
		return {
			# Translators: This is the label for a combobox in the
			# document formatting settings panel.
			ReportTableHeaders.OFF: _("Off"),
			# Translators: This is the label for a combobox in the
			# document formatting settings panel.
			ReportTableHeaders.ROWS_AND_COLUMNS: _("Rows and columns"),
			# Translators: This is the label for a combobox in the
			# document formatting settings panel.
			ReportTableHeaders.ROWS: _("Rows"),
			# Translators: This is the label for a combobox in the
			# document formatting settings panel.
			ReportTableHeaders.COLUMNS: _("Columns"),
		}
