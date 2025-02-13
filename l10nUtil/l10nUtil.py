# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import sys
import tempfile
import lxml.etree
import os
import shutil
import argparse
from ..user_docs import markdownTranslate
from ..user_docs import md2html
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
		f"Processed {segmentCount} segments, removing {emptyTargetCount} empty targets, {corruptTargetcount} corrupt targets"
	)


def stripXliff(xliffPath: str, outputPath: str):
	"""
	Removes notes and skeleton elements from an xliff file before upload to Crowdin.
	Also removes empty and corrupt translations.
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
	file = xliffRoot.find("./xliff:file", namespaces=namespace)
	units = file.findall("./xliff:unit", namespaces=namespace)
	segmentCount = 0
	emptyCount = 0
	corruptCount = 0
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
		if not targetText:
			emptyCount += 1
			file.remove(unit)
		elif targetText in (
			"<target/>",
			"&lt;target/&gt;",
			"<target></target>",
			"&lt;target&gt;&lt;/target&gt;",
		):
			corruptCount += 1
			file.remove(unit)
	xliff.write(outputPath, encoding="utf-8")
	keptTranslations = (
		# segmentCount - (emptyCount + corruptCount)
	)
	print(
		f"Processed {segmentCount} segments, removing {emptyCount} empty translations, {corruptCount} corrupt translations, keeping {keptTranslations} translations"
	)


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
	downloadTranslationFileCommand = commands.add_parser(
		"downloadTranslationFile",
		help="Download a translation file from Crowdin.",
	)
	downloadTranslationFileCommand.add_argument(
		"language",
		help="The language code to download the translation for."
	)
	downloadTranslationFileCommand.add_argument(
		"crowdinFilePath",
		choices=crowdinFileIDs.keys(),
		help="The Crowdin file path"
	)
	downloadTranslationFileCommand.add_argument(
		"localFilePath",
		nargs="?",
		default=None,
		help="The path to save the local file. If not provided, the Crowdin file path will be used."
	)

	uploadTranslationFileCommand = commands.add_parser(
		"uploadTranslationFile",
		help="Upload a translation file to Crowdin.",
	)
	uploadTranslationFileCommand.add_argument(
		"language",
		help="The language code to upload the translation for."
	)
	uploadTranslationFileCommand.add_argument(
		"crowdinFilePath",
		choices=crowdinFileIDs.keys(),
		help="The Crowdin file path"
	)
	uploadTranslationFileCommand.add_argument(
		   "localFilePath",
		   nargs="?",
		default=None,
		help="The path to the local file to be uploaded. If not provided, the Crowdin file path will be used."
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
				preprocessXliff(localFilePath, tmp.name)
				stripXliff(tmp.name, tmp.name)
				localFilePath = tmp.name
				needsDelete = True
			uploadTranslationFile(args.crowdinFilePath, localFilePath, args.language)
			if needsDelete:
				os.remove(localFilePath)
		case _:
			raise ValueError(f"Unknown command {args.command}")
