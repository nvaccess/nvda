import os
from comtypes import GUID
import winreg
from _bridge.components.proxies.synthDriver import SynthDriverProxy
from _bridge.clients.synthDriverHost32 import createSynthDriverHost32

CLSID_TTSEnumerator = GUID("{D67C0280-C743-11cd-80E5-00AA003E4B50}")

class SynthDriver(SynthDriverProxy):
	name = "sapi4_32"
	description = "Microsoft Speech API version 4 (32 bit proxy)"
	_synthProxy = None

	@classmethod
	def check(cls):
		try:
			winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"CLSID\%s" % CLSID_TTSEnumerator, 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY).Close()
			return True
		except WindowsError:
			return False

	def __init__(self):
		self._host = createSynthDriverHost32()
		remoteDriver = self._host.SynthDriver('sapi4')
		super(SynthDriver, self).__init__(remoteDriver)
