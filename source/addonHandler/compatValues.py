# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Values used by addonHandler and addonVersionCheck"""
KNOWN_BIT = 0x1  # KNOWN_BIT is not explicitly used alone, but used to denote UNKNOWN or in combination with
# AUTO_DEDUCED_BIT or MANUALLY_SET_BIT
AUTO_DEDUCED_BIT = 0x1 << 1
MANUALLY_SET_BIT = 0x1 << 2
COMPATIBLE_BIT = 0x1 << 3

# Convenience values, values should not have both AUTO_DEDUCED_BIT and MANUALLY_SET_BITs set.
UNKNOWN = 0x0  # UNKNOWN is considered incompatible.
MANUALLY_SET_INCOMPATIBLE = KNOWN_BIT | MANUALLY_SET_BIT  # No COMPATIBLE_BIT
MANUALLY_SET_COMPATIBLE = KNOWN_BIT | MANUALLY_SET_BIT | COMPATIBLE_BIT
AUTO_DEDUCED_COMPATIBLE = KNOWN_BIT | AUTO_DEDUCED_BIT | COMPATIBLE_BIT
AUTO_DEDUCED_INCOMPATIBLE = KNOWN_BIT | AUTO_DEDUCED_BIT  # No COMPATIBLE_BIT

KNOWN_MASK = KNOWN_BIT | AUTO_DEDUCED_BIT | MANUALLY_SET_BIT
