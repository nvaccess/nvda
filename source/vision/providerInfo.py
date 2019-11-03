# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited
from dataclasses import dataclass
from typing import Type
from .providerBase import VisionEnhancementProvider

ProviderIdT = str
ModuleNameT = str
TranslatedNameT = str
#RolesT = List[Role]


@dataclass
class ProviderInfo:
	providerId: ProviderIdT
	moduleName: ModuleNameT
	translatedName: TranslatedNameT
	providerClass: Type[VisionEnhancementProvider]
