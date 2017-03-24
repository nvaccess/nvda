/**
 * Because AutoHotkey's DllCall function can be a bit tricky for newcomers, I've taken the liberty of creating the following wrapper functions.
 * But of course, you could just as easily call the DLL directly, as I have done inside the functions.  But it might be easier to save the wrapper
 * functions to a separate file and then including them (AutoHotkey has a #include directive similar to C++).
 */
nvdaController_speakText(text)
{
	return DllCall(A_ScriptDir . "\nvdaControllerClient32.dll\nvdaController_speakText", Str, text)
}
nvdaController_brailleMessage(msg)
{
	return DllCall(A_ScriptDir . "\nvdaControllerClient32.dll\nvdaController_brailleMessage", Str, msg)
}
nvdaController_testIfRunning()
{
	return DllCall("nvdaControllerClient32.dll\nvdaController_testIfRunning")
}
nvdaController_cancelSpeech()
{
	return DllCall(A_ScriptDir . "\nvdaControllerClient32.dll\nvdaController_cancelSpeech")
}

/**
 * And here are some actual examples.
 */

; This Control+1 hotkey checks if NVDA is running and lets the user know one way or the other
^1::
test1 := nvdaController_testIfRunning()
if (test1 != 0)
{
	; NVDA is not running, so provide some basic debug info.
	message := "NVDA is not running.  "
	if (Errorlevel)
	{
		message .= "The DLL call returned """ . test1 . """ and ErrorLevel was set to """ . ErrorLevel . """."
		message .= "Please refer to www.autohotkey.com for more information."
	}
	MsgBox % message
}
else
{
	; NVDA is running, so spreak and braille this information so the user knows.
	nvdaController_speakText("NVDA is running.")
	nvdaController_brailleMessage("NVDA is running.")
}
return

; This hotkey basically makes the S key work like Control (it makes NVDA stop talking)
s::nvdaController_cancelSpeech()
