# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2024 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Flags used to define the possible values for an option in the configuration.
Use Flag.MEMBER.value to set a new value or compare with an option in the config;
use Flag.MEMBER.displayString in the UI for a translatable description of this member.

When creating new parameter options, consider using F{FeatureFlag} which explicitely defines
the default value.
"""

from enum import unique
from utils.displayString import (
	DisplayStringIntEnum,
	DisplayStringStrEnum,
	DisplayStringIntFlag,
)


@unique
class NVDAKey(DisplayStringIntFlag):
	"""IntFlag enumeration containing the possible config values for "Select NVDA Modifier Keys" option in
	keyboard settings.
	
	Use NVDAKey.MEMBER.value to compare with the config;
	the config stores a bitwise combination of one or more of these values.
	use NVDAKey.MEMBER.displayString in the UI for a translatable description of this member.
	"""
	
	CAPS_LOCK = 1
	NUMPAD_INSERT = 2
	EXTENDED_INSERT = 4
	
	@property
	def _displayStringLabels(self):
		# Imported lazily since this module is imported before gettext translation is installed.
		from keyLabels import localizedKeyLabels
		return {
			NVDAKey.CAPS_LOCK: localizedKeyLabels['capslock'],
			NVDAKey.NUMPAD_INSERT: localizedKeyLabels['numpadinsert'],
			NVDAKey.EXTENDED_INSERT: localizedKeyLabels['insert'],
		}


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
class TetherTo(DisplayStringStrEnum):
	"""Enumeration containing the possible config values for "Tether to" option in braille settings.
	
	Use TetherTo.MEMBER.value to compare with the config;
	use TetherTo.MEMBER.displayString in the UI for a translatable description of this member.
	"""
	
	AUTO = "auto"
	FOCUS = "focus"
	REVIEW = "review"
	
	@property
	def _displayStringLabels(self):
		return {
			# Translators: The label for a braille setting indicating that braille should be
			# tethered to focus or review cursor automatically.
			TetherTo.AUTO: _("automatically"),
			# Translators: The label for a braille setting indicating that braille should be tethered to focus.
			TetherTo.FOCUS: _("to focus"),
			# Translators: The label for a braille setting indicating that braille should be tethered
			# to the review cursor.
			TetherTo.REVIEW: _("to review"),
		}


@unique
class BrailleMode(DisplayStringStrEnum):
	"""Enumeration containing the possible config values for "Braille mode" option in braille settings.
	Use BrailleMode.MEMBER.value to compare with the config;
	use BrailleMode.MEMBER.displayString in the UI for a translatable description of this member.
	"""
	FOLLOW_CURSORS = "followCursors"
	SPEECH_OUTPUT = "speechOutput"

	@property
	def _displayStringLabels(self) -> dict["BrailleMode", str]:
		return {
			# Translators: The label for a braille mode
			BrailleMode.FOLLOW_CURSORS: _("follow cursors"),
			# Translators: The label for a braille mode
			BrailleMode.SPEECH_OUTPUT: _("display speech output")
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
			ReportLineIndentation.OFF: pgettext('line indentation setting', "Off"),
			# Translators: A choice in a combo box in the document formatting dialog to report indentation
			# with Speech.
			ReportLineIndentation.SPEECH: pgettext('line indentation setting', "Speech"),
			# Translators: A choice in a combo box in the document formatting dialog to report indentation
			# with tones.
			ReportLineIndentation.TONES: pgettext('line indentation setting', "Tones"),
			# Translators: A choice in a combo box in the document formatting dialog to report indentation with both
			# Speech and tones.
			ReportLineIndentation.SPEECH_AND_TONES: pgettext('line indentation setting', "Both Speech and Tones"),
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


@unique
class ReportCellBorders(DisplayStringIntEnum):
	"""Enumeration containing the possible config values to report cell borders.
	
	Use ReportCellBorders.MEMBER.value to compare with the config;
	use ReportCellBorders.MEMBER.displayString in the UI for a translatable description of this member.
	"""
	
	OFF = 0
	STYLE = 1
	COLOR_AND_STYLE = 2
	
	@property
	def _displayStringLabels(self):
		return {
			# Translators: This is the label for a combobox in the
			# document formatting settings panel.
			ReportCellBorders.OFF: _("Off"),
			# Translators: This is the label for a combobox in the
			# document formatting settings panel.
			ReportCellBorders.STYLE: _("Styles"),
			# Translators: This is the label for a combobox in the
			# document formatting settings panel.
			ReportCellBorders.COLOR_AND_STYLE: _("Both Colors and Styles"),
		}


class AddonsAutomaticUpdate(DisplayStringStrEnum):
	NOTIFY = "notify"
	# TODO: uncomment when implementing #3208
	# UPDATE = "update"
	DISABLED = "disabled"

	@property
	def _displayStringLabels(self):
		return {
			# Translators: This is a label for the automatic update behaviour for add-ons.
			# It will notify the user when updates are available.
			self.NOTIFY: _("Notify"),
			# self.UPDATE: _("Update Automatically"),
			# Translators: This is a label for the automatic update behaviour for add-ons.
			self.DISABLED: _("Disabled"),
		}
