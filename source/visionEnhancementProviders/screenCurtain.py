# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""
Former module for screen curtain when implemented as a vision enhancement provider.

See ``source/screenCurtain.py`` for the current implementation.
"""

from utils import _deprecate
from logHandler import log

log.warning("visionEnhancementProviders.screenCurtain is deprecated.")

__getattr__ = _deprecate.handleDeprecations(
	_deprecate.MovedSymbol("MAGCOLOREFFECT", "winBindings.magnification"),
	_deprecate.MovedSymbol("isScreenFullyBlack", "NVDAHelper.localLib"),
	_deprecate.MovedSymbol("WarnOnLoadDialog", "screenCurtain"),
	_deprecate.movedSymbol("warnOnLoadCheckBoxText ", "screenCurtain"),
	_deprecate.movedSymbol("TRANSFORM_BLACK", "screenCurtain"),
)
