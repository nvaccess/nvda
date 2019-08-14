#appModules/esysuite.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2016-2018 Didier Poitou (Eurobraille), Babbage B.V.

"""App module for Esysuite

Esysuite is a self braille/voice application.
NVDA should sleep during Esysuite activity.
"""

import appModuleHandler

class AppModule(appModuleHandler.AppModule):

	sleepMode = True
