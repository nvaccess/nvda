# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from urllib.parse import urlparse


def _valueToSamePage(value: str, constantIdentifier: str) -> bool:
	if not value or not constantIdentifier:
		return False
	# Parse the URLs
	valueParsed = urlparse(value)
	constantIdentifierParsed = urlparse(constantIdentifier)
	# Compare the netloc and path
	if (
		valueParsed.scheme == constantIdentifierParsed.scheme
		and valueParsed.netloc == constantIdentifierParsed.netloc
		and valueParsed.path == constantIdentifierParsed.path
		and valueParsed.fragment
	):
		return True
	return False
