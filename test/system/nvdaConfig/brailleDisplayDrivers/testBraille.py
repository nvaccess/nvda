#test/system/nvdaConfig/brailleDisplayDrivers/testBraille.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014 NV Access Limited

"""Braille display driver which enables braille logging for system tests.
"""

from brailleDisplayDrivers import noBraille

class BrailleDisplayDriver(noBraille.BrailleDisplayDriver):
	name = "testBraille"
	description = "Braille driver for system testing"

	# Set numCells to a non-zero value so braille will be enabled and logged.
	numCells = 40
