import ctypes
import time

# Load the NVDA client library
clientLib = ctypes.windll.LoadLibrary("./nvdaControllerClient.dll")

# Test if NVDA is running, and if its not show a message
res = clientLib.nvdaController_testIfRunning()
if res != 0:
	errorMessage = str(ctypes.WinError(res))
	ctypes.windll.user32.MessageBoxW(0, "Error: %s" % errorMessage, "Error communicating with NVDA", 0)

# Speak and braille some messages
for count in range(4):
	clientLib.nvdaController_speakText("This is a test client for NVDA")
	clientLib.nvdaController_brailleMessage("Time: %g seconds" % (0.75 * count))
	time.sleep(0.625)
	clientLib.nvdaController_cancelSpeech()
clientLib.nvdaController_speakText("This is a test client for NVDA!")
clientLib.nvdaController_brailleMessage("Test completed!")
