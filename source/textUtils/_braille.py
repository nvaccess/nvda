# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Wang Chong, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from typing import cast

from louisHelper import Typeform
from textUtils import OffsetConverter


def _applyOffsetConverter(
	converter: OffsetConverter,
	textToTranslateTypeforms: list[Typeform] | None,
	cursorPos: int | None,
) -> tuple[str, list[Typeform] | None, int | None]:
	if textToTranslateTypeforms is not None:
		textToTranslateTypeforms = [
			textToTranslateTypeforms[cast(int, converter.encodedToStrOffsets(encodedOffset))]
			for encodedOffset in range(converter.encodedStringLength)
		]
	if cursorPos is not None:
		cursorPos = cast(int, converter.strToEncodedOffsets(cursorPos))
	return cast(str, getattr(converter, "encoded")), textToTranslateTypeforms, cursorPos
