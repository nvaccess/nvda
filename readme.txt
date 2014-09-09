= NVDA Source Code Read Me =
This document describes how to prepare and use the NVDA source code.
For more information about NVDA, see the NVDA web site: http://www.nvaccess.org/
For information about obtaining the source code, please see http://community.nvda-project.org/wiki/AccessingAndRunningSourceCode

== Dependencies ==
The NVDA source depends on several other packages to run correctly.

=== Installed Dependencies ===
The following dependencies need to be installed on your system:
* Python, version 2.7.8, 32 bit: http://www.python.org/
* Microsoft Visual Studio 2012 Update 1 or later (Express for Windows Desktop, or Professional)
	* Download for Visual Studio Express 2012 (Windows Desktop): http://www.microsoft.com/en-au/download/details.aspx?id=34673
	* Download for Visual Studio 2012 latest update package: http://go.microsoft.com/fwlink/?LinkId=301713 


=== Git Submodules ===
Most of the dependencies are contained in Git submodules.
If you didn't pass the --recursive option to git clone, you will need to run git submodule update --init.
Whenever a required submodule commit changes (e.g. after git pull), you will need to run git submodule update.
If you aren't sure, run git submodule update after every git pull, merge or checkout.

The following dependencies are included in Git submodules:
* comtypes, version 0.6.2: http://sourceforge.net/projects/comtypes/
* wxPython, version 3.0.0.1: http://www.wxpython.org/
* Python Windows Extensions, build 218: http://sourceforge.net/projects/pywin32/ 
* eSpeak, version 1.48.03: http://espeak.sourceforge.net/
* IAccessible2, version 1.3: http://www.linuxfoundation.org/collaborate/workgroups/accessibility/iaccessible2
* ConfigObj, version 4.6.0: http://www.voidspace.org.uk/python/configobj.html
* liblouis, version 2.5.4: http://www.liblouis.org/
* NVDA images and sounds
* System dlls not present on many systems: mfc90.dll, msvcp90.dll, msvcr90.dll, Microsoft.VC90.CRT.manifest
* Adobe Acrobat accessibility interface, version XI: http://download.macromedia.com/pub/developer/acrobat/AcrobatAccess.zip
* Adobe FlashAccessibility interface typelib
* txt2tags, version 2.5: http://txt2tags.sourceforge.net/
* MinHook, tagged version 1.2.2: https://github.com/RaMMicHaeL/minhook
* SCons, version 2.3.2: http://www.scons.org/
* brlapi Python bindings, version 0.5.7 or later, distributed with BRLTTY for Windows, version 4.2-2: http://brl.thefreecat.org/brltty/
* ALVA BC6 generic dll, version 3.0.4.1
* lilli.dll, version 2.1.0.0
* Handy Tech Braille SDK, version 1.4.2.0: ftp://ftp.handytech.de/public/Software/BrailleDriver/HTBrailleSDK_1420a.zip
* pyserial, version 2.5: http://pypi.python.org/pypi/pyserial
* HanSoneConnect.dll, version 2.0.0.1
* SyncBraille.dll, version 1.0.0.1
* Python interface to FTDI driver/chip: http://fluidmotion.dyndns.org/zenphoto/index.php?p=news&title=Python-interface-to-FTDI-driver-chip
* Py2Exe, version 0.6.9: http://sourceforge.net/projects/py2exe/
* Nulsoft Install System, version 2.46: http://nsis.sourceforge.net/
* NSIS UAC plug-in, version 0.2.4, ansi: http://nsis.sourceforge.net/UAC_plug-in
* xgettext and msgfmt from GNU gettext: http://sourceforge.net/projects/cppcms/files/boost_locale/gettext_for_windows/
* epydoc, version 3.0.1 with patch for bug #303: http://epydoc.sourceforge.net/

=== Other Dependencies ===
These dependencies are not included in Git submodules, but aren't needed by most people.
* If you want to be able to use the Handy Tech braille display driver when running from source code, you will need to install the Handy Tech universal driver: ftp://ftp.handytech.de/public/Software/BrailleDriver/bsd1206a.exe
* To generate developer documentation for nvdaHelper: Doxygen Windows installer, version 1.7.3: http://www.stack.nl/~dimitri/doxygen/download.html

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
	* debugCRT: the libraries will be linked against the debug C runtime and assertions will be enabled. (By default, the normal CRT is used and assertions are disabled.)
	* RTC: runtime checks (stack corruption, uninitialized variables, etc.) will be enabled. (The default is no runtime checks.)
The special keywords none and all can also be used in place of the individual flags.

An example follows that enables debug CRT and runtype checks 
scons source nvdaHelperDebugFlags=debugCRT,RTC

Symbol pdb files are always produced when building, regardless of the debug flags.
However, they are not included in the NVDA distribution.
Instead, scons symbolArchive will package them as a separate archive.

By default, builds also do not use any compiler optimizations.
Please see the release keyword argument for what compiler optimizations it will enable.

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
		* This enables various C++ compiler optimizations such as /O2 and whole-program optimization.
		* It also instructs Python to generate optimized byte code.
	* publisher: The publisher of this build.
	* certFile: The certificate file with which to sign executables. The certificate must be in pfx format and contain the private key.
	* certPassword: The password for the private key in the signing certificate. If omitted, no password will be assumed.
	* certTimestampServer: The URL of the timestamping server to use to timestamp authenticode signatures. If omitted, signatures will not be timestamped.
	* outputDir: The directory where the final built archives and such will be placed.
	* targetArchitectures: The target architectures that NVDA should support. Possible values are all, x86 and x86_64. This should generally be left as the default.

For example, to build a launcher  with a specific version, you might type:
scons launcher version=test1
