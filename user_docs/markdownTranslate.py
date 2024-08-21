# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import Generator
import tempfile
import os
import contextlib
import lxml.etree
import argparse
import uuid
import re
from itertools import zip_longest
from xml.sax.saxutils import escape as xmlEscape
from xml.sax.saxutils import unescape as xmlUnescape
import difflib
from dataclasses import dataclass
import subprocess

RAW_GITHUB_REPO_URL = "https://raw.githubusercontent.com/nvaccess/nvda"
re_kcTitle = re.compile(r"^(<!--\s+KC:title:\s*)(.+?)(\s*-->)$")
re_kcSettingsSection = re.compile(r"^(<!--\s+KC:settingsSection:\s*)(.+?)(\s*-->)$")
re_comment = re.compile(r"^<!--.+-->$")
re_heading = re.compile(r"^(#+\s+)(.+?)((?:\s+\{#.+\})?)$")
re_bullet = re.compile(r"^(\s*\*\s+)(.+)$")
re_number = re.compile(r"^(\s*[0-9]+\.\s+)(.+)$")
re_hiddenHeaderRow = re.compile(r"^\|\s*\.\s*\{\.hideHeaderRow\}\s*(\|\s*\.\s*)*\|$")
re_postTableHeaderLine = re.compile(r"^(\|\s*-+\s*)+\|$")
re_tableRow = re.compile(r"^(\|)(.+)(\|)$")
re_translationID = re.compile(r"^(.*)\$\(ID:([0-9a-f-]+)\)(.*)$")


def prettyPathString(path: str) -> str:
	return os.path.relpath(path, os.getcwd())


@contextlib.contextmanager
def createAndDeleteTempFilePath_contextManager(
	dir: str | None = None, prefix: str | None = None, suffix: str | None = None
) -> Generator[str, None, None]:
	"""A context manager that creates a temporary file and deletes it when the context is exited"""
	with tempfile.NamedTemporaryFile(dir=dir, prefix=prefix, suffix=suffix, delete=False) as tempFile:
		tempFilePath = tempFile.name
		tempFile.close()
		yield tempFilePath
		os.remove(tempFilePath)


def getLastCommitID(filePath) -> str:
	# Run the git log command to get the last commit ID for the given file
	result = subprocess.run(
		["git", "log", "-n", "1", "--pretty=format:%H", "--", filePath],
		capture_output=True,
		text=True,
		check=True,
	)
	commitID = result.stdout.strip()
	if not re.match(r"[0-9a-f]{40}", commitID):
		raise ValueError(f"Invalid commit ID: '{commitID}' for file '{filePath}'")
	return commitID


def getGitDir() -> str:
	# Run the git rev-parse command to get the root of the git directory
	result = subprocess.run(
		["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
	)
	gitDir = result.stdout.strip()
	if not os.path.isdir(gitDir):
		raise ValueError(f"Invalid git directory: '{gitDir}'")
	return gitDir


def getRawGithubURLForPath(filePath: str):
	gitDirPath = getGitDir()
	commitID = getLastCommitID(filePath)
	relativePath = os.path.relpath(os.path.abspath(filePath), gitDirPath)
	relativePath = relativePath.replace("\\", "/")
	return f"{RAW_GITHUB_REPO_URL}/{commitID}/{relativePath}"


def skeletonizeLine(mdLine: str) -> str | None:
	prefix = ""
	suffix = ""
	if (
		mdLine.isspace()
		or mdLine.strip() == "[TOC]"
		or re_hiddenHeaderRow.match(mdLine)
		or re_postTableHeaderLine.match(mdLine)
	):
		return None
	elif m := re_heading.match(mdLine):
		prefix, content, suffix = m.groups()
	elif m := re_bullet.match(mdLine):
		prefix, content = m.groups()
	elif m := re_number.match(mdLine):
		prefix, content = m.groups()
	elif m := re_tableRow.match(mdLine):
		prefix, content, suffix = m.groups()
	elif m := re_kcTitle.match(mdLine):
		prefix, content, suffix = m.groups()
	elif m := re_kcSettingsSection.match(mdLine):
		prefix, content, suffix = m.groups()
	elif re_comment.match(mdLine):
		return None
	ID = str(uuid.uuid4())
	return f"{prefix}$(ID:{ID}){suffix}\n"


@dataclass
class Result_generateSkeleton:
	numTotalLines: int = 0
	numTranslationPlaceholders: int = 0


def generateSkeleton(mdPath: str, outputPath: str) -> Result_generateSkeleton:
	print(f"Generating skeleton file {prettyPathString(outputPath)} from {prettyPathString(mdPath)}...")
	res = Result_generateSkeleton()
	with (
		open(mdPath, "r", encoding="utf8") as mdFile,
		open(outputPath, "w", encoding="utf8", newline="") as outputFile,
	):
		for mdLine in mdFile.readlines():
			res.numTotalLines += 1
			skelLine = skeletonizeLine(mdLine)
			if skelLine:
				res.numTranslationPlaceholders += 1
			else:
				skelLine = mdLine
			outputFile.write(skelLine)
		print(
			f"Generated skeleton file with {res.numTotalLines} total lines and {res.numTranslationPlaceholders} translation placeholders"
		)
		return res


@dataclass
class Result_updateSkeleton:
	numAddedLines: int = 0
	numAddedTranslationPlaceholders: int = 0
	numRemovedLines: int = 0
	numRemovedTranslationPlaceholders: int = 0
	numUnchangedLines: int = 0
	numUnchangedTranslationPlaceholders: int = 0


def extractSkeleton(xliffPath: str, outputPath: str):
	print(f"Extracting skeleton from {prettyPathString(xliffPath)} to {prettyPathString(outputPath)}...")
	with contextlib.ExitStack() as stack:
		outputFile = stack.enter_context(open(outputPath, "w", encoding="utf8", newline=""))
		xliff = lxml.etree.parse(xliffPath)
		xliffRoot = xliff.getroot()
		namespace = {"xliff": "urn:oasis:names:tc:xliff:document:2.0"}
		if xliffRoot.tag != "{urn:oasis:names:tc:xliff:document:2.0}xliff":
			raise ValueError("Not an xliff file")
		skeletonNode = xliffRoot.find("./xliff:file/xliff:skeleton", namespaces=namespace)
		if skeletonNode is None:
			raise ValueError("No skeleton found in xliff file")
		skeletonContent = skeletonNode.text.strip()
		outputFile.write(xmlUnescape(skeletonContent))
		print(f"Extracted skeleton to {prettyPathString(outputPath)}")


def updateSkeleton(
	origMdPath: str, newMdPath: str, origSkelPath: str, outputPath: str
) -> Result_updateSkeleton:
	print(
		f"Creating updated skeleton file {prettyPathString(outputPath)} from {prettyPathString(origSkelPath)} with changes from {prettyPathString(origMdPath)} to {prettyPathString(newMdPath)}..."
	)
	res = Result_updateSkeleton()
	with contextlib.ExitStack() as stack:
		origMdFile = stack.enter_context(open(origMdPath, "r", encoding="utf8"))
		newMdFile = stack.enter_context(open(newMdPath, "r", encoding="utf8"))
		origSkelFile = stack.enter_context(open(origSkelPath, "r", encoding="utf8"))
		outputFile = stack.enter_context(open(outputPath, "w", encoding="utf8", newline=""))
		mdDiff = difflib.ndiff(origMdFile.readlines(), newMdFile.readlines())
		origSkelLines = iter(origSkelFile.readlines())
		for mdDiffLine in mdDiff:
			if mdDiffLine.startswith("?"):
				continue
			if mdDiffLine.startswith(" "):
				res.numUnchangedLines += 1
				skelLine = next(origSkelLines)
				if re_translationID.match(skelLine):
					res.numUnchangedTranslationPlaceholders += 1
				outputFile.write(skelLine)
			elif mdDiffLine.startswith("+"):
				res.numAddedLines += 1
				skelLine = skeletonizeLine(mdDiffLine[2:])
				if skelLine:
					res.numAddedTranslationPlaceholders += 1
				else:
					skelLine = mdDiffLine[2:]
				outputFile.write(skelLine)
			elif mdDiffLine.startswith("-"):
				res.numRemovedLines += 1
				origSkelLine = next(origSkelLines)
				if re_translationID.match(origSkelLine):
					res.numRemovedTranslationPlaceholders += 1
			else:
				raise ValueError(f"Unexpected diff line: {mdDiffLine}")
		print(
			f"Updated skeleton file with {res.numAddedLines} added lines ({res.numAddedTranslationPlaceholders} translation placeholders), {res.numRemovedLines} removed lines ({res.numRemovedTranslationPlaceholders} translation placeholders), and {res.numUnchangedLines} unchanged lines ({res.numUnchangedTranslationPlaceholders} translation placeholders)"
		)
		return res


@dataclass
class Result_generateXliff:
	numTranslatableStrings: int = 0


def generateXliff(
	mdPath: str,
	outputPath: str,
	skelPath: str | None = None,
) -> Result_generateXliff:
	# If a skeleton file is not provided, first generate one
	with contextlib.ExitStack() as stack:
		if not skelPath:
			skelPath = stack.enter_context(
				createAndDeleteTempFilePath_contextManager(
					dir=os.path.dirname(outputPath),
					prefix=os.path.basename(mdPath),
					suffix=".skel",
				)
			)
			generateSkeleton(mdPath=mdPath, outputPath=skelPath)
		with open(skelPath, "r", encoding="utf8") as skelFile:
			skelContent = skelFile.read()
	res = Result_generateXliff()
	print(
		f"Generating xliff file {prettyPathString(outputPath)} from {prettyPathString(mdPath)} and {prettyPathString(skelPath)}..."
	)
	with contextlib.ExitStack() as stack:
		mdFile = stack.enter_context(open(mdPath, "r", encoding="utf8"))
		outputFile = stack.enter_context(open(outputPath, "w", encoding="utf8", newline=""))
		fileID = os.path.basename(mdPath)
		mdUri = getRawGithubURLForPath(mdPath)
		print(f"Including Github raw URL: {mdUri}")
		outputFile.write(
			'<?xml version="1.0"?>\n'
			f'<xliff xmlns="urn:oasis:names:tc:xliff:document:2.0" version="2.0" srcLang="en">\n'
			f'<file id="{fileID}" original="{mdUri}">\n'
		)
		outputFile.write(f"<skeleton>\n{xmlEscape(skelContent)}\n</skeleton>\n")
		res.numTranslatableStrings = 0
		for lineNo, (mdLine, skelLine) in enumerate(
			zip_longest(mdFile.readlines(), skelContent.splitlines(keepends=True)), start=1
		):
			mdLine = mdLine.rstrip()
			skelLine = skelLine.rstrip()
			if m := re_translationID.match(skelLine):
				res.numTranslatableStrings += 1
				prefix, ID, suffix = m.groups()
				if prefix and not mdLine.startswith(prefix):
					raise ValueError(f'Line {lineNo}: does not start with "{prefix}", {mdLine=}, {skelLine=}')
				if suffix and not mdLine.endswith(suffix):
					raise ValueError(f'Line {lineNo}: does not end with "{suffix}", {mdLine=}, {skelLine=}')
				source = mdLine[len(prefix) : len(mdLine) - len(suffix)]
				outputFile.write(
					f'<unit id="{ID}">\n' "<notes>\n" f'<note appliesTo="source">line: {lineNo + 1}</note>\n'
				)
				if prefix:
					outputFile.write(f'<note appliesTo="source">prefix: {xmlEscape(prefix)}</note>\n')
				if suffix:
					outputFile.write(f'<note appliesTo="source">suffix: {xmlEscape(suffix)}</note>\n')
				outputFile.write(
					"</notes>\n"
					f"<segment>\n"
					f"<source>{xmlEscape(source)}</source>\n"
					"</segment>\n"
					"</unit>\n"
				)
			else:
				if mdLine != skelLine:
					raise ValueError(f"Line {lineNo}: {mdLine=} does not match {skelLine=}")
		outputFile.write("</file>\n" "</xliff>")
		print(f"Generated xliff file with {res.numTranslatableStrings} translatable strings")
		return res


@dataclass
class Result_translateXliff:
	numTranslatedStrings: int = 0


def updateXliff(
	xliffPath: str,
	mdPath: str,
	outputPath: str,
):
	# uses generateMarkdown, extractSkeleton, updateSkeleton, and generateXliff to generate an updated xliff file.
	outputDir = os.path.dirname(outputPath)
	print(
		f"Generating updated xliff file {prettyPathString(outputPath)} from {prettyPathString(xliffPath)} and {prettyPathString(mdPath)}..."
	)
	with contextlib.ExitStack() as stack:
		origMdPath = stack.enter_context(
			createAndDeleteTempFilePath_contextManager(dir=outputDir, prefix="generated_", suffix=".md")
		)
		generateMarkdown(xliffPath=xliffPath, outputPath=origMdPath, translated=False)
		origSkelPath = stack.enter_context(
			createAndDeleteTempFilePath_contextManager(dir=outputDir, prefix="extracted_", suffix=".skel")
		)
		extractSkeleton(xliffPath=xliffPath, outputPath=origSkelPath)
		updatedSkelPath = stack.enter_context(
			createAndDeleteTempFilePath_contextManager(dir=outputDir, prefix="updated_", suffix=".skel")
		)
		updateSkeleton(
			origMdPath=origMdPath,
			newMdPath=mdPath,
			origSkelPath=origSkelPath,
			outputPath=updatedSkelPath,
		)
		generateXliff(
			mdPath=mdPath,
			skelPath=updatedSkelPath,
			outputPath=outputPath,
		)
		print(f"Generated updated xliff file {prettyPathString(outputPath)}")


def translateXliff(
	xliffPath: str,
	lang: str,
	pretranslatedMdPath: str,
	outputPath: str,
	allowBadAnchors: bool = False,
) -> Result_translateXliff:
	print(
		f"Creating {lang} translated xliff file {prettyPathString(outputPath)} from {prettyPathString(xliffPath)} using {prettyPathString(pretranslatedMdPath)}..."
	)
	res = Result_translateXliff()
	with contextlib.ExitStack() as stack:
		pretranslatedMdFile = stack.enter_context(open(pretranslatedMdPath, "r", encoding="utf8"))
		xliff = lxml.etree.parse(xliffPath)
		xliffRoot = xliff.getroot()
		namespace = {"xliff": "urn:oasis:names:tc:xliff:document:2.0"}
		if xliffRoot.tag != "{urn:oasis:names:tc:xliff:document:2.0}xliff":
			raise ValueError("Not an xliff file")
		xliffRoot.set("trgLang", lang)
		skeletonNode = xliffRoot.find("./xliff:file/xliff:skeleton", namespaces=namespace)
		if skeletonNode is None:
			raise ValueError("No skeleton found in xliff file")
		skeletonContent = xmlUnescape(skeletonNode.text).strip()
		for lineNo, (skelLine, pretranslatedLine) in enumerate(
			zip_longest(skeletonContent.splitlines(), pretranslatedMdFile.readlines()),
			start=1,
		):
			skelLine = skelLine.rstrip()
			pretranslatedLine = pretranslatedLine.rstrip()
			if m := re_translationID.match(skelLine):
				prefix, ID, suffix = m.groups()
				if prefix and not pretranslatedLine.startswith(prefix):
					raise ValueError(
						f'Line {lineNo} of translation does not start with "{prefix}", {pretranslatedLine=}, {skelLine=}'
					)
				if suffix and not pretranslatedLine.endswith(suffix):
					if allowBadAnchors and (m := re_heading.match(pretranslatedLine)):
						print(f"Warning: ignoring bad anchor in line {lineNo}: {pretranslatedLine}")
						suffix = m.group(3)
				if suffix and not pretranslatedLine.endswith(suffix):
					raise ValueError(
						f'Line {lineNo} of translation: does not end with "{suffix}", {pretranslatedLine=}, {skelLine=}'
					)
				translation = pretranslatedLine[len(prefix) : len(pretranslatedLine) - len(suffix)]
				unit = xliffRoot.find(f'./xliff:file/xliff:unit[@id="{ID}"]', namespaces=namespace)
				if unit is not None:
					segment = unit.find("./xliff:segment", namespaces=namespace)
					if segment is not None:
						target = lxml.etree.Element("target")
						target.text = xmlEscape(translation)
						target.tail = "\n"
						segment.append(target)
						res.numTranslatedStrings += 1
					else:
						raise ValueError(f"No segment found for unit {ID}")
				else:
					raise ValueError(f"Cannot locate Unit {ID} in xliff file")
		xliff.write(outputPath, encoding="utf8", xml_declaration=True)
		print(f"Translated xliff file with {res.numTranslatedStrings} translated strings")
		return res


@dataclass
class Result_generateMarkdown:
	numTotalLines = 0
	numTranslatableStrings = 0
	numTranslatedStrings = 0


def generateMarkdown(xliffPath: str, outputPath: str, translated: bool = True):
	print(f"Generating markdown file {prettyPathString(outputPath)} from {prettyPathString(xliffPath)}...")
	res = Result_generateMarkdown()
	with contextlib.ExitStack() as stack:
		outputFile = stack.enter_context(open(outputPath, "w", encoding="utf8", newline=""))
		xliff = lxml.etree.parse(xliffPath)
		xliffRoot = xliff.getroot()
		namespace = {"xliff": "urn:oasis:names:tc:xliff:document:2.0"}
		if xliffRoot.tag != "{urn:oasis:names:tc:xliff:document:2.0}xliff":
			raise ValueError("Not an xliff file")
		skeletonNode = xliffRoot.find("./xliff:file/xliff:skeleton", namespaces=namespace)
		if skeletonNode is None:
			raise ValueError("No skeleton found in xliff file")
		skeletonContent = xmlUnescape(skeletonNode.text).strip()
		for line in skeletonContent.splitlines(keepends=True):
			res.numTotalLines += 1
			if m := re_translationID.match(line):
				prefix, ID, suffix = m.groups()
				res.numTranslatableStrings += 1
				unit = xliffRoot.find(f'./xliff:file/xliff:unit[@id="{ID}"]', namespaces=namespace)
				if unit is not None:
					segment = unit.find("./xliff:segment", namespaces=namespace)
					if segment is not None:
						source = segment.find("./xliff:source", namespaces=namespace)
						if translated:
							target = segment.find("./xliff:target", namespaces=namespace)
						else:
							target = None
						if target is not None and target.text:
							res.numTranslatedStrings += 1
							translation = xmlUnescape(target.text)
						elif source is not None and source.text:
							translation = xmlUnescape(source.text)
						else:
							raise ValueError(f"No source or target found for unit {ID}")
					else:
						raise ValueError(f"No segment found for unit {ID}")
				else:
					raise ValueError(f"Cannot locate Unit {ID} in xliff file")
				outputFile.write(f"{prefix}{translation}{suffix}\n")
			else:
				outputFile.write(line)
		print(
			f"Generated markdown file with {res.numTotalLines} total lines, {res.numTranslatableStrings} translatable strings, and {res.numTranslatedStrings} translated strings"
		)
		return res


def ensureFilesMatch(path1: str, path2: str, allowBadAnchors: bool = False):
	print(f"Ensuring files {prettyPathString(path1)} and {prettyPathString(path2)} match...")
	with contextlib.ExitStack() as stack:
		file1 = stack.enter_context(open(path1, "r", encoding="utf8"))
		file2 = stack.enter_context(open(path2, "r", encoding="utf8"))
		for lineNo, (line1, line2) in enumerate(zip_longest(file1.readlines(), file2.readlines()), start=1):
			line1 = line1.rstrip()
			line2 = line2.rstrip()
			if line1 != line2:
				if (
					re_postTableHeaderLine.match(line1)
					and re_postTableHeaderLine.match(line2)
					and line1.count("|") == line2.count("|")
				):
					print(
						f"Warning: ignoring cell padding of post table header line at line {lineNo}: {line1}, {line2}"
					)
					continue
				if (
					re_hiddenHeaderRow.match(line1)
					and re_hiddenHeaderRow.match(line2)
					and line1.count("|") == line2.count("|")
				):
					print(
						f"Warning: ignoring cell padding of hidden header row at line {lineNo}: {line1}, {line2}"
					)
					continue
				if allowBadAnchors and (m1 := re_heading.match(line1)) and (m2 := re_heading.match(line2)):
					print(f"Warning: ignoring bad anchor in headings at line {lineNo}: {line1}, {line2}")
					line1 = m1.group(1) + m1.group(2)
					line2 = m2.group(1) + m2.group(2)
			if line1 != line2:
				raise ValueError(f"Files do not match at line {lineNo}: {line1=} {line2=}")
		print("Files match")


def markdownTranslateCommand(command: str, *args):
	print(f"Running markdownTranslate command: {command} {' '.join(args)}")
	subprocess.run(["python", __file__, command, *args], check=True)


def runTests(testDir: str):
	outDir = os.path.join(testDir, "output")
	os.makedirs(outDir, exist_ok=True)
	markdownTranslateCommand(
		"generateXliff",
		"-m",
		os.path.join(testDir, "en_2024.2_userGuide.md"),
		"-o",
		os.path.join(outDir, "en_2024.2_userGuide.xliff"),
	)
	markdownTranslateCommand(
		"generateMarkdown",
		"-x",
		os.path.join(outDir, "en_2024.2_userGuide.xliff"),
		"-o",
		os.path.join(outDir, "rebuilt_en_2024.2_userGuide.md"),
		"-u",
	)
	ensureFilesMatch(
		os.path.join(outDir, "rebuilt_en_2024.2_userGuide.md"),
		os.path.join(testDir, "en_2024.2_userGuide.md"),
	)
	markdownTranslateCommand(
		"updateXliff",
		"-x",
		os.path.join(outDir, "en_2024.2_userGuide.xliff"),
		"-m",
		os.path.join(testDir, "en_2024.3beta6_userGuide.md"),
		"-o",
		os.path.join(outDir, "en_2024.3beta6_userGuide.xliff"),
	)
	markdownTranslateCommand(
		"generateMarkdown",
		"-x",
		os.path.join(outDir, "en_2024.3beta6_userGuide.xliff"),
		"-o",
		os.path.join(outDir, "rebuilt_en_2024.3beta6_userGuide.md"),
		"-u",
	)
	ensureFilesMatch(
		os.path.join(outDir, "rebuilt_en_2024.3beta6_userGuide.md"),
		os.path.join(testDir, "en_2024.3beta6_userGuide.md"),
	)
	markdownTranslateCommand(
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
	markdownTranslateCommand(
		"generateMarkdown",
		"-x",
		os.path.join(outDir, "fr_2024.3beta6_userGuide.xliff"),
		"-o",
		os.path.join(outDir, "fr_2024.3beta6_userGuide.md"),
	)
	ensureFilesMatch(
		os.path.join(outDir, "fr_2024.3beta6_userGuide.md"),
		os.path.join(testDir, "fr_pretranslated_2024.3beta6_userGuide.md"),
	)


def pretranslateAllPossibleLanguages(langsDir: str, mdBaseName: str):
	# This function walks through all language directories in the given directory, skipping en (English) and translates the English xlif and skel file along with the lang's pretranslated md file
	enXliffPath = os.path.join(langsDir, "en", f"{mdBaseName}.xliff")
	if not os.path.exists(enXliffPath):
		raise ValueError(f"English xliff file {enXliffPath} does not exist")
	allLangs = set()
	succeededLangs = set()
	skippedLangs = set()
	for langDir in os.listdir(langsDir):
		if langDir == "en":
			continue
		langDirPath = os.path.join(langsDir, langDir)
		if not os.path.isdir(langDirPath):
			continue
		langPretranslatedMdPath = os.path.join(langDirPath, f"{mdBaseName}.md")
		if not os.path.exists(langPretranslatedMdPath):
			continue
		allLangs.add(langDir)
		langXliffPath = os.path.join(langDirPath, f"{mdBaseName}.xliff")
		if os.path.exists(langXliffPath):
			print(f"Skipping {langDir} as the xliff file already exists")
			skippedLangs.add(langDir)
			continue
		try:
			translateXliff(
				xliffPath=enXliffPath,
				lang=langDir,
				pretranslatedMdPath=langPretranslatedMdPath,
				outputPath=langXliffPath,
				allowBadAnchors=True,
			)
		except Exception as e:
			print(f"Failed to translate {langDir}: {e}")
			continue
		rebuiltLangMdPath = os.path.join(langDirPath, f"rebuilt_{mdBaseName}.md")
		try:
			generateMarkdown(
				xliffPath=langXliffPath,
				outputPath=rebuiltLangMdPath,
			)
		except Exception as e:
			print(f"Failed to rebuild {langDir} markdown: {e}")
			os.remove(langXliffPath)
			continue
		try:
			ensureFilesMatch(rebuiltLangMdPath, langPretranslatedMdPath, allowBadAnchors=True)
		except Exception as e:
			print(f"Rebuilt {langDir} markdown does not match pretranslated markdown: {e}")
			os.remove(langXliffPath)
			continue
		os.remove(rebuiltLangMdPath)
		print(f"Successfully pretranslated {langDir}")
		succeededLangs.add(langDir)
	if len(skippedLangs) > 0:
		print(f"Skipped {len(skippedLangs)} languages already pretranslated.")
	print(f"Pretranslated {len(succeededLangs)} out of {len(allLangs) - len(skippedLangs)} languages.")


if __name__ == "__main__":
	mainParser = argparse.ArgumentParser()
	commandParser = mainParser.add_subparsers(title="commands", dest="command", required=True)
	generateXliffParser = commandParser.add_parser("generateXliff")
	generateXliffParser.add_argument(
		"-m",
		"--markdown",
		dest="md",
		type=str,
		required=True,
		help="The markdown file to generate the xliff file for",
	)
	generateXliffParser.add_argument(
		"-o", "--output", dest="output", type=str, required=True, help="The file to output the xliff file to"
	)
	updateXliffParser = commandParser.add_parser("updateXliff")
	updateXliffParser.add_argument(
		"-x", "--xliff", dest="xliff", type=str, required=True, help="The original xliff file"
	)
	updateXliffParser.add_argument(
		"-m", "--newMarkdown", dest="md", type=str, required=True, help="The new markdown file"
	)
	updateXliffParser.add_argument(
		"-o",
		"--output",
		dest="output",
		type=str,
		required=True,
		help="The file to output the updated xliff to",
	)
	translateXliffParser = commandParser.add_parser("translateXliff")
	translateXliffParser.add_argument(
		"-x", "--xliff", dest="xliff", type=str, required=True, help="The xliff file to translate"
	)
	translateXliffParser.add_argument(
		"-l", "--lang", dest="lang", type=str, required=True, help="The language to translate to"
	)
	translateXliffParser.add_argument(
		"-p",
		"--pretranslatedMarkdown",
		dest="pretranslatedMd",
		type=str,
		required=True,
		help="The pretranslated markdown file to use",
	)
	translateXliffParser.add_argument(
		"-o",
		"--output",
		dest="output",
		type=str,
		required=True,
		help="The file to output the translated xliff file to",
	)
	generateMarkdownParser = commandParser.add_parser("generateMarkdown")
	generateMarkdownParser.add_argument(
		"-x",
		"--xliff",
		dest="xliff",
		type=str,
		required=True,
		help="The xliff file to generate the markdown file for",
	)
	generateMarkdownParser.add_argument(
		"-o",
		"--output",
		dest="output",
		type=str,
		required=True,
		help="The file to output the markdown file to",
	)
	generateMarkdownParser.add_argument(
		"-u",
		"--untranslated",
		dest="translated",
		action="store_false",
		help="Generate the markdown file with the untranslated strings",
	)
	testParser = commandParser.add_parser("runTests")
	testParser.add_argument(
		"-d",
		"--test-dir",
		dest="testDir",
		type=str,
		required=True,
		help="The directory containing the test files",
	)
	pretranslateLangsParser = commandParser.add_parser("pretranslateLangs")
	pretranslateLangsParser.add_argument(
		"-d",
		"--langs-dir",
		dest="langsDir",
		type=str,
		required=True,
		help="The directory containing the language directories",
	)
	pretranslateLangsParser.add_argument(
		"-b",
		"--md-base-name",
		dest="mdBaseName",
		type=str,
		required=True,
		help="The base name of the markdown files to pretranslate",
	)
	args = mainParser.parse_args()
	if args.command == "generateXliff":
		generateXliff(mdPath=args.md, outputPath=args.output)
	elif args.command == "updateXliff":
		updateXliff(
			xliffPath=args.xliff,
			mdPath=args.md,
			outputPath=args.output,
		)
	elif args.command == "generateMarkdown":
		generateMarkdown(xliffPath=args.xliff, outputPath=args.output, translated=args.translated)
	elif args.command == "translateXliff":
		translateXliff(
			xliffPath=args.xliff,
			lang=args.lang,
			pretranslatedMdPath=args.pretranslatedMd,
			outputPath=args.output,
		)
	elif args.command == "pretranslateLangs":
		pretranslateAllPossibleLanguages(langsDir=args.langsDir, mdBaseName=args.mdBaseName)
	elif args.command == "runTests":
		runTests(args.testDir)
	else:
		raise ValueError(f"Unknown command: {args.command}")
