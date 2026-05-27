# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024-2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the markdownTranslate module."""

import importlib.util
import tempfile
import unittest
from unittest import mock
import subprocess
import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET


class TestMarkdownTranslate(unittest.TestCase):
	markdownTranslateScriptPath = os.path.join(
		os.path.dirname(__file__),
		"..",
		"..",
		"source",
		"markdownTranslate.py",
	)
	testDir = os.path.join(os.path.dirname(__file__), "..", "markdownTranslate")

	def setUp(self):
		self.outDir = tempfile.TemporaryDirectory()

	def tearDown(self):
		self.outDir.cleanup()

	def runMarkdownTranslateCommand(self, description: str, args: list[str]):
		failed = False
		try:
			subprocess.run(
				[sys.executable, self.markdownTranslateScriptPath, *args],
				check=True,
				capture_output=True,
			)
		except subprocess.CalledProcessError:
			failed = True
		if failed:
			message = f"Failed when trying to {description} with command: {' '.join(args)}"
			self.fail(message)

	def test_markdownTranslate(self):
		outDir = self.outDir.name
		testDir = self.testDir
		self.runMarkdownTranslateCommand(
			description="Generate an xliff file from the English 2024.2 user guide markdown file",
			args=[
				"generateXliff",
				"-m",
				os.path.join(testDir, "en_2024.2_userGuide.md"),
				"-o",
				os.path.join(outDir, "en_2024.2_userGuide.xliff"),
			],
		)
		self.runMarkdownTranslateCommand(
			description="Regenerate the 2024.2 markdown file from the generated 2024.2 xliff file",
			args=[
				"generateMarkdown",
				"-x",
				os.path.join(outDir, "en_2024.2_userGuide.xliff"),
				"-o",
				os.path.join(outDir, "rebuilt_en_2024.2_userGuide.md"),
				"-u",
			],
		)
		self.runMarkdownTranslateCommand(
			description="Ensure the regenerated 2024.2 markdown file matches the original 2024.2 markdown file",
			args=[
				"ensureMarkdownFilesMatch",
				os.path.join(outDir, "rebuilt_en_2024.2_userGuide.md"),
				os.path.join(testDir, "en_2024.2_userGuide.md"),
			],
		)
		self.runMarkdownTranslateCommand(
			description="Update the 2024.2 xliff file with the changes between the English 2024.2 and 2024.3beta6 user guide markdown files",
			args=[
				"updateXliff",
				"-x",
				os.path.join(outDir, "en_2024.2_userGuide.xliff"),
				"-m",
				os.path.join(testDir, "en_2024.3beta6_userGuide.md"),
				"-o",
				os.path.join(outDir, "en_2024.3beta6_userGuide.xliff"),
			],
		)
		self.runMarkdownTranslateCommand(
			description="Regenerate the 2024.3beta6 markdown file from the updated xliff file",
			args=[
				"generateMarkdown",
				"-x",
				os.path.join(outDir, "en_2024.3beta6_userGuide.xliff"),
				"-o",
				os.path.join(outDir, "rebuilt_en_2024.3beta6_userGuide.md"),
				"-u",
			],
		)
		self.runMarkdownTranslateCommand(
			description="Ensure the regenerated 2024.3beta6 markdown file matches the original 2024.3beta6 markdown",
			args=[
				"ensureMarkdownFilesMatch",
				os.path.join(outDir, "rebuilt_en_2024.3beta6_userGuide.md"),
				os.path.join(testDir, "en_2024.3beta6_userGuide.md"),
			],
		)
		self.runMarkdownTranslateCommand(
			description="Translate the 2024.3beta6 xliff file to French using the existing pretranslated French 2024.3beta6 user guide markdown file",
			args=[
				"translateXliff",
				"-x",
				os.path.join(outDir, "en_2024.3beta6_userGuide.xliff"),
				"-l",
				"fr",
				"-p",
				os.path.join(testDir, "fr_pretranslated_2024.3beta6_userGuide.md"),
				"-o",
				os.path.join(outDir, "fr_2024.3beta6_userGuide.xliff"),
			],
		)
		self.runMarkdownTranslateCommand(
			description="Regenerate the French 2024.3beta6 user guide markdown file from the French translated 2024.3beta6 xliff file",
			args=[
				"generateMarkdown",
				"-x",
				os.path.join(outDir, "fr_2024.3beta6_userGuide.xliff"),
				"-o",
				os.path.join(outDir, "fr_2024.3beta6_userGuide.md"),
			],
		)
		self.runMarkdownTranslateCommand(
			description="Ensure the regenerated French 2024.3beta6 user guide markdown file matches the original French 2024.3beta6 user guide markdown file",
			args=[
				"ensureMarkdownFilesMatch",
				os.path.join(outDir, "fr_2024.3beta6_userGuide.md"),
				os.path.join(testDir, "fr_pretranslated_2024.3beta6_userGuide.md"),
			],
		)

	def test_generateXliff_preservesInlineMarkdownLintCommentsInSkeleton(self):
		outDir = self.outDir.name
		inputMdPath = os.path.join(self.testDir, "markdownlint_inlineComments.md")
		xliffPath = os.path.join(outDir, "markdownlint.xliff")
		spec = importlib.util.spec_from_file_location("markdownTranslateUnderTest", self.markdownTranslateScriptPath)
		self.assertIsNotNone(spec)
		if spec is None or spec.loader is None:
			self.fail("Unable to load markdownTranslate module for testing")
		markdownTranslateModule = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(markdownTranslateModule)
		with mock.patch.object(
			markdownTranslateModule,
			"getRawGithubURLForPath",
			return_value=Path(inputMdPath).resolve().as_uri(),
		):
			markdownTranslateModule.generateXliff(mdPath=inputMdPath, outputPath=xliffPath)

		xliff = ET.parse(xliffPath)
		xliffRoot = xliff.getroot()
		namespace = {"xliff": "urn:oasis:names:tc:xliff:document:2.0"}
		skeletonNode = xliffRoot.find("./xliff:file/xliff:skeleton", namespace)
		self.assertIsNotNone(skeletonNode)
		skeletonContent = skeletonNode.text
		self.assertIsNotNone(skeletonContent)
		self.assertIn("$(ID:", skeletonContent)
		self.assertIn("<!-- markdownlint-disable-line MD041 -->", skeletonContent)
		self.assertIn("<!-- markdownlint-disable-line MD013 -->", skeletonContent)
