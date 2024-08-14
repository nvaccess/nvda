# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2024 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


def _valueToSamePage(value: str, constantIdentifier: str) -> bool:
	"""Function used to check if link destination points to the same page"""
	if not value or not constantIdentifier:
		return False
	if constantIdentifier.endswith("/"):
		constantIdentifier = constantIdentifier[:-1]
	queryParamCharPos = constantIdentifier.find("?")
	if queryParamCharPos > 0:
		constantIdentifier = constantIdentifier[:queryParamCharPos]
	if value.startswith(f"{constantIdentifier}#"):
		return True
	return False
