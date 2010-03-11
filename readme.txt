= NVDA Source Code Read Me =

This document describes how to prepare and use the NVDA source code. For more information about NVDA, see the NVDA web site:
http://www.nvda-project.org/

== Dependencies ==
The NVDA source depends on several other packages to run correctly, as described below. All directories mentioned are relative to the root of the NVDA source distribution/checkout. Please create any directories mentioned that don't already exist.

If you are running a 64 bit version of Windows, you should install the 32 bit versions of any dependencies that provide both 32 bit and 64 bit versions.

General dependencies:
	* Python 2.6, version 2.6.4 or later: http://www.python.org/
	* comtypes, version 0.6.2 or later: http://www.sourceforge.net/projects/comtypes/
	* wxPython unicode (for Python 2.6), version 2.8.9.1 or later: http://www.wxpython.org/
	* Python Windows Extensions (for Python 2.6), build 212 or later: http://www.sourceforge.net/projects/pywin32/ 
	* eSpeak, version 1.43 or later, Windows dll:
		* Official web site: http://espeak.sourceforge.net/
		* The Windows dll is tricky to build, so a pre-built version has been provided for convenience at http://www.nvda-project.org/3rdParty/
		* Copy espeak.dll and espeak-data into the source\synthDrivers directory.
	* Additional variants for eSpeak: http://www.nvda-project.org/espeak-variants/
		* Extract the archive into the source\synthDrivers directory.
	* IAccessible2, version 1.1.0.0 or later:
		* The proxy dll and typelib are required.
		* Pre-built versions have been provided for convenience at http://www.nvda-project.org/3rdParty/
		* Copy ia2.tlb into the source\typelibs directory.
		* Copy the 32 bit version of the proxy dll into the source\lib directory, naming it IAccessible2Proxy.dll.
		* Copy the 64 bit version of the proxy dll into the source\lib64 directory, naming it IAccessible2Proxy.dll.
	* ConfigObj, version 4.6.0 or later:
		* Web site: http://www.voidspace.org.uk/python/configobj.html
		* Copy configobj.py and validate.py into the source directory.
	* liblouis, version 1.8.0 or later, Windows dll and Python bindings:
		* Official web site: http://code.google.com/p/liblouis/
		* A pre-built version has been provided for convenience at http://www.nvda-project.org/3rdParty/
		* Copy the louis Python package directory into the source directory.
		* Copy the liblouis dll into the source directory.
		* Copy the liblouis translation tables into the source\louis\tables directory.
			* In the pre-built version, this has already been done.
	* NVDA media (images and sounds): http://www.nvda-project.org/nvda-media/
		* Extract the archive into the root of your NVDA source distribution.
	* System dlls not present on many systems: mfc90.dll, msvcp90.dll, msvcr90.dll, Microsoft.VC90.CRT.manifest:
		* IF you don't have them already, all of these files have been bundled for convenience at http://www.nvda-project.org/3rdParty/system-dlls.7z
		* Copy them either into the source directory or into your Windows system32 directory.
	* nvdaHelper:
		* You can build this yourself. You need to have the Windows SDK installed, which is quite large. See source\nvdaHelper\building.txt for instructions.
		* Alternatively, pre-built versions are provided alongside NVDA snapshots for convenience. See http://www.nvda-project.org/snapshots/
			* Extract this archive into the root of your NVDA source distribution.
	* Adobe AcrobatAccess interface typelib:
		* You can build this yourself using midl from the idl located at http://www.adobe.com/devnet/acrobat/downloads/ClientFiles.zip
		* Alternatively, a pre-built version has been provided for convenience at http://www.nvda-project.org/3rdParty/AcrobatAccess.tlb
		* Copy AcrobatAccess.tlb into the source\typelibs directory.
	* Adobe FlashAccessibility interface typelib: http://www.nvda-project.org/3rdParty/FlashAccessibility.tlb
	* MinHook 1.1.0 or later: http://www.codeproject.com/KB/winsdk/LibMinHook.aspx
		* Download the binary archive.
			* You will need an account on CodeProject to download from there. For convenience, a mirror has been provided at http://www.nvda-project.org/3rdParty/
		* Copy MinHook.x86.dll into the source\lib directory.
		* Copy MinHook.x64.dll into the source\lib64 directory.

To use the brltty braille display driver:
	* brlapi Python bindings, version 0.5.3 or later, distributed with BRLTTY for Windows, version 4.0-2 or later:
		* You can download BRLTTY for Windows at http://brl.thefreecat.org/brltty/
		* The brlapi Python bindings can be found in the BRLTTY installation directory and are named brlapi-x.y.z.exe

To use the Alva BC640/680 braille display driver:
	* ALVA BC6 generic dll, version 2.0.3.0 or later: http://www.nvda-project.org/3rdParty/alvaw32.dll
		* Copy alvaw32.dll into the source\brailleDisplayDrivers directory.

To build a binary version of NVDA:
	* Py2Exe (for Python 2.6), version 0.6.9 or later: http://www.sourceforge.net/projects/py2exe/

To build an installer:
	* Nulsoft Install System, version 2.42 or later: http://nsis.sourceforge.net/
	* NSIS UAC plug-in, version 0.0.11d or later: http://nsis.sourceforge.net/UAC_plug-in
		* Copy the ANSI build of UAC.dll (found in release\a in the archive) into the installer directory.

== Preparing the Source Tree ==
Before you can run the NVDA source code, you must run generate.py located in the source directory.
You should do this again whenever the version of comtypes changes or new language files are added.

== Running the Source Code ==
To start NVDA from source code, run nvda.pyw located in the source directory.

== Building a Standalone Binary Version of NVDA ==
You can use py2exe to make a binary build of NVDA which can be run on a system without Python and all of NVDA's other dependencies installed (as we do for snapshots and releases).

Assuming py2exe is installed, open a command prompt, change to the NVDA source directory and type:
setup.py py2exe

== Building an NVDA Installer ==
To build an NVDA installer:
	1. First build a standalone binary version as described in the previous section.
	2. Using Windows Explorer, locate nvda.nsi in the installer directory.
	3. Press the applications key and choose "Compile NSIS Script".
The installer will be built and placed in the installer directory.
