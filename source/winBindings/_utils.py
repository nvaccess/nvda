# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Akash Kakkar
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from typing import Any


def _makeUnavailable(name: str, message: str, loadError: Exception | None) -> Any:
	def unavailable(*args: Any, **kwargs: Any) -> None:
		raise OSError(message) from loadError

	unavailable.__name__ = name
	return unavailable
