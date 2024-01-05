# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from importlib.util import find_spec
import io
import pathlib
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


def md2html_actionFunc(
		target: list[SCons.Node.FS.File],
		source: list[SCons.Node.FS.File],
		env: SCons.Environment.Environment
):
	import markdown
	import versionInfo

	with open(source[0].path, "rb") as mdFile:
		mdStr = mdFile.read()

	# Replace tags in source file
	mdStr = mdStr.replace(b"NVDA_VERSION", env["version"].encode("utf-8"))
	mdStr = mdStr.replace(b"NVDA_URL", versionInfo.url.encode("utf-8"))
	mdStr = mdStr.replace(b"NVDA_COPYRIGHT_YEARS", versionInfo.copyrightYears.encode("utf-8"))

	# Write replaced source to buffer
	mdBuffer = io.BytesIO()
	mdBuffer.write(mdStr)

	# Make next read at start of buffer
	mdBuffer.seek(0)
	titleStr = mdBuffer.readline()
	# Remove heading hashes and trailing whitespace to get the tab title
	titleStr = titleStr.lstrip(b"# ").rstrip().decode("utf-8")

	lang = pathlib.Path(source[0].path).parent.name
	htmlBuffer = io.BytesIO()
	htmlBuffer.write(
		f"""
<!DOCTYPE html>
<html lang="{lang}" dir="{"rtl" if lang in _RTLlangCodes else "ltr"}">
<head>
<meta charset="utf-8">
<title>{titleStr}</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="stylesheet" href="styles.css">
</head>
<body>
	""".encode("utf-8")
	)

	# Make next read from start of buffer
	mdBuffer.seek(0)
	# Make next write append at end of buffer
	htmlBuffer.seek(0, io.SEEK_END)

	extensions = set(DEFAULT_EXTENSIONS)
	if target[0].path.endswith("keyCommands.html"):
		from keyCommandsDoc import KeyCommandsExtension
		extensions.add(KeyCommandsExtension())

	markdown.markdownFromFile(
		input=mdBuffer,
		output=htmlBuffer,
		encoding="utf-8",
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
		"keyCommandsDoc",
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
