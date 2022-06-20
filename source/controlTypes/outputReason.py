# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2021 NV Access Limited, Babbage B.V.

from enum import Enum, auto


class OutputReason(Enum):
	"""Specify the reason that a given piece of output was generated.
	"""
	#: An object to be reported due to a focus change or similar.
	FOCUS = auto()
	#: An ancestor of the focus object to be reported due to a focus change or similar.
	FOCUSENTERED = auto()
	#: An item under the mouse.
	MOUSE = auto()
	#: A response to a user query.
	QUERY = auto()
	#: Reporting a change to an object.
	CHANGE = auto()
	#: A generic, screen reader specific message.
	MESSAGE = auto()
	#: Text reported as part of a say all.
	SAYALL = auto()
	#: Content reported due to caret movement or similar.
	CARET = auto()
	#: No output, but any state should be cached as if output had occurred.
	ONLYCACHE = auto()

	QUICKNAV = auto()
