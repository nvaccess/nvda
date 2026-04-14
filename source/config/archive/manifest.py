from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConfigArchiveManifest:
	formatVersion: int
	configSchemaVersion: int
	nvdaVersion: str
	createdAt: datetime
