# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""Unit tests for the markdownTranslate module."""

import tempfile
import unittest
import subprocess
import sys
import os


class TestMarkdownTranslate(unittest.TestCase):
	markdownTranslateScriptPath = os.path.join(
		os.path.dirname(__file__), "..", "..", "user_docs", "markdownTranslate.py"
	)
	testDir = os.path.join(os.path.dirname(__file__), "..", "markdownTranslate")

	def setUp(self):
		self.outDir = tempfile.TemporaryDirectory()

	def tearDown(self):
		self.outDir.cleanup()

	def runMarkdownTranslateCommand(self, command: str, *args):
		print(f"Running markdownTranslate command: {command} {' '.join(args)}")
		subprocess.run([sys.executable, self.markdownTranslateScriptPath, command, *args], check=True)

	def test_markdownTranslate(self):
		outDir = self.outDir.name
		testDir = self.testDir
		with self.subTest("Generate an xliff file from the English 2024.2 user guide markdown file"):
			self.runMarkdownTranslateCommand(
				"generateXliff",
				"-m",
				os.path.join(testDir, "en_2024.2_userGuide.md"),
				"-o",
				os.path.join(outDir, "en_2024.2_userGuide.xliff"),
			)
		with self.subTest(
			"Regenerate the markdown file from the xliff file and ensure it matches the original markdown file"
		):
			self.runMarkdownTranslateCommand(
				"generateMarkdown",
				"-x",
				os.path.join(outDir, "en_2024.2_userGuide.xliff"),
				"-o",
				os.path.join(outDir, "rebuilt_en_2024.2_userGuide.md"),
				"-u",
			)
			self.runMarkdownTranslateCommand(
				"ensureMarkdownFilesMatch",
				os.path.join(outDir, "rebuilt_en_2024.2_userGuide.md"),
				os.path.join(testDir, "en_2024.2_userGuide.md"),
			)
		with self.subTest(
			"Update the xliff file with the changes between the English 2024.2 and 2024.3beta6 user guide markdown files"
		):
			self.runMarkdownTranslateCommand(
				"updateXliff",
				"-x",
				os.path.join(outDir, "en_2024.2_userGuide.xliff"),
				"-m",
				os.path.join(testDir, "en_2024.3beta6_userGuide.md"),
				"-o",
				os.path.join(outDir, "en_2024.3beta6_userGuide.xliff"),
			)
		with self.subTest(
			"Regenerate the markdown file from the updated xliff file and ensure it matches the English 2024.3beta6 user guide markdown file"
		):
			self.runMarkdownTranslateCommand(
				"generateMarkdown",
				"-x",
				os.path.join(outDir, "en_2024.3beta6_userGuide.xliff"),
				"-o",
				os.path.join(outDir, "rebuilt_en_2024.3beta6_userGuide.md"),
				"-u",
			)
			self.runMarkdownTranslateCommand(
				"ensureMarkdownFilesMatch",
				os.path.join(outDir, "rebuilt_en_2024.3beta6_userGuide.md"),
				os.path.join(testDir, "en_2024.3beta6_userGuide.md"),
			)
		with self.subTest(
			"Translate the xliff file to French using the pretranslated French 2024.3beta6 user guide markdown file"
		):
			self.runMarkdownTranslateCommand(
				"translateXliff",
				"-x",
				os.path.join(outDir, "en_2024.3beta6_userGuide.xliff"),
				"-l",
				"fr",
				"-p",
				os.path.join(testDir, "fr_pretranslated_2024.3beta6_userGuide.md"),
				"-o",
				os.path.join(outDir, "fr_2024.3beta6_userGuide.xliff"),
			)
		with self.subTest(
			"Regenerate the French 2024.3beta6 user guide markdown file from the translated xliff file"
			" and ensure it matches the pretranslated French 2024.3beta6 user guide markdown file"
		):
			self.runMarkdownTranslateCommand(
				"generateMarkdown",
				"-x",
				os.path.join(outDir, "fr_2024.3beta6_userGuide.xliff"),
				"-o",
				os.path.join(outDir, "fr_2024.3beta6_userGuide.md"),
			)
			self.runMarkdownTranslateCommand(
				"ensureMarkdownFilesMatch",
				os.path.join(outDir, "fr_2024.3beta6_userGuide.md"),
				os.path.join(testDir, "fr_pretranslated_2024.3beta6_userGuide.md"),
			)
