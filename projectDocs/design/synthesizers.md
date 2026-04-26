# Synthesizers

## SAPI 4

SAPI 4 synthesizers are not included with NVDA, and the runtimes are no longer included with Windows.
Despite this, SAPI 4 support is still required, as many users prefer older synthesizers which rely on the SAPI 4 API.

To test SAPI 4, you must install the SAPI 4 runtimes (or the SDK containing the runtimes) from Microsoft, as well as a synthesizer.
Microsoft no longer hosts downloads for these, but archives and mirrors exist.

First, you can download and install either only the SAPI 4 runtimes from [this Microsoft archive](http://web.archive.org/web/20150910165037/http://activex.microsoft.com/activex/controls/sapi/spchapi.exe), or the SAPI 4 SDK from [this Microsoft archive](https://web.archive.org/web/20030203082745/http://download.microsoft.com/download/speechSDK/Install/4.0a/WIN98/EN-US/SAPI4SDK.exe), which contains the SAPI 4 runtimes, offline documentation, and sample source code & test applications.
If you only need the offline documentation, you can download the documentation for SAPI 4 COM interfaces from [this Microsoft archive](https://web.archive.org/web/19990418101425/http://www.microsoft.com/iit/onlineDocs/speechsdk4-com.chm).

After installing the runtimes, download and install a SAPI 4 synthesizer from [this Microsoft archive](http://web.archive.org/web/20150910005021if_/http://activex.microsoft.com/activex/controls/agent2/tv_enua.exe).

After this, you should be able to select SAPI 4 as a NVDA synthesizer.
