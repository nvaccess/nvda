# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import enum


class RPC(enum.IntEnum):
	E_CALL_CANCELED = -2147418110
	S_SERVER_UNAVAILABLE = 1722
	S_CALL_FAILED_DNE = 1727
	E_CALL_REJECTED = -2147418111
	E_DISCONNECTED = -2147417848
