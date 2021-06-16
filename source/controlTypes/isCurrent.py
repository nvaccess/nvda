# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2021 NV Access Limited, Babbage B.V.

from typing import Dict

from utils.displayString import DisplayStringStrEnum


class IsCurrent(DisplayStringStrEnum):
	"""Values to use within NVDA to denote 'current' values.
	These describe if an item is the current item within a particular kind of selection.
	EG aria-current
	"""
	NO = "false"
	YES = "true"
	PAGE = "page"
	STEP = "step"
	LOCATION = "location"
	DATE = "date"
	TIME = "time"

	@property
	def _displayStringLabels(self):
		return _isCurrentLabels

	@property
	def displayString(self):
		try:
			return super().displayString
		except KeyError:
			return self.YES.displayString


#: Text to use for 'current' values. These describe if an item is the current item
#: within a particular kind of selection. EG aria-current
_isCurrentLabels: Dict[IsCurrent, str] = {
	IsCurrent.NO: "",  # There is nothing extra to say for items that are not current.
	# Translators: Presented when an item is marked as current in a collection of items
	IsCurrent.YES: _("current"),
	# Translators: Presented when a page item is marked as current in a collection of page items
	IsCurrent.PAGE: _("current page"),
	# Translators: Presented when a step item is marked as current in a collection of step items
	IsCurrent.STEP: _("current step"),
	# Translators: Presented when a location item is marked as current in a collection of location items
	IsCurrent.LOCATION: _("current location"),
	# Translators: Presented when a date item is marked as current in a collection of date items
	IsCurrent.DATE: _("current date"),
	# Translators: Presented when a time item is marked as current in a collection of time items
	IsCurrent.TIME: _("current time"),
}
