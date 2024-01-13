# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from importlib.util import find_spec
import io
import pathlib
import re
import shutil

import SCons.Node.FS
import SCons.Environment

DEFAULT_EXTENSIONS = frozenset({
	# Supports tables, HTML mixed with markdown, code blocks and more
	"markdown.extensions.extra",
	# Allows TOC with [TOC], allows anchors set by "# Title {#foo}"
	"markdown.extensions.toc",
	# Allows setting attributes with {@id=foo}
	"markdown.extensions.legacy_attrs",
	# Adds code highlighting to code blocks
	"markdown.extensions.codehilite",
	# Makes list behaviour better, including 2 space indents by default
	"mdx_truly_sane_lists",
	# External links will open in a new tab, and title will be set to the link text
	"markdown_link_attr_modifier",
	# Adds links to GitHub authors, issues and PRs
	"mdx_gh_links",
})

_extensionConfigs = {
	"markdown_link_attr_modifier": {
		"new_tab": "external_only",
		"auto_title": "on",
	},
	"mdx_gh_links": {
		"user": "nvaccess",
		"repo": "nvda",
	},
}

_RTLlangCodes = {"ar", "fa", "he"}


def _replaceNVDATags(md: str, env: SCons.Environment.Environment) -> str:
	import versionInfo
	# Replace tags in source file
	md = md.replace("NVDA_VERSION", env["version"])
	md = md.replace("NVDA_URL", versionInfo.url)
	md = md.replace("NVDA_COPYRIGHT_YEARS", versionInfo.copyrightYears)
	return md


def _getTitle(mdBuffer: io.BytesIO, isKeyCommands: bool = False) -> str:
	if isKeyCommands:
		TITLE_RE = re.compile(r"^<!-- KC:title: (.*) -->$")
		# Make next read at start of buffer
		mdBuffer.seek(0)
		for line in mdBuffer.readlines():
			match = TITLE_RE.match(line.decode("utf-8").strip())
			if match:
				return match.group(1)

		raise ValueError("No KC:title command found in userGuide.md")

	else:
		# Make next read at start of buffer
		mdBuffer.seek(0)
		# Remove heading hashes and trailing whitespace to get the tab title
		title = mdBuffer.readline().decode("utf-8").strip().lstrip("# ")

	return title


def md2html_actionFunc(
		target: list[SCons.Node.FS.File],
		source: list[SCons.Node.FS.File],
		env: SCons.Environment.Environment
):
	import markdown
	isKeyCommands = target[0].path.endswith("keyCommands.html")

	with open(source[0].path, "r", encoding="utf-8") as mdFile:
		mdStr = mdFile.read()

	mdStr = _replaceNVDATags(mdStr, env)

	# Write replaced source to buffer.
	# md has a bug with StringIO, so BytesIO is required.
	mdBuffer = io.BytesIO()
	mdBuffer.write(mdStr.encode("utf-8"))

	lang = pathlib.Path(source[0].path).parent.name
	title = _getTitle(mdBuffer, isKeyCommands)
	# md has a bug with StringIO, so BytesIO is required.
	htmlBuffer = io.BytesIO()
	htmlBuffer.write(
		f"""
<!DOCTYPE html>
<html lang="{lang}" dir="{"rtl" if lang in _RTLlangCodes else "ltr"}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="stylesheet" href="styles.css">
</head>
<body>
	""".strip().encode("utf-8")
	)

	# Make next read from start of buffer
	mdBuffer.seek(0)
	# Make next write append at end of buffer
	htmlBuffer.seek(0, io.SEEK_END)

	extensions = set(DEFAULT_EXTENSIONS)
	if isKeyCommands:
		from user_docs.keyCommandsDoc import KeyCommandsExtension
		extensions.add(KeyCommandsExtension())

	markdown.markdownFromFile(
		input=mdBuffer,
		output=htmlBuffer,
		# https://python-markdown.github.io/extensions/
		extensions=extensions,
		extension_configs=_extensionConfigs,
	)

	# Make next write append at end of buffer
	htmlBuffer.seek(0, io.SEEK_END)
	htmlBuffer.write(b"\n</body>\n</html>\n")

	with open(target[0].path, "wb") as targetFile:
		# Make next read at start of buffer
		htmlBuffer.seek(0)
		shutil.copyfileobj(htmlBuffer, targetFile)

	mdBuffer.close()
	htmlBuffer.close()


def exists(env: SCons.Environment.Environment) -> bool:
	for ext in [
		"markdown",
		"markdown_link_attr_modifier",
		"mdx_truly_sane_lists",
		"mdx_gh_links",
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
