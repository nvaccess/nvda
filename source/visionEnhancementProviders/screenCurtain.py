#visionEnhancementProviders/screenCurtain.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Screen curtain implementation based on the windows magnification API.
This implementation only works on Windows 8 and above.
"""

import vision
import winVersion
from ctypes import byref
from collections import OrderedDict
try:
	import winMagnification
except AttributeError:
	winMagnification = None
else:
	TRANSFORM_BLACK = winMagnification.MAGCOLOREFFECT()
	TRANSFORM_BLACK.transform[4][4] = 1.0

class VisionEnhancementProvider(vision.providerBase.VisionEnhancementProvider):
	name = "screenCurtain"
	# Translators: Description of a vision enhancement provider that disables output to the screen,
	# making it black.
	description = _("Screen Curtain")
	supportedRoles = frozenset([vision.constants.Role.COLORENHANCER])

	@classmethod
	def check(cls):
		return winVersion.isFullScreenMagnificationAvailable()

	def __init__(self):
		super(VisionEnhancementProvider, self).__init__()
		winMagnification.MagInitialize()
		winMagnification.MagSetFullscreenColorEffect(byref(TRANSFORM_BLACK))

	def terminate(self):
		super(VisionEnhancementProvider, self).terminate()
		winMagnification.MagUninitialize()

	def registerEventExtensionPoints(self, extensionPoints):
		# The screen curtain isn't interested in any events
		pass
