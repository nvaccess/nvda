# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited, Babbage B.V., Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
appModule for Visual Studio Code Insiders.
Imports the appModule for Visual Studio Code.
"""

# Normally these Flake8 errors shouldn't be ignored but here we are simply reusing existing ap module.

from .code import *  # noqa: F401, F403
