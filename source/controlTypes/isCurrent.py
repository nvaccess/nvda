# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2021 NV Access Limited, Babbage B.V.

from enum import Enum
from typing import Dict

from logHandler import log


class IsCurrent(Enum):
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
	def displayString(self):
		"""
		@return: The translated UI display string that should be used for this value of the IsCurrent enum
		"""
		try:
			return _isCurrentLabels[self]
		except KeyError:
			log.debugWarning(f"No translation mapping for: {self}")
			# there is a value for 'current' but NVDA hasn't learned about it yet,
			# at least describe in the general sense that this item is 'current'
			return _isCurrentLabels[IsCurrent.YES]


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
