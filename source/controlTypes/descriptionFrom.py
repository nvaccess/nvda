# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited

from enum import (
	auto,
	Enum,
)


class DescriptionFrom(Enum):
	"""Values to use within NVDA to denote possible values for DescriptionFrom.
	These are used to determine how the source of the 'description' property if an NVDAObject.
	"""
	UNKNOWN = auto()
	ARIA_DESCRIPTION = "aria-description"
	ARIA_DESCRIBED_BY = "aria-describedby"
	RUBY_ANNOTATION = "ruby-annotation"
	SUMMARY = "summary"
	TABLE_CAPTION = "table-caption"
	TOOLTIP = "tooltip"  # (either via @title or aria-describedby + role="tooltip")
	BUTTON_LABEL = "button-label"
