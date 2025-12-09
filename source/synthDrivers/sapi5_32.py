import os
from comtypes import GUID
import winreg
from _bridge.components.proxies.synthDriver import SynthDriverProxy
from _bridge.clients.synthDriverHost32 import createSynthDriverHost32


class SynthDriver(SynthDriverProxy):
	name = "sapi5_32"
	description = "Microsoft Speech API version 5 (32 bit proxy)"
	_synthProxy = None

	@classmethod
	def check(cls):
		try:
			r = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "SAPI.SPVoice", 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
			r.Close()
			return True
		except:  # noqa: E722
			return False

	def __init__(self):
		self._host = createSynthDriverHost32()
		remoteDriver = self._host.SynthDriver('sapi5')
		super(SynthDriver, self).__init__(remoteDriver)
