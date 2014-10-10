#mathPres/liblouisutdml.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import ctypes
import braille
import mathPres

liblouisutdml = ctypes.windll.liblouisutdml

class Liblouisutdml(mathPres.MathPresentationProvider):

	def getBrailleForMathMl(self, mathMl):
		mathMl = mathMl.encode("UTF-8")
		# If liblouisutdml adds the XML header, the last character gets
		# truncated unless we add 1 to the length.
		inLen = len(mathMl) + 1
		outLen = ctypes.c_int(inLen)
		outBuf = ctypes.create_unicode_buffer(outLen.value)
		if liblouisutdml.lbu_translateString(os.path.join(braille.TABLES_DIR, "nemeth.cfg"),
				mathMl, inLen,
				outBuf, ctypes.byref(outLen),
				None, None, 0) <= 0:
			raise RuntimeError
		return outBuf.value
