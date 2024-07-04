# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	Dict,
	Protocol,
	Union,
)


class _SupportsStrT(Protocol):
	"""
	Valid config values must support str(),
	as this is how they are written to disk
	"""

	def __str__(self) -> str: ...


_cacheKeyT = str
_cacheValueT = Union["_cacheT", _SupportsStrT, KeyError]
_cacheT = Dict[str, _cacheValueT]
