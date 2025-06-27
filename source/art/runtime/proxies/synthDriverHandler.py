# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""SynthDriverHandler module proxy for add-ons running in ART."""

from typing import Any, Dict, List, Optional

from .base import ServiceProxyMixin

# Re-export base classes from synthDrivers
from .synthDrivers import SynthDriver, VoiceInfo


# ------------------------------------------------------------------
# Extension-point notification proxies
# ------------------------------------------------------------------
class _SynthNotification(ServiceProxyMixin):
	"""Proxy object mimicking NVDA's synthIndexReached / synthDoneSpeaking.

	It exposes a .notify(**kwargs) method so existing synthesizers can call
	`synthIndexReached.notify(synth=self, index=idx)` or
	`synthDoneSpeaking.notify(synth=self)`.
	The call is forwarded to Core's SpeechService via RPC.
	"""

	_service_env_var = "NVDA_ART_SPEECH_SERVICE_URI"

	def __init__(self, name: str, _kind: str):
		# name is the string identifier (e.g., "synthIndexReached")
		# _kind is either "index" or "done"
		self.name = name
		self._kind = _kind

	def notify(self, *, synth, index: int | None = None, **_ignored):
		service = self._get_service()
		if not service or not getattr(synth, "name", None):
			return
		try:
			if self._kind == "index" and index is not None:
				service.notifyIndexReached(synth.name, index)
			elif self._kind == "done":
				service.notifySpeechDone(synth.name)
		except Exception:
			# Never let logging failures crash add-ons
			pass


# Constants that synths import
synthIndexReached = _SynthNotification("synthIndexReached", "index")
synthDoneSpeaking = _SynthNotification("synthDoneSpeaking", "done")


class _SynthDriverHandlerProxy(ServiceProxyMixin):
	"""Internal proxy class for synthDriverHandler service."""

	_service_env_var = "NVDA_ART_SPEECH_SERVICE_URI"


def getSynth() -> Optional[SynthDriver]:
	"""Get the current synthesizer.

	In ART, this returns None as synths don't have access to other synths.

	@return: None (synths in ART are isolated)
	"""
	return None


def getSynthList() -> List[tuple]:
	"""Get list of available synthesizers.

	@return: Empty list (not available in ART)
	"""
	return []


def setSynth(name: str) -> bool:
	"""Set the current synthesizer.

	@param name: Name of the synthesizer to set
	@return: False (not available in ART)
	"""
	return False


# Re-export for compatibility
__all__ = [
	"SynthDriver",
	"VoiceInfo",
	"getSynth",
	"getSynthList",
	"setSynth",
	"synthIndexReached",
	"synthDoneSpeaking",
]
