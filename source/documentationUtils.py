# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Łukasz Golonka, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from functools import lru_cache
import os

import markdown
import nh3

import globalVars
from gui import blockAction
import languageHandler
import NVDAState
from logHandler import log
import ui
import queueHandler
import wx


def getDocFilePath(fileName: str, localized: bool = True) -> str | None:
	if not getDocFilePath.rootPath:
		if NVDAState.isRunningAsSource():
			getDocFilePath.rootPath = os.path.join(globalVars.appDir, "..", "user_docs")
		else:
			getDocFilePath.rootPath = os.path.join(globalVars.appDir, "documentation")

	if localized:
		lang = languageHandler.getLanguage()
		tryLangs = [lang]
		if "_" in lang:
			# This locale has a sub-locale, but documentation might not exist for the sub-locale, so try stripping it.
			tryLangs.append(lang.split("_")[0])
		# If all else fails, use English.
		tryLangs.append("en")

		fileName, fileExt = os.path.splitext(fileName)
		for tryLang in tryLangs:
			tryDir = os.path.join(getDocFilePath.rootPath, tryLang)
			if not os.path.isdir(tryDir):
				continue

			tryPath = os.path.join(tryDir, f"{fileName}.html")
			if os.path.isfile(tryPath):
				return tryPath
		return None
	else:
		# Not localized.
		if NVDAState.isRunningAsSource() and fileName == "copying.txt":
			# If running from source, this file is in the root dir.
			return os.path.join(globalVars.appDir, "..", fileName)
		else:
			return os.path.join(getDocFilePath.rootPath, fileName)


getDocFilePath.rootPath = None


def reportNoDocumentation(fileName: str, useMsgBox: bool = False) -> None:
	# Translators: Message reported upon action (e.g. context sensitive help, open documentation from NVDA menu)
	noDocMessage = _("No documentation found.")
	log.debugWarning(
		f"Documentation not found ({fileName}): possible cause - running from source without building user docs.",
	)
	if useMsgBox:
		# Import late to avoid circular impoort.
		from gui.message import messageBox

		messageBox(
			noDocMessage,
			# Translators: the title of an error message dialog
			_("Error"),
			wx.OK | wx.ICON_ERROR,
		)
	else:
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, noDocMessage)


@lru_cache(maxsize=1)
def _getSanitizedHtmlLicense() -> str:
	licenseFilename: str = getDocFilePath("copying.txt", False)
	with open(licenseFilename, "r", encoding="utf-8") as licenseFile:
		htmlLicense = markdown.markdown(licenseFile.read())
	return nh3.clean(htmlLicense)


@blockAction.when(
	# HTML includes links which shouldn't be accessible
	# in secure contexts as it opens a browser.
	blockAction.Context.SECURE_MODE,
)
def displayLicense():
	ui.browseableMessage(
		_getSanitizedHtmlLicense(),
		# Translators: The title of the dialog to show the NVDA License.
		_("NVDA License"),
		isHtml=True,
	)
