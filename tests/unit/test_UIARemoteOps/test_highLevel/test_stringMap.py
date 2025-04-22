# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops Unit tests for string maps.
"""

from unittest import TestCase
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI


class Test_stringMap(TestCase):

	def test_newStringMap(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			sm = ra.newStringMap()
			ra.Return(sm)

		sm = op.execute()
		self.assertEqual(sm, {})

	def test_insert(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			sm = ra.newStringMap()
			sm['a'] = 1
			sm['b'] = 2
			ra.Return(sm)

		sm = op.execute()
		self.assertEqual(sm, {'a': 1, 'b': 2})

	def test_lookup(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			sm = ra.newStringMap()
			sm['a'] = 1
			sm['b'] = 2
			a = sm['a']
			b = sm['b']
			ra.Return(a, b)

		a, b = op.execute()
		self.assertEqual(a, 1)
		self.assertEqual(b, 2)

	def test_hasKey(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			sm = ra.newStringMap()
			sm['a'] = 1
			has_a = sm.hasKey('a')
			has_b = sm.hasKey('b')
			ra.Return(has_a, has_b)

		has_a, has_b = op.execute()
		self.assertEqual(has_a, True)
		self.assertEqual(has_b, False)

	def test_remove(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			sm = ra.newStringMap()
			sm['a'] = "hello"
			sm['b'] = "goodbye"
			sm.remove('a')
			ra.Return(sm)

		sm = op.execute()
		self.assertEqual(sm, {'b': "goodbye"})

	def test_size(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			sm = ra.newStringMap()
			initialSize = sm.size()
			sm['a'] = 1
			sm['b'] = 2
			finalSize = sm.size()
			ra.Return(initialSize, finalSize)

		initialSize, finalSize = op.execute()
		self.assertEqual(initialSize, 0)
		self.assertEqual(finalSize, 2)
