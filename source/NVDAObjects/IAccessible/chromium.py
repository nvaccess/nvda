#NVDAObjects/IAccessible/chromium.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
# Copyright (C) 2010-2013 NV Access Limited

"""NVDAObjects for the Chromium browser project
"""

from comtypes import COMError
import oleacc
import controlTypes
import IAccessibleHandler
from NVDAObjects.IAccessible import IAccessible
from virtualBuffers.gecko_ia2 import Gecko_ia2 as GeckoVBuf
from . import ia2Web

class ChromeVBuf(GeckoVBuf):

	def __contains__(self, obj):
		if obj.windowHandle != self.rootNVDAObject.windowHandle:
			return False
		accId = obj.IA2UniqueID
		if accId == self.rootID:
			return True
		try:
			self.rootNVDAObject.IAccessibleObject.accChild(accId)
		except COMError:
			return False
		return True

class Document(ia2Web.Document):

	def _get_treeInterceptorClass(self):
		states = self.states
		if controlTypes.STATE_READONLY in states and controlTypes.STATE_BUSY not in states:
			return ChromeVBuf
		return super(Document, self).treeInterceptorClass

def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class(es) for Chromium objects.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	ia2Web.findExtraOverlayClasses(obj, clsList,
		documentClass=Document)
