#vision/constants.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Constants for the vision framework.
"""

class Role:
	"""
	Several roles a vision enhancement provider could fulfill.
	"""
	# This should be a string enum when Python 3 arrives.
	MAGNIFIER = "magnifier"
	HIGHLIGHTER = "highlighter"
	COLORENHANCER = "colorEnhancer"

Role.DESCRIPTIONS = {
	# Translators: The name for a vision enhancement provider that magnifies (a part of) the screen.
	Role.MAGNIFIER: _("Magnifier"),
	# Translators: The name for a vision enhancement provider that highlights important areas on screen,
	# such as the focus, caret or review cursor location.
	Role.HIGHLIGHTER: _("Highlighter"),
	# Translators: The name for a vision enhancement provider that enhances the color presentation.
	# (i.e. color inversion, gray scale coloring, etc.)
	Role.COLORENHANCER: _("Color enhancer"),
}

