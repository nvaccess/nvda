# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2026 NV Access Limited, Neil Soiffer, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import re
import xml.etree.ElementTree as ElementTree
from collections.abc import Generator
from ctypes import (
	Array,
	WinError,
	c_wchar,
	windll,
)
from os import path
from typing import Optional, TYPE_CHECKING, Type

import braille
import config
import gui
import libmathcat_py as libmathcat
import speech
import ui
import winKernel
import winUser
from api import getClipData
from keyboardHandler import KeyboardInputGesture
from logHandler import log
from scriptHandler import script
from NVDAState import ReadPaths

from speech.commands import (
	BeepCommand,
	PitchCommand,
	SpeechCommand,
	SynthCommand,
)
from synthDriverHandler import (
	SynthDriver,
	getSynth,
)
from textUtils import WCHAR_ENCODING

import mathPres
from .localization import getLanguageToUse
from .navCommands import NAV_COMMANDS
from .preferences import applyUserPreferences
from .speech import convertSSMLTextForNVDA

if TYPE_CHECKING:
	from locationHelper import RectLTRB
	from NVDAObjects import NVDAObject


_MATHML_NAMESPACE = "http://www.w3.org/1998/Math/MathML"
_NAV_NODE_ID_PREFIX = "nvda-math-node-"
_NAV_NODE_ID_ADDED_ATTR = "data-nvda-math-id-added"
_NAV_NODE_ORIGINAL_ID_ATTR = "data-nvda-math-original-id"

# Translators: The name of the category of MathCAT navigation commands in the Input Gestures dialog.
SCRCAT_MATHCAT_NAV = _("MathCat navigation")


class MathCATInteraction(mathPres.MathInteractionNVDAObject):
	"""An NVDA object used to interact with MathML."""

	__gestures = {}

	# Put MathML or other formats on the clipboard.
	# MathML is put on the clipboard using the two formats below (defined by MathML spec)
	# We use both formats because some apps may only use one or the other
	# Note: filed https://github.com/nvaccess/nvda/issues/13240 to make this usable outside of MathCAT
	CF_MathML: int = windll.user32.RegisterClipboardFormatW("MathML")
	CF_MathML_Presentation: int = windll.user32.RegisterClipboardFormatW(
		"MathML Presentation",
	)

	def __init__(
		self,
		provider: mathPres.MathPresentationProvider | None = None,
		mathMl: str | None = None,
		sourceObj: Optional["NVDAObject"] = None,
		mathNodeRectsById: Optional[dict[str, "RectLTRB"]] = None,
		originalMathMl: str | None = None,
	):
		"""Initialize the MathCATInteraction object.

		:param provider: Optional presentation provider.
		:param mathMl: Optional initial MathML string.
		:param sourceObj: Optional source object containing the math.
		:param mathNodeRectsById: Map of synthetic MathML ids to source rectangles.
		:param originalMathMl: Unmodified MathML, used for copy commands.
		"""
		super(MathCATInteraction, self).__init__(provider=provider, mathMl=mathMl, sourceObj=sourceObj)
		self._mathNodeRectsById = mathNodeRectsById or {}
		if originalMathMl is not None:
			self.initMathML = originalMathMl
		elif mathMl is None:
			self.initMathML = "<math></math>"
		else:
			self.initMathML = mathMl

	@staticmethod
	def _stripMathMlNamespace(tag: str) -> str:
		return tag.rsplit("}", 1)[-1]

	@classmethod
	def _getSyntheticNodeId(cls, nodePath: tuple[int, ...]) -> str:
		if not nodePath:
			return f"{_NAV_NODE_ID_PREFIX}root"
		return f"{_NAV_NODE_ID_PREFIX}{'-'.join(str(index) for index in nodePath)}"

	@classmethod
	def _iterMathMlElements(
		cls,
		element: ElementTree.Element,
		nodePath: tuple[int, ...],
	) -> Generator[tuple[ElementTree.Element, tuple[int, ...]], None, None]:
		yield element, nodePath
		mathElementChildren = tuple(child for child in element if isinstance(child.tag, str))
		for index, child in enumerate(mathElementChildren):
			yield from cls._iterMathMlElements(child, nodePath + (index,))

	@classmethod
	def _addSyntheticIdsToMathMl(
		cls,
		mathml: str,
	) -> tuple[str, dict[str, tuple[tuple[int, ...], str]]]:
		ElementTree.register_namespace("", _MATHML_NAMESPACE)
		try:
			root = ElementTree.fromstring(mathPres.stripExtraneousXml(mathml))
		except ElementTree.ParseError:
			log.debugWarning("Math highlight could not parse MathML for synthetic node ids", exc_info=True)
			return mathml, {}
		if cls._stripMathMlNamespace(root.tag) != "math":
			log.debug("Math highlight did not add synthetic ids because MathML root is not <math>")
			return mathml, {}
		nodeInfoById: dict[str, tuple[tuple[int, ...], str]] = {}
		for element, nodePath in cls._iterMathMlElements(root, ()):
			nodeId = cls._getSyntheticNodeId(nodePath)
			if originalId := element.get("id"):
				element.set(_NAV_NODE_ORIGINAL_ID_ATTR, originalId)
			element.set("id", nodeId)
			element.set(_NAV_NODE_ID_ADDED_ATTR, "true")
			nodeInfoById[nodeId] = (nodePath, cls._stripMathMlNamespace(element.tag))
		return ElementTree.tostring(root, encoding="unicode"), nodeInfoById

	@classmethod
	def _removeSyntheticIdsFromMathMl(cls, mathml: str) -> str:
		try:
			root = ElementTree.fromstring(mathml)
		except ElementTree.ParseError:
			return mathml
		for element, _nodePath in cls._iterMathMlElements(root, ()):
			if element.get(_NAV_NODE_ID_ADDED_ATTR) != "true":
				continue
			originalId = element.attrib.pop(_NAV_NODE_ORIGINAL_ID_ATTR, None)
			if originalId is not None:
				element.set("id", originalId)
			else:
				element.attrib.pop("id", None)
			element.attrib.pop(_NAV_NODE_ID_ADDED_ATTR, None)
		return ElementTree.tostring(root, encoding="unicode")

	@classmethod
	def prepareMathMlForNavigation(
		cls,
		mathml: str,
		sourceObj: Optional["NVDAObject"],
	) -> tuple[str, dict[str, "RectLTRB"]]:
		"""Add synthetic ids to MathML and map those ids to IA2 rectangles."""
		if not sourceObj:
			return mathml, {}
		from NVDAObjects.IAccessible.ia2Web import Math as Ia2WebMath

		if not isinstance(sourceObj, Ia2WebMath):
			return mathml, {}
		mathmlWithIds, mathMlNodeInfoById = cls._addSyntheticIdsToMathMl(mathml)
		if not mathMlNodeInfoById:
			return mathml, {}
		try:
			ia2NodeInfoByPath = sourceObj.getMathNodeInfoByPath()
		except Exception:
			log.debugWarning("Math highlight could not build IA2 rectangle map", exc_info=True)
			return mathmlWithIds, {}
		nodeRectsById: dict[str, "RectLTRB"] = {}
		missingPathCount = 0
		tagMismatchCount = 0
		for nodeId, (nodePath, mathMlTag) in mathMlNodeInfoById.items():
			try:
				ia2Tag, rect = ia2NodeInfoByPath[nodePath]
			except KeyError:
				missingPathCount += 1
				continue
			if ia2Tag != mathMlTag:
				tagMismatchCount += 1
				continue
			nodeRectsById[nodeId] = rect
		log.debug(
			f"Math highlight added synthetic ids to {len(mathMlNodeInfoById)} MathML nodes; "
			f"mapped {len(nodeRectsById)} ids to IA2 rectangles; "
			f"missing IA2 paths: {missingPathCount}; tag mismatches: {tagMismatchCount}",
		)
		return mathmlWithIds, nodeRectsById

	def reportFocus(self) -> None:
		"""Calls MathCAT's ZoomIn command and speaks the resulting text."""
		super(MathCATInteraction, self).reportFocus()
		try:
			text: str = libmathcat.DoNavigateCommand("ZoomIn")
			speech.speak(convertSSMLTextForNVDA(text))
			self._updateMathHighlight()
		except Exception:
			log.exception()
			# Translators: this message reports an error in starting navigation of math.
			ui.message(pgettext("math", "Error in starting navigation of math."))
			self._clearMathHighlight()

	def _getHighlightRect(self) -> Optional["RectLTRB"]:
		"""Get the navigation rectangle for a supported web math source object."""
		sourceObj = self.sourceObj
		if not sourceObj:
			return None
		from NVDAObjects.IAccessible.ia2Web import Math as Ia2WebMath

		if not isinstance(sourceObj, Ia2WebMath):
			return None
		try:
			nodeId = libmathcat.GetNavigationMathMLId()[0]
		except Exception:
			log.debugWarning("Error getting MathCAT navigation node id", exc_info=True)
		else:
			log.debug(f"Math highlight resolving MathCAT navigation node id {nodeId!r}")
			if nodeId in self._mathNodeRectsById:
				log.debug(f"Math highlight matched synthetic MathML id {nodeId!r}")
				return self._mathNodeRectsById[nodeId]
			if nodeId.startswith(_NAV_NODE_ID_PREFIX):
				log.debug(f"Math highlight found synthetic MathML id {nodeId!r}, but it has no mapped IA2 rectangle")
				log.debug(f"Math highlight falling back to source rectangle for node id {nodeId!r}")
			else:
				log.debug("Math highlight MathCAT navigation id was not an NVDA synthetic id")
				try:
					return sourceObj.getMathNodeRectById(nodeId)
				except LookupError:
					log.debug(f"Math highlight falling back to source rectangle for node id {nodeId!r}")
					pass
		try:
			if sourceObj.hasIrrelevantLocation:
				return None
			location = sourceObj.location
		except Exception:
			log.debugWarning("Error getting math source location", exc_info=True)
			return None
		return location.toLTRB() if location else None

	def _updateMathHighlight(self) -> None:
		import vision

		if vision.handler:
			vision.handler.handleMathNavigation(self._getHighlightRect())

	def _clearMathHighlight(self) -> None:
		import vision

		if vision.handler:
			vision.handler.handleMathNavigation(None)

	def getBrailleRegions(
		self,
		review: bool = False,
	) -> Generator[braille.Region, None, None]:
		"""Yields braille.Region objects for this MathCATInteraction object."""
		yield braille.NVDAObjectRegion(self, appendText=" ")
		region: braille.Region = braille.Region()
		region.focusToHardLeft = True
		try:
			region.rawText = libmathcat.GetBraille("")
		except Exception:
			log.exception()
			# Translators: this message alerts users to an error in brailling math.
			ui.message(pgettext("math", "Error in brailling math: see NVDA error log for details"))
			region.rawText = ""

		yield region

	def _doNavigateCommand(self, commandName: str) -> None:
		"""Perform the named MathCAT navigation command.

		:param commandName: The MathCAT command name (e.g. "MovePrevious").
		"""
		try:
			text = libmathcat.DoNavigateCommand(commandName)
			speech.speak(convertSSMLTextForNVDA(text))
			self._updateMathHighlight()
		except Exception:
			log.exception()
			# Translators: this message alerts users to an error in navigating math.
			ui.message(pgettext("math", "Error in navigating math"))
			self._clearMathHighlight()

		self._updateBraille()

	def _updateBraille(self) -> None:
		"""Update the braille display to reflect the current navigation position."""
		if not braille.handler.enabled:
			return

		try:
			navNode: tuple[str, int] = libmathcat.GetNavigationMathMLId()
			brailleChars = libmathcat.GetBraille(navNode[0])
			region: braille.Region = braille.Region()
			region.rawText = brailleChars
			region.focusToHardLeft = True
			region.update()
			braille.handler.buffer.regions.append(region)
			braille.handler.buffer.focus(region)
			braille.handler.buffer.update()
			braille.handler.update()
		except Exception:
			log.exception()
			# Translators: this message alerts users to an error brailling math.
			ui.message(pgettext("math", "Error in brailling math"))

	@classmethod
	def _createNavScripts(cls) -> None:
		"""Dynamically create individual scripts for each MathCAT navigation command."""
		for cmd in NAV_COMMANDS:
			scriptSuffix = cmd.commandName[0].lower() + cmd.commandName[1:]
			funcName = f"script_{scriptSuffix}"
			script = lambda self, gesture, _cmd=cmd.commandName: self._doNavigateCommand(_cmd)  # noqa: E731
			script.__doc__ = cmd.description
			script.__name__ = funcName
			script.category = SCRCAT_MATHCAT_NAV
			script.speakOnDemand = cmd.speakOnDemand
			setattr(cls, funcName, script)
			for gesture in cmd.gestures:
				cls.__gestures[gesture] = scriptSuffix

	_startsWithMath: re.Pattern = re.compile("\\s*?<math")

	@script(
		# Translators: Message to be announced during Keyboard Help
		description=_("Copy navigation focus to clipboard"),
		# Translators: Name of the section in "Input gestures" dialog.
		category=_("Clipboard"),
		gesture="kb:control+c",
	)
	def script_rawdataToClip(self, gesture: KeyboardInputGesture) -> None:
		"""Copies the raw data to the clipboard, either as MathML, ASCII math, or LaTeX, depending on user preferences.

		:param gesture: The gesture which activated this script.
		"""
		try:
			copyAs: str = "mathml"  # value used even if "CopyAs" pref is invalid
			textToCopy: str = ""
			try:
				copyAs = libmathcat.GetPreference("CopyAs").lower()
			except Exception:
				log.exception("Not able to get 'CopyAs' preference.")
			if copyAs == "asciimath" or copyAs == "latex":
				# save the old braille code, set the new one, get the braille, then reset the code
				savedBrailleCode: str = libmathcat.GetPreference("BrailleCode")
				libmathcat.SetPreference("BrailleCode", "LaTeX" if copyAs == "latex" else "ASCIIMath")
				textToCopy = libmathcat.GetNavigationBraille()
				libmathcat.SetPreference("BrailleCode", savedBrailleCode)
				if copyAs == "asciimath":
					copyAs = "ASCIIMath"  # speaks better in at least some voices
			else:
				mathml: str = libmathcat.GetNavigationMathML()[0]
				if not re.match(self._startsWithMath, mathml):
					mathml = "<math>\n" + mathml + "</math>"  # copy will fix up name spacing
				elif self.initMathML != "":
					mathml = self.initMathML
				if copyAs == "speech":
					# save the old MathML, set the navigation MathML as MathMl, get the speech, then reset the MathML
					savedMathML: str = self.initMathML
					savedTTS: str = libmathcat.GetPreference("TTS")
					if savedMathML == "":  # shouldn't happen
						raise Exception("Internal error -- MathML not set for copy")
					libmathcat.SetPreference("TTS", "None")
					libmathcat.SetMathML(mathml)
					# get the speech text and collapse the whitespace
					textToCopy = " ".join(libmathcat.GetSpokenText().split())
					libmathcat.SetPreference("TTS", savedTTS)
					libmathcat.SetMathML(savedMathML)
				else:
					textToCopy = self._wrapMathMLForClipBoard(mathml)

			self._copyToClipAsMathML(textToCopy, copyAs == "mathml")
			# Translators: copy to clipboard
			ui.message(pgettext("math", "copy as ") + copyAs)
		except Exception:
			log.exception()
			# Translators: alerts users to an error copying math.
			ui.message(pgettext("unable to copy math"))

	# not a perfect match sequence, but should capture normal MathML
	_mathTagHasNameSpace: re.Pattern = re.compile("<math .*?xmlns.+?>")
	_hasDataAttr: re.Pattern = re.compile(" data-[^=]+='[^']*'")

	def _wrapMathMLForClipBoard(self, text: str) -> str:
		"""Cleanup the MathML a little."""
		text = self._removeSyntheticIdsFromMathMl(text)
		mathMLWithNS: str = re.sub(self._hasDataAttr, "", text)
		if not re.match(self._mathTagHasNameSpace, mathMLWithNS):
			mathMLWithNS = mathMLWithNS.replace(
				"math",
				"math xmlns='http://www.w3.org/1998/Math/MathML'",
				1,
			)
		return mathMLWithNS

	def _copyToClipAsMathML(
		self,
		text: str,
		isMathML: bool,
		notify: bool | None = False,
	) -> bool:
		"""Copies the given text to the windows clipboard.

		:param text: the text which will be copied to the clipboard.
		:param notify: whether to emit a confirmation message.
		:returns: True if it succeeds, False otherwise.
		"""
		# copied from api.py and modified to use CF_MathML_Presentation
		if not isinstance(text, str) or len(text) == 0:
			return False

		try:
			with winUser.openClipboard(gui.mainFrame.Handle):
				winUser.emptyClipboard()
				if isMathML:
					self._setClipboardData(self.CF_MathML, '<?xml version="1.0"?>' + text)
					self._setClipboardData(self.CF_MathML_Presentation, '<?xml version="1.0"?>' + text)
				self._setClipboardData(winUser.CF_UNICODETEXT, text)
			got: str = getClipData()
		except OSError:
			if notify:
				ui.reportTextCopiedToClipboard()  # No argument reports a failure.
			return False
		if got == text:
			if notify:
				ui.reportTextCopiedToClipboard(text)
			return True
		if notify:
			ui.reportTextCopiedToClipboard()  # No argument reports a failure.
		return False

	def _setClipboardData(self, format: int, data: str) -> None:
		"""Sets the clipboard data to the given data with the specified format.

		:param format: The format for the clipboard data.
			This is an integer format code returned by windll.user32.RegisterClipboardFormatW.
		:param data: The data to set on the clipboard.
		"""
		# Need to support MathML Presentation, so this is copied from winUser.py and the first two lines are removed
		# For now only unicode is a supported format
		text: str = data
		bufLen: int = len(text.encode(WCHAR_ENCODING, errors="surrogatepass")) + 2
		# Allocate global memory
		h: winKernel.HGLOBAL = winKernel.HGLOBAL.alloc(winKernel.GMEM_MOVEABLE, bufLen)
		# Acquire a lock to the global memory receiving a local memory address
		with h.lock() as addr:
			# Write the text into the allocated memory
			buf: Array[c_wchar] = (c_wchar * bufLen).from_address(addr)
			buf.value = text
		# Set the clipboard data with the global memory
		if not windll.user32.SetClipboardData(format, h):
			raise WinError()
		# NULL the global memory handle so that it is not freed at the end of scope as the clipboard now has it.
		h.forget()


class MathCAT(mathPres.MathPresentationProvider):
	supportsInteractionSourceObj: bool = True

	def __init__(self):
		"""Initializes MathCAT, loading the rules specified in the rules directory."""

		try:
			# IMPORTANT -- SetRulesDir must be the first call to libmathcat besides GetVersion()
			rulesDir: str = path.join(
				ReadPaths.mathCATDir,
				"Rules",
			)
			log.info(f"MathCAT {libmathcat.GetVersion()} installed. Using rules dir: {rulesDir}")
			libmathcat.SetRulesDir(rulesDir)
			libmathcat.SetPreference("TTS", "SSML")
			applyUserPreferences()
		except Exception:
			log.exception()
			# Translators: this message directs users to look in the log file
			ui.message(pgettext("math", "Error navigating math"))

	def getSpeechForMathMl(
		self,
		mathml: str,
	) -> list[str | SpeechCommand]:
		"""Outputs a MathML string as speech.

		:param mathml: A MathML string.
		:returns: A list of speech commands and strings representing the given MathML.
		"""
		synth: SynthDriver = getSynth()
		synthConfig = config.conf["speech"][synth.name]
		try:
			# need to set Language before the MathML for DecimalSeparator canonicalization
			language: str = getLanguageToUse()
			# MathCAT should probably be extended to accept "extlang" tagging, but it uses lang-region tagging at the moment
			libmathcat.SetPreference("Language", language)
			libmathcat.SetMathML(mathml)
		except Exception:
			log.exception()
			log.exception(f"MathML is {mathml}")
			# Translators: this message reports when invalid math is found.
			ui.message(pgettext("math", "Invalid math formatting found"))
			libmathcat.SetMathML("<math></math>")
		try:
			supportedCommands: set[Type["SynthCommand"]] = synth.supportedCommands
			# Set preferences for capital letters
			libmathcat.SetPreference(
				"CapitalLetters_Beep",
				"true" if synthConfig["beepForCapitals"] else "false",
			)
			libmathcat.SetPreference(
				"CapitalLetters_UseWord",
				"true" if synthConfig["sayCapForCapitals"] else "false",
			)
			if PitchCommand in supportedCommands:
				libmathcat.SetPreference("CapitalLetters_Pitch", str(synthConfig["capPitchChange"]))
			if self._addSounds():
				return (
					[BeepCommand(800, 25)]
					+ convertSSMLTextForNVDA(libmathcat.GetSpokenText())
					+ [BeepCommand(600, 15)]
				)
			else:
				return convertSSMLTextForNVDA(libmathcat.GetSpokenText())

		except Exception:
			log.exception()
			# Translators: this message reports an error in speaking math.
			ui.message(pgettext("math", "Error in speaking math."))
			return [""]

	def _addSounds(self) -> bool:
		"""Queries the user preferences to determine whether or not sounds should be added.

		:returns: True if MathCAT's `SpeechSound` preference is set, and False otherwise.
		"""
		try:
			return libmathcat.GetPreference("SpeechSound") != "None"
		except Exception:
			log.exception()
			return False

	def getBrailleForMathMl(self, mathml: str) -> str:
		"""Gets the braille representation of a given MathML string by calling MathCAT's GetBraille function.

		:param mathml: A MathML string.
		:returns: A braille string representing the input MathML.
		"""
		try:
			libmathcat.SetMathML(mathml)
		except Exception:
			log.exception(f"MathML is {mathml}")
			# Translators: this message reports illegal MathML.
			ui.message(pgettext("math", "Illegal MathML found."))
			libmathcat.SetMathML("<math></math>")
		try:
			return libmathcat.GetBraille("")
		except Exception:
			log.exception()
			# Translators: this message reports an error in brailling math.
			ui.message(pgettext("math", "Error in brailling math."))
			return ""

	def interactWithMathMl(self, mathml: str, sourceObj: Optional["NVDAObject"] = None) -> None:
		"""Interact with a MathML string, creating a MathCATInteraction object.

		:param mathml: The MathML representing the math to interact with.
		:param sourceObj: Optional source object containing the math.
		"""
		originalMathMl = mathml
		mathml, mathNodeRectsById = MathCATInteraction.prepareMathMlForNavigation(mathml, sourceObj)
		try:
			libmathcat.SetMathML(mathml)
		except Exception:
			log.exception(f"MathML is {mathml}")
			# Translators: this message reports illegal MathML.
			ui.message(pgettext("math", "Illegal MathML found."))
			libmathcat.SetMathML("<math></math>")
		interaction = MathCATInteraction(
			provider=self,
			mathMl=mathml,
			sourceObj=sourceObj,
			mathNodeRectsById=mathNodeRectsById,
			originalMathMl=originalMathMl,
		)
		interaction.setFocus()
		interaction._updateBraille()
