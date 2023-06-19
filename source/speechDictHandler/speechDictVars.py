# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017-2023 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This submodule is deprecated and new code should not be added."""

from logHandler import log
import NVDAState
from NVDAState import WritePaths


if NVDAState._allowDeprecatedAPI():
	log.warning(
		"speechDictHandler.speechDictVars.speechDictsPath is deprecated, "
		"instead use WritePaths.speechDictsDir",
		stack_info=True
	)
	speechDictsPath = WritePaths.speechDictsDir
