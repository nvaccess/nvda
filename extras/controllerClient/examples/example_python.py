# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2023 NV Access Limited, Łukasz Golonka, Leonard de Ruijter
# This file is covered by the GNU Lesser General Public License, version 2.1.
# See the file license.txt for more details.

import ctypes
import time

# Load the NVDA client library
clientLib = ctypes.windll.LoadLibrary("./nvdaControllerClient.dll")

# Test if NVDA is running, and if its not show a message
res = clientLib.nvdaController_testIfRunning()
if res != 0:
	errorMessage = str(ctypes.WinError(res))
	ctypes.windll.user32.MessageBoxW(0, f"Error: {errorMessage}", "Error communicating with NVDA", 0)

# Speak and braille some messages
for count in range(4):
	clientLib.nvdaController_speakText("This is a test client for NVDA")
	clientLib.nvdaController_brailleMessage("Time: %g seconds" % (0.75 * count))
	time.sleep(0.625)
	clientLib.nvdaController_cancelSpeech()


# Test SSML output
@ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_wchar_p)
def onMarkReached(name: str) -> int:
	print(f"Reached SSML mark with name: {name}")
	return 0


ssml = (
	'<speak>'
	'This is one sentence. '
	'<mark name="test" />'
	'<prosody pitch="200%">This sentence is pronounced with higher pitch.</prosody>'
	'<mark name="test2" />'
	'This is a third sentence. '
	'<mark name="test3" />'
	'This is a fourth sentence. We will stay silent for a second after this one.'
	'<break time="1000ms" />'
	'<mark name="test4" />'
	'This is a fifth sentence. '
	'<mark name="test5" />'
	'</speak>'
)
clientLib.nvdaController_setOnSsmlMarkReachedCallback(onMarkReached)
clientLib.nvdaController_speakSsml(ssml, -1, 0, False)
clientLib.nvdaController_setOnSsmlMarkReachedCallback(None)
clientLib.nvdaController_brailleMessage("Test completed!")
