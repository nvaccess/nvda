# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited


from __future__ import annotations
from ..builder import (
	InstructionBase,
)


class _TypedInstruction(InstructionBase):

	@property
	def params(self) -> dict[str, object]:
		return vars(self)
