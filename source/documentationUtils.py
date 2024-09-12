# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2023 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from typing import Optional
import os

import globalVars
import languageHandler
import NVDAState
from logHandler import log
import ui
import queueHandler
from gui.message import messageBox
import wx


def getDocFilePath(fileName: str, localized: bool = True) -> Optional[str]:
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

			# Some out of date translations might include .txt files which are now .html files in newer translations.
			# Therefore, ignore the extension and try both .html and .txt.
			for tryExt in ("html", "txt"):
				tryPath = os.path.join(tryDir, f"{fileName}.{tryExt}")
				if os.path.isfile(tryPath):
					return tryPath
		return None
	else:
		# Not localized.
		if NVDAState.isRunningAsSource() and fileName in ("copying.txt", "contributors.txt"):
			# If running from source, these two files are in the root dir.
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
		messageBox(
			noDocMessage,
			# Translators: the title of an error message dialog
			_("Error"),
			wx.OK | wx.ICON_ERROR,
		)
	else:
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, noDocMessage)
