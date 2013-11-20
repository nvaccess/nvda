#sourceEnv.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2013 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Set up the Python environment when running from source.
"""

import sys
import os

sys.path.insert(1, os.path.abspath(
	os.path.join(__file__, "..", "..", "miscDeps", "python")))
