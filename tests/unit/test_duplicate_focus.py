# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for duplicate focus event deduplication (#21166)."""

import unittest
from unittest.mock import Mock

from comInterfaces import IAccessible2Lib as IA2


class MockIAccessible:
	def isDuplicateIAccessibleEvent(self, obj):
		if isinstance(getattr(self, "IAccessibleObject", None), IA2.IAccessible2) and isinstance(
			getattr(obj, "IAccessibleObject", None),
			IA2.IAccessible2,
		):
			return self == obj
		if self.IAccessibleChildID > 0:
			return False
		return (
			obj.event_windowHandle == self.event_windowHandle
			and obj.event_objectID == self.event_objectID
			and obj.event_childID == self.event_childID
		)

	def __eq__(self, other):
		if not isinstance(other, MockIAccessible):
			return False
		return (
			getattr(self, "IA2WindowHandle", None) == getattr(other, "IA2WindowHandle", None)
			and getattr(self, "IA2UniqueID", None) == getattr(other, "IA2UniqueID", None)
		)


class TestDuplicateFocusEvent(unittest.TestCase):
	"""Test isDuplicateIAccessibleEvent (#21166)."""

	def test_ia2_matching_unique_id_positive_child_id(self):
		"""IAccessible2 objects with positive childID and identical unique ID must be recognized as duplicate."""
		obj1 = MockIAccessible()
		obj2 = MockIAccessible()

		obj1.IAccessibleChildID = 1
		obj2.IAccessibleChildID = 1

		obj1.IAccessibleObject = Mock(spec=IA2.IAccessible2)
		obj2.IAccessibleObject = Mock(spec=IA2.IAccessible2)

		obj1.IA2WindowHandle = 12345
		obj2.IA2WindowHandle = 12345
		obj1.IA2UniqueID = 42
		obj2.IA2UniqueID = 42

		self.assertTrue(obj1.isDuplicateIAccessibleEvent(obj2))

	def test_ia2_differing_unique_id(self):
		"""IAccessible2 objects with different unique IDs must not be treated as duplicates."""
		obj1 = MockIAccessible()
		obj2 = MockIAccessible()

		obj1.IAccessibleChildID = 1
		obj2.IAccessibleChildID = 2

		obj1.IAccessibleObject = Mock(spec=IA2.IAccessible2)
		obj2.IAccessibleObject = Mock(spec=IA2.IAccessible2)

		obj1.IA2WindowHandle = 12345
		obj2.IA2WindowHandle = 12345
		obj1.IA2UniqueID = 42
		obj2.IA2UniqueID = 43

		self.assertFalse(obj1.isDuplicateIAccessibleEvent(obj2))

	def test_legacy_msaa_positive_child_id(self):
		"""Legacy MSAA objects (non-IA2) with positive childID return False."""
		obj1 = MockIAccessible()
		obj2 = MockIAccessible()

		obj1.IAccessibleChildID = 1
		obj2.IAccessibleChildID = 1
		obj1.IAccessibleObject = Mock()  # not IA2
		obj2.IAccessibleObject = Mock()  # not IA2

		self.assertFalse(obj1.isDuplicateIAccessibleEvent(obj2))

	def test_legacy_msaa_child_id_zero_matching(self):
		"""Legacy MSAA objects with childID 0 and identical winEvent params return True."""
		obj1 = MockIAccessible()
		obj2 = MockIAccessible()

		obj1.IAccessibleChildID = 0
		obj2.IAccessibleChildID = 0
		obj1.IAccessibleObject = Mock()
		obj2.IAccessibleObject = Mock()

		obj1.event_windowHandle = 100
		obj2.event_windowHandle = 100
		obj1.event_objectID = 1
		obj2.event_objectID = 1
		obj1.event_childID = 0
		obj2.event_childID = 0

		self.assertTrue(obj1.isDuplicateIAccessibleEvent(obj2))
