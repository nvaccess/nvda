# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2025 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


from winBindings import user32 as _user32
from .constants import SysColorIndex
from utils import _deprecate

_deprecate.handleDeprecations(
	_deprecate.MovedSymbol("user32", "winBindings.user32", "dll"),
)


def GetSysColor(index: SysColorIndex):
	return _user32.GetSysColor(index)
