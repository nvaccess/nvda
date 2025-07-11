# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Message serialization for remote NVDA communication.

This module handles serializing and deserializing messages between NVDA instances.
It provides special handling for speech commands and other NVDA-specific data types.

Module Features
-------------
* A generic :class:`.Serializer` interface
* A concrete :class:`.JSONSerializer` implementation for NVDA Remote messages

Supported Data Types
------------------
* Basic JSON data types
* Speech command objects
* Custom message types via the 'type' field
"""

import json
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Any, Dict, Type, TypeVar, Union

import speech.commands
from logHandler import log


T = TypeVar("T")
JSONDict = Dict[str, Any]


class Serializer(metaclass=ABCMeta):
	"""Base class for message serialization.

	Defines the interface for serializing messages between NVDA instances.
	Concrete implementations should handle converting Python objects to/from
	a wire format suitable for network transmission.

	Note
	----
	This is an abstract base class. Subclasses must implement
	:meth:`serialize` and :meth:`deserialize`.
	"""

	@abstractmethod
	def serialize(self, type: str | None = None, **obj: Any) -> bytes:
		"""Convert a message to bytes for transmission.

		:param type: Message type identifier, used for routing
		:param obj: Message payload as keyword arguments
		:return: Serialized message as bytes
		:raises NotImplementedError: Must be implemented by subclasses
		"""
		raise NotImplementedError

	@abstractmethod
	def deserialize(self, data: bytes) -> JSONDict:
		"""Convert received bytes back into a message dict.

		:param data: Raw message bytes to deserialize
		:return: Dict containing the deserialized message
		:raises NotImplementedError: Must be implemented by subclasses
		"""
		raise NotImplementedError


class JSONSerializer(Serializer):
	"""JSON-based message serializer with NVDA-specific type handling.

	Implements message serialization using JSON encoding with special handling for
	NVDA speech commands and other custom types. Messages are encoded as UTF-8
	with newline separation.
	"""

	SEP: bytes = b"\n"
	"""Message separator for streaming protocols"""

	def serialize(self, type: str | None = None, **obj: Any) -> bytes:
		"""Serialize a message to JSON bytes.

		Converts message type and payload to JSON format, handling Enum types
		and using CustomEncoder for NVDA-specific objects.

		:param type: Message type identifier (string or Enum)
		:param obj: Message payload to serialize
		:return: UTF-8 encoded JSON with newline separator
		:rtype: bytes
		"""
		if type is not None:
			if isinstance(type, Enum) and not isinstance(type, str):
				type = type.value
		obj["type"] = type
		data = json.dumps(obj, cls=SpeechCommandJSONEncoder).encode("UTF-8") + self.SEP
		return data

	def deserialize(self, data: bytes) -> JSONDict:
		"""Deserialize JSON message bytes.

		Converts JSON bytes back to a dict, using as_sequence hook to
		reconstruct NVDA speech commands.

		:param data: UTF-8 encoded JSON bytes
		:return: Dict containing the deserialized message
		"""
		obj = json.loads(data, object_hook=asSequence)
		return obj


SEQUENCE_CLASSES = (
	speech.commands.SynthCommand,
	speech.commands.EndUtteranceCommand,
)


class SpeechCommandJSONEncoder(json.JSONEncoder):
	"""Custom JSON encoder for NVDA speech commands.

	Handles serialization of speech command objects by converting them
	to a list containing their class name and instance variables.

	:note: Inherits from :class:`json.JSONEncoder`
	"""

	def default(self, obj: Any) -> Any:
		"""Convert speech commands to serializable format.

		:param obj: Object to serialize
		:return: For speech commands, returns a list containing [class_name, instance_vars].
		        For other types, returns the default JSON encoding.
		"""
		if isSubclassOrInstance(obj, SEQUENCE_CLASSES):
			return [obj.__class__.__name__, obj.__dict__]
		return super().default(obj)


def isSubclassOrInstance(unknown: Any, possible: Union[Type[T], tuple[Type[T], ...]]) -> bool:
	"""Check if an object is a subclass or instance of given type(s).

	Safely handles both types and instances, useful for type checking
	during serialization.

	:param unknown: Object or type to check
	:param possible: Type or tuple of types to check against
	:return: True if unknown is a subclass or instance of possible

	Example::

	    >>> isSubclassOrInstance(str, (int, str))
	    True
	    >>> isSubclassOrInstance("hello", (int, str))
	    True
	"""
	try:
		return issubclass(unknown, possible)
	except TypeError:
		return isinstance(unknown, possible)


def asSequence(dct: JSONDict) -> JSONDict:
	"""Reconstruct speech command objects from deserialized JSON.

	Handles the 'speak' message type by converting serialized speech
	commands back into their original object form.

	:param dct: Dict containing potentially serialized speech commands
	:return: Dict with reconstructed speech command objects if applicable,
	        otherwise returns the input unchanged
	:warning: Logs a warning if an unknown sequence type is encountered

	.. warning::

		This function modifies the input dictionary in place.
		Copy the dictionary first if you need access to the unmodified data.
	"""
	if not ("type" in dct and dct["type"] == "speak" and "sequence" in dct):
		return dct
	sequence = []
	for item in dct["sequence"]:
		if not isinstance(item, list):
			sequence.append(item)
			continue
		name, values = item
		cls = getattr(speech.commands, name, None)
		if cls is None or not issubclass(cls, SEQUENCE_CLASSES):
			log.warning("Unknown sequence type received: %r" % name)
			continue
		cls = cls.__new__(cls)
		cls.__dict__.update(values)
		sequence.append(cls)
	dct["sequence"] = sequence
	return dct
