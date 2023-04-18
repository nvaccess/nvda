# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	Generator,
	TYPE_CHECKING,
)

if TYPE_CHECKING:
	from . import Addon  # noqa: F401


AddonGeneratorT = Generator["Addon", None, None]
