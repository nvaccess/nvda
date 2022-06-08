# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import dataclasses
import json
import typing


@dataclasses.dataclass(frozen=True)  # once created, it should not be modified.
class AddonDetailsModel:
	"""Typing for information from API
	"""
	addonId: str
	displayName: str
	description: str
	publisher: str
	versionName: str
	channel: str
	homepage: str
	licenseName: str
	licenseUrl: str
	sourceUrl: str
	addonURL: str
	fileSHA: str


def _createModelFromData(jsonData: str) -> typing.List[AddonDetailsModel]:
	"""Use json string to construct a listing of available addons.
	See https://github.com/nvaccess/addon-datastore#api-data-generation-details
	for details of the data.
	"""
	data = json.loads(jsonData)

	return [
		AddonDetailsModel(
			addonId=addon["addonId"],
			displayName=addon["displayName"],
			description=addon["description"],
			publisher=addon["publisher"],
			channel=addon["channel"],
			versionName=addon["addonVersionName"],
			homepage=addon["homepage"],
			licenseName=addon["license"],
			licenseUrl=addon["licenseURL"],
			sourceUrl=addon["sourceURL"],
			addonURL=addon["URL"],
			fileSHA=addon["sha256"],
		)
		for addon in data
	]
