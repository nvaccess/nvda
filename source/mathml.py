#mathml.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2013 NV Access Limited

import controlTypes

tagNamesToNVDARoles = {
	"mfrac": controlTypes.ROLE_MATH_FRACTION,
	"mi": controlTypes.ROLE_MATH_IDENTIFIER,
	"mn": controlTypes.ROLE_MATH_NUMBER,
	"mo": controlTypes.ROLE_MATH_OPERATOR,
	"mrow": controlTypes.ROLE_MATH_ROW,
	"msqrt": controlTypes.ROLE_MATH_SQRT,
	"msup": controlTypes.ROLE_MATH_SUPERSCRIPT,
}
