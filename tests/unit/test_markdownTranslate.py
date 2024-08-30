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
		os.path.dirname(__file__),
		"..",
		"..",
		"user_docs",
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
			subprocess.run([sys.executable, self.markdownTranslateScriptPath, *args], check=True)
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
