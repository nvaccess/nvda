#NVDAObjects/IAccessible/adobeFlash.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from . import IAccessible
from NVDAObjects import NVDAObjectTextInfo
from comtypes import COMError, IServiceProvider
from comtypes.gen.FlashAccessibility import ISimpleTextSelection
from logHandler import log

class InputTextFieldTextInfo(NVDAObjectTextInfo):

	def _getStoryText(self):
		return self.obj.value or ""

	def _getCaretOffset(self):
		try:
			return self.obj.ISimpleTextSelectionObject.GetSelection()[1]
		except (COMError, AttributeError):
			raise RuntimeError

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
	("ExtendedDown","moveByLine"),
	("ExtendedLeft","moveByCharacter"),
	("ExtendedRight","moveByCharacter"),
	("ExtendedPrior","moveByLine"),
	("ExtendedNext","moveByLine"),
	("Control+ExtendedLeft","moveByWord"),
	("Control+ExtendedRight","moveByWord"),
	("control+extendedDown","moveByParagraph"),
	("control+extendedUp","moveByParagraph"),
	("ExtendedHome","moveByCharacter"),
	("ExtendedEnd","moveByCharacter"),
	("control+extendedHome","moveByLine"),
	("control+extendedEnd","moveByLine"),
	("ExtendedDelete","delete"),
	("Back","backspace"),
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
