#tests/checkPot.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""Check a translation template (pot) for strings without translator comments.
"""

import sys

# Existing messages that we know don't have translator comments yet.
# Ideally, all of these should get translator comments,
# but this is not realistic right now.
# A message should be removed from here once a translator comment is added for it.
# Note that checkPot will fail with an unexpected success
# if a translator comment is found for one of these messages.
EXPECTED_MESSAGES_WITHOUT_COMMENTS = {
	'%s landmark',
	'border',
	'filler',
	'line',
	'data item',
	'header item',
	'calendar',
	'video',
	'audio',
	'modal',
	'iconified',
	'editable',
	'checkable',
	'draggable',
	'dragging',
	'sorted',
	'sorted ascending',
	'sorted descending',
	'gesture map File Error',
	'text \\"%s\\" not found',
	'Find Error',
	'Selected %s',
	'on',
	'Type help(object) to get help about object.',
	'Type exit() to exit the console',
	'NVDA Python Console',
	'Emulates pressing %s on the system keyboard',
	'continuous section break',
	'new column section break',
	'new page section break',
	'even pages section break',
	'odd pages section break',
	'column break',
	'background pattern {pattern}',
	'NVDA Speech Viewer',
	'text mode',
	'object mode',
	'NonVisual Desktop Access',
	'A free and open source screen reader for Microsoft Windows',
	'Copyright (C) {years} NVDA Contributors',
	'Display',
	'Reports and moves the review cursor to a recent message',
	'left',
	'right',
	'Show the Handy Tech driver configuration window.',
	'Recognition failed',
	'General settings',
	'Change the synthesizer to be used',
	'Choose the voice, rate, pitch and volume to use',
	'Change reporting of mouse shape and object under mouse',
	'Configure how and when the review cursor moves',
	'Change reporting of objects',
	'Change virtual buffers specific settings',
	'Change settings of document properties',
	'NVDA &web site',
	'Reset all settings to saved state',
	'Reset all settings to default state',
	'Write the current configuration to nvda.ini',
	'E&xit',
	'Options',
	'Error renaming profile.',
	'Use this profile for:',
	'This change requires administrator privileges.',
	'Insufficient Privileges',
	'Synthesizer Error',
	'Dictionary Entry Error',
	'Could not load the %s display.',
	'Braille Display Error',
	'word',
	'Taskbar',
	'%s items',
	'invoke',
	'Desktop',
	'Input Message is {title}: {message}',
	'Input Message is {message}',
	'Series color: {colorName} ',
	'Comments',
	'Endnotes',
	'Even pages footer',
	'Even pages header',
	'First page footer',
	'First page header',
	'Footnotes',
	'Primary footer',
	'Primary header',
	'Text frame',
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
	with file(fileName, "rt") as pot:
		for line in pot:
			line = line.rstrip()
			if not line:
				# End of message.
				hasComment = False
				sourceLines = []
				context = ""
				continue
			if line == 'msgid ""':
				# Header.
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
					# Multi-line msgid.
					# Subsequent lines are just quoted strings which should be concatenated.
					msgid = ""
					for line in pot:
						if line.startswith("msgstr "):
							# This begins the translated message, so msgid has ended.
							break
						msgid += getStringFromLine(line)
				else:
					# Single line msgid.
					# Example: msgid "Secure Desktop"
					msgid = getStringFromLine(line)
				if context:
					# The context must be considered as part of the message.
					message = "[{context}] {msgid}".format(context=context, msgid=msgid)
				else:
					message = msgid
				isExpectedError = message in EXPECTED_MESSAGES_WITHOUT_COMMENTS
				if not hasComment and isExpectedError:
					expectedErrors += 1
					continue
				if hasComment and isExpectedError:
					error = ("Message has translator comment, but one wasn't expected.\n"
						"This is good, but please remove from EXPECTED_MESSAGES_WITHOUT_COMMENTS in tests/checkPot.py")
					unexpectedSuccesses += 1
				elif not hasComment:
					errors += 1
					error = "Message has no translator comment."
				else:
					continue
				print("{error}\n"
					"Source lines: {lines}\n"
					"Message: {message}\n"
					.format(error=error, lines=" ".join(sourceLines), message=message))
				continue
	print("{errors} errors, {unexpectedSuccesses} unexpected successes, {expectedErrors} expected errors"
		.format(errors=errors, unexpectedSuccesses=unexpectedSuccesses, expectedErrors=expectedErrors))
	return errors + unexpectedSuccesses

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
