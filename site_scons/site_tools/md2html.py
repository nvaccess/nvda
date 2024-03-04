# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023-2024 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from copy import deepcopy
from importlib.util import find_spec
import io
import pathlib
import re
import shutil

import SCons.Node.FS
import SCons.Environment

DEFAULT_EXTENSIONS = frozenset({
	# Supports tables, HTML mixed with markdown, code blocks, custom attributes and more
	"markdown.extensions.extra",
	# Allows TOC with [TOC]"
	"markdown.extensions.toc",
	# Makes list behaviour better, including 2 space indents by default
	"mdx_truly_sane_lists",
	# External links will open in a new tab, and title will be set to the link text
	"markdown_link_attr_modifier",
	# Adds links to GitHub authors, issues and PRs
	"mdx_gh_links",
})

EXTENSIONS_CONFIG = {
	"markdown_link_attr_modifier": {
		"new_tab": "external_only",
		"auto_title": "on",
	},
	"mdx_gh_links": {
		"user": "nvaccess",
		"repo": "nvda",
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
{extraStylesheet}
</head>
<body>
""".strip()


def _replaceNVDATags(md: str, env: SCons.Environment.Environment) -> str:
	import versionInfo
	# Replace tags in source file
	md = md.replace("NVDA_VERSION", env["version"])
	md = md.replace("NVDA_URL", versionInfo.url)
	md = md.replace("NVDA_COPYRIGHT_YEARS", versionInfo.copyrightYears)
	return md


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

	extensions = set(DEFAULT_EXTENSIONS)
	if isKeyCommands:
		from user_docs.keyCommandsDoc import KeyCommandsExtension
		extensions.add(KeyCommandsExtension())

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


def md2html_actionFunc(
		target: list[SCons.Node.FS.File],
		source: list[SCons.Node.FS.File],
		env: SCons.Environment.Environment
):
	isKeyCommands = target[0].path.endswith("keyCommands.html")
	isUserGuide = target[0].path.endswith("userGuide.html")
	isDevGuide = target[0].path.endswith("developerGuide.html")
	isChanges = target[0].path.endswith("changes.html")

	with open(source[0].path, "r", encoding="utf-8") as mdFile:
		mdStr = mdFile.read()

	mdStr = _replaceNVDATags(mdStr, env)

	with io.StringIO() as mdBuffer:
		mdBuffer.write(mdStr)
		title = _getTitle(mdBuffer, isKeyCommands)

	lang = pathlib.Path(source[0].path).parent.name

	if isUserGuide or isDevGuide:
		extraStylesheet = '<link rel="stylesheet" href="numberedHeadings.css">'
	elif isChanges or isKeyCommands:
		extraStylesheet = ""
	else:
		raise ValueError(f"Unknown target type for {target[0].path}")

	htmlBuffer = io.StringIO()
	htmlBuffer.write(
		HTML_HEADERS.format(
			lang=lang,
			dir="rtl" if lang in RTL_LANG_CODES else "ltr",
			title=title,
			extraStylesheet=extraStylesheet,
		)
	)

	htmlOutput = _generateSanitizedHTML(mdStr, isKeyCommands)
	# Make next write append at end of buffer
	htmlBuffer.seek(0, io.SEEK_END)
	htmlBuffer.write(htmlOutput)

	# Make next write append at end of buffer
	htmlBuffer.seek(0, io.SEEK_END)
	htmlBuffer.write("\n</body>\n</html>\n")

	with open(target[0].path, "w", encoding="utf-8") as targetFile:
		# Make next read at start of buffer
		htmlBuffer.seek(0)
		shutil.copyfileobj(htmlBuffer, targetFile)

	htmlBuffer.close()


def exists(env: SCons.Environment.Environment) -> bool:
	for ext in [
		"markdown",
		"markdown_link_attr_modifier",
		"mdx_truly_sane_lists",
		"mdx_gh_links",
		"nh3",
		"user_docs.keyCommandsDoc",
	]:
		if find_spec(ext) is None:
			return False
	return True


def generate(env: SCons.Environment.Environment):
	env["BUILDERS"]["md2html"] = env.Builder(
		action=env.Action(md2html_actionFunc, lambda t, s, e: f"Converting {s[0].path} to {t[0].path}"),
		suffix=".html",
		src_suffix=".md"
	)
