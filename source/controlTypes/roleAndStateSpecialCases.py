# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited

from . import (
	Role,
	State,
)
from typing import (
	Tuple,
	Set,
)


def transformRoleStates(role: Role, states: Set[State]) -> Tuple[Role, Set[State]]:
	""" Map NVDA Role-State combinations to adjusted NVDA Role-State combinations.
	Some combinations of roles and states may be better represented with some alternative combination.
	As an example:
	Role.PROGRESSBAR with State.INDETERMINATE should be represented by only the Role.BUSY_INDICATOR, with
	no State.INDETERMINATE, or State.HALFCHECKED.
	@param role: NVDA Role to consider
	@param states: NVDA States to consider
	@return: A tuple with the new Role and modified States set.
	"""
	if(
		role in [Role.PROGRESSBAR, Role.BUSY_INDICATOR]
		and states.intersection({State.INDETERMINATE, State.HALFCHECKED})
	):
		# Don't report indeterminate progress bars as "half-checked"
		# L{State.HALFCHECKED} maps from oleacc.STATE_SYSTEM_MIXED,
		# which has the same value as oleacc.STATE_SYSTEM_INDETERMINATE.
		# L{State.INDETERMINATE} is not mapped directly from any IA or IA2 state.
		# A progress bar that can not convey progress, only activity, is a busy indicator.
		states.discard(State.HALFCHECKED)
		states.add(State.INDETERMINATE)
		return Role.BUSY_INDICATOR, states
	return role, states
