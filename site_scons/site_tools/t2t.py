# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2024 NV Access Limited, James Teh
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import SCons


def txt2tags_actionFunc(
		target: list[SCons.Node.FS.File],
		source: list[SCons.Node.FS.File],
		env: SCons.Environment.Environment
):
	import txt2tags
	from keyCommandsDoc import Command

	with open(source[0].path, "r", encoding="utf-8") as mdFile:
		mdOriginal = mdFile.read()
		mdStr = str(mdOriginal)

	with open(source[0].path, "w", encoding="utf-8") as mdFile:
		# Substitute t2t key commands with markdown comments temporarily
		for command in Command:
			mdStr = command.t2tRegex().sub(lambda m: f"<!-- KC:{m.group(1)} -->", mdStr)
		mdFile.write(mdStr)

	txt2tags.exec_command_line([source[0].path])

	with open(source[0].path, "w", encoding="utf-8") as mdFile:
		# Restore to original
		mdFile.write(mdOriginal)


def exists(env: SCons.Environment.Environment) -> bool:
	try:
		import txt2tags
		return True
	except ImportError:
		return False


def generate(env: SCons.Environment.Environment):
	env["BUILDERS"]["txt2tags"] = env.Builder(
		action=env.Action(txt2tags_actionFunc, lambda t, s, e: f"Converting {s[0].path} to md"),
		suffix='.md',
		src_suffix='.t2t'
	)
