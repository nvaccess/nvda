# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited.
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


CROWDIN_PROJECT_ID = 598017


def fetchCrowdinAuthToken() -> str:
	"""
	Fetch the Crowdin auth token from the ~/.nvda_crowdin file or prompt the user for it.
	If provided by the user, the token will be saved to the ~/.nvda_crowdin file.
	:return: The auth token
	"""
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


def main():
	args = argparse.ArgumentParser()
	commands = args.add_subparsers(title="commands", dest="command", required=True)
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
			uploadTranslationFile(args.crowdinFilePath, localFilePath, args.language)
			if needsDelete:
				os.remove(localFilePath)
		case _:
			raise ValueError(f"Unknown command {args.command}")


if __name__ == "__main__":
	main()
