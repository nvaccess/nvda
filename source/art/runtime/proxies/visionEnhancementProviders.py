# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""VisionEnhancementProviders package proxy for add-ons running in ART."""

import sys
from types import ModuleType

# Create a module that acts as the visionEnhancementProviders package
__path__ = []

# This module needs to be importable as a package
sys.modules[__name__] = sys.modules.get(__name__, ModuleType(__name__))
