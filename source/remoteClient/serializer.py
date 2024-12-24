"""Message serialization for remote NVDA communication.

This module handles serializing and deserializing messages between NVDA instances,
with special handling for speech commands and other NVDA-specific data types.
It provides both a generic Serializer interface and a concrete JSONSerializer
implementation that handles the specific message format used by NVDA Remote.

The serialization format supports:
- Basic JSON data types
- Speech command objects
- Custom message types via the 'type' field
"""

from abc import abstractmethod
from enum import Enum
from logging import getLogger
from typing import Any, Dict, Optional, Type, Union, TypeVar
import json

import speech.commands

log = getLogger("serializer")

T = TypeVar("T")
JSONDict = Dict[str, Any]


class Serializer:
	"""Base class for message serialization.

	Defines the interface for serializing messages between NVDA instances.
	Concrete implementations should handle converting Python objects to/from
	a wire format suitable for network transmission.
	"""

	@abstractmethod
	def serialize(self, type: Optional[str] = None, **obj: Any) -> bytes:
		"""Convert a message to bytes for transmission.

		Args:
			type: Message type identifier, used for routing
			**obj: Message payload as keyword arguments

		Returns:
			Serialized message as bytes
		"""
		raise NotImplementedError

	@abstractmethod
	def deserialize(self, data: bytes) -> JSONDict:
		"""Convert received bytes back into a message dict.

		Args:
			data: Raw message bytes to deserialize

		Returns:
			Dict containing the deserialized message
		"""
		raise NotImplementedError


class JSONSerializer(Serializer):
	"""JSON-based message serializer with NVDA-specific type handling.

	Implements message serialization using JSON encoding with special handling for
	NVDA speech commands and other custom types. Messages are encoded as UTF-8
	with newline separation.
	"""

	SEP: bytes = b"\n"  # Message separator for streaming protocols

	def serialize(self, type: Optional[str] = None, **obj: Any) -> bytes:
		"""Serialize a message to JSON bytes.

		Converts message type and payload to JSON format, handling Enum types
		and using CustomEncoder for NVDA-specific objects.

		Args:
			type: Message type identifier (string or Enum)
			**obj: Message payload to serialize

		Returns:
			UTF-8 encoded JSON with newline separator
		"""
		if type is not None:
			if isinstance(type, Enum):
				type = type.value
		obj["type"] = type
		data = json.dumps(obj, cls=CustomEncoder).encode("UTF-8") + self.SEP
		return data

	def deserialize(self, data: bytes) -> JSONDict:
		"""Deserialize JSON message bytes.

		Converts JSON bytes back to a dict, using as_sequence hook to
		reconstruct NVDA speech commands.

		Args:
			data: UTF-8 encoded JSON bytes

		Returns:
			Dict containing the deserialized message
		"""
		obj = json.loads(data, object_hook=as_sequence)
		return obj


SEQUENCE_CLASSES = (
	speech.commands.SynthCommand,
	speech.commands.EndUtteranceCommand,
)


class CustomEncoder(json.JSONEncoder):
	"""Custom JSON encoder for NVDA speech commands.

	Handles serialization of speech command objects by converting them
	to a list containing their class name and instance variables.
	"""

	def default(self, obj: Any) -> Any:
		"""Convert speech commands to serializable format.

		Args:
			obj: Object to serialize

		Returns:
			List containing [class_name, instance_vars] for speech commands,
			or default JSON encoding for other types
		"""
		if is_subclass_or_instance(obj, SEQUENCE_CLASSES):
			return [obj.__class__.__name__, obj.__dict__]
		return super().default(obj)


def is_subclass_or_instance(unknown: Any, possible: Union[Type[T], tuple[Type[T], ...]]) -> bool:
	"""Check if an object is a subclass or instance of given type(s).

	Safely handles both types and instances, useful for type checking
	during serialization.

	Args:
		unknown: Object or type to check
		possible: Type or tuple of types to check against

	Returns:
		True if unknown is a subclass or instance of possible
	"""
	try:
		return issubclass(unknown, possible)
	except TypeError:
		return isinstance(unknown, possible)


def as_sequence(dct: JSONDict) -> JSONDict:
	"""Reconstruct speech command objects from deserialized JSON.

	Handles the 'speak' message type by converting serialized speech
	commands back into their original object form.

	Args:
		dct: Dict containing potentially serialized speech commands

	Returns:
		Dict with reconstructed speech command objects if applicable,
		otherwise returns the input unchanged
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
