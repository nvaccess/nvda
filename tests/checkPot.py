# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017-2023 NV Access Limited, Ethan Holliger, Dinesh Kaushal, Leonard de Ruijter,
# Joseph Lee, Julien Cochuyt, Łukasz Golonka, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Check a translation template (pot) for strings without translator comments."""

import sys
from typing import Set


# Existing messages that we know don't have translator comments yet.
# Ideally, all of these should get translator comments,
# but this is not realistic right now.
# A message should be removed from here once a translator comment is added for it.
# Note that checkPot will fail with an unexpected success
# if a translator comment is found for one of these messages.
EXPECTED_MESSAGES_WITHOUT_COMMENTS = {
	"border",
	"filler",
	"line",
	"data item",
	"header item",
	"calendar",
	"video",
	"audio",
	"modal",
	"iconified",
	"editable",
	"checkable",
	"draggable",
	"dragging",
	"sorted",
	"sorted ascending",
	"sorted descending",
	"gesture map File Error",
	"Type help(object) to get help about object.",
	"Type exit() to exit the console",
	"NVDA Python Console",
	"Emulates pressing %s on the system keyboard",
	"continuous section break",
	"new column section break",
	"new page section break",
	"even pages section break",
	"odd pages section break",
	"column break",
	"background pattern {pattern}",
	"NVDA Speech Viewer",
	"text mode",
	"object mode",
	"NonVisual Desktop Access",
	"A free and open source screen reader for Microsoft Windows",
	"Copyright (C) {years} NVDA Contributors",
	"Display",
	"left",
	"right",
	"Error renaming profile.",
	"Use this profile for:",
	"This change requires administrator privileges.",
	"Insufficient Privileges",
	"word",
	"Taskbar",
	"invoke",
	"Desktop",
	"Input Message is {title}: {message}",
	"Input Message is {message}",
	"Comments",
	"Endnotes",
	"Even pages footer",
	"Even pages header",
	"First page footer",
	"First page header",
	"Footnotes",
	"Primary footer",
	"Primary header",
	"Text frame",
	# core.py:87
	r'Your gesture map file contains errors.\n"More details about the errors can be found in the log file."',
}


def checkPot(fileName):
	"""Returns the number of errors.
	Also prints error messages and a summary to standard output.
	"""
	# This function reads a gettext translation template (pot) line by line,
	# parsing only the content it needs.
	# See this link for info about the format of gettext translation files:
	# https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html
	errors = 0
	expectedErrors = 0
	unexpectedSuccesses = 0
	foundMessagesWithOutComments: Set[str] = set()
	with open(fileName, "rt", encoding="utf-8") as pot:
		passedHeader = False
		for line in pot:
			line = line.rstrip()
			if not line:
				# End of message.
				hasComment = False
				sourceLines = []
				context = ""
				continue
			if line == 'msgid ""' and not passedHeader:
				# The first msgid in POT files is expected to be empty, and considered part of the header.
				# Once it has been passed, any subsequent empty msgid marks the start of a long msgid split
				# accross multiple lines.
				passedHeader = True
				continue
			if line.startswith("#. Translators: "):
				# This is a comment for translators.
				# Example: "#. Translators: a message reported in the SetRowHeader script for Microsoft Word."
				hasComment = True
				continue
			if line.startswith("#: "):
				# This specifies the files and line numbers where this message was found.
				# Example: "#: NVDAObjects\window\winword.py:1322"
				# Strip the "#: " prefix (3 chars).
				sourceLines.append(line[3:])
				continue
			if line.startswith('msgctxt "'):
				# This is the context used to disambiguate messages.
				context = getStringFromLine(line)
				continue
			if line.startswith("msgid "):
				# This is the untranslated message.
				# Get the message.
				if line == 'msgid ""':
					# Long msgid, split across multiple lines.
					# Subsequent lines are just quoted strings which should be concatenated.
					# Example:
					# 	msgid ""
					# 	"Toggles single letter navigation on and off. When on, single letter keys in "
					# 	"browse mode jump to various kinds of elements on the page. When off, these "
					# 	"keys are passed to the application"
					msgid = ""
					for line in pot:
						if line.startswith("msgstr "):
							# This begins the translated message, so msgid has ended.
							break
						msgid += getStringFromLine(line)
				else:
					# Short msgid, presented on a single line.
					# Example: msgid "Secure Desktop"
					msgid = getStringFromLine(line)
				if context:
					# The context must be considered as part of the message.
					message = "[{context}] {msgid}".format(context=context, msgid=msgid)
				else:
					message = msgid
				isExpectedError = message in EXPECTED_MESSAGES_WITHOUT_COMMENTS
				if isExpectedError:
					foundMessagesWithOutComments.add(message)
				if not hasComment and isExpectedError:
					expectedErrors += 1
					continue
				if hasComment and isExpectedError:
					error = (
						"Message has translator comment, but one wasn't expected.\n"
						"This is good, but please remove from EXPECTED_MESSAGES_WITHOUT_COMMENTS in tests/checkPot.py"
					)
					unexpectedSuccesses += 1
				elif not hasComment:
					errors += 1
					error = "Message has no translator comment."
				else:
					continue
				print(
					"{error}\nSource lines: {lines}\nMessage: {message}\n".format(
						error=error,
						lines=" ".join(sourceLines),
						message=message,
					),
					file=sys.stderr,
				)
				continue
	removedTranslatableMessages = EXPECTED_MESSAGES_WITHOUT_COMMENTS - foundMessagesWithOutComments
	if removedTranslatableMessages:
		print(
			"The following messages are no longer present in the source code "
			"and should be removed from `EXPECTED_MESSAGES_WITHOUT_COMMENTS`:",
			file=sys.stderr,
		)
		print("\n".join(removedTranslatableMessages), file=sys.stderr)
	print(
		f"{errors} errors, {unexpectedSuccesses} unexpected successes, {expectedErrors} expected errors, "
		f"{len(removedTranslatableMessages)} messages marked as expected errors not present in the source code",
		file=sys.stderr,
	)
	return errors + unexpectedSuccesses + len(removedTranslatableMessages)


def getStringFromLine(line):
	if line.startswith('"'):
		# The quoted string begins at the start of the line.
		quoted = line
	else:
		# The quoted string starts after a command.
		# Example: msgid "Secure Desktop"
		quoted = line.split(" ", 1)[1]
	# Strip the quotes.
	return quoted[1:-1]


if __name__ == "__main__":
	# Support command line usage for quick testing.
	fileName = sys.argv[1]
	print(checkPot(fileName))
