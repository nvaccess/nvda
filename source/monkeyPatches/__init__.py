# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from . import wxMonkeyPatches


applyWxMonkeyPatches = wxMonkeyPatches.apply


def applyMonkeyPatches():
	# Apply several monkey patches to comtypes
	from . import comtypesMonkeyPatches
	comtypesMonkeyPatches.applyMonkeyPatches()

	# Apply patches to Enum, prevent cyclic references on ValueError during construction
	from . import enumPatches
	enumPatches.replace__new__()
