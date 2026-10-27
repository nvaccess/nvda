# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for Addon.getLogModulePrefixes, used to filter the log viewer by add-on."""

import os
import tempfile
import unittest

import addonHandler

MANIFEST_CONTENTS = """name = testAddon
summary = Test add-on
author = Test author
version = 0.1
"""


class TestGetLogModulePrefixes(unittest.TestCase):
	"""Tests for Addon.getLogModulePrefixes."""

	def _makeAddon(self, dirName: str) -> addonHandler.Addon:
		addonPath = os.path.join(self._tempDir.name, dirName)
		os.makedirs(addonPath)
		with open(os.path.join(addonPath, addonHandler.MANIFEST_FILENAME), "w", encoding="utf-8") as f:
			f.write(MANIFEST_CONTENTS)
		return addonHandler.Addon(addonPath)

	def setUp(self) -> None:
		self._tempDir = tempfile.TemporaryDirectory()

	def tearDown(self) -> None:
		self._tempDir.cleanup()

	def test_moduleFileIncluded(self):
		"""A plain module file in a plugin-type directory contributes a prefix."""
		addon = self._makeAddon("testAddon")
		pluginDir = os.path.join(addon.path, "globalPlugins")
		os.makedirs(pluginDir)
		open(os.path.join(pluginDir, "foo.py"), "w").close()
		self.assertIn("globalPlugins.foo", addon.getLogModulePrefixes())

	def test_subPackageIncluded(self):
		"""A sub-package (directory with __init__.py) in a plugin-type directory contributes a prefix."""
		addon = self._makeAddon("testAddon")
		subPackageDir = os.path.join(addon.path, "appModules", "notepad")
		os.makedirs(subPackageDir)
		open(os.path.join(subPackageDir, "__init__.py"), "w").close()
		self.assertIn("appModules.notepad", addon.getLogModulePrefixes())

	def test_initPyItselfExcluded(self):
		"""The package's own __init__.py does not contribute a prefix for itself."""
		addon = self._makeAddon("testAddon")
		pluginDir = os.path.join(addon.path, "globalPlugins")
		os.makedirs(pluginDir)
		open(os.path.join(pluginDir, "__init__.py"), "w").close()
		prefixes = addon.getLogModulePrefixes()
		self.assertNotIn("globalPlugins.__init__", prefixes)
		self.assertFalse(any(p.startswith("globalPlugins.") for p in prefixes))

	def test_missingPluginDirectorySkipped(self):
		"""A plugin-type directory the add-on does not contain is silently skipped."""
		addon = self._makeAddon("testAddon")
		# No plugin-type directories are created at all.
		prefixes = addon.getLogModulePrefixes()
		self.assertFalse(any("." in p and not p.startswith("addons.") for p in prefixes))

	def test_nonIdentifierEntryExcluded(self):
		"""A file or directory whose name is not a valid Python module name is excluded."""
		addon = self._makeAddon("testAddon")
		pluginDir = os.path.join(addon.path, "globalPlugins")
		os.makedirs(pluginDir)
		# Hyphens are not valid in Python identifiers.
		open(os.path.join(pluginDir, "not-a-module.py"), "w").close()
		prefixes = addon.getLogModulePrefixes()
		self.assertFalse(any(p.startswith("globalPlugins.") for p in prefixes))

	def test_loadModulePrefixAlwaysIncluded(self):
		"""The synthetic prefix used by Addon.loadModule (e.g. for installTasks) is always included,
		with dots in the add-on's directory name replaced by underscores.
		"""
		addon = self._makeAddon("testAddon.pendingInstall")
		self.assertIn("addons.testAddon_pendingInstall", addon.getLogModulePrefixes())
