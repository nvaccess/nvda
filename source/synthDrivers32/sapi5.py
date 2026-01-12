# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Leonard de Ruijter, gexgd0419
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import sys
import os
import comtypes.client

# Precompile the SAPI5 COM interfaces
# Placing them where NvDA's original sapi5 driver expects them.
sys.modules['comInterfaces.SpeechLib'] = comtypes.client.GetModule(r'c:\windows\system32\speech\common\sapi.dll') 

# Point the sonic module to the 32 bit build of its dll 
from . import _sonic
_sonic.SONIC_DLL_PATH = os.path.join(os.path.dirname(__file__), 'sonic.dll')

from ._sapi5 import SynthDriver

__all__ = ["SynthDriver"]
