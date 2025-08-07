# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import argparse
import sys
import winUser

from typing import IO


class _WideParserHelpFormatter(argparse.RawTextHelpFormatter):
	def __init__(self, prog: str, indent_increment: int = 2, max_help_position: int = 50, width: int = 1000):
		"""
		A custom formatter for argparse help messages that uses a wider width.
		:param prog: The program name.
		:param indent_increment: The number of spaces to indent for each level of nesting.
		:param max_help_position: The maximum starting column of the help text.
		:param width: The width of the help text.
		"""

		super().__init__(prog, indent_increment, max_help_position, width)


class NoConsoleOptionParser(argparse.ArgumentParser):
	"""
	A commandline option parser that shows its messages using dialogs,
	as this pyw file has no dos console window associated with it.
	"""

	def print_help(self, file: IO[str] | None = None):
		"""Shows help in a standard Windows message dialog"""
		winUser.MessageBox(0, self.format_help(), "Help", 0)

	def error(self, message: str):
		"""Shows an error in a standard Windows message dialog, and then exits NVDA"""
		out = ""
		out = self.format_usage()
		out += f"\nerror: {message}"
		winUser.MessageBox(0, out, "Command-line Argument Error", winUser.MB_ICONERROR)
		sys.exit(2)


def stringToBool(string):
	"""Wrapper for configobj.validate.is_boolean to raise the proper exception for wrong values."""
	from configobj.validate import is_boolean, ValidateError

	try:
		return is_boolean(string)
	except ValidateError as e:
		raise argparse.ArgumentTypeError(e.message)


def stringToLang(value: str) -> str:
	"""Perform basic case normalization for ease of use."""
	import languageHandler

	if value.casefold() == "Windows".casefold():
		normalizedLang = "Windows"
	else:
		normalizedLang = languageHandler.normalizeLanguage(value)
	possibleLangNames = languageHandler.listNVDALocales()
	if normalizedLang is not None and normalizedLang in possibleLangNames:
		return normalizedLang
	raise argparse.ArgumentTypeError(f"Language code should be one of:\n{', '.join(possibleLangNames)}.")


_parser: NoConsoleOptionParser | None = None
"""The arguments parser used by NVDA.
"""


def _createNVDAArgParser() -> NoConsoleOptionParser:
	"""Create a parser to process NVDA option arguments."""

	parser = NoConsoleOptionParser(formatter_class=_WideParserHelpFormatter, allow_abbrev=False)
	quitGroup = parser.add_mutually_exclusive_group()
	quitGroup.add_argument(
		"-q",
		"--quit",
		action="store_true",
		dest="quit",
		default=False,
		help="Quit already running copy of NVDA",
	)
	parser.add_argument(
		"-k",
		"--check-running",
		action="store_true",
		dest="check_running",
		default=False,
		help="Report whether NVDA is running via the exit code; 0 if running, 1 if not running",
	)
	parser.add_argument(
		"-f",
		"--log-file",
		dest="logFileName",
		type=str,
		help="The file to which log messages should be written.\n"
		'Default destination is "%%TEMP%%\\nvda.log".\n'
		"Logging is always disabled if secure mode is enabled.\n",
	)
	parser.add_argument(
		"-l",
		"--log-level",
		dest="logLevel",
		type=int,
		default=0,  # 0 means unspecified in command line.
		choices=[10, 12, 15, 20, 100],
		help="The lowest level of message logged (debug 10, input/output 12, debugwarning 15, info 20, off 100).\n"
		"Default value is 20 (info) or the user configured setting.\n"
		"Logging is always disabled if secure mode is enabled.\n",
	)
	parser.add_argument(
		"-c",
		"--config-path",
		dest="configPath",
		default=None,
		type=str,
		help="The path where all settings for NVDA are stored.\n"
		"The default value is forced if secure mode is enabled.\n",
	)
	parser.add_argument(
		"-n",
		"--lang",
		dest="language",
		default=None,
		type=stringToLang,
		help=(
			"Override the configured NVDA language.\n"
			'Set to "Windows" for current user default, "en" for English, etc.'
		),
	)
	parser.add_argument(
		"-m",
		"--minimal",
		action="store_true",
		dest="minimal",
		default=False,
		help="No sounds, no interface, no start message etc",
	)
	# --secure is used to force secure mode.
	# Documented in the userGuide in #SecureMode.
	parser.add_argument(
		"-s",
		"--secure",
		action="store_true",
		dest="secure",
		default=False,
		help="Starts NVDA in secure mode",
	)
	parser.add_argument(
		"-d",
		"--disable-addons",
		action="store_true",
		dest="disableAddons",
		default=False,
		help="Disable all add-ons",
	)
	parser.add_argument(
		"--debug-logging",
		action="store_true",
		dest="debugLogging",
		default=False,
		help="Enable debug level logging just for this run.\n"
		"This setting will override any other log level (--loglevel, -l) argument given, "
		"as well as no logging option.",
	)
	parser.add_argument(
		"--no-logging",
		action="store_true",
		dest="noLogging",
		default=False,
		help="Disable logging completely for this run.\n"
		"This setting can be overwritten with other log level (--loglevel, -l) "
		"switch or if debug logging is specified.",
	)
	parser.add_argument(
		"--no-sr-flag",
		action="store_false",
		dest="changeScreenReaderFlag",
		default=True,
		help="Don't change the global system screen reader flag",
	)
	installGroup = parser.add_mutually_exclusive_group()
	installGroup.add_argument(
		"--install",
		action="store_true",
		dest="install",
		default=False,
		help="Installs NVDA (starting the new copy after installation)",
	)
	installGroup.add_argument(
		"--install-silent",
		action="store_true",
		dest="installSilent",
		default=False,
		help="Installs NVDA silently (does not start the new copy after installation).",
	)
	installGroup.add_argument(
		"--create-portable",
		action="store_true",
		dest="createPortable",
		default=False,
		help="Creates a portable copy of NVDA (and starts the new copy).\n"
		"Requires `--portable-path` to be specified.\n",
	)
	installGroup.add_argument(
		"--create-portable-silent",
		action="store_true",
		dest="createPortableSilent",
		default=False,
		help="Creates a portable copy of NVDA (without starting the new copy).\n"
		"This option suppresses warnings when writing to non-empty directories "
		"and may overwrite files without warning.\n"
		"Requires --portable-path to be specified.\n",
	)
	parser.add_argument(
		"--portable-path",
		dest="portablePath",
		default=None,
		type=str,
		help="The path where a portable copy will be created",
	)
	parser.add_argument(
		"--launcher",
		action="store_true",
		dest="launcher",
		default=False,
		help="Started from the launcher",
	)
	parser.add_argument(
		"--enable-start-on-logon",
		metavar="True|False",
		type=stringToBool,
		dest="enableStartOnLogon",
		default=None,
		help="When installing, enable NVDA's start on the logon screen",
	)
	parser.add_argument(
		"--copy-portable-config",
		action="store_true",
		dest="copyPortableConfig",
		default=False,
		help=(
			"When installing, copy the portable configuration "
			"from the provided path (--config-path, -c) to the current user account"
		),
	)
	# This option is passed by Ease of Access so that if someone downgrades without uninstalling
	# (despite our discouragement), the downgraded copy won't be started in non-secure mode on secure desktops.
	# (Older versions always required the --secure option to start in secure mode.)
	# If this occurs, the user will see an obscure error,
	# but that's far better than a major security hazzard.
	# If this option is provided, NVDA will not replace an already running instance (#10179)
	parser.add_argument(
		"--ease-of-access",
		action="store_true",
		dest="easeOfAccess",
		default=False,
		help="Started by Windows Ease of Access",
	)
	return parser


def getParser() -> NoConsoleOptionParser:
	global _parser
	if not _parser:
		_parser = _createNVDAArgParser()
	return _parser
