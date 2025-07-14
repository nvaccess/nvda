# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2014-2025 NV Access Limited, James Teh
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Utilities to check a gettext po file for errors."""

import codecs
import re
import subprocess
import sys

MSGFMT = r"miscDeps\\tools\\msgfmt.exe" if sys.platform == "win32" else "msgfmt"


class PoChecker:
	"""Checks a po file for errors not detected by msgfmt.
	This first runs msgfmt to check for syntax errors.
	It then checks for mismatched Python percent and brace interpolations.
	Construct an instance and call the L{check} method.
	"""

	FUZZY = "#, fuzzy"
	MSGID = "msgid"
	MSGID_PLURAL = "msgid_plural"
	MSGSTR = "msgstr"

	def __init__(self, po: str):
		"""Constructor.
		:param po: The path to the po file to check.
		"""
		self._poPath = po
		with codecs.open(po, "r", "utf-8") as file:
			self._poContent = file.readlines()
		self._string: str | None = None

		self.alerts: list[str] = []
		"""List of error and warning messages found in the po file."""

		self.hasSyntaxError: bool = False
		"""Whether there is a syntax error in the po file."""

		self.warningCount: int = 0
		"""Number of warnings found."""

		self.errorCount: int = 0
		"""Number of errors found."""

	def _addToString(self, line: list[str], startingCommand: str | None = None) -> None:
		"""Helper function to add a line to the current string.
		:param line: The line to add.
		:param startingCommand: The command that started this string, if any.
			This is used to determine whether to strip the command and quotes.
		"""
		if startingCommand:
			# Strip the command and the quotes.
			self._string = line[len(startingCommand) + 2 : -1]
		else:
			# Strip the quotes.
			self._string += line[1:-1]

	def _finishString(self) -> str:
		"""Helper function to finish the current string.
		:return: The finished string.
		"""
		string = self._string
		self._string = None
		return string

	def _messageAlert(self, alert: str, isError: bool = True) -> None:
		"""Helper function to add an alert about a message.
		:param alert: The alert message.
		:param isError: Whether this is an error or a warning.
		"""
		if self._fuzzy:
			# Fuzzy messages don't get used, so this shouldn't be considered an error.
			isError = False
		if isError:
			self.errorCount += 1
		else:
			self.warningCount += 1
		if self._fuzzy:
			msgType = "Fuzzy message"
		else:
			msgType = "Message"
		self.alerts.append(
			f"{msgType} starting on line {self._messageLineNum}\n"
			f'Original: "{self._msgid}"\n'
			f'Translated: "{self._msgstr[-1]}"\n'
			f"{'Error' if isError else 'Warning'}: {alert}",
		)

	def _checkSyntax(self) -> None:
		"""Check the syntax of the po file using msgfmt.
		This will set the hasSyntaxError attribute to True if there is a syntax error.
		"""
		result = subprocess.run(
			(MSGFMT, "-o", "-", self._poPath),
			stdout=subprocess.DEVNULL,
			stderr=subprocess.PIPE,
			text=True,  # Ensures stderr is a text stream
		)
		if result.returncode != 0:
			output = result.stderr.rstrip().replace("\r\n", "\n")
			self.alerts.append(output)
			self.hasSyntaxError = True
			self.errorCount = 1

	def _checkMessages(self) -> None:
		command = None
		self._msgid = None
		self._msgid_plural = None
		self._msgstr = None
		nextFuzzy = False
		self._fuzzy = False
		for lineNum, line in enumerate(self._poContent, 1):
			line = line.strip()
			if line.startswith(self.FUZZY):
				nextFuzzy = True
				continue
			elif line.startswith(self.MSGID) and not line.startswith(self.MSGID_PLURAL):
				# New message.
				if self._msgstr is not None:
					self._msgstr[-1] = self._finishString()
					# Check the message we just handled.
					self._checkMessage()
				command = self.MSGID
				start = command
				self._messageLineNum = lineNum
				self._fuzzy = nextFuzzy
				nextFuzzy = False
			elif line.startswith(self.MSGID_PLURAL):
				self._msgid = self._finishString()
				command = self.MSGID_PLURAL
				start = command
			elif line.startswith(self.MSGSTR):
				self._handleMsgStrReaching(lastCommand=command)
				command = self.MSGSTR
				start = line[: line.find(" ")]
			elif line.startswith('"'):
				# Continuing a string.
				start = None
			else:
				# This line isn't of interest.
				continue
			self._addToString(line, startingCommand=start)
		if command == self.MSGSTR:
			# Handle the last message.
			self._msgstr[-1] = self._finishString()
			self._checkMessage()

	def _handleMsgStrReaching(self, lastCommand: str) -> None:
		"""Helper function used by _checkMessages to handle the required processing when reaching a line
		starting with "msgstr".
		:param lastCommand: the current command just before the msgstr line is reached.
		"""

		# Finish the string of the last command and check the message if it was an msgstr
		if lastCommand == self.MSGID:
			self._msgid = self._finishString()
		elif lastCommand == self.MSGID_PLURAL:
			self._msgid_plural = self._finishString()
		elif lastCommand == self.MSGSTR:
			self._msgstr[-1] = self._finishString()
			self._checkMessage()
		else:
			raise RuntimeError(f"Unexpected command before line {self._messageLineNum}: {lastCommand}")

		# For first msgstr create the msgstr list
		if lastCommand != self.MSGSTR:
			self._msgstr = []

		# Initiate the string for the current msgstr
		self._msgstr.append("")

	def check(self) -> bool:
		"""Check the file.
		Once this returns, you can call getReport to obtain a report.
		This method should not be called more than once.
		:return: True if the file is okay, False if there were problems.
		"""
		self._checkSyntax()
		if self.alerts:
			return False
		self._checkMessages()
		if self.alerts:
			return False
		return True

	RE_UNNAMED_PERCENT = re.compile(r"(?<!%)%[.\d]*[a-zA-Z]")
	RE_NAMED_PERCENT = re.compile(r"(?<!%)%\([^(]+\)[.\d]*[a-zA-Z]")
	RE_FORMAT = re.compile(r"(?<!{){([^{}:]+):?[^{}]*}")

	def _getInterpolations(self, text: str) -> tuple[list[str], set[str], set[str]]:
		"""Get the percent and brace interpolations in a string.
		:param text: The text to check.
		:return: A tuple of three sets:
			- unnamed percent interpolations (e.g. %s, %d)
			- named percent interpolations (e.g. %(name)s)
			- brace format interpolations (e.g. {name}, {name:format})
		"""
		unnamedPercent = self.RE_UNNAMED_PERCENT.findall(text)
		namedPercent = set(self.RE_NAMED_PERCENT.findall(text))
		formats = set()
		for m in self.RE_FORMAT.finditer(text):
			if not m.group(1):
				self._messageAlert("Unspecified positional argument in brace format")
			formats.add(m.group(0))
		return unnamedPercent, namedPercent, formats

	def _formatInterpolations(
		self,
		unnamedPercent: list[str],
		namedPercent: set[str],
		formats: set[str],
	) -> str:
		"""Format the interpolations for display in an error message.
		:param unnamedPercent: The unnamed percent interpolations.
		:param namedPercent: The named percent interpolations.
		:param formats: The brace format interpolations.
		"""
		out: list[str] = []
		if unnamedPercent:
			out.append(f"unnamed percent interpolations in this order: {unnamedPercent}")
		if namedPercent:
			out.append(f"these named percent interpolations: {namedPercent}")
		if formats:
			out.append(f"these brace format interpolations: {formats}")
		if not out:
			return "no interpolations"
		return "\n\tAnd ".join(out)

	def _checkMessage(self) -> None:
		idUnnamedPercent, idNamedPercent, idFormats = self._getInterpolations(self._msgid)
		if not self._msgstr[-1]:
			return
		strUnnamedPercent, strNamedPercent, strFormats = self._getInterpolations(self._msgstr[-1])
		error = False
		alerts = []
		if idUnnamedPercent != strUnnamedPercent:
			if idUnnamedPercent:
				alerts.append("unnamed percent interpolations differ")
				error = True
			else:
				alerts.append("unexpected presence of unnamed percent interpolations")
		if idNamedPercent - strNamedPercent:
			alerts.append("missing named percent interpolation")
		if strNamedPercent - idNamedPercent:
			if idNamedPercent:
				alerts.append("extra named percent interpolation")
				error = True
			else:
				alerts.append("unexpected presence of named percent interpolations")
		if idFormats - strFormats:
			alerts.append("missing brace format interpolation")
		if strFormats - idFormats:
			if idFormats:
				alerts.append("extra brace format interpolation")
				error = True
			else:
				alerts.append("unexpected presence of brace format interpolations")
		if alerts:
			self._messageAlert(
				f"{', '.join(alerts)}\n"
				f"Expected: {self._formatInterpolations(idUnnamedPercent, idNamedPercent, idFormats)}\n"
				f"Got: {self._formatInterpolations(strUnnamedPercent, strNamedPercent, strFormats)}",
				isError=error,
			)

	def getReport(self) -> str | None:
		"""Get a text report about any errors or warnings.
		:return: The text or None if there were no problems.
		"""
		if not self.alerts:
			return None
		report = f"File {self._poPath}: "
		if self.hasSyntaxError:
			report += "syntax error"
		else:
			if self.errorCount:
				msg = "error" if self.errorCount == 1 else "errors"
				report += f"{self.errorCount} {msg}"
			if self.warningCount:
				if self.errorCount:
					report += ", "
				msg = "warning" if self.warningCount == 1 else "warnings"
				report += f"{self.warningCount} {msg}"
		report += "\n\n" + "\n\n".join(self.alerts)
		return report


def main():
	if len(sys.argv) <= 1:
		sys.exit("Usage: [poChecker.py] <po file> [<po file> ...]")
	exitCode = 0
	for filename in sys.argv[1:]:
		c = PoChecker(filename)
		if not c.check():
			report = c.getReport() + "\n\n"
			encoding = "cp1252" if sys.platform == "win32" else "utf-8"
			print(report.encode(encoding, errors="backslashreplace").decode("utf-8", errors="backslashreplace"))
		if c.errorCount > 0:
			exitCode = 1
	return exitCode


if __name__ == "__main__":
	sys.exit(main())
