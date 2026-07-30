# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
rpyc-over-pipes transport for the add-on runtime.

This package provides the generic, feature-agnostic plumbing used by both ends of an add-on runtime connection:

* Restricted rpyc protocol configuration;
* ``Service`` base class (what NVDA and add-ons interact with);
* ``Proxy`` base class (adapts between internal details and the ART API);
* ``Connection`` wrapper over a bidirectional pipe stream.

Importing this package applies the rpyc patches we rely on (see ``config``).

Nothing here is specific to any feature (synth, braille, etc); feature contracts are built on top of this layer as "components".
"""

from .config import PROTOCOL_CONFIG
from .connection import Connection
from .proxy import Proxy
from .service import Service

__all__ = ["PROTOCOL_CONFIG", "Connection", "Proxy", "Service"]
