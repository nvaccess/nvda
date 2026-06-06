# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

import config
from config.configFlags import TetherTo
from config.featureFlagEnums import ReviewRoutingMovesSystemCaretFlag


def _routingShouldMoveSystemCaret() -> bool:
	"""Returns whether pressing a braille routing key should move the system caret."""
	reviewRoutingMovesSystemCaret = config.conf["braille"]["reviewRoutingMovesSystemCaret"].calculated()
	configuredTether = config.conf["braille"]["tetherTo"]
	shouldMoveCaretTetheredReview = (
		configuredTether == TetherTo.REVIEW.value
		and reviewRoutingMovesSystemCaret == ReviewRoutingMovesSystemCaretFlag.ALWAYS
	)
	shouldMoveCaretTetheredAuto = (
		configuredTether == TetherTo.AUTO.value
		and reviewRoutingMovesSystemCaret != ReviewRoutingMovesSystemCaretFlag.NEVER
	)
	return shouldMoveCaretTetheredAuto or shouldMoveCaretTetheredReview
