# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2024 NV Access Limited, Mesar Hameed, Takuya Nishimoto
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Generates the Key Commands document from the User Guide.
Works as a Python Markdown Extension:
https://python-markdown.github.io/extensions/

Refer to user guide standards for more information on syntax rules:
https://github.com/nvaccess/nvda/blob/master/projectDocs/dev/userGuideStandards.md
"""

from enum import auto, Enum, IntEnum, StrEnum
import re
from collections.abc import Iterator

from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor


LINE_END = "\r\n"


class Section(IntEnum):
	"""Sections must be nested in this order."""
	HEADER = auto()
	BODY = auto()


class Command(StrEnum):
	TITLE = "title"
	BEGIN_INCLUDE = "beginInclude"
	END_INCLUDE = "endInclude"
	SETTING = "setting"
	SETTINGS_SECTION = "settingsSection"

	def t2tRegex(self) -> re.Pattern:
		return re.compile(rf"%kc:({self.value}.*)")


class Regex(Enum):
	COMMAND = re.compile(r"^<!-- KC:(?P<cmd>[^:\s]+)(?:: (?P<arg>.*))? -->$")
	HEADING = re.compile(r"^(?P<id>#+)(?P<txt>.*)$")
	SETTING_SINGLE_KEY = re.compile(r"^[^|]+?[:：]\s*(.+?)\s*$")
	TABLE_ROW = re.compile(r"^(\|.*\|)$")


class KeyCommandsError(Exception):
	"""Raised due to an error encountered in the User Guide related to generation of the Key Commands document.
	"""


class KeyCommandsExtension(Extension):
	# Magic number, priorities are not well documented.
	# It's unclear what the range of priorities are to compare to, but 25 seems to work, 1 doesn't.
	# See https://python-markdown.github.io/extensions/api/#registries
	PRIORITY = 25

	def extendMarkdown(self, md: Markdown):
		md.preprocessors.register(KeyCommandsPreprocessor(md), 'key_commands', self.PRIORITY)


class KeyCommandsPreprocessor(Preprocessor):
	def __init__(self, md: Markdown | None):
		super().__init__(md)
		self.initialize()

	def initialize(self):
		self._ugLines: Iterator[str] = iter(())
		self._kcLines: list[str] = []
		#: The current section of the key commands file.
		self._kcSect: Section = Section.HEADER
		#: The current stack of headings.
		self._headings: list[re.Match] = []
		#: The 0 based level of the last heading in L{_headings} written to the key commands file.
		self._kcLastHeadingLevel: int = -1
		#: Whether lines which aren't commands should be written to the key commands file as is.
		self._kcInclude: bool = False
		#: The header row for settings sections.
		self._settingsHeaderRow: str | None = None
		#: The number of layouts for settings in a settings section.
		self._settingsNumLayouts: int = 0
		#: The current line number being processed, used to present location of syntax errors
		self._lineNum: int = 0
		# We want to skip the title line to replace it with the KC:TITLE command argument.
		self._skippedTitle = False

	def run(self, lines: list[str]) -> list[str]:
		# Turn this into an iterator so we can use next() to seek through lines.
		self._ugLines = iter(lines)
		for line in self._ugLines:
			line = line.strip()
			self._lineNum += 1

			# We want to skip the title line to replace it with the KC:TITLE command argument.
			if line.startswith("# ") and not self._skippedTitle:
				self._skippedTitle = True
				continue

			m = Regex.COMMAND.value.match(line)
			if m:
				self._command(**m.groupdict())
				continue

			m = Regex.HEADING.value.match(line)
			if m:
				self._heading(m)
				continue

			if self._kcInclude:
				self._kcLines.append(line)

		return self._kcLines.copy()

	def _command(self, cmd: Command | None = None, arg: str | None = None):
		# Handle header commands.
		if cmd == Command.TITLE.value:
			if self._kcSect > Section.HEADER:
				raise KeyCommandsError(f"{self._lineNum}, title command is not valid here")
			# Write the title and two blank lines to complete the txt2tags header section.
			self._kcLines.append("# " + arg + LINE_END * 2)
			self._kcSect = Section.BODY
			return

		elif self._kcSect == Section.HEADER:
			raise KeyCommandsError(f"{self._lineNum}, title must be the first command")

		if cmd == Command.BEGIN_INCLUDE.value:
			self._writeHeadings()
			self._kcInclude = True
		elif cmd == Command.END_INCLUDE.value:
			self._kcInclude = False
			self._kcLines.append("")

		elif cmd == Command.SETTINGS_SECTION.value:
			# The argument is the table header row for the settings section.
			# Replace t2t header syntax with markdown syntax.
			self._settingsHeaderRow = arg.replace("||", "|")
			# There are name and description columns.
			# Each of the remaining columns provides keystrokes for one layout.
			# There's one less delimiter than there are columns, hence subtracting 1 instead of 2.
			self._settingsNumLayouts = arg.strip("|").count("|") - 1
			if self._settingsNumLayouts < 1:
				raise KeyCommandsError(
					f"{self._lineNum}, settingsSection command must specify the header row for a table"
					" summarising the settings"
				)

		elif cmd == Command.SETTING.value:
			self._handleSetting()

		else:
			raise KeyCommandsError(f"{self._lineNum}, Invalid command {cmd}")

	def _seekNonEmptyLine(self) -> str:
		"""Seeks to the next non-empty line in the user guide.
		"""
		line = next(self._ugLines).strip()
		self._lineNum += 1
		while not line:
			try:
				line = next(self._ugLines).strip()
			except StopIteration:
				return line
			self._lineNum += 1
		return line

	def _areHeadingsPending(self) -> bool:
		return self._kcLastHeadingLevel < len(self._headings) - 1

	def _writeHeadings(self):
		level = self._kcLastHeadingLevel + 1
		# Only write headings we haven't yet written.
		for level, heading in enumerate(self._headings[level:], level):
			self._kcLines.append(heading.group(0))
		self._kcLastHeadingLevel = level

	def _heading(self, m: re.Match):
		# We work with 0 based heading levels.
		level = len(m.group("id")) - 1
		try:
			del self._headings[level:]
		except IndexError:
			pass
		self._headings.append(m)
		self._kcLastHeadingLevel = min(self._kcLastHeadingLevel, level - 1)

	def _handleSetting(self):
		if not self._settingsHeaderRow:
			raise KeyCommandsError("%d, setting command cannot be used before settingsSection command" % self._lineNum)

		if self._areHeadingsPending():
			# There are new headings to write.
			# If there was a previous settings table, it ends here, so write a blank line.
			self._kcLines.append("")
			self._writeHeadings()
			# New headings were written, so we need to output the header row.
			self._kcLines.append(self._settingsHeaderRow)
			numCols = self._settingsNumLayouts + 2  # name + description + layouts
			self._kcLines.append("|" + "---|" * numCols)

		# The next line should be a heading which is the name of the setting.
		line = self._seekNonEmptyLine()
		m = Regex.HEADING.value.match(line)
		if not m:
			raise KeyCommandsError(f"{self._lineNum}, setting command must be followed by heading")
		name = m.group("txt")

		# The next few lines should be table rows for each layout.
		# Alternatively, if the key is common to all layouts,
		# there will be a single line of text specifying the key after a colon.
		keys: list[str] = []
		for _layout in range(self._settingsNumLayouts):
			line = self._seekNonEmptyLine()

			m = Regex.SETTING_SINGLE_KEY.value.match(line)
			if m:
				keys.append(m.group(1))
				break
			elif not Regex.TABLE_ROW.value.match(line):
				raise KeyCommandsError(
					f"{self._lineNum}, setting command: "
					"There must be one table row for each keyboard layout"
				)

			# This is a table row.
			# The key will be the second column.
			try:
				key = line.strip("|").split("|")[1].strip()
			except IndexError:
				raise KeyCommandsError(f"{self._lineNum}, setting command: Key entry not found in table row.")
			else:
				keys.append(key)

		if 1 == len(keys) < self._settingsNumLayouts:
			# The key has only been specified once, so it is the same in all layouts.
			key = keys[0]
			keys[1:] = (key for _layout in range(self._settingsNumLayouts - 1))

		# There should now be a blank line.
		line = next(self._ugLines).strip()
		self._lineNum += 1
		if line:
			raise KeyCommandsError(
				f"{self._lineNum}, setting command: The keyboard shortcuts must be followed by a blank line. "
				"Multiple keys must be included in a table. "
				f"Erroneous key: {key}"
			)

		# Finally, the next line should be the description.
		desc = self._seekNonEmptyLine()
		self._kcLines.append(f"| {name} | {' | '.join(keys)} | {desc} |")
		if not self._kcLines[-2].startswith("|"):
			# The previous line was not a table, so this is a new table.
			# Write the header row.
			numCols = len(keys) + 2  # name + description + layouts
			self._kcLines.append("|" + "---|" * numCols)
