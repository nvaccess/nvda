"""Run SCons from the NVDA source environment.
"""

import sys
import os
sys.path.append(os.path.abspath(
	os.path.join(__file__, "..", "source")))
import sourceEnv
del sys.path[-1]
import SCons.Script
SCons.Script.main()
