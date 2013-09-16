= NVDA Source Code Read Me =

This document describes how to prepare and use the NVDA source code. For more information about NVDA, see the NVDA web site:
http://www.nvda-project.org/

== Dependencies ==
The NVDA source depends on several other packages to run correctly, as described below.

All directories mentioned are relative to the root of the NVDA source distribution. Please create any directories mentioned that don't already exist.

If you are running a 64 bit version of Windows, you should install the 32 bit versions of any dependencies that provide both 32 bit and 64 bit versions unless otherwise specified.

Earlier or later versions of these dependencies may work, but the version listed is the version that has been widely tested and is used for official builds.

General dependencies:
	* Python 2.7, version 2.7.5: http://www.python.org/
	* comtypes, version 0.6.2: http://www.sourceforge.net/projects/comtypes/
	* wxPython 2.8 unicode (for Python 2.7), version 2.8.12.1: http://www.wxpython.org/
	* Python Windows Extensions (for Python 2.7), build 218: http://www.sourceforge.net/projects/pywin32/ 
	* eSpeak, version 1.47.11:
		* Official web site: http://espeak.sourceforge.net/
		* Download the espeak source archive. Note that it must be an official source archive from the espeak website containing already compiled phoneme data, not straight from svn. 
		* Extract it in to include/espeak so that include/espeak/src, include/espeak/dictsource, include/espeak/platforms and include/espeak/espeak-data all exist.
	* IAccessible2, version 1.3: http://www.linuxfoundation.org/collaborate/workgroups/accessibility/iaccessible2
		* Download the merged IDL and copy it to include\ia2\ia2.idl.
	* ConfigObj, version 4.6.0:
		* Web site: http://www.voidspace.org.uk/python/configobj.html
		* Copy configobj.py and validate.py into the global Python site-packages directory.
	* liblouis, version 2.5.3:
		* Official web site: http://www.liblouis.org/
		* This is included as a Git submodule.
	* NVDA media (images and sounds): http://www.nvda-project.org/nvda-media/
		* Extract the archive into the root of your NVDA source distribution.
	* System dlls not present on many systems: mfc90.dll, msvcp90.dll, msvcr90.dll, Microsoft.VC90.CRT.manifest:
		* If you don't have them already, all of these files have been bundled for convenience at http://www.nvda-project.org/3rdParty/system-dlls.7z
		* Copy them either into the source directory or into your Windows system32 directory.
	* Adobe Acrobat accessibility interface, version XI: http://download.macromedia.com/pub/developer/acrobat/AcrobatAccess.zip
		* Extract the AcrobatAccess.idl file into include\AcrobatAccess.
	* Adobe FlashAccessibility interface typelib: http://www.nvda-project.org/3rdParty/FlashAccessibility.tlb
		* Copy FlashAccessibility.tlb into the source\typelibs directory.
	* txt2tags, version 2.5: http://txt2tags.sourceforge.net/
		* Copy the txt2tags Python script to the global Python site-packages directory, naming it txt2tags.py.
	* Microsoft Windows SDK, version 7.0: http://www.microsoft.com/downloads/en/details.aspx?FamilyID=c17ba869-9671-4330-a63e-1fd44e0e2505&displaylang=en
		* You need to install both the 32 bit and 64 bit libraries and tools.
	* MinHook, rev e21b54a: http://www.codeproject.com/KB/winsdk/LibMinHook.aspx
		* This is included as a git submodule
	* SCons, version 2.2.0: http://www.scons.org/
		* As the scons command (scons.bat) is installed in to the scripts directory inside the directory where you installed Python, it is necessary to add the scripts  directory to your path variable so that you can run scons from anywhere. The rest of this readme assumes that scons can be run in this way.

To use the brltty braille display driver:
	* brlapi Python bindings (for Python 2.7), version 0.5.7 or later, distributed with BRLTTY for Windows, version 4.2-2:
		* You can download BRLTTY for Windows at http://brl.thefreecat.org/brltty/
		* The brlapi Python bindings can be found in the BRLTTY installation directory and are named brlapi-x.y.z.exe

To use the ALVA BC640/680 braille display driver:
	* ALVA BC6 generic dll, version 3.0.4.1: http://www.nvda-project.org/3rdParty/alvaw32.dll
		* Copy alvaw32.dll into the source\brailleDisplayDrivers directory.

To use the MDV Lilli braille display driver:
	* lilli.dll, version 2.1.0.0: http://www.nvda-project.org/3rdParty/lilli.dll
		* Copy lilli.dll into the source\brailleDisplayDrivers directory.

To use the Handy Tech braille display driver:
	* Handy Tech Braille SDK, version 1.4.2.0: ftp://ftp.handytech.de/public/Software/BrailleDriver/HTBrailleSDK_1420a.zip
		* Copy these files from the SDK's prog directory into NVDA's source\brailleDisplayDrivers\handyTech directory: HtBrailleDriverServer.dll, HtBrailleDriverServer.tlb, sbsupport.dll, dealers.dat
	* If you want to be able to use this driver when running from source code, you will need to install the Handy Tech universal driver: ftp://ftp.handytech.de/public/Software/BrailleDriver/bsd1206a.exe

To use the Baum, BrailleNote, Brailliant B, hedo, Papenmeier and/or Seika braille display drivers:
	* pyserial (for Python 2.x), version 2.5: http://pypi.python.org/pypi/pyserial

To use the HIMS Braille Sense/Braille EDGE braille display driver:
	* HanSoneConnect.dll, version 2.0.0.1: http://www.nvda-project.org/3rdParty/HanSoneConnect.dll
		* Copy HanSoneConnect.dll into the source\brailleDisplayDrivers\hims directory.

To use the HIMS SyncBraille braille display driver:
	* SyncBraille.dll, version 1.0.0.1: http://www.nvda-project.org/3rdParty/SyncBraille.dll
		* Copy SyncBraille.dll into the source\brailleDisplayDrivers\syncBraille directory.

To use the Papenmeier braille display driver:
	* Python interface to FTDI driver/chip: http://fluidmotion.dyndns.org/zenphoto/index.php?p=news&title=Python-interface-to-FTDI-driver-chip
		* Download the archive.
		* Extract ftdi2.py into the global Python site-packages directory.

To build a binary version of NVDA:
	* Py2Exe (for Python 2.7), version 0.6.9: http://www.sourceforge.net/projects/py2exe/
	* 7-Zip: http://www.7-zip.org/
	* Nulsoft Install System, version 2.46: http://nsis.sourceforge.net/
	* NSIS UAC plug-in, version 0.2.4:
		* Web site: http://nsis.sourceforge.net/UAC_plug-in
		* Copy both ansi\uac.dll and uac.nsh into the uninstaller directory.

To generate developer documentation:
	* epydoc, version 3.0.1:
		* Official web site: http://epydoc.sourceforge.net/
		* Epydoc is no longer being maintained, but there is a bug in version 3.0.1 which affects NVDA.
		* A build including a fix for this bug can be found at: http://files.nvaccess.org/3rdParty/epydoc-3.0.1+bug2585292.win32.exe

To generate developer documentation for nvdaHelper:
	* Doxygen Windows installer, version 1.7.3: http://www.stack.nl/~dimitri/doxygen/download.html 

To generate a gettext translation template:
	* xgettext and msgfmt from GNU gettext:
		* A Windows build is available at http://sourceforge.net/projects/cppcms/files/boost_locale/gettext_for_windows/
		* Copy xgettext.exe and msgfmt.exe into the tools directory.

== Preparing the Source Tree ==
Before you can run the NVDA source code, you must prepare the source tree.
You do this by opening a command prompt, changing to the root of the NVDA source distribution and typing:
scons source
You should do this again whenever the version of comtypes changes or language files are added or changed.
Note that if you want to access user documentation from the help menu while running the source version, you will also need to add user_docs to the commandline like so:
scons source user_docs
Though while simply testing or committing changes, it may be faster usually just doing scons source as user documentation will change each time the revision number changes.

=== Compiling NVDAHelper with Debugging Options ===
Among other things, preparing the source tree builds the NVDAHelper libraries.  
If trying to debug nvdaHelper, You can control various  debugging options  with the nvdaHelperDebugFlags command line variable. It takes one or more of the following flags:
	* symbols: debugging symbols will be added to the DLLs and pdb files will be generated for use with a debugger. (symbols are produced by default, but if specifying nvdaHelperDebugFlags and you want symbols it is still necessary to  specify this keyword.)
	* debugCRT: the libraries will be linked against the debug C runtime and assertions will be enabled. (By default, the normal CRT is used and assertions are disabled.)
	* noOptimize: All compiler optimizations will be disabled. (Optimization 2 [/O2] is used by default.)
	* RTC: runtime checks (stack corruption, uninitialized variables, etc.) will be enabled. (The default is no runtime checks.)
The special keywords none and all can also be used in place of the individual flags.

An example follows that enables symbols and disables optimizations:
scons source nvdaHelperDebugFlags=symbols,noOptimize

== Running the Source Code ==
To start NVDA from source code, run nvda.pyw located in the source directory.

== Building NVDA ==
A binary build of NVDA can be run on a system without Python and all of NVDA's other dependencies installed (as we do for snapshots and releases).

Binary archives and bundles can be created using scons from the root of the NVDA source distribution. To build any of the following, open a command prompt and change to this directory.

To make a non-archived binary build (equivalent to an extracted portable archive), type:
scons dist
The build will be created in the dist directory.

To create a launcher  archive (one executable allowing for installation or portable dist generation), type:
scons launcher
The archive will be placed in the output directory.

To generate developer documentation, type:
scons devDocs
The developer docs will be placed in the devDocs folder in the output directory.

To generate developer documentation for nvdaHelper (not included in the devDocs target):
scons devDocs_nvdaHelper
The documentation will be placed in the devDocs\nvdaHelper folder in the output directory.

To generate an archive of debug symbols for the various dll/exe binaries, type:
scons symbolsArchive
The archive will be placed in the output directory.

To generate a gettext translation template (for translators), type:
scons pot

Optionally, the build can  be customised by providing variables on the command line:
	* version: The version of this build.
	* release: Whether this is a release version.
	* publisher: The publisher of this build.
	* certFile: The certificate file with which to sign executables. The certificate must be in pfx format and contain the private key.
	* certPassword: The password for the private key in the signing certificate. If omitted, no password will be assumed.
	* certTimestampServer: The URL of the timestamping server to use to timestamp authenticode signatures. If omitted, signatures will not be timestamped.
	* outputDir: The directory where the final built archives and such will be placed.
	* targetArchitectures: The target architectures that NVDA should support. Possible values are all, x86 and x86_64. This should generally be left as the default.

For example, to build a launcher  with a specific version, you might type:
scons launcher version=test1
