# NVDA

NVDA (NonVisual Desktop Access) is a free, open source screen reader for Microsoft Windows.
It is developed by NV Access in collaboration with a global community of contributors.
To learn more about NVDA or download a copy, visit the main [NV Access](http://www.nvaccess.org/) website.

## Key Project Links
* [NV Access](https://www.nvaccess.org/): The main home of NVDA
* [NVDA on GitHub](https://github.com/nvaccess/nvda)
* [NVDA issues on GitHub](https://github.com/nvaccess/nvda/issues): Bug reports, feature requests, etc.
* [NVDA development snapshots](https://www.nvaccess.org/files/nvda/snapshots/): Automatically generated builds of the project in its current state of development
* [NVDA add-ons](https://addons.nvda-project.org/): Get add-ons to enhance NVDA
* [Translating NVDA](https://github.com/nvaccess/nvda/wiki/Translating): Information about how to translate NVDA into another language
* [NVDA community wiki](https://github.com/nvaccess/nvda-community/wiki): Articles contributed by the community
* [NVDA Controller Client](http://www.nvda-project.org/nvdaControllerClient/nvdaControllerClient_20100219.7z) (2010-02-19): NVDA API for external applications to directly speak or braille messages, etc.
* [NVDA Developer Guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html)
* [Contributing to NVDA](https://github.com/nvaccess/nvda/wiki/Contributing): Guidelines for contributing to the NVDA source code
* [NVDA development email list](https://nvda-devel.groups.io/) ([Old archives](http://nabble.nvda-project.org/Development-f1.html)): Discussion about NVDA development
* [NVDA commits email list](https://lists.sourceforge.net/lists/listinfo/nvda-commits): Notifications for all commits to the Git repository

## Getting the Source Code
The NVDA project uses the [Git](https://www.git-scm.com/) version control system for its source code and documentation.

The NVDA Git repository is located at https://github.com/nvaccess/nvda.git. You can clone it with the following command, which will place files in a directory named `nvda`:

```
git clone --recursive https://github.com/nvaccess/nvda.git
```

The `--recursive` option is needed to retrieve various Git submodules we use.

## Dependencies
The NVDA source depends on several other packages to run correctly.

### Installed Dependencies
The following dependencies need to be installed on your system:

* [Python](https://www.python.org/), version 3.7, 32 bit
	* Use latest minor version if possible.
* Microsoft Visual Studio 2017 Community, Version 15.3 or later:
	* Download from https://visualstudio.microsoft.com/vs/older-downloads/
	* When installing Visual Studio, you need to enable the following:
		On the Workloads tab, in the Windows group:
			* Universal Windows Platform Development
			* Desktop development with C++
		* Then in the Installation details section, under Desktop for C++, Optional grouping, ensure the following are selected:
			* VC++ 2017 v141 toolset (x86,x64)
			* Windows 10 SDK (10.0.17134.0) for Desktop C++ x86 and x64
			* Visual C++ ATL for x86 and x64
		* In the Installation details section, under Individual components, ensure the following are selected:
			* Visual C++ compilers and libraries for ARM64
			* Visual C++ ATL for ARM64


### Git Submodules
Most of the dependencies are contained in Git submodules.
If you didn't pass the `--recursive` option to git clone, you will need to run `git submodule update --init`.
Whenever a required submodule commit changes (e.g. after git pull), you will need to run `git submodule update`.
If you aren't sure, run `git submodule update` after every git pull, merge or checkout.

For reference, the following run time dependencies are included in Git submodules:

* [comtypes](https://github.com/enthought/comtypes), version 1.1.7
* [wxPython](https://www.wxpython.org/), version 4.0.3
* [eSpeak NG](https://github.com/espeak-ng/espeak-ng), version 1.51-dev commit ca65812a
* [Sonic](https://github.com/waywardgeek/sonic), commit 4f8c1d11
* [IAccessible2](https://wiki.linuxfoundation.org/accessibility/iaccessible2/start), commit 21bbb176
* [ConfigObj](https://github.com/DiffSK/configobj), commit 5b5de48
* [Six](https://pypi.python.org/pypi/six), version 1.12.0, required by wxPython and ConfigObj
* [liblouis](http://www.liblouis.org/), version 3.10.0 commit 146c0757
* [Unicode Common Locale Data Repository (CLDR)](http://cldr.unicode.org/) Emoji Annotations, version 36.0
* NVDA images and sounds
* [Adobe Acrobat accessibility interface, version XI](https://download.macromedia.com/pub/developer/acrobat/AcrobatAccess.zip)
* Adobe FlashAccessibility interface typelib
* [MinHook](https://github.com/RaMMicHaeL/minhook), tagged version 1.2.2
* brlapi Python bindings, version 0.7.0 or later, distributed with [BRLTTY for Windows](https://brltty.app/download.html/brltty/), version 4.2-2
* lilli.dll, version 2.1.0.0
* [pySerial](https://pypi.python.org/pypi/pyserial), version 3.4
* [Python interface to FTDI driver/chip](http://fluidmotion.dyndns.org/zenphoto/index.php?p=news&title=Python-interface-to-FTDI-driver-chip)
* Java Access Bridge 32 bit, from Zulu Community OpenJDK build 13.0.1+10Zulu (13.28.11)

Additionally, the following build time dependencies are included in Git submodules:

* [Py2Exe](https://github.com/albertosottile/py2exe/), version 0.9.3.2 commit b372a8e
* [Python Windows Extensions](https://sourceforge.net/projects/pywin32/ ), build 224, required by py2exe
* [txt2tags](https://txt2tags.org/), version 2.5
* [SCons](https://www.scons.org/), version 3.0.4
* [Nulsoft Install System](https://nsis.sourceforge.io/Main_Page/), version 2.51
* [NSIS UAC plug-in](https://nsis.sourceforge.io/UAC_plug-in), version 0.2.4, ansi
* xgettext and msgfmt from [GNU gettext](https://sourceforge.net/projects/cppcms/files/boost_locale/gettext_for_windows/)
* [epydoc](http://epydoc.sourceforge.net/), version 3.0.1 with patch for bug #303
* [Boost Optional (stand-alone header)](https://github.com/akrzemi1/Optional), from commit [3922965](https://github.com/akrzemi1/Optional/commit/3922965396fc455c6b1770374b9b4111799588a9)

### Other Dependencies
To lint using Flake 8 locally using our SCons integration, some dependencies are installed (automatically) via pip.
Although this [must be run manually](#linting-your-changes), developers may wish to first configure a Python Virtual Environment to ensure their general install is not affected.
* Flake8
* Flake8-tabs


The following dependencies aren't needed by most people, and are not included in Git submodules:

* To generate developer documentation for nvdaHelper: [Doxygen Windows installer](http://www.doxygen.nl/download.html), version 1.8.15:
* When you are using Visual Studio Code as your integrated development environment of preference, you can make use of our [prepopulated workspace configuration](https://github.com/nvaccess/vscode-nvda/) for [Visual Studio Code](https://code.visualstudio.com/).
	While this VSCode project is not included as a submodule in the NVDA repository, you can easily check out the workspace configuration in your repository by executing the following from the root of the repository.

	```git clone https://github.com/nvaccess/vscode-nvda.git .vscode```

## Preparing the Source Tree
Before you can run the NVDA source code, you must prepare the source tree.
You do this by opening a command prompt, changing to the root of the NVDA source distribution and typing:

```
scons source
```

You should do this again whenever the version of comtypes changes or language files are added or changed.
Note that if you want to access user documentation from the help menu while running the source version, you will also need to add `user_docs` to the command line like so:

```
scons source user_docs
```

While simply testing or committing changes, it may be faster usually just doing `scons source` as user documentation will change each time the revision number changes.

### Compiling NVDAHelper with Debugging Options
Among other things, preparing the source tree builds the NVDAHelper libraries.
If trying to debug nvdaHelper, you can control various debugging options by building with the `nvdaHelperDebugFlags` and `nvdaHelperLogLevel` command line variables.

The `nvdaHelperLogLevel` variable specifies the level of logging (0-59) you wish to see, lower is more verbose. The default is 15.

The `nvdaHelperDebugFlags` variable takes one or more of the following flags:

* debugCRT: the libraries will be linked against the debug C runtime and assertions will be enabled. (By default, the normal CRT is used and assertions are disabled.)
* RTC: runtime checks (stack corruption, uninitialized variables, etc.) will be enabled. (The default is no runtime checks.)
* analyze: runs MSVC code analysis on all nvdaHelper code, holting on any warning. (default is no analysis).

The special keywords none and all can also be used in place of the individual flags.

An example follows that enables debug CRT and runtype checks 

```
scons source nvdaHelperDebugFlags=debugCRT,RTC
```

Symbol pdb files are always produced when building, regardless of the debug flags.
However, they are not included in the NVDA distribution.
Instead, `scons symbolsArchive` will package them as a separate archive.

By default, builds also do not use any compiler optimizations.
Please see the `release` keyword argument for what compiler optimizations it will enable.

## Running the Source Code
To start NVDA from source code, run `nvda.pyw` located in the source directory.
To view help on the arguments that NVDA will accept, use the `-h` or `--help` option.
These arguments are also documented in the user guide.
Since NVDA is a Windows application (rather than command line), it is best to run it with `pythonw.exe`.
However, if during development you encounter an error early in the startup of NVDA, you can use `python.exe` which is likely to give more information about the error.

## Building NVDA
A binary build of NVDA can be run on a system without Python and all of NVDA's other dependencies installed (as we do for snapshots and releases).

Binary archives and bundles can be created using scons from the root of the NVDA source distribution. To build any of the following, open a command prompt and change to this directory.

To make a non-archived binary build (equivalent to an extracted portable archive), type:

```
scons dist
```

The build will be created in the dist directory.

### Building the installer

To create a launcher archive (one executable allowing for installation or portable dist generation), type:

```
scons launcher
```

The archive will be placed in the output directory.

### Building the developer documentation

To generate the NVDA developer guide, type:

```
scons developerGuide
```

The developer guide will be placed in the `devDocs` folder in the output directory.
Note that the Python 3 sources of NVDA currently do not support building NVDA developer documentation using the `scons devDocs` command.

To generate developer documentation for nvdaHelper (not included in the devDocs target):

```
scons devDocs_nvdaHelper
```

The documentation will be placed in the `devDocs\nvdaHelper` folder in the output directory.

### Generate debug symbols archive
To generate an archive of debug symbols for the various dll/exe binaries, type:

```
scons symbolsArchive
```

The archive will be placed in the output directory.

### Generate translation template
To generate a gettext translation template (for translators), type:

```
scons pot
```

### Customising the build
Optionally, the build can be customised by providing variables on the command line:

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

For example, to build a launcher with a specific version, you might type:

```
scons launcher version=test1
```

For more see the `sconstruct` file.

## Running Automated Tests
If you make a change to the NVDA code, you should run NVDA's automated tests.
These tests help to ensure that code changes do not unintentionally break functionality that was previously working.

To run the tests (unit tests, translatable string checks), first change directory to the root of the NVDA source distribution as above.
Then, run:

```
scons tests
```

### Unit tests
To run only specific unit tests, specify them using the `unitTests` variable on the command line.
The tests should be provided as a comma separated list.
Each test should be specified as a Python module, class or method relative to the `tests\unit` directory.
For example, to run only methods in the `TestMove` and `TestSelection` classes in the file `tests\unit\test_cursorManager.py` file, run this command:

```
scons tests unitTests=test_cursorManager.TestMove,test_cursorManager.TestSelection
```

### Translatable string checks
To run only the translatable string checks (which check that all translatable strings have translator comments), run:

```
scons checkPot
```

### Linting your changes
In order to ensure your changes comply with NVDA's coding style you can run the Flake8 linter locally.
Some developers have found certain linting error messages misleading, these are clarified in `tests/lint/readme.md`.
Running via SCons will use Flake8 to inspect only the differences between your working directory and the specified `base` branch.
If you create a Pull Request, the `base` branch you use here should be the same as the target you would use for a Pull Request. In most cases it will be `origin/master`.
```
scons lint base=origin/master
```

To be warned about linting errors faster, you may wish to integrate Flake8 other development tools you are using.
For more details, see `tests/lint/readme.md`

### System Tests
You may also use scons to run the system tests, though this will still rely on having set up the dependencies (see `tests/system/readme.md`).

```
scons systemTests
```

To run only specific system tests, specify them using the `filter` variable on the command line.
This filter accepts wildcard characters.

```
scons systemTests filter="Read welcome dialog"
```

## Contributing to NVDA

If you would like to contribute code or documentation to NVDA, you can read more information in our [contributing guide](https://github.com/nvaccess/nvda/wiki/Contributing).
