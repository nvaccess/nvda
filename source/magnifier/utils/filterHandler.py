# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from enum import Enum
from winBindings.magnification import MAGCOLOREFFECT


def _createColorEffect(
		matrix: tuple,
) -> MAGCOLOREFFECT:
	"""Create a MAGCOLOREFFECT from a flat matrix tuple."""
	effect = MAGCOLOREFFECT()
	for i in range(5):
		for j in range(5):
			effect.transform[i][j] = matrix[i * 5 + j]
	return effect


class FilterMatrix(Enum):
	NORMAL = _createColorEffect(
		(
			1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
		)
	)

	GRAYSCALE = _createColorEffect(
		(
			0.33,
			0.33,
			0.33,
			0.0,
			0.0,
			0.59,
			0.59,
			0.59,
			0.0,
			0.0,
			0.11,
			0.11,
			0.11,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
		)
	)

	INVERTED = _createColorEffect(
		(
			-1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			-1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			-1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
			0.0,
			1.0,
			1.0,
			1.0,
			0.0,
			1.0,
		),
	)
