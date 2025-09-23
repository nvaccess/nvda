# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VirusTotalScanResults:
	scanUrl: str
	malicious: int
	undetected: int
	harmless: int
	suspicious: int
	failure: int
	timeout: int
	confirmedTimeout: int
	typeUnsupported: int

	@classmethod
	def fromDict(cls, addon: dict[str, Any]) -> "VirusTotalScanResults | None":
		try:
			analysisStats = addon["scanResults"]["virusTotal"][0]["last_analysis_stats"]
			return cls(
				scanUrl=addon["vtScanUrl"],
				malicious=analysisStats["malicious"],
				undetected=analysisStats["undetected"],
				harmless=analysisStats["harmless"],
				suspicious=analysisStats["suspicious"],
				failure=analysisStats["failure"],
				timeout=analysisStats["timeout"],
				confirmedTimeout=analysisStats["confirmed-timeout"],
				typeUnsupported=analysisStats["type-unsupported"],
			)
		except KeyError:
			return None

	@property
	def totalScans(self) -> int:
		return self.malicious + self.undetected + self.harmless + self.suspicious

	@property
	def totalFlagged(self) -> int:
		return self.malicious + self.suspicious
