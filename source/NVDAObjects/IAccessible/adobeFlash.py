#NVDAObjects/IAccessible/adobeFlash.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winUser
import oleacc
from . import IAccessible
from NVDAObjects import NVDAObjectTextInfo
from NVDAObjects.behaviors import EditableTextWithoutAutoSelectDetection
from comtypes import COMError, IServiceProvider, hresult
from comtypes.gen.FlashAccessibility import ISimpleTextSelection, IFlashAccessibility
from logHandler import log

class InputTextFieldTextInfo(NVDAObjectTextInfo):

	def _getStoryText(self):
		return self.obj.value or ""

	def _getRawSelectionOffsets(self):
		try:
			return self.obj.ISimpleTextSelectionObject.GetSelection()
		except COMError, e:
			if e.hresult == hresult.E_FAIL:
				# The documentation says that an empty field should return 0 for both values, but instead, we seem to get E_FAIL.
				# An empty field still has a valid caret.
				return 0, 0
			else:
				raise RuntimeError
		except AttributeError:
			raise RuntimeError

	def _getCaretOffset(self):
		# We want the active (moving) end of the selection.
		return self._getRawSelectionOffsets()[1]

	def _getSelectionOffsets(self):
		# This might be a backwards selection, but for now, we should always return the values in ascending order.
		return sorted(self._getRawSelectionOffsets())

class InputTextField(EditableTextWithoutAutoSelectDetection, IAccessible):
	TextInfo = InputTextFieldTextInfo

class Root(IAccessible):
	def _get_presentationType(self):
		return self.presType_content


	def _get_virtualBufferClass(self):
		import virtualBuffers.adobeFlash
		return virtualBuffers.adobeFlash.AdobeFlash

def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class if this is a Flash object.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	try:
		servProv = obj.IAccessibleObject.QueryInterface(IServiceProvider)
	except COMError:
		return

	# Check whether this is the Flash root accessible.
	if obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT:
		try:
			servProv.QueryService(IFlashAccessibility._iid_, IFlashAccessibility)
			clsList.append(Root)
		except COMError:
			pass
		# If this is a client and IFlashAccessibility wasn't present, this is not a Flash object.
		return

	# Check whether this is a Flash input text field.
	try:
		# We have to fetch ISimpleTextSelectionObject in order to check whether this is an input text field, so store it on the instance.
		obj.ISimpleTextSelectionObject = servProv.QueryService(ISimpleTextSelection._iid_, ISimpleTextSelection)
		clsList.append(InputTextField)
	except COMError:
		pass
