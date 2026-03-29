# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from typing import NamedTuple


class NavCommand(NamedTuple):
	"""Contains the necessary data to create the script for a MathCAT command."""

	gestures: tuple[str, ...]
	commandName: str
	description: str
	speakOnDemand: bool = False


def _buildNavCommands() -> list[NavCommand]:
	"""Build and return the complete list of MathCAT navigation commands."""
	commands: list[NavCommand] = [
		NavCommand(
			("kb:leftArrow",),
			"MovePrevious",
			# Translators: Input help message for the move to previous item in math command.
			pgettext("math", "Move to previous item in math"),
		),
		NavCommand(
			("kb:rightArrow",),
			"MoveNext",
			# Translators: Input help message for the move to next item in math command.
			pgettext("math", "Move to next item in math"),
		),
		NavCommand(
			("kb:upArrow",),
			"ZoomOut",
			# Translators: Input help message for the zoom out in math command.
			pgettext("math", "Zoom out in math"),
		),
		NavCommand(
			("kb:downArrow",),
			"ZoomIn",
			# Translators: Input help message for the zoom in in math command.
			pgettext("math", "Zoom in in math"),
		),
		NavCommand(
			("kb:control+leftArrow", "kb:control+alt+leftArrow"),
			"MoveCellPrevious",
			# Translators: Input help message for the move to previous table cell or digit in math command.
			pgettext("math", "Move to previous table cell or digit in math"),
		),
		NavCommand(
			("kb:control+rightArrow", "kb:control+alt+rightArrow"),
			"MoveCellNext",
			# Translators: Input help message for the move to next table cell or digit in math command.
			pgettext("math", "Move to next table cell or digit in math"),
		),
		NavCommand(
			("kb:control+upArrow", "kb:control+alt+upArrow"),
			"MoveCellUp",
			# Translators: Input help message for the move to cell or digit above in math command.
			pgettext("math", "Move to cell or digit above in math"),
		),
		NavCommand(
			("kb:control+downArrow", "kb:control+alt+downArrow"),
			"MoveCellDown",
			# Translators: Input help message for the move to cell or digit below in math command.
			pgettext("math", "Move to cell or digit below in math"),
		),
		NavCommand(
			("kb:shift+leftArrow",),
			"ReadPrevious",
			# Translators: Input help message for the read previous item in math command.
			pgettext("math", "Read previous item in math"),
			speakOnDemand=True,
		),
		NavCommand(
			("kb:shift+rightArrow",),
			"ReadNext",
			# Translators: Input help message for the read next item in math command.
			pgettext("math", "Read next item in math"),
			speakOnDemand=True,
		),
		NavCommand(
			("kb:shift+upArrow",),
			"ToggleZoomLockUp",
			# Translators: Input help message for the change math navigation mode to larger command.
			pgettext("math", "Change math navigation mode to larger"),
		),
		NavCommand(
			("kb:shift+downArrow",),
			"ToggleZoomLockDown",
			# Translators: Input help message for the change math navigation mode to smaller command.
			pgettext("math", "Change math navigation mode to smaller"),
		),
		NavCommand(
			("kb:control+shift+leftArrow",),
			"DescribePrevious",
			# Translators: Input help message for the describe previous item in math command.
			pgettext("math", "Describe previous item in math"),
			speakOnDemand=True,
		),
		NavCommand(
			("kb:control+shift+rightArrow",),
			"DescribeNext",
			# Translators: Input help message for the describe next item in math command.
			pgettext("math", "Describe next item in math"),
			speakOnDemand=True,
		),
		NavCommand(
			("kb:control+shift+upArrow",),
			"ZoomOutAll",
			# Translators: Input help message for the zoom out all the way in math command.
			pgettext("math", "Zoom out all the way in math"),
		),
		NavCommand(
			("kb:control+shift+downArrow",),
			"ZoomInAll",
			# Translators: Input help message for the zoom in all the way in math command.
			pgettext("math", "Zoom in all the way in math"),
		),
		NavCommand(
			("kb:enter",),
			"WhereAmI",
			# Translators: Input help message for the report current position in math command.
			pgettext("math", "Report current position in math"),
			speakOnDemand=True,
		),
		NavCommand(
			("kb:control+enter",),
			"WhereAmIAll",
			# Translators: Input help message for the report global position in math command.
			pgettext("math", "Report global position in math"),
			speakOnDemand=True,
		),
		NavCommand(
			("kb:space",),
			"ReadCurrent",
			# Translators: Input help message for the read current item in math command.
			pgettext("math", "Read current item in math"),
			speakOnDemand=True,
		),
		NavCommand(
			("kb:control+space",),
			"ReadCellCurrent",
			# Translators: Input help message for the read current table cell in math command.
			pgettext("math", "Read current table cell in math"),
			speakOnDemand=True,
		),
		NavCommand(
			("kb:shift+space",),
			"ToggleSpeakMode",
			# Translators: Input help message for the toggle math speech mode between read and describe command.
			pgettext("math", "Toggle math speech mode between read and describe"),
		),
		NavCommand(
			("kb:control+shift+space",),
			"DescribeCurrent",
			# Translators: Input help message for the describe current item in math command.
			pgettext("math", "Describe current item in math"),
			speakOnDemand=True,
		),
		NavCommand(
			("kb:home",),
			"MoveStart",
			# Translators: Input help message for the move to start of math expression command.
			pgettext("math", "Move to start of math expression"),
		),
		NavCommand(
			("kb:control+home",),
			"MoveLineStart",
			# Translators: Input help message for the move to start of line in math command.
			pgettext("math", "Move to start of line in math"),
		),
		NavCommand(
			("kb:shift+home",),
			"MoveColumnStart",
			# Translators: Input help message for the move to start of column in math command.
			pgettext("math", "Move to start of column in math"),
		),
		NavCommand(
			("kb:end",),
			"MoveEnd",
			# Translators: Input help message for the move to end of math expression command.
			pgettext("math", "Move to end of math expression"),
		),
		NavCommand(
			("kb:control+end",),
			"MoveLineEnd",
			# Translators: Input help message for the move to end of line in math command.
			pgettext("math", "Move to end of line in math"),
		),
		NavCommand(
			("kb:shift+end",),
			"MoveColumnEnd",
			# Translators: Input help message for the move to end of column in math command.
			pgettext("math", "Move to end of column in math"),
		),
		NavCommand(
			("kb:backspace",),
			"MoveLastLocation",
			# Translators: Input help message for the move back to last position in math command.
			pgettext("math", "Move back to last position in math"),
		),
	]

	# Add placemarker commands for each number 0-9
	for n in range(10):
		placemarker = n if n != 0 else 10
		commands.extend(
			[
				NavCommand(
					(f"kb:{n}",),
					f"MoveTo{n}",
					# Translators: Input help message for the jump to placemarker command; {n} is replaced with the placemarker number.
					pgettext("math", "Jump to placemarker {n} in math").format(n=placemarker),
				),
				NavCommand(
					(f"kb:control+{n}",),
					f"SetPlacemarker{n}",
					# Translators: Input help message for the set placemarker command; {n} is replaced with the placemarker number.
					pgettext("math", "Set placemarker {n} in math").format(n=placemarker),
				),
				NavCommand(
					(f"kb:shift+{n}",),
					f"Read{n}",
					# Translators: Input help message for the read placemarker command; {n} is replaced with the placemarker number.
					pgettext("math", "Read placemarker {n} in math").format(n=placemarker),
					speakOnDemand=True,
				),
				NavCommand(
					(f"kb:control+shift+{n}",),
					f"Describe{n}",
					# Translators: Input help message for the describe placemarker command; {n} is replaced with the placemarker number.
					pgettext("math", "Describe placemarker {n} in math").format(n=placemarker),
					speakOnDemand=True,
				),
			],
		)

	return commands


NAV_COMMANDS = _buildNavCommands()
