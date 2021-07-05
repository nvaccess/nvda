# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

def applyMonkeyPatches():
	# Apply several monkey patches to comtypes
	from . import comtypesMonkeyPatches  # patches are applied once imported

	# Apply patches to Enum, prevent cyclic references on ValueError during construction
	from . import enumPatches
	enumPatches.replace__new__()