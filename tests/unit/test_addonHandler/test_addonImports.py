# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the cleanup of add-on modules imported into sys.modules."""

import os
import sys
import tempfile
import types
import unittest

import addonHandler

MANIFEST_CONTENTS = """name = testAddon
summary = Test add-on
author = Test author
version = 0.1
"""

ADDON_MODULE_CONTENTS: dict[str, str] = {
	"__init__.py": "",
	"sibling.py": "",
	"mainMod.py": "from . import sibling\n",
}


class TestCleanupAddonImports(unittest.TestCase):
	"""Tests for the removal of an add-on's modules from sys.modules by Addon._cleanupAddonImports."""

	def setUp(self) -> None:
		self._modulesBefore = set(sys.modules)
		self._tempDir = tempfile.TemporaryDirectory()
		addonPath = os.path.join(self._tempDir.name, "testAddon")
		libPath = os.path.join(addonPath, "lib")
		os.makedirs(libPath)
		with open(os.path.join(addonPath, addonHandler.MANIFEST_FILENAME), "w", encoding="utf-8") as f:
			f.write(MANIFEST_CONTENTS)
		for fileName, contents in ADDON_MODULE_CONTENTS.items():
			with open(os.path.join(libPath, fileName), "w", encoding="utf-8") as f:
				f.write(contents)
		self.addon = addonHandler.Addon(addonPath)
		self.addon._modulesBeforeInstall = set(sys.modules)

	def tearDown(self) -> None:
		for modName in set(sys.modules) - self._modulesBefore:
			del sys.modules[modName]
		self._tempDir.cleanup()

	def _injectModule(self, name: str) -> types.ModuleType:
		"""Adds a synthetic module to sys.modules and returns it.

		:param name: The name to register the module under.
		:return: The registered module.
		"""
		module = types.ModuleType(name)
		sys.modules[name] = module
		return module

	def test_transitivelyImportedAddonModuleRemoved(self):
		"""A module imported by another add-on module rather than by loadModule is removed."""
		self.addon.loadModule("lib.mainMod")
		siblingName = "addons.testAddon.lib.sibling"
		self.assertIn(siblingName, sys.modules)
		self.assertNotIn(siblingName, self.addon._importedAddonModules)
		self.addon._cleanupAddonImports()
		self.assertNotIn(siblingName, sys.modules)

	def test_addonModuleRemovedRegardlessOfPathCase(self):
		"""A module whose file path differs from the add-on path only in case is removed."""
		module = self._injectModule("fakeCasedAddonModule")
		module.__file__ = os.path.join(self.addon.path.upper(), "lib", "mod.py")
		self.addon._cleanupAddonImports()
		self.assertNotIn("fakeCasedAddonModule", sys.modules)

	def test_moduleWithoutFileAttributeKept(self):
		"""A module without a __file__ attribute survives the cleanup."""
		self._injectModule("fakeBuiltinModule")
		self.addon._cleanupAddonImports()
		self.assertIn("fakeBuiltinModule", sys.modules)

	def test_moduleFromSiblingPathPrefixKept(self):
		"""A module from a directory whose path starts with the add-on path survives the cleanup."""
		module = self._injectModule("fakeSiblingPathModule")
		module.__file__ = os.path.join(self.addon.path + "Extra", "mod.py")
		self.addon._cleanupAddonImports()
		self.assertIn("fakeSiblingPathModule", sys.modules)

	def test_moduleWithNoneFileKept(self):
		"""A module whose __file__ attribute is None survives the cleanup."""
		module = self._injectModule("fakeNamespaceModule")
		module.__file__ = None
		self.addon._cleanupAddonImports()
		self.assertIn("fakeNamespaceModule", sys.modules)

	def test_recordedModulesRemovedAndListCleared(self):
		"""Modules recorded by loadModule are removed and the record is emptied."""
		self.addon.loadModule("lib.mainMod")
		recordedNames = list(self.addon._importedAddonModules)
		self.assertIn("addons.testAddon.lib.mainMod", recordedNames)
		self.addon._cleanupAddonImports()
		for modName in recordedNames:
			self.assertNotIn(modName, sys.modules)
		self.assertEqual(self.addon._importedAddonModules, [])
