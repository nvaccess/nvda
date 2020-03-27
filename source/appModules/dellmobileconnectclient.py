# appModules/dellmobileconnectclient.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""The dellmobileconnectclient executable is used for some notifications.
Import the main Dell Mobile Connect appModule to handle these cases."""

# Normally these Flake8 errors shouldn't be ignored but here we are simply reusing existing ap module.
from .dellmobileconnectuniversalclient import AppModule  # noqa: F401, F403
