# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024-2025 NV Access Limited.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import crowdin_api as crowdin
import tempfile
import lxml.etree
import os
import shutil
import argparse
import markdownTranslate
import md2html
import requests
import codecs
import re
import subprocess
import sys
import zipfile
import time

CROWDIN_PROJECT_ID = 598017
POLLING_INTERVAL_SECONDS = 5
EXPORT_TIMEOUT_SECONDS = 60 * 10  # 10 minutes


def fetchCrowdinAuthToken() -> str:
	"""
	Fetch the Crowdin auth token from the ~/.nvda_crowdin file or prompt the user for it.
	If provided by the user, the token will be saved to the ~/.nvda_crowdin file.
	:return: The auth token
	"""
	crowdinAuthToken = os.getenv("crowdinAuthToken", "")
	if crowdinAuthToken:
		print("Using Crowdin auth token from environment variable.")
		return crowdinAuthToken
	token_path = os.path.expanduser("~/.nvda_crowdin")
	if os.path.exists(token_path):
		with open(token_path, "r") as f:
			token = f.read().strip()
			print("Using auth token from ~/.nvda_crowdin")
			return token
	print("A Crowdin auth token is required to proceed.")
	print("Please visit https://crowdin.com/settings#api-key")
	print("Create a personal access token with translations permissions, and enter it below.")
	token = input("Enter Crowdin auth token: ").strip()
	with open(token_path, "w") as f:
		f.write(token)
	return token


_crowdinClient = None


def getCrowdinClient() -> crowdin.CrowdinClient:
	"""
	Create or fetch the Crowdin client instance.
	:return: The Crowdin client
	"""
	global _crowdinClient
	if _crowdinClient is None:
		token = fetchCrowdinAuthToken()
		_crowdinClient = crowdin.CrowdinClient(project_id=CROWDIN_PROJECT_ID, token=token)
	return _crowdinClient


def fetchLanguageFromXliff(xliffPath: str, source: bool = False) -> str:
	"""
	Fetch the language from an xliff file.
	This function also prints a message to the console stating the detected language if found, or a warning if not found.
	:param xliffPath: Path to the xliff file
	:param source: If True, fetch the source language, otherwise fetch the target language
	:return: The language code
	"""
	xliff = lxml.etree.parse(xliffPath)
	xliffRoot = xliff.getroot()
	if xliffRoot.tag != "{urn:oasis:names:tc:xliff:document:2.0}xliff":
		raise ValueError(f"Not an xliff file: {xliffPath}")
	lang = xliffRoot.get("srcLang" if source else "trgLang")
	if lang is None:
		print(f"Could not detect language for xliff file {xliffPath}, {source=}")
	else:
		print(f"Detected language {lang} for xliff file {xliffPath}, {source=}")
	return lang


def preprocessXliff(xliffPath: str, outputPath: str):
	"""
	Replace corrupt or empty translated segment targets with the source text,
	marking the segment again as "initial" state.
	This function also prints a message to the console stating the number of segments processed and the numbers of empty, corrupt, source and existing translations removed.
	:param xliffPath: Path to the xliff file to be processed
	:param outputPath: Path to the resulting xliff file
	"""
	print(f"Preprocessing xliff file at {xliffPath}")
	namespace = {"xliff": "urn:oasis:names:tc:xliff:document:2.0"}
	xliff = lxml.etree.parse(xliffPath)
	xliffRoot = xliff.getroot()
	if xliffRoot.tag != "{urn:oasis:names:tc:xliff:document:2.0}xliff":
		raise ValueError(f"Not an xliff file: {xliffPath}")
	file = xliffRoot.find("./xliff:file", namespaces=namespace)
	units = file.findall("./xliff:unit", namespaces=namespace)
	segmentCount = 0
	emptyTargetCount = 0
	corruptTargetcount = 0
	for unit in units:
		segment = unit.find("./xliff:segment", namespaces=namespace)
		if segment is None:
			print("Warning: No segment element in unit")
			continue
		source = segment.find("./xliff:source", namespaces=namespace)
		if source is None:
			print("Warning: No source element in segment")
			continue
		sourceText = source.text
		segmentCount += 1
		target = segment.find("./xliff:target", namespaces=namespace)
		if target is None:
			continue
		targetText = target.text
		# Correct empty targets
		if not targetText:
			emptyTargetCount += 1
			target.text = sourceText
			segment.set("state", "initial")
		# Correct corrupt target tags
		elif targetText in (
			"<target/>",
			"&lt;target/&gt;",
			"<target></target>",
			"&lt;target&gt;&lt;/target&gt;",
		):
			corruptTargetcount += 1
			target.text = sourceText
			segment.set("state", "initial")
			xliff.write(outputPath, encoding="utf-8")
	print(
		f"Processed {segmentCount} segments, removing {emptyTargetCount} empty targets, {corruptTargetcount} corrupt targets",
	)


def stripXliff(xliffPath: str, outputPath: str, oldXliffPath: str | None = None):
	"""
	Removes notes and skeleton elements from an xliff file before upload to Crowdin.
	Removes empty and corrupt translations.
	Removes untranslated segments.
	Removes existing translations if an old xliff file is provided.
	This function also prints a message to the console stating the number of segments processed and the numbers of empty, corrupt, source and existing translations removed.
	:param xliffPath: Path to the xliff file to be stripped
	:param outputPath: Path to the resulting xliff file
	:param oldXliffPath: Path to the old xliff file containing existing translations that should be also stripped.
	"""
	print(f"Creating stripped xliff at {outputPath} from {xliffPath}")
	namespace = {"xliff": "urn:oasis:names:tc:xliff:document:2.0"}
	xliff = lxml.etree.parse(xliffPath)
	xliffRoot = xliff.getroot()
	if xliffRoot.tag != "{urn:oasis:names:tc:xliff:document:2.0}xliff":
		raise ValueError(f"Not an xliff file: {xliffPath}")
	oldXliffRoot = None
	if oldXliffPath:
		oldXliff = lxml.etree.parse(oldXliffPath)
		oldXliffRoot = oldXliff.getroot()
		if oldXliffRoot.tag != "{urn:oasis:names:tc:xliff:document:2.0}xliff":
			raise ValueError(f"Not an xliff file: {oldXliffPath}")
	skeletonNode = xliffRoot.find("./xliff:file/xliff:skeleton", namespaces=namespace)
	if skeletonNode is not None:
		skeletonNode.getparent().remove(skeletonNode)
	file = xliffRoot.find("./xliff:file", namespaces=namespace)
	units = file.findall("./xliff:unit", namespaces=namespace)
	segmentCount = 0
	untranslatedCount = 0
	emptyCount = 0
	corruptCount = 0
	existingTranslationCount = 0
	for unit in units:
		unitID = unit.get("id")
		notes = unit.find("./xliff:notes", namespaces=namespace)
		if notes is not None:
			unit.remove(notes)
		segment = unit.find("./xliff:segment", namespaces=namespace)
		if segment is None:
			print("Warning: No segment element in unit")
			continue
		segmentCount += 1
		state = segment.get("state")
		if state == "initial":
			file.remove(unit)
			untranslatedCount += 1
			continue
		target = segment.find("./xliff:target", namespaces=namespace)
		if target is None:
			file.remove(unit)
			untranslatedCount += 1
			continue
		targetText = target.text
		if not targetText:
			emptyCount += 1
			file.remove(unit)
			continue
		elif targetText in (
			"<target/>",
			"&lt;target/&gt;",
			"<target></target>",
			"&lt;target&gt;&lt;/target&gt;",
		):
			corruptCount += 1
			file.remove(unit)
			continue
		if oldXliffRoot:
			# Remove existing translations
			oldTarget = oldXliffRoot.find(
				f"./xliff:file/xliff:unit[@id='{unitID}']/xliff:segment/xliff:target",
				namespaces=namespace,
			)
			if oldTarget is not None and oldTarget.getparent().get("state") != "initial":
				if oldTarget.text == targetText:
					file.remove(unit)
					existingTranslationCount += 1
	xliff.write(outputPath, encoding="utf-8")
	if corruptCount > 0:
		print(f"Removed {corruptCount} corrupt translations.")
	if emptyCount > 0:
		print(f"Removed {emptyCount} empty translations.")
	if existingTranslationCount > 0:
		print(f"Ignored {existingTranslationCount} existing translations.")
	keptTranslations = segmentCount - untranslatedCount - emptyCount - corruptCount - existingTranslationCount
	print(f"Added or changed {keptTranslations} translations.")


crowdinFileIDs = {
	"nvda.po": 2,
	# alias for nvda.po
	"nvda.pot": 2,
	"userGuide.xliff": 18,
	# lowercase alias for userGuide.xliff
	"userguide.xliff": 18,
	"changes.xliff": 20,
}


def downloadTranslationFile(crowdinFilePath: str, localFilePath: str, language: str):
	"""
	Download a translation file from Crowdin.
	:param crowdinFilePath: The Crowdin file path
	:param localFilePath: The path to save the local file
	:param language: The language code to download the translation for
	"""
	fileId = crowdinFileIDs[crowdinFilePath]
	print(f"Requesting export of {crowdinFilePath} for {language} from Crowdin")
	res = getCrowdinClient().translations.export_project_translation(
		fileIds=[fileId],
		targetLanguageId=language,
	)
	if res is None:
		raise ValueError("Crowdin export failed")
	download_url = res["data"]["url"]
	print(f"Downloading from {download_url}")
	with open(localFilePath, "wb") as f:
		r = requests.get(download_url)
		f.write(r.content)
	print(f"Saved to {localFilePath}")


def uploadTranslationFile(crowdinFilePath: str, localFilePath: str, language: str):
	"""
	Upload a translation file to Crowdin.
	:param crowdinFilePath: The Crowdin file path
	:param localFilePath: The path to the local file to be uploaded
	:param language: The language code to upload the translation for
	"""
	fileId = crowdinFileIDs[crowdinFilePath]
	print(f"Uploading {localFilePath} to Crowdin")
	res = getCrowdinClient().storages.add_storage(
		open(localFilePath, "rb"),
	)
	if res is None:
		raise ValueError("Crowdin storage upload failed")
	storageId = res["data"]["id"]
	print(f"Stored with ID {storageId}")
	print(f"Importing translation for {crowdinFilePath} in {language} from storage with ID {storageId}")
	res = getCrowdinClient().translations.upload_translation(
		fileId=fileId,
		languageId=language,
		storageId=storageId,
		autoApproveImported=True,
		importEqSuggestions=True,
	)
	print("Done")


def exportTranslations(outputDir: str, language: str | None = None):
	"""
	Export translation files from Crowdin as a bundle.
	:param outputDir: Directory to save translation files.
	:param language: The language code to export (e.g., 'es', 'fr', 'de').
		If None, exports all languages.
	"""

	# Create output directory if it doesn't exist
	os.makedirs(outputDir, exist_ok=True)

	client = getCrowdinClient()

	requestData = {
		"skipUntranslatedStrings": False,
		"skipUntranslatedFiles": False,
		"exportApprovedOnly": False,
	}

	if language is not None:
		requestData["targetLanguageIds"] = [language]

	if language is None:
		print("Requesting export of all translations from Crowdin...")
	else:
		print(f"Requesting export of all translations for language: {language}")
	build_res = client.translations.build_project_translation(request_data=requestData)

	if language is None:
		zip_filename = "translations.zip"
	else:
		zip_filename = f"translations_{language}.zip"

	if build_res is None:
		raise ValueError("Failed to start translation build")

	build_id = build_res["data"]["id"]
	print(f"Build started with ID: {build_id}")

	# Wait for the build to complete
	print("Waiting for build to complete...")
	while True:
		status_res = client.translations.check_project_build_status(build_id)
		if status_res is None:
			raise ValueError("Failed to check build status")

		status = status_res["data"]["status"]
		progress = status_res["data"]["progress"]
		print(f"Build status: {status} ({progress}%)")

		if status == "finished":
			break
		elif status == "failed":
			raise ValueError("Translation build failed")

		time.sleep(POLLING_INTERVAL_SECONDS)

	# Download the completed build
	print("Downloading translations archive...")
	download_res = client.translations.download_project_translations(build_id)
	if download_res is None:
		raise ValueError("Failed to get download URL")

	download_url = download_res["data"]["url"]
	print(f"Downloading from {download_url}")

	# Download and extract the ZIP file
	zip_path = os.path.join(outputDir, zip_filename)
	response = requests.get(download_url, stream=True, timeout=EXPORT_TIMEOUT_SECONDS)
	response.raise_for_status()

	with open(zip_path, "wb") as f:
		for chunk in response.iter_content(chunk_size=8192):
			f.write(chunk)

	print(f"Archive saved to {zip_path}")
	print("Extracting translations...")

	with zipfile.ZipFile(zip_path, "r") as zip_ref:
		zip_ref.extractall(outputDir)

	# Remove the zip file
	os.remove(zip_path)

	if language is None:
		print(f"\nExport complete! All translations extracted to '{outputDir}' directory.")
	else:
		print(f"\nExport complete! All {language} translations extracted to '{outputDir}' directory.")


class _PoChecker:
	"""Checks a po file for errors not detected by msgfmt.
	This first runs msgfmt to check for syntax errors.
	It then checks for mismatched Python percent and brace interpolations.
	Construct an instance and call the L{check} method.
	"""

	FUZZY = "#, fuzzy"
	MSGID = "msgid"
	MSGID_PLURAL = "msgid_plural"
	MSGSTR = "msgstr"

	def __init__(self, po: str):
		"""Constructor.
		:param po: The path to the po file to check.
		"""
		self._poPath = po
		with codecs.open(po, "r", "utf-8") as file:
			self._poContent = file.readlines()
		self._string: str | None = None

		self.alerts: list[str] = []
		"""List of error and warning messages found in the po file."""

		self.hasSyntaxError: bool = False
		"""Whether there is a syntax error in the po file."""

		self.warningCount: int = 0
		"""Number of warnings found."""

		self.errorCount: int = 0
		"""Number of errors found."""

	def _addToString(self, line: list[str], startingCommand: str | None = None) -> None:
		"""Helper function to add a line to the current string.
		:param line: The line to add.
		:param startingCommand: The command that started this string, if any.
			This is used to determine whether to strip the command and quotes.
		"""
		if startingCommand:
			# Strip the command and the quotes.
			self._string = line[len(startingCommand) + 2 : -1]
		else:
			# Strip the quotes.
			self._string += line[1:-1]

	def _finishString(self) -> str:
		"""Helper function to finish the current string.
		:return: The finished string.
		"""
		string = self._string
		self._string = None
		return string

	def _messageAlert(self, alert: str, isError: bool = True) -> None:
		"""Helper function to add an alert about a message.
		:param alert: The alert message.
		:param isError: Whether this is an error or a warning.
		"""
		if self._fuzzy:
			# Fuzzy messages don't get used, so this shouldn't be considered an error.
			isError = False
		if isError:
			self.errorCount += 1
		else:
			self.warningCount += 1
		if self._fuzzy:
			msgType = "Fuzzy message"
		else:
			msgType = "Message"
		self.alerts.append(
			f"{msgType} starting on line {self._messageLineNum}\n"
			f'Original: "{self._msgid}"\n'
			f'Translated: "{self._msgstr[-1]}"\n'
			f"{'ERROR' if isError else 'WARNING'}: {alert}",
		)

	@property
	def MSGFMT_PATH(self) -> str:
		try:
			# When running from source, miscDeps is the sibling of parent this script.
			_MSGFMT = os.path.join(os.path.dirname(__file__), "..", "miscDeps", "tools", "msgfmt.exe")
		except NameError:
			# When running from a frozen executable, __file__ is not defined.
			# In this case, we use the distribution path.
			# When running from a distribution, source/l10nUtil.py is built to l10nUtil.exe.
			# miscDeps is the sibling of this script in the distribution.
			_MSGFMT = os.path.join(sys.prefix, "miscDeps", "tools", "msgfmt.exe")

		if not os.path.exists(_MSGFMT):
			raise FileNotFoundError(
				"msgfmt executable not found. "
				"Please ensure that miscDeps/tools/msgfmt.exe exists in the source tree or distribution.",
			)
		return _MSGFMT

	def _checkSyntax(self) -> None:
		"""Check the syntax of the po file using msgfmt.
		This will set the hasSyntaxError attribute to True if there is a syntax error.
		"""

		result = subprocess.run(
			(self.MSGFMT_PATH, "-o", "-", self._poPath),
			stdout=subprocess.DEVNULL,
			stderr=subprocess.PIPE,
			text=True,  # Ensures stderr is a text stream
		)
		if result.returncode != 0:
			output = result.stderr.rstrip().replace("\r\n", "\n")
			self.alerts.append(output)
			self.hasSyntaxError = True
			self.errorCount = 1

	def _checkMessages(self) -> None:
		command = None
		self._msgid = None
		self._msgid_plural = None
		self._msgstr = None
		nextFuzzy = False
		self._fuzzy = False
		for lineNum, line in enumerate(self._poContent, 1):
			line = line.strip()
			if line.startswith(self.FUZZY):
				nextFuzzy = True
				continue
			elif line.startswith(self.MSGID) and not line.startswith(self.MSGID_PLURAL):
				# New message.
				if self._msgstr is not None:
					self._msgstr[-1] = self._finishString()
					# Check the message we just handled.
					self._checkMessage()
				command = self.MSGID
				start = command
				self._messageLineNum = lineNum
				self._fuzzy = nextFuzzy
				nextFuzzy = False
			elif line.startswith(self.MSGID_PLURAL):
				self._msgid = self._finishString()
				command = self.MSGID_PLURAL
				start = command
			elif line.startswith(self.MSGSTR):
				self._handleMsgStrReaching(lastCommand=command)
				command = self.MSGSTR
				start = line[: line.find(" ")]
			elif line.startswith('"'):
				# Continuing a string.
				start = None
			else:
				# This line isn't of interest.
				continue
			self._addToString(line, startingCommand=start)
		if command == self.MSGSTR:
			# Handle the last message.
			self._msgstr[-1] = self._finishString()
			self._checkMessage()

	def _handleMsgStrReaching(self, lastCommand: str) -> None:
		"""Helper function used by _checkMessages to handle the required processing when reaching a line
		starting with "msgstr".
		:param lastCommand: the current command just before the msgstr line is reached.
		"""

		# Finish the string of the last command and check the message if it was an msgstr
		if lastCommand == self.MSGID:
			self._msgid = self._finishString()
		elif lastCommand == self.MSGID_PLURAL:
			self._msgid_plural = self._finishString()
		elif lastCommand == self.MSGSTR:
			self._msgstr[-1] = self._finishString()
			self._checkMessage()
		else:
			raise RuntimeError(f"Unexpected command before line {self._messageLineNum}: {lastCommand}")

		# For first msgstr create the msgstr list
		if lastCommand != self.MSGSTR:
			self._msgstr = []

		# Initiate the string for the current msgstr
		self._msgstr.append("")

	def check(self) -> bool:
		"""Check the file.
		Once this returns, you can call getReport to obtain a report.
		This method should not be called more than once.
		:return: True if the file is okay, False if there were problems.
		"""
		self._checkSyntax()
		if self.alerts:
			return False
		self._checkMessages()
		if self.alerts:
			return False
		return True

	# e.g. %s %d %10.2f %-5s (but not %%) or %%(name)s %(name)d
	RE_UNNAMED_PERCENT = re.compile(
		# Does not include optional mapping key, as that's handled by a different regex
		r"""
		(?:(?<=%%)|(?<!%))?%  # Percent sign, optionally preceded by 2 percent signs, but not by just 1
		[#0+-]*  # Optional conversion flags
		\d*  # Optional minimum field width
		(?:\.\d+)?  # Optional precision specifier - if present, must be a full stop followed by 1-or-more digits
		[hlL]?  # Optional length specifier - has no effect in Python
		[diouxXeEfFgGcrsa]  # Conversion type
		""",
		flags=re.VERBOSE,
	)
	# e.g. %(name)s %(name)d
	RE_NAMED_PERCENT = re.compile(r"(?<!%)%\([^(]+\)[.\d]*[a-zA-Z]")
	# e.g. {name} {name:format}
	RE_FORMAT = re.compile(r"(?<!{){([^{}:]*):?[^{}]*}")

	def _getInterpolations(self, text: str) -> tuple[list[str], set[str], set[str]]:
		"""Get the percent and brace interpolations in a string.
		:param text: The text to check.
		:return: A tuple of a list and two sets:
			- unnamed percent interpolations (e.g. %s, %d)
			- named percent interpolations (e.g. %(name)s)
			- brace format interpolations (e.g. {name}, {name:format})
		"""
		unnamedPercent = self.RE_UNNAMED_PERCENT.findall(text)
		namedPercent = set(self.RE_NAMED_PERCENT.findall(text))
		formats = set()
		for m in self.RE_FORMAT.finditer(text):
			if not m.group(1):
				self._messageAlert(
					"Unspecified positional argument in brace format",
					# Skip as error as many of these had been introduced in the source .po files.
					# These should be fixed in the source .po files to add names to instances of "{}".
					# This causes issues where the order of the arguments change in the string.
					# e.g. "Character: {}\nReplacement: {}" being translated to "Replacement: {}\nCharacter: {}"
					# will result in the expected interpolation being in the wrong place.
					# This should be changed isError=True.
					isError=False,
				)
			formats.add(m.group(0))
		return unnamedPercent, namedPercent, formats

	def _formatInterpolations(
		self,
		unnamedPercent: list[str],
		namedPercent: set[str],
		formats: set[str],
	) -> str:
		"""Format the interpolations for display in an error message.
		:param unnamedPercent: The unnamed percent interpolations.
		:param namedPercent: The named percent interpolations.
		:param formats: The brace format interpolations.
		"""
		out: list[str] = []
		if unnamedPercent:
			out.append(f"unnamed percent interpolations in this order: {unnamedPercent}")
		if namedPercent:
			out.append(f"these named percent interpolations: {namedPercent}")
		if formats:
			out.append(f"these brace format interpolations: {formats}")
		if not out:
			return "no interpolations"
		return "\n\tAnd ".join(out)

	def _checkMessage(self) -> None:
		idUnnamedPercent, idNamedPercent, idFormats = self._getInterpolations(self._msgid)
		if not self._msgstr[-1]:
			return
		strUnnamedPercent, strNamedPercent, strFormats = self._getInterpolations(self._msgstr[-1])
		error = False
		alerts = []
		if idUnnamedPercent != strUnnamedPercent:
			if idUnnamedPercent:
				alerts.append("unnamed percent interpolations differ")
				error = True
			else:
				alerts.append("unexpected presence of unnamed percent interpolations")
		if idNamedPercent - strNamedPercent:
			alerts.append("missing named percent interpolation")
			error = True
		if strNamedPercent - idNamedPercent:
			if idNamedPercent:
				alerts.append("extra named percent interpolation")
				error = True
			else:
				alerts.append("unexpected presence of named percent interpolations")
		if idFormats - strFormats:
			alerts.append("missing brace format interpolation")
			error = True
		if strFormats - idFormats:
			if idFormats:
				alerts.append("extra brace format interpolation")
				error = True
			else:
				alerts.append("unexpected presence of brace format interpolations")
		if alerts:
			self._messageAlert(
				f"{', '.join(alerts)}\n"
				f"Expected: {self._formatInterpolations(idUnnamedPercent, idNamedPercent, idFormats)}\n"
				f"Got: {self._formatInterpolations(strUnnamedPercent, strNamedPercent, strFormats)}",
				isError=error,
			)

	def getReport(self) -> str | None:
		"""Get a text report about any errors or warnings.
		:return: The text or None if there were no problems.
		"""
		if not self.alerts:
			return None
		report = f"File {self._poPath}: "
		if self.hasSyntaxError:
			report += "syntax error"
		else:
			if self.errorCount:
				msg = "error" if self.errorCount == 1 else "errors"
				report += f"{self.errorCount} {msg}"
			if self.warningCount:
				if self.errorCount:
					report += ", "
				msg = "warning" if self.warningCount == 1 else "warnings"
				report += f"{self.warningCount} {msg}"
		report += "\n\n" + "\n\n".join(self.alerts)
		return report


def checkPo(poFilePath: str) -> tuple[bool, str | None]:
	"""Check a po file for errors.
	:param poFilePath: The path to the po file to check.
	:return:
	True if the file is okay or has warnings, False if there were fatal errors.
	A report about the errors or warnings found, or None if there were no problems.
	"""
	c = _PoChecker(poFilePath)
	report = None
	if not c.check():
		report = c.getReport()
		if report:
			report = report.encode("cp1252", errors="backslashreplace").decode(
				"utf-8",
				errors="backslashreplace",
			)
	return not bool(c.errorCount), report


def main():
	args = argparse.ArgumentParser()
	commands = args.add_subparsers(title="commands", dest="command", required=True)
	command_checkPo = commands.add_parser("checkPo", help="Check po files")
	# Allow entering arbitrary po file paths, not just those in the source tree
	command_checkPo.add_argument(
		"poFilePaths",
		help="Paths to the po file to check",
		nargs="+",
	)
	command_xliff2md = commands.add_parser("xliff2md", help="Convert xliff to markdown")
	command_xliff2md.add_argument(
		"-u",
		"--untranslated",
		help="Produce the untranslated markdown file",
		action="store_true",
		default=False,
	)
	command_xliff2md.add_argument("xliffPath", help="Path to the xliff file")
	command_xliff2md.add_argument("mdPath", help="Path to the resulting markdown file")
	command_md2html = commands.add_parser("md2html", help="Convert markdown to html")
	command_md2html.add_argument("-l", "--lang", help="Language code", action="store", default="en")
	command_md2html.add_argument(
		"-t",
		"--docType",
		help="Type of document",
		action="store",
		choices=["userGuide", "developerGuide", "changes", "keyCommands"],
	)
	command_md2html.add_argument("mdPath", help="Path to the markdown file")
	command_md2html.add_argument("htmlPath", help="Path to the resulting html file")
	command_xliff2html = commands.add_parser("xliff2html", help="Convert xliff to html")
	command_xliff2html.add_argument("-l", "--lang", help="Language code", action="store", required=False)
	command_xliff2html.add_argument(
		"-t",
		"--docType",
		help="Type of document",
		action="store",
		choices=["userGuide", "developerGuide", "changes", "keyCommands"],
	)
	command_xliff2html.add_argument(
		"-u",
		"--untranslated",
		help="Produce the untranslated markdown file",
		action="store_true",
		default=False,
	)
	command_xliff2html.add_argument("xliffPath", help="Path to the xliff file")
	command_xliff2html.add_argument("htmlPath", help="Path to the resulting html file")
	downloadTranslationFileCommand = commands.add_parser(
		"downloadTranslationFile",
		help="Download a translation file from Crowdin.",
	)
	downloadTranslationFileCommand.add_argument(
		"language",
		help="The language code to download the translation for.",
	)
	downloadTranslationFileCommand.add_argument(
		"crowdinFilePath",
		choices=crowdinFileIDs.keys(),
		help="The Crowdin file path",
	)
	downloadTranslationFileCommand.add_argument(
		"localFilePath",
		nargs="?",
		default=None,
		help="The path to save the local file. If not provided, the Crowdin file path will be used.",
	)

	uploadTranslationFileCommand = commands.add_parser(
		"uploadTranslationFile",
		help="Upload a translation file to Crowdin.",
	)
	uploadTranslationFileCommand.add_argument(
		"-o",
		"--old",
		help="Path to the old unchanged xliff file. If provided, only new or changed translations will be uploaded.",
		default=None,
	)
	uploadTranslationFileCommand.add_argument(
		"language",
		help="The language code to upload the translation for.",
	)
	uploadTranslationFileCommand.add_argument(
		"crowdinFilePath",
		choices=crowdinFileIDs.keys(),
		help="The Crowdin file path",
	)
	uploadTranslationFileCommand.add_argument(
		"localFilePath",
		nargs="?",
		default=None,
		help="The path to the local file to be uploaded. If not provided, the Crowdin file path will be used.",
	)

	exportTranslationsCommand = commands.add_parser(
		"exportTranslations",
		help="Export translation files from Crowdin as a bundle. If no language is specified, exports all languages.",
	)
	exportTranslationsCommand.add_argument(
		"-o",
		"--output",
		help="Directory to save translation files",
		required=True,
	)
	exportTranslationsCommand.add_argument(
		"-l",
		"--language",
		help="Language code to export (e.g., 'es', 'fr', 'de'). If not specified, exports all languages.",
		default=None,
	)

	args = args.parse_args()
	match args.command:
		case "xliff2md":
			markdownTranslate.generateMarkdown(
				xliffPath=args.xliffPath,
				outputPath=args.mdPath,
				translated=not args.untranslated,
			)
		case "md2html":
			md2html.main(source=args.mdPath, dest=args.htmlPath, lang=args.lang, docType=args.docType)
		case "xliff2html":
			lang = args.lang or fetchLanguageFromXliff(args.xliffPath, source=args.untranslated)
			temp_mdFile = tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8")
			temp_mdFile.close()
			try:
				markdownTranslate.generateMarkdown(
					xliffPath=args.xliffPath,
					outputPath=temp_mdFile.name,
					translated=not args.untranslated,
				)
				md2html.main(source=temp_mdFile.name, dest=args.htmlPath, lang=lang, docType=args.docType)
			finally:
				os.remove(temp_mdFile.name)
		case "downloadTranslationFile":
			localFilePath = args.localFilePath or args.crowdinFilePath
			downloadTranslationFile(args.crowdinFilePath, localFilePath, args.language)
			if args.crowdinFilePath.endswith(".xliff"):
				preprocessXliff(localFilePath, localFilePath)
			elif localFilePath.endswith(".po"):
				success, report = checkPo(localFilePath)
				if report:
					print(report)
				if not success:
					print(f"\nWarning: Po file {localFilePath} has fatal errors.")
		case "checkPo":
			poFilePaths = args.poFilePaths
			badFilePaths: list[str] = []
			for poFilePath in poFilePaths:
				success, report = checkPo(poFilePath)
				if report:
					print(report)
				if not success:
					badFilePaths.append(poFilePath)
			if badFilePaths:
				print(f"\nOne or more po files had fatal errors: {', '.join(badFilePaths)}")
				sys.exit(1)
		case "uploadTranslationFile":
			localFilePath = args.localFilePath or args.crowdinFilePath
			needsDelete = False
			if args.crowdinFilePath.endswith(".xliff"):
				tmp = tempfile.NamedTemporaryFile(suffix=".xliff", delete=False, mode="w")
				tmp.close()
				shutil.copyfile(localFilePath, tmp.name)
				stripXliff(tmp.name, tmp.name, args.old)
				localFilePath = tmp.name
				needsDelete = True
			elif localFilePath.endswith(".po"):
				success, report = checkPo(localFilePath)
				if report:
					print(report)
				if not success:
					print(f"\nPo file {localFilePath} has errors. Upload aborted.")
					sys.exit(1)
			uploadTranslationFile(args.crowdinFilePath, localFilePath, args.language)
			if needsDelete:
				os.remove(localFilePath)
		case "exportTranslations":
			exportTranslations(args.output, args.language)
		case _:
			raise ValueError(f"Unknown command {args.command}")


if __name__ == "__main__":
	main()
