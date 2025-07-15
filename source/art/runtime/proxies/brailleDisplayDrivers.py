# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""BrailleDisplayDrivers package proxy for add-ons running in ART."""

import sys
from types import ModuleType

# Import the base BrailleDisplayDriver class so addons can inherit from it
from art.runtime.base.brailleDisplayDrivers import BrailleDisplayDriver

# Create a module that acts as the brailleDisplayDrivers package
__path__ = []

# This module needs to be importable as a package
sys.modules[__name__] = sys.modules.get(__name__, ModuleType(__name__))

# Export the base classes
__all__ = ["BrailleDisplayDriver"]
