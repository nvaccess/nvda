= NVDA Source Code Read Me =

This document describes how to prepare and use the NVDA source code. For more information about NVDA, see the NVDA web site:
http://www.nvda-project.org/

== Dependencies ==
The NVDA source depends on several other packages to run correctly, as described below. All directories mentioned are relative to the root of the NVDA source distribution. Please create any directories mentioned that don't already exist.

If you are running a 64 bit version of Windows, you should install the 32 bit versions of any dependencies that provide both 32 bit and 64 bit versions unless otherwise specified.

General dependencies:
	* Python 2.7, version 2.7.0 or later: http://www.python.org/
	* comtypes, version 0.6.2 or later: http://www.sourceforge.net/projects/comtypes/
	* wxPython unicode (for Python 2.7), version 2.8.11.0 or later: http://www.wxpython.org/
	* Python Windows Extensions (for Python 2.7), build 214 or later: http://www.sourceforge.net/projects/pywin32/ 
	* eSpeak, version 1.44.03 or later, Windows dll:
		* Official web site: http://espeak.sourceforge.net/
		* The Windows dll is tricky to build, so a pre-built version has been provided for convenience at http://www.nvda-project.org/3rdParty/
		* Copy espeak.dll and espeak-data into the source\synthDrivers directory.
	* Additional variants for eSpeak: http://www.nvda-project.org/espeak-variants/
		* Extract the archive into the source\synthDrivers directory.
	* IAccessible2, version 1.1.0.0 or later: http://www.linuxfoundation.org/en/Accessibility/IAccessible2
		* Download the merged IDL and copy it to include\ia2\ia2.idl.
		* The proxy dll and typelib are also required.
			* Pre-built versions have been provided for convenience at http://www.nvda-project.org/3rdParty/
		* Copy ia2.tlb into the source\typelibs directory.
		* Copy the 32 bit version of the proxy dll into the source\lib directory, naming it IAccessible2Proxy.dll.
		* Copy the 64 bit version of the proxy dll into the source\lib64 directory, naming it IAccessible2Proxy.dll.
	* ConfigObj, version 4.6.0 or later:
		* Web site: http://www.voidspace.org.uk/python/configobj.html
		* Copy configobj.py and validate.py into the global Python site-packages directory.
	* liblouis, version 2.1.1 or later, Windows dll and Python bindings:
		* Official web site: http://code.google.com/p/liblouis/
		* A pre-built version has been provided for convenience at http://www.nvda-project.org/3rdParty/
		* Copy the louis Python package directory into the source directory.
		* Copy the liblouis dll into the source directory.
		* Copy the liblouis translation tables into the source\louis\tables directory.
			* In the pre-built version, this has already been done.
	* NVDA media (images and sounds): http://www.nvda-project.org/nvda-media/
		* Extract the archive into the root of your NVDA source distribution.
	* System dlls not present on many systems: mfc90.dll, msvcp90.dll, msvcr90.dll, Microsoft.VC90.CRT.manifest:
		* If you don't have them already, all of these files have been bundled for convenience at http://www.nvda-project.org/3rdParty/system-dlls.7z
		* Copy them either into the source directory or into your Windows system32 directory.
	* Adobe Acrobat accessibility interface, version 9.1 or later:
		* This can be found in the client files archive available from http://www.adobe.com/devnet/acrobat/interapplication_communication.html
			* The archive is named something like Acrobat_Accessibility_9.1.zip.
		* Extract the AcrobatAccess.idl file into include\AcrobatAccess.
		* The typelib is also required.
			* A pre-built version has been provided for convenience at http://www.nvda-project.org/3rdParty/AcrobatAccess.tlb
		* Copy AcrobatAccess.tlb into the source\typelibs directory.
	* Adobe FlashAccessibility interface typelib: http://www.nvda-project.org/3rdParty/FlashAccessibility.tlb
		* Copy FlashAccessibility.tlb into the source\typelibs directory.
	* txt2tags, version 2.5 or later: http://txt2tags.sourceforge.net/
		* Copy the txt2tags Python script to the global Python site-packages directory, naming it txt2tags.py.
	* Microsoft Windows SDK, version 7.0: http://www.microsoft.com/downloads/en/details.aspx?FamilyID=c17ba869-9671-4330-a63e-1fd44e0e2505&displaylang=en
		* You need to install both the 32 bit and 64 bit libraries and tools.
	* MinHook, version 1.1.0 or later: http://www.codeproject.com/KB/winsdk/LibMinHook.aspx
		*Download the source archive. The file name is something like MinHook_110_src.zip depending on exact version.
			* You will need an account on CodeProject to download from there.
		* extract the libMinHook directory from the source archive into the NVDA include directory.
	* Boost C++ Libraries, version 1.42 or later:
		* You can download the latest Windows installer from http://www.boostpro.com/download
		* On the components page of the installer, make sure to install at least all of the defaults (whatever is already checked).
		* NVDA only uses the Boost headers; none of the pre-compiled libraries are necessary.
	* SCons, version 2.0.0 or later: http://www.scons.org/

To use the brltty braille display driver:
	* brlapi Python bindings (for Python 2.7), version 0.5.5 or later, distributed with BRLTTY for Windows, version 4.2-2 or later:
		* You can download BRLTTY for Windows at http://brl.thefreecat.org/brltty/
		* The brlapi Python bindings can be found in the BRLTTY installation directory and are named brlapi-x.y.z.exe

To use the Alva BC640/680 braille display driver:
	* ALVA BC6 generic dll, version 2.0.3.0 or later: http://www.nvda-project.org/3rdParty/alvaw32.dll
		* Copy alvaw32.dll into the source\brailleDisplayDrivers directory.

To use the MDV Lilli braille display driver:
	* lilli.dll: http://www.nvda-project.org/3rdParty/lilli.dll
		* Copy lilli.dll into the source\brailleDisplayDrivers directory.

To build a binary version of NVDA:
	* Py2Exe (for Python 2.7), version 0.6.9 or later: http://www.sourceforge.net/projects/py2exe/

To build a portable archive:
	* 7-Zip: http://www.7-zip.org/

To build an installer:
	* Nulsoft Install System, version 2.42 or later: http://nsis.sourceforge.net/
	* NSIS UAC plug-in, version 0.0.11d or later: http://nsis.sourceforge.net/UAC_plug-in
		* Copy the ANSI build of UAC.dll (found in release\a in the archive) into the installer directory.

== Preparing the Source Tree ==
Before you can run the NVDA source code, you must prepare the source tree.
You do this by opening a command prompt, changing to the root of the NVDA source distribution and typing:
scons source
You should do this again whenever the version of comtypes changes or new language files are added.

== Running the Source Code ==
To start NVDA from source code, run nvda.pyw located in the source directory.

== Building NVDA ==
A binary build of NVDA can be run on a system without Python and all of NVDA's other dependencies installed (as we do for snapshots and releases).

Binary archives and bundles can be created using scons from the root of the NVDA source distribution. To build any of the following, open a command prompt and change to this directory.

To make a non-archived binary build (equivalent to an extracted portable archive), type:
scons dist
The build will be created in the dist directory.

To create a portable archive, type:
scons portable
The archive will be placed in the output directory.

To build an installer, type:
scons installer
The installer will be placed in the output directory.

Optionally, the build can  be customised by providing variables on the command line:
	* version: The version of this build.
	* release: Whether this is a release version.
	* publisher: The publisher of this build.
	* certFile: The certificate file with which to sign executables. The certificate must be in pfx format and contain the private key.
	* certPassword: The password for the private key in the signing certificate. If omitted, no password will be assumed.
	* outputDir: The directory where the final built archives and such will be placed.
	* targetArchitectures: The target architectures that NVDA should support. Possible values are all, x86 and x86_64. This should generally be left as the default.

For example, to build an installer with a specific version, you might type:
scons installer version=test1
