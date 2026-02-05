# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import types
import os
import sys

# Very basic values to allow things to run.
appDir = os.path.dirname(sys.executable)
appArgs = types.SimpleNamespace()
appArgs.launcher = False
appArgs.secure = False
appArgs.configPath = "."
appArgs.language = None
