# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import json
import unittest
from enum import Enum
from remoteClient.serializer import JSONSerializer, CustomEncoder, as_sequence


# Create a dummy Enum for test purposes.
class DummyEnum(Enum):
	VALUE1 = "value1"
	VALUE2 = "value2"


# Dummy command for testing CustomEncoder fallback.
class DummyCommand:
	def __init__(self, data):
		self.data = data


class TestJSONSerializer(unittest.TestCase):
	def setUp(self):
		self.serializer = JSONSerializer()

	def test_serialize_basic(self):
		# Test basic serialization with a string type and payload.
		message_bytes = self.serializer.serialize(type="test_message", key=123)
		self.assertTrue(message_bytes.endswith(b"\n"))
		message_str = message_bytes.rstrip(b"\n").decode("UTF-8")
		data = json.loads(message_str)
		self.assertEqual(data["type"], "test_message")
		self.assertEqual(data["key"], 123)

	def test_serialize_enum(self):
		# Test that passing an Enum type is serialized to its value.
		message_bytes = self.serializer.serialize(type=DummyEnum.VALUE1, key="abc")
		message_str = message_bytes.rstrip(b"\n").decode("UTF-8")
		data = json.loads(message_str)
		self.assertEqual(data["type"], "value1")
		self.assertEqual(data["key"], "abc")

	def test_round_trip(self):
		# Test that serializing and then deserializing returns the same message data.
		original = {"type": "round_trip", "value": 999}
		message_bytes = self.serializer.serialize(**original)
		# Remove the separator for deserialization.
		data = self.serializer.deserialize(message_bytes.rstrip(JSONSerializer.SEP))
		self.assertEqual(data["type"], "round_trip")
		self.assertEqual(data["value"], 999)

	def test_custom_encoder(self):
		# Test that CustomEncoder falls back to default behavior for non-special objects.
		dummy = DummyCommand("test")
		# Set __dict__ to a non-serializable object (set is not serializable by default)
		dummy.__dict__ = {"data": {1, 2, 3}}
		with self.assertRaises(TypeError) as cm:
			json.dumps(dummy, cls=CustomEncoder)
		self.assertRegex(str(cm.exception), "not JSON serializable")
		# Even if __dict__ is set to a serializable value, it should still raise error.
		dummy.__dict__ = {"data": "testdata"}
		with self.assertRaises(TypeError) as cm:
			json.dumps(dummy, cls=CustomEncoder)
		self.assertRegex(str(cm.exception), "not JSON serializable")

	def test_as_sequence_no_change(self):
		# Test that as_sequence returns the dictionary unchanged when no special keys exist.
		input_dict = {"type": "other", "foo": "bar"}
		result = as_sequence(input_dict)
		self.assertEqual(result, input_dict)


if __name__ == "__main__":
	unittest.main()
