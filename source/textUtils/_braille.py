# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Wang Chong
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import cast

from textUtils import OffsetConverter


def _applyOffsetConverter(
	converter: OffsetConverter,
	textToTranslateTypeforms: list[int] | None,
	cursorPos: int | None,
) -> tuple[str, list[int] | None, int | None]:
	if textToTranslateTypeforms is not None:
		textToTranslateTypeforms = [
			textToTranslateTypeforms[cast(int, converter.encodedToStrOffsets(encodedOffset))]
			for encodedOffset in range(converter.encodedStringLength)
		]
	if cursorPos is not None:
		cursorPos = cast(int, converter.strToEncodedOffsets(cursorPos))
	return cast(str, getattr(converter, "encoded")), textToTranslateTypeforms, cursorPos
