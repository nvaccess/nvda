# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from comtypes import GUID, COMError
from pycaw.callbacks import MMNotificationClient
from pycaw.api.mmdeviceapi.depend.structures import PROPERTYKEY
from pycaw.utils import AudioUtilities
from pycaw.constants import EDataFlow
from typing import Any
from logHandler import log
import ui
import nvwave
import atexit

deviceEnumerator: Any | None = None
mmClient: MMNotificationClient | None = None


def initialize() -> None:
	if nvwave.usingWasapiWavePlayer():
		global mmClient, deviceEnumerator
		try:
			mmClient = MMNotificationClientImpl()
			deviceEnumerator = AudioUtilities.GetDeviceEnumerator()
			deviceEnumerator.RegisterEndpointNotificationCallback(mmClient)
		except COMError:
			log.exception("Could not initialize audio notifications module")
			return

	else:
		log.debug("Cannot initialize audio notifications as WASAPI is disabled")


@atexit.register
def terminate():
	if (
		nvwave.usingWasapiWavePlayer():
		and mmClient is not None
		and deviceEnumerator is not None
	):
			try:
				deviceEnumerator.UnregisterEndpointNotificationCallback(mmClient)
			except COMError:
				log.exception("Could not terminate audio notifications module"):
				return


GUID_DEVICE_VOLUME_OR_MUTE = GUID("{9855C4CD-DF8C-449C-A181-8191B68BD06C}")
EVENT_MUTE = (GUID_DEVICE_VOLUME_OR_MUTE, 1)


class MMNotificationClientImpl(MMNotificationClient):
	def on_property_value_changed(self, device_id: str, property_struct: PROPERTYKEY, fmtid: GUID, pid: int):
		global EVENT_MUTE
		match (fmtid, pid):
			case EVENT_MUTE:
				defaultMicrophone = AudioUtilities.GetMicrophone()
				defaultMicrophoneId = defaultMicrophone.GetId() if defaultMicrophone is not None else None
				device = deviceEnumerator.GetDevice(device_id)
				deviceObject = AudioUtilities.CreateDevice(device)
				if device_id == defaultMicrophoneId:
					microphoneName = ""
					isMicrophone = True
				else:
					microphoneName = deviceObject.FriendlyName
					isMicrophone = AudioUtilities.GetEndpointDataFlow(device_id, 1) == EDataFlow.eCapture.value
				if isMicrophone:
					isMuted = deviceObject.EndpointVolume.GetMute()
					if isMuted:
						# Translators: notification spoken when microphone muted/unmuted
						msg = _("Muted microphone %s") % microphoneName
					else:
						# Translators: notification spoken when microphone muted/unmuted
						msg = _("Unmuted microphone %s") % microphoneName
					ui.message(msg)
