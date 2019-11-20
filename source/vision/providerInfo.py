# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited
from dataclasses import dataclass
from typing import Type
from vision import providerBase

ProviderIdT = str
ModuleNameT = str
DisplayNameT = str


@dataclass(frozen=True)
class ProviderInfo:
	providerId: ProviderIdT
	moduleName: ModuleNameT
	displayName: DisplayNameT
	providerClass: Type[providerBase.VisionEnhancementProvider]
