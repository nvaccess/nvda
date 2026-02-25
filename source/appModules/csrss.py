# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for the Client Server Runtime Process (csrss.exe).

This app module provides a workaround for permission issues when attempting to
determine the alive status of the csrss.exe process. The csrss.exe process is
a critical Windows system process that manages console windows and GUI shutdown.
"""

import appModuleHandler


class AppModule(appModuleHandler.AppModule):
	isAlive = True
	"""Due to security restrictions, NVDA typically cannot query the alive status of
	this system process through normal means. Therefore, bypass these permission issues.
	The process is essential and always alive anyway.
	"""
