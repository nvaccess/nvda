import time
import ctypes

#Load the NVDA client library
clientLib=ctypes.cdll.LoadLibrary('./nvdaControllerClient32.dll')

#Test if NVDA is running, and if its not show a message
res=clientLib.nvdaController_testIfRunning()
if res!=0:
	errorMessage=str(ctypes.WinError(res))
	ctypes.windll.user32.MessageBoxW(0,u"Error: %s"%errorMessage,u"Error communicating with NVDA",0)

#Speak and braille some messages
for count in xrange(4):
	clientLib.nvdaController_speakText(u"This is a test client for NVDA")
	clientLib.nvdaController_brailleMessage(u"Time: %g seconds"%(0.75*count))
	time.sleep(0.625)
	clientLib.nvdaController_cancelSpeech()
clientLib.nvdaController_speakText(u"This is a test client for NVDA!")
clientLib.nvdaController_brailleMessage(u"Test completed!")
