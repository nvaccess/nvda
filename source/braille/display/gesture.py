# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

import re
from typing import Optional

import baseObject
import config
import inputCore
import NVDAState
import scriptHandler
from logHandler import log

import braille

from .driver import _getDisplayDriver


class BrailleDisplayGesture(inputCore.InputGesture):
	"""A button, wheel or other control pressed on a braille display.
	Subclasses must provide :attr:`source` and :attr:`id`.
	Optionally, :attr:`model` can be provided to facilitate model specific gestures.
	:attr:`cellIndexes` should be provided for gestures addressed to specific braille cells,
	such as routing keys or touch-sensitive cells (e.g. Handy Tech Active Tactile Control).
	Subclasses can also inherit from :class:`brailleInput.BrailleInputGesture` if the display has a braille keyboard.
	If the braille display driver is a :class:`baseObject.ScriptableObject`, it can provide scripts specific to input gestures from this display.
	"""

	shouldPreventSystemIdle = True

	def _get_source(self):
		"""The string used to identify all gestures from this display.
		This should generally be the driver name.
		This string will be included in the source portion of gesture identifiers.
		For example, if this was C{alvaBC6},
		a display specific gesture identifier might be C{br(alvaBC6):etouch1}.
		@rtype: str
		"""
		raise NotImplementedError

	def _get_model(self):
		"""The string used to identify all gestures from a specific braille display model.
		This should be an alphanumeric short version of the model name, without spaces.
		This string will be included in the source portion of gesture identifiers.
		For example, if this was C{alvaBC6},
		the model string could look like C{680},
		and a corresponding display specific gesture identifier might be C{br(alvaBC6.680):etouch1}.
		@rtype: str; C{None} if model specific gestures are not supported
		"""
		return None

	def _get_id(self):
		"""The unique, display specific id for this gesture.
		@rtype: str
		"""
		raise NotImplementedError

	cellIndexes: list[int] | None = None
	"""Indexes of braille cells addressed by this gesture, e.g. routing keys or touch cells.
	``None`` if this gesture is not cell-addressed.
	"""

	@classmethod
	def idForCellCount(cls, count: int, baseName: str = "routing") -> str:
		"""Return the conventional gesture id suffix for a cell-addressed gesture.

		When more than one cell is addressed, the base name is prefixed with ``"multi"``
		and its first character is uppercased.  For example::

			idForCellCount(1, "routing")        # "routing"
			idForCellCount(2, "routing")        # "multiRouting"
			idForCellCount(2, "secondRouting")  # "multiSecondRouting"

		:param count: Number of cells addressed.
		:param baseName: The gesture id for a single-cell press in this range.
		:return: The base name if *count* <= 1, otherwise the multi-prefixed form.
		"""
		if count > 1:
			return f"multi{baseName[0].upper()}{baseName[1:]}"
		return baseName

	if NVDAState._allowDeprecatedAPI():

		def _get_routingIndex(self) -> int | None:
			"""Deprecated. Use :attr:`cellIndexes` instead.

			Returns the highest cell index, or ``None`` if no cells are addressed.
			"""
			return max(self.cellIndexes) if self.cellIndexes else None

		def _set_routingIndex(self, value: int | None) -> None:
			"""Deprecated. Set :attr:`cellIndexes` instead."""
			log.warning(
				"Setting BrailleDisplayGesture.routingIndex is deprecated, set cellIndexes instead.",
				stack_info=True,
			)
			self.cellIndexes = [value] if value is not None else None

	_cellIndexesStr: str | None

	def _get__cellIndexesStr(self) -> str | None:
		"""A string representation of cell indexes for identification and display purposes."""
		if "+" not in self.id and self.cellIndexes:
			# This is an indexed gesture without additional keys, in which case the identifier can be extended with indexes.
			return "+".join(f"{i + 1}" for i in self.cellIndexes)
		return None

	def _get_identifiers(self):
		ids = []
		if self._cellIndexesStr:
			ids.append(f"br({self.source}):{self.id}{self._cellIndexesStr}")
		ids.append(f"br({self.source}):{self.id}")
		if self.model:
			# Model based ids should take priority.
			if self._cellIndexesStr:
				ids.insert(0, f"br({self.source}.{self.model}):{self.id}{self._cellIndexesStr}")
			ids.insert(1, f"br({self.source}.{self.model}):{self.id}")
		import brailleInput

		if isinstance(self, brailleInput.BrailleInputGesture):
			ids.extend(brailleInput.BrailleInputGesture._get_identifiers(self))
		return ids

	def _get_displayName(self):
		import brailleInput

		if isinstance(self, brailleInput.BrailleInputGesture):
			name = brailleInput.BrailleInputGesture._get_displayName(self)
			if name:
				return name
		if self._cellIndexesStr:
			return f"{self.id}{self._cellIndexesStr}"
		return self.id

	def _get_scriptableObject(self):
		display = braille.handler.display
		if isinstance(display, baseObject.ScriptableObject):
			return display
		return super(BrailleDisplayGesture, self).scriptableObject

	def _get_script(self):
		# Overrides L{inputCore.InputGesture._get_script} to support modifier keys.
		# Also processes modifiers held by braille input.
		# Import late to avoid circular import.
		import brailleInput

		gestureKeys = set(self.keyNames)
		gestureModifiers = brailleInput.handler.currentModifiers.copy()
		script = scriptHandler.findScript(self)
		if script:
			scriptName = script.__name__
			if not (gestureModifiers and scriptName.startswith("script_kb:")):
				self.script = script
				return self.script
		# Either no script for this gesture has been found, or braille input is holding modifiers.
		# Process this gesture for possible modifiers if it consists of more than one key.
		# For example, if L{self.id} is 'key1+key2',
		# key1 is bound to 'kb:control' and key2 to 'kb:tab',
		# this gesture should execute 'kb:control+tab'.
		# Combining emulated modifiers with braille input (#7306) is not yet supported.
		if len(gestureKeys) > 1:
			for keys, modifiers in braille.handler.display._getModifierGestures(self.model):
				if keys < gestureKeys:
					gestureModifiers |= modifiers
					gestureKeys -= keys
		if not gestureModifiers:
			return None
		if gestureKeys != set(self.keyNames):
			# Find a script for L{gestureKeys}.
			id = "+".join(gestureKeys)
			fakeGestureIds = ["br({source}):{id}".format(source=self.source, id=id)]
			if self.model:
				fakeGestureIds.insert(
					0,
					"br({source}.{model}):{id}".format(source=self.source, model=self.model, id=id),
				)
			scriptNames = []
			globalMaps = [inputCore.manager.userGestureMap, braille.handler.display.gestureMap]
			for globalMap in globalMaps:
				for fakeGestureId in fakeGestureIds:
					scriptNames.extend(
						scriptName
						for cls, scriptName in globalMap.getScriptsForGesture(fakeGestureId.lower())
						if scriptName and scriptName.startswith("kb")
					)
			if not scriptNames:
				# Gesture contains modifiers, but no keyboard emulate script exists for the gesture without modifiers
				return None
			# We can't bother about multiple scripts for a gesture, we will just use the first one
			combinedScriptName = "kb:{modifiers}+{keys}".format(
				modifiers="+".join(gestureModifiers),
				keys=scriptNames[0].split(":")[1],
			)
		elif script and scriptName:
			combinedScriptName = "kb:{modifiers}+{keys}".format(
				modifiers="+".join(gestureModifiers),
				keys=scriptName.split(":")[1],
			)
		else:
			return None
		self.script = scriptHandler._makeKbEmulateScript(combinedScriptName)
		brailleInput.handler.currentModifiers.clear()
		return self.script

	def _get_keyNames(self):
		"""The names of the keys that are part of this gesture.
		@rtype: list
		"""
		return self.id.split("+")

	def _get_speechEffectWhenExecuted(self) -> Optional[str]:
		from globalCommands import commands

		if not config.conf["braille"]["interruptSpeechWhileScrolling"] and self.script in {
			commands.script_braille_scrollBack,
			commands.script_braille_scrollForward,
		}:
			return None
		return super().speechEffectWhenExecuted

	#: Compiled regular expression to match an identifier including an optional model name
	#: The model name should be an alphanumeric string without spaces.
	#: @type: RegexObject
	ID_PARTS_REGEX = re.compile(r"br\((\w+)(?:\.(\w+))?\):([\w+]+)", re.U)

	@classmethod
	def getDisplayTextForIdentifier(cls, identifier):
		# Translators: Displayed when the source driver of a braille display gesture is unknown.
		unknownDisplayDescription = _("Unknown braille display")
		idParts = cls.ID_PARTS_REGEX.match(identifier)
		if not idParts:
			log.error("Invalid braille gesture identifier: %s" % identifier)
			return unknownDisplayDescription, "malformed:%s" % identifier
		source, modelName, key = idParts.groups()
		# Optimisation: Do not try to get the braille display class if this identifier belongs to the current driver.
		if braille.handler.display.name.lower() == source.lower():
			description = braille.handler.display.description
		else:
			try:
				description = _getDisplayDriver(source, caseSensitive=False).description
			except ImportError:
				description = unknownDisplayDescription
		if modelName:  # The identifier contains a model name
			return description, "{modelName}: {key}".format(
				modelName=modelName,
				key=key,
			)
		else:
			return description, key


inputCore.registerGestureSource("br", BrailleDisplayGesture)
