# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This package is not a Robot Framework library itself, it contains:
- GlobalPlugin and SynthDriver used to get information out of NVDA for use by the system tests
- Module `configManager.py` used to install the GlobalPlugin, SynthDriver, and config for the system test.
- Some shared code used by the above as well as other RobotFramework libraries.
"""

# Expose shared code. Lint error F401 imported but unused. Exposing like this makes importing easier, and
# allows code to be re-organized without having to fix many import statements.
from .blockUntilConditionMet import _blockUntilConditionMet  # noqa: F401
from .getLib import _getLib  # noqa: F401

_nvdaSpyAlias = "nvdaSpyLib"
