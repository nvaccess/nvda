import os
from io import StringIO
from typing import Tuple

import addonAPIVersion
import languageHandler
from configobj import ConfigObj
from configobj.validate import Validator
from logHandler import log
from six import string_types


class AddonManifest(ConfigObj):
	"""Add-on manifest file. It contains metadata about an NVDA add-on package."""

	configspec = ConfigObj(
		StringIO(
			"""
# NVDA Add-on Manifest configuration specification
# Add-on unique name
# Suggested convention is lowerCamelCase.
name = string()

# short summary (label) of the add-on to show to users.
summary = string()

# Long description with further information and instructions
description = string(default=None)

# Name of the author or entity that created the add-on
author = string()

# Version of the add-on.
# Suggested convention is <major>.<minor>.<patch> format.
version = string()

# The minimum required NVDA version for this add-on to work correctly.
# Should be less than or equal to lastTestedNVDAVersion
minimumNVDAVersion = apiVersion(default="0.0.0")

# Must be greater than or equal to minimumNVDAVersion
lastTestedNVDAVersion = apiVersion(default="0.0.0")

# URL for more information about the add-on, e.g. a homepage.
# Should begin with https://
url = string(default=None)

# Name of default documentation file for the add-on.
docFileName = string(default=None)

# Custom braille tables
[brailleTables]
	# The key is the table file name (not the full path)
	[[__many__]]
		displayName = string()
		contracted = boolean(default=false)
		input = boolean(default=true)
		output = boolean(default=true)

# Symbol Pronunciation
[symbolDictionaries]
	# The key is the symbol dictionary file name (not the full path)
	[[__many__]]
		displayName = string()
		mandatory = boolean(default=false)

# NOTE: apiVersion:
# EG: 2019.1.0 or 0.0.0
# Must have 3 integers separated by dots.
# The first integer must be a Year (4 characters)
# "0.0.0" is also valid.
# The final integer can be left out, and in that case will default to 0. E.g. 2019.1

""",
		),
	)

	def __init__(self, input, translatedInput=None):
		"""Constructs an L{AddonManifest} instance from manifest string data
		@param input: data to read the manifest information
		@type input: a fie-like object.
		@param translatedInput: translated manifest input
		@type translatedInput: file-like object
		"""
		super().__init__(input, configspec=self.configspec, encoding="utf-8", default_encoding="utf-8")
		self._errors = None
		val = Validator({"apiVersion": validate_apiVersionString})
		result = self.validate(val, copy=True, preserve_errors=True)
		if result != True:  # noqa: E712
			self._errors = result
		elif True != self._validateApiVersionRange():  # noqa: E712
			self._errors = "Constraint not met: minimumNVDAVersion ({}) <= lastTestedNVDAVersion ({})".format(
				self.get("minimumNVDAVersion"),
				self.get("lastTestedNVDAVersion"),
			)
		self._translatedConfig = None
		if translatedInput is not None:
			self._translatedConfig = ConfigObj(translatedInput, encoding="utf-8", default_encoding="utf-8")
			for k in ("summary", "description"):
				val = self._translatedConfig.get(k)
				if val:
					self[k] = val
			for fileName, tableConfig in self._translatedConfig.get("brailleTables", {}).items():
				value = tableConfig.get("displayName")
				if value:
					self["brailleTables"][fileName]["displayName"] = value
			for fileName, dictConfig in self._translatedConfig.get("symbolDictionaries", {}).items():
				value = dictConfig.get("displayName")
				if value:
					self["symbolDictionaries"][fileName]["displayName"] = value

	@property
	def errors(self):
		return self._errors

	def _validateApiVersionRange(self):
		lastTested = self.get("lastTestedNVDAVersion")
		minRequiredVersion = self.get("minimumNVDAVersion")
		return minRequiredVersion <= lastTested


def _report_manifest_errors(manifest):
	log.warning("Error loading manifest:\n%s", manifest.errors)


def validate_apiVersionString(value: str) -> Tuple[int, int, int]:
	"""
	@raises: configobj.validate.ValidateError on validation error
	"""
	from configobj.validate import ValidateError

	if not value or value == "None":
		return (0, 0, 0)
	if not isinstance(value, string_types):
		raise ValidateError('Expected an apiVersion in the form of a string. EG "2019.1.0"')
	try:
		return addonAPIVersion.getAPIVersionTupleFromString(value)
	except ValueError as e:
		raise ValidateError('"{}" is not a valid API Version string: {}'.format(value, e))


MANIFEST_FILENAME = "manifest.ini"


def _translatedManifestPaths(lang=None, forBundle=False):
	if lang is None:
		lang = languageHandler.getLanguage()  # can't rely on default keyword arguments here.
	langs = [lang]
	if "_" in lang:
		langs.append(lang.split("_")[0])
		if lang != "en" and not lang.startswith("en_"):
			langs.append("en")
	sep = "/" if forBundle else os.path.sep
	return [sep.join(("locale", lang, MANIFEST_FILENAME)) for lang in langs]
