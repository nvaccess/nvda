# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Flags used for the configuration.
"""
from enum import unique
from utils.displayString import DisplayStringIntEnum


@unique
class ReportTableHeaders(DisplayStringIntEnum):
	"""The possible config values to report table headers.
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
