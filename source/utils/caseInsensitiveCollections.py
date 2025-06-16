# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from typing import (
	Iterable,
)


class CaseInsensitiveSet(set):
	def __init__(self, *args: Iterable[str]):
		if len(args) > 1:
			raise TypeError(
				f"{type(self).__name__} expected at most 1 argument, got {len(args)}",
			)
		values = args[0] if args else ()
		for v in values:
			self.add(v)

	def add(self, __element: str) -> None:
		__element = __element.casefold()
		return super().add(__element)

	def discard(self, __element: str) -> None:
		__element = __element.casefold()
		return super().discard(__element)

	def remove(self, __element: str) -> None:
		__element = __element.casefold()
		return super().remove(__element)

	def __contains__(self, __o: object) -> bool:
		if isinstance(__o, str):
			__o = __o.casefold()
		return super().__contains__(__o)
