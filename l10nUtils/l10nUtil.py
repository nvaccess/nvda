# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import sys
import tempfile
import lxml.etree
import os
import argparse
import markdownTranslate


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "user_docs"))
import md2html
import subprocess
from crowdinSync import downloadTranslationFile, uploadTranslationFile, crowdinFileIDs

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
	:param xliffPath: Path to the xliff file to be stripped
	:param outputPath: Path to the resulting xliff file
	"""
	print(f"Creating corrected xliff at {outputPath} from {xliffPath}")
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
	sourceTargetcount = 0
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
		f"Processed {segmentCount} segments, removing {emptyTargetCount} empty targets, {corruptTargetcount} corrupt targets"
	)


def stripXliff(xliffPath: str, outputPath: str, oldXliffPath: str | None = None):
	"""
	Removes translations that already exist in an old xliff file,
	and removes notes and skeleton elements from an xliff file before upload to Crowdin.
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
	skeletonNode = xliffRoot.find("./xliff:file/xliff:skeleton", namespaces=namespace)
	if skeletonNode is not None:
		skeletonNode.getparent().remove(skeletonNode)
	if oldXliffPath:
		oldXliff = lxml.etree.parse(oldXliffPath)
		oldXliffRoot = oldXliff.getroot()
		if oldXliffRoot.tag != "{urn:oasis:names:tc:xliff:document:2.0}xliff":
			raise ValueError(f"Not an xliff file: {oldXliffPath}")
	else:
		oldXliffRoot = None
	file = xliffRoot.find("./xliff:file", namespaces=namespace)
	units = file.findall("./xliff:unit", namespaces=namespace)
	segmentCount = 0
	existingTranslationCount = 0
	for unit in units:
		notes = unit.find("./xliff:notes", namespaces=namespace)
		if notes is not None:
			unit.remove(notes)
		segment = unit.find("./xliff:segment", namespaces=namespace)
		if segment is None:
			print("Warning: No segment element in unit")
			continue
		state = segment.get("state")
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
		# remove translations that already exist in the old xliff file
		if oldXliffRoot is not None:
			unitId = unit.get("id")
			oldTarget = oldXliffRoot.find(
				f'./xliff:file/xliff:unit[@id="{unitId}"]/xliff:segment/xliff:target',
				namespaces=namespace,
			)
			if oldTarget is not None and oldTarget.text == targetText:
				existingTranslationCount += 1
				file.remove(unit)
	xliff.write(outputPath, encoding="utf-8")
	keptTranslations = (
		segmentCount - existingTranslationCount
	)
	print(
		f"Processed {segmentCount} segments, removing {existingTranslationCount} existing translations, resulting in {keptTranslations} translations kept",
	)


def translateFile(crowdinFilePath: str, language: str):
	backupFilePath = f"{crowdinFilePath}.bak"
	print(f"Starting translation process for {crowdinFilePath} in {language}")
	temp_dir = tempfile.mkdtemp()
	try:
		# Download the translated file
		print("Downloading the translated file...")
		downloaded_file = os.path.join(temp_dir, "downloaded.xliff")
		downloadTranslationFile(crowdinFilePath, downloaded_file, language)
		print(f"Downloaded file to {downloaded_file}")

		# Preprocess the file, correcting empty / corrupt targets.
		print("Preprocessing the downloaded file...")
		preprocessed_file = os.path.join(temp_dir, "preprocessed.xliff")
		preprocessXliff(downloaded_file, preprocessed_file)
		print(f"Preprocessed file saved to {preprocessed_file}")

		# Open the file in Poedit for translation
		print("Opening the file in Poedit for translation...")
		poedit_path = os.path.join(os.environ.get("PROGRAMFILES", "c:\\program files"), "Poedit", "poedit.exe")
		subprocess.run([poedit_path, preprocessed_file], check=True)
		print("Translation completed in Poedit")

		# Preprocess the file again in case Poedit created any empty or corrupt targets.
		print("Preprocessing the file again after translation...")
		preprocessed_file_again = os.path.join(temp_dir, "preprocessed_again.xliff")
		preprocessXliff(preprocessed_file, preprocessed_file_again)
		print(f"Preprocessed again file saved to {preprocessed_file_again}")

		# Strip the file, leaving only the newly translated segments for upload.
		print("Stripping the file to remove existing translations...")
		stripped_file = os.path.join(temp_dir, "stripped.xliff")
		stripXliff(preprocessed_file_again, stripped_file, downloaded_file)
		print(f"Stripped file saved to {stripped_file}")

		# Upload the translated file
		print("Uploading the translated file...")
		try:
			uploadTranslationFile(crowdinFilePath, stripped_file, language)
		except Exception as e:
			print(f"Error uploading file: {e}")
			print(f"Saving translated file to {backupFilePath} for manual upload.")
			os.rename(stripped_file, backupFilePath)
		else:
			print("Successfully uploaded translated file.")
	finally:
		# Clean up temporary files
		print("Cleaning up temporary files...")
		if os.path.exists(temp_dir):
			for file in os.listdir(temp_dir):
				os.remove(os.path.join(temp_dir, file))
			os.rmdir(temp_dir)
		print("Translation process completed.")


if __name__ == "__main__":
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
	command_stripXliff = commands.add_parser(
		"stripXliff",
		help="Remove prefilled, empty or corrupt target tags from an xliff file before upload to Crowdin. Optionally also remove translations that already exist in an old xliff file",
	)
	command_stripXliff.add_argument(
		"-o",
		"--oldXliffPath",
		help="Path to the old xliff file containing existing translations that should be stripped",
		action="store",
		default=None,
	)
	command_stripXliff.add_argument("xliffPath", help="Path to the xliff file")
	command_stripXliff.add_argument("outputPath", help="Path to the resulting xliff file")
	command_translate = commands.add_parser(
		"translate",
		help="Download, preprocess, translate, preprocess again, strip, and upload a translation file.",
	)
	command_translate.add_argument(
		"crowdinFilePath",
		choices=crowdinFileIDs.keys(),
		help="The Crowdin file path"
	)
	command_translate.add_argument("language", help="The language code to download the translation for.")
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
		case "stripXliff":
			stripXliff(args.xliffPath, args.outputPath, args.oldXliffPath)
		case "translate":
			translateFile(args.crowdinFilePath, args.language)
		case _:
			raise ValueError(f"Unknown command {args.command}")
