# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This is just an alias which maps the appModule for Notepad++ to the right binary file
by exposing everything from the real module in its namespace.
"""

import nvdaBuiltin.appModules.notepadPlusPlus as baseAppMod


for name, value in baseAppMod.__dict__.items():
	if name.startswith("_"):
		continue
	globals()[name] = value
