# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Support for WhatsApp WebView2 app.
Notably, this app module disables browse mode for WhatsApp by default."""

import appModuleHandler


class AppModule(appModuleHandler.AppModule):
	disableBrowseModeByDefault: bool = True
