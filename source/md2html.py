# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023-2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import argparse
from copy import deepcopy
import io
import re
import shutil
from typing import Any

_DEFAULT_EXTENSIONS_ORDERED = (
	# Supports tables, HTML mixed with markdown, code blocks, custom attributes and more
	"markdown.extensions.extra",
	# Used to preserve tabs in code blocks
	"pymdownx.superfences",
	# Allows TOC with [TOC]"
	"markdown.extensions.toc",
	# Makes list behaviour better, including 2 space indents by default
	"mdx_truly_sane_lists",
	# External links will open in a new tab, and title will be set to the link text
	"markdown_link_attr_modifier",
	# Adds links to GitHub authors, issues and PRs
	"mdx_gh_links",
)
"""
Default extensions to use for markdown conversion.
Order is important, as some extensions depend on or affect others.
"""


def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	if attrName == "DEFAULT_EXTENSIONS":
		# Note: this should only log in situations where it will not be excessively noisy.
		from logHandler import log

		log.warning(
			"Importing DEFAULT_EXTENSIONS from here is deprecated. Importing from md2html is discouraged. ",
			# Include stack info so testers can report warning to add-on author.
			stack_info=True,
		)
		# Return a frozenset to match the API of the deprecated DEFAULT_EXTENSIONS symbol.
		return frozenset(_DEFAULT_EXTENSIONS_ORDERED)
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")


EXTENSIONS_CONFIG = {
	"markdown_link_attr_modifier": {
		"new_tab": "external_only",
		"auto_title": "on",
	},
	"mdx_gh_links": {
		"user": "nvaccess",
		"repo": "nvda",
	},
	"pymdownx.superfences": {
		"preserve_tabs": True,
	},
}

RTL_LANG_CODES = frozenset({"ar", "fa", "he"})

HTML_HEADERS = """
<!DOCTYPE html>
<html lang="{lang}" dir="{dir}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="stylesheet" href="styles.css">
<link rel="shortcut icon" href="favicon.ico">
{extraStylesheet}
</head>
<body>
""".strip()


def _getTitle(mdBuffer: io.StringIO, isKeyCommands: bool = False) -> str:
	if isKeyCommands:
		TITLE_RE = re.compile(r"^<!-- KC:title: (.*) -->$")
		# Make next read at start of buffer
		mdBuffer.seek(0)
		for line in mdBuffer.readlines():
			match = TITLE_RE.match(line.strip())
			if match:
				return match.group(1)

		raise ValueError("No KC:title command found in userGuide.md")

	else:
		# Make next read at start of buffer
		mdBuffer.seek(0)
		# Remove heading hashes and trailing whitespace to get the tab title
		title = mdBuffer.readline().strip().lstrip("# ")

	return title


def _createAttributeFilter() -> dict[str, set[str]]:
	# Create attribute filter exceptions for HTML sanitization
	import nh3

	allowedAttributes: dict[str, set[str]] = deepcopy(nh3.ALLOWED_ATTRIBUTES)

	attributesWithAnchors = {"h1", "h2", "h3", "h4", "h5", "h6", "td"}
	attributesWithClass = {"div", "span", "a", "th", "td"}

	# Allow IDs for anchors
	for attr in attributesWithAnchors:
		if attr not in allowedAttributes:
			allowedAttributes[attr] = set()
		allowedAttributes[attr].add("id")

	# Allow class for styling
	for attr in attributesWithClass:
		if attr not in allowedAttributes:
			allowedAttributes[attr] = set()
		allowedAttributes[attr].add("class")

	# link rel and target is set by markdown_link_attr_modifier
	allowedAttributes["a"].update({"rel", "target"})

	return allowedAttributes


ALLOWED_ATTRIBUTES = _createAttributeFilter()


def _generateSanitizedHTML(md: str, isKeyCommands: bool = False) -> str:
	import markdown
	import nh3

	extensions = list(_DEFAULT_EXTENSIONS_ORDERED)
	if isKeyCommands:
		from keyCommandsDoc import KeyCommandsExtension

		extensions.append(KeyCommandsExtension())

	htmlOutput = markdown.markdown(
		text=md,
		extensions=extensions,
		extension_configs=EXTENSIONS_CONFIG,
	)

	# Sanitize html output from markdown to prevent XSS from translators
	htmlOutput = nh3.clean(
		htmlOutput,
		attributes=ALLOWED_ATTRIBUTES,
		# link rel is handled by markdown_link_attr_modifier
		link_rel=None,
		# Keep key command comments and similar
		strip_comments=False,
	)

	return htmlOutput


def main(source: str, dest: str, lang: str = "en", docType: str | None = None):
	print(f"Converting {docType or 'document'} ({lang=}) at {source} to {dest}")
	isUserGuide = docType == "userGuide"
	isDevGuide = docType == "developerGuide"
	isChanges = docType == "changes"
	isKeyCommands = docType == "keyCommands"
	if docType and not any([isUserGuide, isDevGuide, isChanges, isKeyCommands]):
		raise ValueError(f"Unknown docType {docType}")
	with open(source, "r", encoding="utf-8") as mdFile:
		mdStr = mdFile.read()

	with io.StringIO() as mdBuffer:
		mdBuffer.write(mdStr)
		title = _getTitle(mdBuffer, isKeyCommands)

	if isUserGuide or isDevGuide:
		extraStylesheet = '<link rel="stylesheet" href="numberedHeadings.css">'
	elif isChanges or isKeyCommands:
		extraStylesheet = ""
	else:
		raise ValueError(f"Unknown target type for {dest}")

	htmlBuffer = io.StringIO()
	htmlBuffer.write(
		HTML_HEADERS.format(
			lang=lang,
			dir="rtl" if lang in RTL_LANG_CODES else "ltr",
			title=title,
			extraStylesheet=extraStylesheet,
		),
	)

	htmlOutput = _generateSanitizedHTML(mdStr, isKeyCommands)
	# Make next write append at end of buffer
	htmlBuffer.seek(0, io.SEEK_END)
	htmlBuffer.write(htmlOutput)

	# Make next write append at end of buffer
	htmlBuffer.seek(0, io.SEEK_END)
	htmlBuffer.write("\n</body>\n</html>\n")

	with open(dest, "w", encoding="utf-8") as targetFile:
		# Make next read at start of buffer
		htmlBuffer.seek(0)
		shutil.copyfileobj(htmlBuffer, targetFile)

	htmlBuffer.close()


if __name__ == "__main__":
	args = argparse.ArgumentParser()
	args.add_argument("-l", "--lang", help="Language code", action="store", default="en")
	args.add_argument(
		"-t",
		"--docType",
		help="Type of document",
		action="store",
		choices=["userGuide", "developerGuide", "changes", "keyCommands"],
	)
	args.add_argument("source", help="Path to the markdown file")
	args.add_argument("dest", help="Path to the resulting html file")
	args = args.parse_args()
	main(source=args.source, dest=args.dest, lang=args.lang, docType=args.docType)
