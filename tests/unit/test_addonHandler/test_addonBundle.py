# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Christopher Toth
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Unit tests for the AddonBundle module."""

import os
import tempfile
import unittest
import zipfile
from unittest.mock import MagicMock, PropertyMock, mock_open, patch

from addonHandler.addonBase import AddonError
from addonHandler.AddonBundle import AddonBundle, createAddonBundleFromPath


class TestAddonBundle(unittest.TestCase):
	"""Tests for the AddonBundle class."""

	def assertAddonError(self, callable_obj, expected_message=None, expected_substring=None):
		"""Helper method to test for AddonError exceptions.

		Args:
			callable_obj: A callable that should raise AddonError
			expected_message: The exact error message expected (optional)
			expected_substring: A substring that should be in the error message (optional)
		"""
		with self.assertRaises(AddonError) as context:
			callable_obj()

		if expected_message is not None:
			self.assertEqual(expected_message, str(context.exception))

		if expected_substring is not None:
			self.assertIn(expected_substring, str(context.exception))

		return context.exception

	def create_mock_bundle(self, mock_zipfile, manifest_errors=None):
		"""Helper method to create a mock bundle with the specified configuration.

		Args:
			mock_zipfile: The mocked zipfile.ZipFile
			manifest_errors: Errors to include in the manifest, or None for a valid manifest

		Returns:
			tuple: (bundle, mock_zip_instance)
		"""
		# Setup mock zipfile
		mock_zip_instance = MagicMock()
		mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

		# Mock the manifest file in the zip
		mock_manifest = MagicMock()
		mock_zip_instance.open.return_value = mock_manifest

		# Mock AddonManifest
		mock_manifest_obj = MagicMock()
		mock_manifest_obj.errors = manifest_errors

		with patch("addonHandler.AddonBundle.AddonManifest", return_value=mock_manifest_obj):
			# Create an AddonBundle - this will raise an error if manifest_errors is not None
			bundle = AddonBundle("path/to/addon.nvda-addon")
			return (bundle, mock_zip_instance)

	def setUp(self):
		"""Set up test environment."""
		# Create a temporary directory for test files
		self.temp_dir = tempfile.mkdtemp()
		self.created_files = []

		# Use shutil.rmtree for proper recursive cleanup
		import shutil

		self.addCleanup(lambda: shutil.rmtree(self.temp_dir, ignore_errors=True))

		# Track any files created outside the temp directory
		self.addCleanup(self.cleanup_created_files)

		# Mock manifest content
		self.manifest_content = """
name = "test-addon"
summary = "Test Addon"
description = "Test addon for unit testing"
author = "NVDA Tests"
version = "1.0.0"
minimumNVDAVersion = "2023.1.0"
lastTestedNVDAVersion = "2023.1.0"
"""

	def cleanup_created_files(self):
		"""Clean up any files created outside the temp directory."""
		for file_path in self.created_files:
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					import shutil

					shutil.rmtree(file_path, ignore_errors=True)
			except (OSError, IOError):
				pass  # Ignore errors during cleanup

	@patch("zipfile.ZipFile")
	def test_init_valid_bundle(self, mock_zipfile):
		"""Test initialization with a valid addon bundle."""
		# Setup mock zipfile
		mock_zip_instance = MagicMock()
		mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

		# Mock the manifest file in the zip
		mock_manifest = MagicMock()
		mock_zip_instance.open.return_value = mock_manifest

		# Mock AddonManifest to return a valid manifest
		mock_manifest_obj = MagicMock()
		mock_manifest_obj.errors = None

		with patch("addonHandler.AddonBundle.AddonManifest", return_value=mock_manifest_obj):
			# Create an AddonBundle
			bundle = AddonBundle("path/to/addon.nvda-addon")

			# Verify the bundle was created correctly
			self.assertEqual(bundle._path, "path/to/addon.nvda-addon")
			self.assertEqual(bundle.manifest, mock_manifest_obj)

			# Verify zipfile was opened
			mock_zipfile.assert_called_once_with("path/to/addon.nvda-addon", "r")

	@patch("zipfile.ZipFile")
	def test_init_invalid_zip(self, mock_zipfile):
		"""Test initialization with an invalid zip file."""
		# Make zipfile.ZipFile raise a BadZipfile exception
		mock_zipfile.side_effect = zipfile.BadZipfile("Invalid zip file")

		# Attempt to create an AddonBundle with an invalid zip
		with self.assertRaises(AddonError) as context:
			AddonBundle("path/to/invalid.nvda-addon")

		# Verify the error message
		self.assertIn("Invalid bundle file", str(context.exception))

	@patch("zipfile.ZipFile")
	def test_init_missing_file(self, mock_zipfile):
		"""Test initialization with a missing file."""
		# Make zipfile.ZipFile raise a FileNotFoundError
		mock_zipfile.side_effect = FileNotFoundError("File not found")

		# Attempt to create an AddonBundle with a missing file
		with self.assertRaises(AddonError) as context:
			AddonBundle("path/to/nonexistent.nvda-addon")

		# Verify the error message
		self.assertIn("Invalid bundle file", str(context.exception))

	@patch("zipfile.ZipFile")
	def test_init_manifest_errors(self, mock_zipfile):
		"""Test initialization with manifest errors."""
		# Setup mock zipfile
		mock_zip_instance = MagicMock()
		mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

		# Mock the manifest file in the zip
		mock_manifest = MagicMock()
		mock_zip_instance.open.return_value = mock_manifest

		# Mock AddonManifest to return a manifest with errors
		mock_manifest_obj = MagicMock()
		mock_manifest_obj.errors = "Some manifest errors"

		with patch("addonHandler.AddonBundle.AddonManifest", return_value=mock_manifest_obj):
			with patch("addonHandler.AddonBundle._report_manifest_errors"):
				# Test that creating an AddonBundle with manifest errors raises AddonError
				self.assertAddonError(
					lambda: AddonBundle("path/to/addon.nvda-addon"),
					expected_message="Manifest file has errors.",
				)

	@patch("zipfile.ZipFile")
	def test_extract(self, mock_zipfile):
		"""Test extracting the bundle."""
		# Setup mock zipfile
		mock_zip_instance = MagicMock()
		mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

		# Mock the manifest file in the zip
		mock_manifest = MagicMock()
		mock_zip_instance.open.return_value = mock_manifest

		# Mock AddonManifest to return a valid manifest
		mock_manifest_obj = MagicMock()
		mock_manifest_obj.errors = None

		# Create test info list for the zip
		mock_info1 = MagicMock()
		mock_info1.filename = "file1.txt"
		mock_info2 = MagicMock()
		mock_info2.filename = "file2.txt"
		mock_zip_instance.infolist.return_value = [mock_info1, mock_info2]

		with patch("addonHandler.AddonBundle.AddonManifest", return_value=mock_manifest_obj):
			# Create an AddonBundle
			bundle = AddonBundle("path/to/addon.nvda-addon")

			# Extract the bundle
			bundle.extract("extract/path")

			# Verify the extraction
			mock_zip_instance.extract.assert_any_call(mock_info1, "extract/path")
			mock_zip_instance.extract.assert_any_call(mock_info2, "extract/path")

	@patch("zipfile.ZipFile")
	def test_extract_bytes_filename(self, mock_zipfile):
		"""Test extracting the bundle with bytes filenames."""
		# Setup mock zipfile
		mock_zip_instance = MagicMock()
		mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

		# Mock the manifest file in the zip
		mock_manifest = MagicMock()
		mock_zip_instance.open.return_value = mock_manifest

		# Mock AddonManifest to return a valid manifest
		mock_manifest_obj = MagicMock()
		mock_manifest_obj.errors = None

		# Create test info with bytes filename
		mock_info = MagicMock()
		mock_info.filename = b"file1.txt"
		mock_zip_instance.infolist.return_value = [mock_info]

		# Mock winKernel.kernel32.GetOEMCP to return a code page
		with patch("winKernel.kernel32.GetOEMCP", return_value=437):
			with patch("addonHandler.AddonBundle.AddonManifest", return_value=mock_manifest_obj):
				# Create an AddonBundle
				bundle = AddonBundle("path/to/addon.nvda-addon")

				# Extract the bundle
				bundle.extract("extract/path")

				# Verify the extraction and filename decoding
				self.assertEqual(mock_info.filename, "file1.txt")
				mock_zip_instance.extract.assert_called_once_with(mock_info, "extract/path")

	@patch("zipfile.ZipFile")
	def test_extract_default_path(self, mock_zipfile):
		"""Test extracting the bundle with default path."""
		# Setup mock zipfile
		mock_zip_instance = MagicMock()
		mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

		# Mock the manifest file in the zip
		mock_manifest = MagicMock()
		mock_zip_instance.open.return_value = mock_manifest

		# Mock AddonManifest to return a valid manifest
		mock_manifest_obj = MagicMock()
		mock_manifest_obj.errors = None

		# Create test info list for the zip
		mock_info = MagicMock()
		mock_info.filename = "file1.txt"
		mock_zip_instance.infolist.return_value = [mock_info]

		with patch("addonHandler.AddonBundle.AddonManifest", return_value=mock_manifest_obj):
			# Create an AddonBundle
			bundle = AddonBundle("path/to/addon.nvda-addon")

			# Create a property mock for pendingInstallPath
			with patch.object(
				AddonBundle,
				"pendingInstallPath",
				new_callable=PropertyMock,
				return_value="pending/install/path",
			):
				# Extract the bundle without specifying a path
				bundle.extract()

				# Verify the extraction used the pendingInstallPath
				mock_zip_instance.extract.assert_called_once_with(mock_info, "pending/install/path")

	@patch("os.path.isfile")
	@patch("zipfile.ZipFile")
	def test_create_addon_bundle_from_path(self, mock_zipfile, mock_isfile):
		"""Test creating an addon bundle from a directory path."""
		# Setup mocks
		mock_isfile.return_value = True

		# Create test file content
		file1_content = "# Test Python file 1"
		file2_content = "# Test Python file 2"

		# Mock file reads for different files
		def mock_open_files(filename, *args, **kwargs):
			mock_file = MagicMock()
			if filename.endswith("manifest.ini"):
				mock_file.read.return_value = self.manifest_content.encode()
			elif filename.endswith("file1.py"):
				mock_file.read.return_value = file1_content.encode()
			elif filename.endswith("file2.py"):
				mock_file.read.return_value = file2_content.encode()
			return mock_file

		# Use a more sophisticated mock_open that handles different files
		with patch("builtins.open", side_effect=mock_open_files):
			# Mock AddonManifest
			mock_manifest = MagicMock()
			mock_manifest.errors = None
			mock_manifest.__getitem__.side_effect = lambda key: {"name": "test-addon", "version": "1.0.0"}[
				key
			]

			with patch("addonHandler.AddonBundle.AddonManifest", return_value=mock_manifest):
				# Mock zipfile.ZipFile
				mock_zip_instance = MagicMock()
				mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

				# Track written files and their contents
				written_files = {}

				# Override the write method to capture file contents
				def mock_write(src_path, dest_path):
					if src_path.endswith("file1.py"):
						written_files[dest_path] = file1_content
					elif src_path.endswith("file2.py"):
						written_files[dest_path] = file2_content
					elif src_path.endswith("manifest.ini"):
						written_files[dest_path] = self.manifest_content

				mock_zip_instance.write.side_effect = mock_write

				# Mock os.walk to return some files
				mock_walk_data = [
					("/path/to/addon", ["dir1"], ["manifest.ini", "file1.py"]),
					("/path/to/addon/dir1", [], ["file2.py"]),
				]

				with patch("os.walk", return_value=mock_walk_data):
					# Create bundle from path
					result = createAddonBundleFromPath("/path/to/addon", "/output/dir")

					# Verify the zipfile was created with the correct parameters
					# Use os.path.normpath to normalize the path separators
					expected_path = os.path.normpath("/output/dir/test-addon-1.0.0.nvda-addon")
					actual_path = mock_zipfile.call_args_list[0][0][0]
					self.assertEqual(os.path.normpath(actual_path), expected_path)

					# Verify files were added to the zip with correct paths
					write_calls = mock_zip_instance.write.call_args_list

					# Check manifest.ini was added
					manifest_calls = [args for args, _ in write_calls if args[0].endswith("manifest.ini")]
					self.assertEqual(len(manifest_calls), 1)
					self.assertEqual(os.path.basename(manifest_calls[0][1]), "manifest.ini")

					# Check file1.py was added
					file1_calls = [args for args, _ in write_calls if args[0].endswith("file1.py")]
					self.assertEqual(len(file1_calls), 1)
					self.assertEqual(os.path.basename(file1_calls[0][1]), "file1.py")

					# Check file2.py was added with correct directory structure
					file2_calls = [args for args, _ in write_calls if args[0].endswith("file2.py")]
					self.assertEqual(len(file2_calls), 1)
					self.assertTrue("dir1" in file2_calls[0][1])
					self.assertEqual(os.path.basename(file2_calls[0][1]), "file2.py")

					# Verify the result is an AddonBundle
					self.assertIsInstance(result, AddonBundle)

	@patch("os.path.isfile")
	def test_create_addon_bundle_missing_manifest(self, mock_isfile):
		"""Test creating an addon bundle with missing manifest."""
		# Setup mock to indicate manifest file doesn't exist
		mock_isfile.return_value = False

		# Attempt to create bundle from path with missing manifest
		with self.assertRaises(AddonError) as context:
			createAddonBundleFromPath("/path/to/addon")

		# Verify the error message
		self.assertIn("Can't find", str(context.exception))
		self.assertIn("manifest file", str(context.exception))

	@patch("os.path.isfile")
	def test_create_addon_bundle_manifest_errors(self, mock_isfile):
		"""Test creating an addon bundle with manifest errors."""
		# Setup mock to indicate manifest file exists
		mock_isfile.return_value = True

		# Mock open to return manifest content
		with patch("builtins.open", mock_open(read_data=self.manifest_content.encode())):
			# Mock AddonManifest to return a manifest with errors
			mock_manifest = MagicMock()
			mock_manifest.errors = "Some manifest errors"

			with patch("addonHandler.AddonBundle.AddonManifest", return_value=mock_manifest):
				with patch("addonHandler.AddonBundle._report_manifest_errors"):
					# Attempt to create bundle from path with manifest errors
					with self.assertRaises(AddonError) as context:
						createAddonBundleFromPath("/path/to/addon")

					# Verify the error message
					self.assertEqual("Manifest file has errors.", str(context.exception))

	@patch("os.path.isfile")
	@patch("zipfile.ZipFile")
	def test_create_addon_bundle_zip_error(self, mock_zipfile, mock_isfile):
		"""Test error handling during zip file creation."""
		# Setup mocks
		mock_isfile.return_value = True

		# Mock open to return manifest content
		with patch("builtins.open", mock_open(read_data=self.manifest_content.encode())):
			# Mock AddonManifest
			mock_manifest = MagicMock()
			mock_manifest.errors = None
			mock_manifest.__getitem__.side_effect = lambda key: {"name": "test-addon", "version": "1.0.0"}[
				key
			]

			with patch("addonHandler.AddonBundle.AddonManifest", return_value=mock_manifest):
				# Make zipfile.ZipFile raise an error
				mock_zipfile.side_effect = OSError("Failed to create zip file")

				# Attempt to create bundle
				with self.assertRaises(OSError) as context:
					createAddonBundleFromPath("/path/to/addon", "/output/dir")

				# Verify the error message
				self.assertIn("Failed to create zip file", str(context.exception))

	@patch("os.path.isfile")
	@patch("zipfile.ZipFile")
	def test_create_addon_bundle_write_error(self, mock_zipfile, mock_isfile):
		"""Test error handling during file writing to zip."""
		# Setup mocks
		mock_isfile.return_value = True

		# Mock open to return manifest content
		with patch("builtins.open", mock_open(read_data=self.manifest_content.encode())):
			# Mock AddonManifest
			mock_manifest = MagicMock()
			mock_manifest.errors = None
			mock_manifest.__getitem__.side_effect = lambda key: {"name": "test-addon", "version": "1.0.0"}[
				key
			]

			with patch("addonHandler.AddonBundle.AddonManifest", return_value=mock_manifest):
				# Setup mock zipfile
				mock_zip_instance = MagicMock()
				mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

				# Make zip.write raise an error
				mock_zip_instance.write.side_effect = OSError("Failed to write file to zip")

				# Mock os.walk to return some files
				mock_walk_data = [
					("/path/to/addon", [], ["manifest.ini"]),
				]

				with patch("os.walk", return_value=mock_walk_data):
					# Attempt to create bundle
					with self.assertRaises(OSError) as context:
						createAddonBundleFromPath("/path/to/addon", "/output/dir")

					# Verify the error message
					self.assertIn("Failed to write file to zip", str(context.exception))

	@patch("os.path.isfile")
	@patch("zipfile.ZipFile")
	def test_path_normalization(self, mock_zipfile, mock_isfile):
		"""Test path normalization across different platforms."""
		# Setup mocks
		mock_isfile.return_value = True

		# Mock open to return manifest content
		with patch("builtins.open", mock_open(read_data=self.manifest_content.encode())):
			# Mock AddonManifest
			mock_manifest = MagicMock()
			mock_manifest.errors = None
			mock_manifest.__getitem__.side_effect = lambda key: {"name": "test-addon", "version": "1.0.0"}[
				key
			]

			with patch("addonHandler.AddonBundle.AddonManifest", return_value=mock_manifest):
				# Mock zipfile.ZipFile
				mock_zip_instance = MagicMock()
				mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

				# Create mixed path separators to test normalization
				mixed_path_data = [
					(r"C:\path\to\addon", ["dir1"], ["manifest.ini"]),
					(r"C:\path\to\addon/dir1", [], ["file.py"]),
				]

				with patch("os.walk", return_value=mixed_path_data):
					# Create bundle from path
					createAddonBundleFromPath(r"C:\path\to\addon", r"C:\output\dir")

					# Verify the zipfile was created with the correct parameters
					expected_path = os.path.normpath(r"C:\output\dir\test-addon-1.0.0.nvda-addon")
					actual_path = mock_zipfile.call_args_list[0][0][0]
					self.assertEqual(os.path.normpath(actual_path), expected_path)

					# Check that paths in the zip are normalized
					write_calls = mock_zip_instance.write.call_args_list
					for args, _ in write_calls:
						# The second argument is the path in the zip file
						# It should use the platform's path separator consistently
						zip_path = args[1]
						self.assertFalse(
							"\\" in zip_path and "/" in zip_path,
							f"Path contains mixed separators: {zip_path}",
						)

	def test_real_file_operations(self):
		"""Integration test with real files."""
		# Create a test addon directory structure
		addon_dir = os.path.join(self.temp_dir, "test-addon")
		os.makedirs(addon_dir)
		self.created_files.append(addon_dir)

		# Create manifest file
		manifest_path = os.path.join(addon_dir, "manifest.ini")
		with open(manifest_path, "w") as f:
			f.write(self.manifest_content)

		# Create a Python file
		addon_code_dir = os.path.join(addon_dir, "globalPlugins")
		os.makedirs(addon_code_dir)
		test_plugin_path = os.path.join(addon_code_dir, "test.py")
		with open(test_plugin_path, "w") as f:
			f.write("# Test plugin file\n")

		# Create the bundle
		output_dir = os.path.join(self.temp_dir, "output")
		os.makedirs(output_dir)
		self.created_files.append(output_dir)

		bundle = createAddonBundleFromPath(addon_dir, output_dir)

		# Verify the bundle was created
		self.assertTrue(os.path.isfile(bundle._path))
		self.assertEqual(bundle.manifest["name"], "test-addon")
		self.assertEqual(bundle.manifest["version"], "1.0.0")

		# Extract the bundle to a new location
		extract_dir = os.path.join(self.temp_dir, "extracted")
		os.makedirs(extract_dir)
		self.created_files.append(extract_dir)

		bundle.extract(extract_dir)

		# Verify the extracted files
		self.assertTrue(os.path.isfile(os.path.join(extract_dir, "manifest.ini")))
		self.assertTrue(os.path.isfile(os.path.join(extract_dir, "globalPlugins", "test.py")))

		# Verify the content of the extracted files
		with open(os.path.join(extract_dir, "manifest.ini"), "r") as f:
			extracted_manifest = f.read()
			self.assertEqual(extracted_manifest.strip(), self.manifest_content.strip())

		with open(os.path.join(extract_dir, "globalPlugins", "test.py"), "r") as f:
			extracted_plugin = f.read()
			self.assertEqual(extracted_plugin.strip(), "# Test plugin file")

	def test_repr(self):
		"""Test the string representation of AddonBundle."""
		# Create a mock AddonBundle
		bundle = AddonBundle.__new__(AddonBundle)
		bundle._path = "path/to/addon.nvda-addon"

		# Check the string representation
		self.assertEqual(repr(bundle), "<AddonBundle at path/to/addon.nvda-addon>")
