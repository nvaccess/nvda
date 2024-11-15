# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

# rather than using the ctypes.c_void_p type, which may encourage attempting to dereference
# what may be an invalid or illegal pointer, we'll treat it as an opaque value.
HWNDValT = int
