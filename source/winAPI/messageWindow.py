# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
A submodule for NVDA's message window, used for handling Windows Messages.

Message windows can be used to handle communications from other processes, new NVDA instances and Windows.
"""

import enum


class WindowMessage(enum.IntEnum):
	POWERBROADCAST = 0x0218
	WTSSESSION_CHANGE = 0x02B1
	"""
	Windows Message for when a Session State Changes.
	Receiving these messages is registered by registerSessionNotification.
	handleSessionChange handles these messages.
	"""
