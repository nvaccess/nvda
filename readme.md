# NVDA

NVDA (NonVisual Desktop Access) is a free, open source screen reader for Microsoft Windows.
It is developed by NV Access in collaboration with a global community of contributors.
To learn more about NVDA or download a copy, visit the main [NV Access](http://www.nvaccess.org/) website.

Please note: the NVDA project has a [Citizen and Contributor Code of Conduct](CODE_OF_CONDUCT.md). NV Access expects that all contributors and other community members will read and abide by the rules set out in this document while participating or contributing to this project.

## Get support
Whether you are a beginner, an advanced user, a new or a long time developer; or if you represent an organization wishing to know more or to contribute to NVDA: you can get support through the included documentation as well as several communication channels dedicated to the NVDA screen reader. Here is an overview of the most important support sources.

### Documentation
* [NVDA User Guide](https://www.nvaccess.org/files/nvda/documentation/userGuide.html)
* [NVDA Developer Guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html)
* [NVDA Add-ons Development Internals](https://github.com/nvdaaddons/DevGuide/wiki)
* [NVDA ControllerClient manual (NVDA API for external applications to directly speak or braille messages, etc.)](https://github.com/nvaccess/nvda/tree/master/extras/controllerClient)
* Further documentation is available in the NVDA repository's [Wiki](https://github.com/nvaccess/nvda/wiki), and in the [Community Wiki](https://github.com/nvaccess/nvda-community/wiki)

### Communication channels
* [NVDA Users Mailing List](https://nvda.groups.io/g/nvda)
* [NVDA Developers Mailing List](https://groups.io/g/nvda-devel)
* [NVDA Add-ons Mailing List](https://groups.io/g/nvda-addons)
* [Instant Messaging channel for NVDA Support](https://gitter.im/nvaccess/NVDA)
* [Other sources including groups and profiles on social media channels, language specific websites and mailing lists etc.](https://github.com/nvaccess/nvda-community/wiki/Connect)

You can also get  direct support from NV Access. See the [NV Access](http://www.nvaccess.org/) website for more details.

## Other Key Project Links
* [NVDA on GitHub](https://github.com/nvaccess/nvda)
* [NVDA issues on GitHub](https://github.com/nvaccess/nvda/issues): Bug reports, feature requests, etc.
* [NVDA development snapshots](https://www.nvaccess.org/files/nvda/snapshots/): Automatically generated builds of the project in its current state of development
* [NVDA add-ons](https://addons.nvda-project.org/): Get add-ons to enhance NVDA
* [NVDA Add-ons coordination and support center](https://github.com/nvdaaddons): all about NVDA's addons environment
* [NVDA Add-ons Template](https://github.com/nvdaaddons/AddonTemplate): A repository for generating the Add-ons template
* [Translating NVDA](https://github.com/nvaccess/nvda/wiki/Translating): Information about how to translate NVDA into another language
* [Contributing to NVDA](https://github.com/nvaccess/nvda/wiki/Contributing): Guidelines for contributing to the NVDA source code
* [NVDA commits email list](https://lists.sourceforge.net/lists/listinfo/nvda-commits): Notifications for all commits to the Git repository
* [Old email archives](http://nabble.nvda-project.org/Development-f1.html): contain discussions about NVDA development

## Getting the Source Code
The NVDA project uses the [Git](https://www.git-scm.com/) version control system for its source code and documentation.

The NVDA Git repository is located at https://github.com/nvaccess/nvda.git. You can clone it with the following command, which will place files in a directory named `nvda`:

```
git clone --recursive https://github.com/nvaccess/nvda.git
```

The `--recursive` option is needed to retrieve various Git submodules we use.

## Supported Operating Systems
Although NVDA can run on any Windows version starting from Windows 7 Service pack 1, building NVDA from source is currently limited to only Windows 10 and above.

## Dependencies
The NVDA source depends on several other packages to run correctly.

### Installed Dependencies
The following dependencies need to be installed on your system:

* [Python](https://www.python.org/), version 3.7, 32 bit
	* Use latest minor version if possible.
* Microsoft Visual Studio 2019 or 2022:
	* To replicate the production build environment, use the [version of Visual Studio 2019 that AppVeyor is using](https://www.appveyor.com/docs/windows-images-software/#visual-studio-2019). 
		* When you do not use the Visual Studio IDE itself, you can download the [build tools](https://aka.ms/vs/16/release/vs_BuildTools.exe)
		* When you are intending to use the Visual Studio IDE (not required for NVDA development), you can download [the community version](https://aka.ms/vs/16/release/vs_Community.exe), which is also used by appveyor
		* The Professional and Enterprise versions are also supported
		* Preview versions are *not* supported
		* Building with Visual Studio 2022 explicitly requires the MSVC v142 - VS 2019 C++ build tools to be installed (see below)
	* When installing Visual Studio, you need to enable the following:
		* In the list  on the Workloads tab
			* in the Windows grouping:
				* Desktop development with C++
			* Then in the Installation details tree view, under Desktop for C++, Optional, ensure the following are selected:
				* MSVC v142 - VS 2019 C++ x64/x86 build tools
				* Windows 11 SDK (10.0.22000.0)
				* C++ ATL for v142 build tools (x86 & x64)
				* C++ Clang tools for Windows
		* On the Individual components tab, ensure the following items are selected:
			* MSVC v142 - VS 2019 C++ ARM64 build tools
			* C++ ATL for v142 build tools (ARM64)


### Git Submodules
Some of the dependencies are contained in Git submodules.
If you didn't pass the `--recursive` option to git clone, you will need to run `git submodule update --init`.
Whenever a required submodule commit changes (e.g. after git pull), you will need to run `git submodule update`.
If you aren't sure, run `git submodule update` after every git pull, merge or checkout.

For reference, the following run time dependencies are included in Git submodules:

* [eSpeak NG](https://github.com/espeak-ng/espeak-ng), version 1.51-dev commit 7e5457f91e10
* [Sonic](https://github.com/waywardgeek/sonic), commit 4f8c1d11
* [IAccessible2](https://wiki.linuxfoundation.org/accessibility/iaccessible2/start), commit cbc1f29631780
* [liblouis](http://www.liblouis.org/), version 3.21.0
* [Unicode Common Locale Data Repository (CLDR)](http://cldr.unicode.org/), version 41.0
* NVDA images and sounds
* [Adobe Acrobat accessibility interface, version XI](https://download.macromedia.com/pub/developer/acrobat/AcrobatAccess.zip)
* [Microsoft Detours](https://github.com/microsoft/Detours), commit 45a76a3
* brlapi Python bindings, version 0.8 or later, distributed with [BRLTTY for Windows](https://brltty.app/download.html), version 6.1
* lilli.dll, version 2.1.0.0
* [Python interface to FTDI driver/chip](http://fluidmotion.dyndns.org/zenphoto/index.php?p=news&title=Python-interface-to-FTDI-driver-chip)
* [Nullsoft Install System](https://nsis.sourceforge.io), version 3.08
* Java Access Bridge 32 bit, from Zulu Community OpenJDK build 13.0.1+10Zulu (13.28.11)
* [Microsoft UI Automation Remote Operations Library, forked from @microsoft by @michaeldcurran](https://www.github.com/michaeldcurran/microsoft-ui-uiautomation/)
	* Commit 224b22f3bf9e
	* The fork specifically adds support for  CallExtension / IsExtensionSupported to the high-level API, see pr microsoft/microsoft-ui-uiautomation#84.

Additionally, the following build time dependencies are included in the miscDeps git submodule: 

* [txt2tags](https://txt2tags.org/), version 2.5
* xgettext and msgfmt from [GNU gettext](https://sourceforge.net/projects/cppcms/files/boost_locale/gettext_for_windows/)

The following dependencies aren't needed by most people, and are not included in Git submodules:
* To generate developer documentation for nvdaHelper: [Doxygen Windows installer](http://www.doxygen.nl/download.html), version 1.8.15:
* When you are using Visual Studio Code as your integrated development environment of preference, you can make use of our [prepopulated workspace configuration](https://github.com/nvaccess/vscode-nvda/) for [Visual Studio Code](https://code.visualstudio.com/).
	While this VSCode project is not included as a submodule in the NVDA repository, you can easily check out the workspace configuration in your repository by executing the following from the root of the repository.

	```git clone https://github.com/nvaccess/vscode-nvda.git .vscode```

### Python dependencies
NVDA and its build system also depend on an extensive list of Python packages. They are all listed with their specific versions in the requirements.txt file in the root of this repository. However, the build system takes care of fetching these itself when needed. These packages will be installed into an isolated Python virtual environment within this repository, and will not affect your system-wide set of packages.
 
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
It is possible to run NVDA directly from source without having to build the full binary package and launcher.
To launch NVDA from source, using `cmd.exe`, execute `runnvda.bat` in the root of the repository.

To view help on the arguments that NVDA will accept, use the `-h` or `--help` option.
These arguments are also documented in the user guide.

## Building NVDA
A binary build of NVDA can be run on a system without Python and all of NVDA's other dependencies installed (as we do for snapshots and releases).

Binary archives and bundles can be created using scons from the root of the NVDA source distribution. To build any of the following, open a command prompt and change to that directory.

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

To generate the HTML-based source code documentation, type:

```
scons devDocs
```

The documentation will be placed in the `NVDA` folder in the output directory.

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
runlint.bat  will use Flake8 to inspect only the differences between your working directory and the specified `base` branch.
If you create a Pull Request, the `base` branch you use here should be the same as the target you would use for a Pull Request. In most cases it will be `origin/master`.
```
runlint origin/master
```

To be warned about linting errors faster, you may wish to integrate Flake8 with other development tools you are using.
For more details, see `tests/lint/readme.md`

### Unit Tests
Unit tests can be run with the `rununittests.bat` script.
Internally this script uses the Nose Python test framework to execute the tests.
Any arguments given to rununittests.bat are forwarded onto Nose.
Please refer to Nose's own documentation on how to filter tests etc.

### System Tests
System tests can be run with the `runsystemtests.bat` script.
Internally this script uses the Robot  test framework to execute the tests.
Any arguments given to runsystemtests.bat are forwarded onto Robot.
For more details (including filtering and exclusion of tests) see `tests/system/readme.md`.

## Contributing to NVDA

If you would like to contribute code or documentation to NVDA, you can read more information in our [contributing guide](https://github.com/nvaccess/nvda/wiki/Contributing).
