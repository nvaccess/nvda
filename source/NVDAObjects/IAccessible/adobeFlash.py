#NVDAObjects/IAccessible/adobeFlash.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from . import IAccessible
from NVDAObjects import NVDAObjectTextInfo
from comtypes import COMError, IServiceProvider, hresult
from comtypes.gen.FlashAccessibility import ISimpleTextSelection
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

class InputTextField(IAccessible):
	TextInfo = InputTextFieldTextInfo

	def __init__(self, ISimpleTextSelectionObject=None, **kwargs):
		super(InputTextField, self).__init__(**kwargs)
		if ISimpleTextSelectionObject:
			self.ISimpleTextSelectionObject = ISimpleTextSelectionObject
		else:
			try:
				self.ISimpleTextSelectionObject = self.IAccessibleObject.QueryInterface(IServiceProvider).QueryService(ISimpleTextSelection._iid_, ISimpleTextSelection)
			except COMError:
				self.ISimpleTextSelectionObject = None

[InputTextField.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","moveByLine"),
	("shift+ExtendedUp","changeSelection"),
	("ExtendedDown","moveByLine"),
	("shift+ExtendedDown","changeSelection"),
	("ExtendedLeft","moveByCharacter"),
	("shift+ExtendedLeft","changeSelection"),
	("ExtendedRight","moveByCharacter"),
	("shift+ExtendedRight","changeSelection"),
	("ExtendedPrior","moveByLine"),
	("shift+ExtendedPrior","changeSelection"),
	("ExtendedNext","moveByLine"),
	("shift+ExtendedNext","changeSelection"),
	("Control+ExtendedLeft","moveByWord"),
	("shift+Control+ExtendedLeft","changeSelection"),
	("Control+ExtendedRight","moveByWord"),
	("shift+Control+ExtendedRight","changeSelection"),
	("control+extendedDown","moveByParagraph"),
	("shift+control+extendedDown","changeSelection"),
	("control+extendedUp","moveByParagraph"),
	("shift+control+extendedUp","changeSelection"),
	("ExtendedHome","moveByCharacter"),
	("shift+ExtendedHome","changeSelection"),
	("ExtendedEnd","moveByCharacter"),
	("shift+ExtendedEnd","changeSelection"),
	("control+extendedHome","moveByLine"),
	("shift+control+extendedHome","changeSelection"),
	("control+extendedEnd","moveByLine"),
	("shift+control+extendedEnd","changeSelection"),
	("ExtendedDelete","delete"),
	("Back","backspace"),
	("control+a","changeSelection"),
]]

def findBestClass(clsList, kwargs):
	"""Determine the most appropriate class if this is a Flash object and provide appropriate kwargs.
	This works similarly to L{NVDAObjects.NVDAObject.findBestClass} except that it never calls any other findBestClass method.
	"""
	IAccessibleObject = kwargs["IAccessibleObject"]
	# Check whether this is a Flash input text field.
	try:
		kwargs["ISimpleTextSelectionObject"] = IAccessibleObject.QueryInterface(IServiceProvider).QueryService(ISimpleTextSelection._iid_, ISimpleTextSelection)
		clsList.append(InputTextField)
	except COMError:
		pass
	return clsList, kwargs
