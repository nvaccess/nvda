# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import ctypes
from enum import Enum


class FilterMatrix(Enum):
	NORMAL = (ctypes.c_float * 25)(
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

	GREYSCALE = (ctypes.c_float * 25)(
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

	INVERTED = (ctypes.c_float * 25)(
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
	)
