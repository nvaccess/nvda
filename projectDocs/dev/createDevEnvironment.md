## Getting the Source Code
The NVDA project uses the [git](https://www.git-scm.com/) version control system for its source code and documentation.

The NVDA repository is located at https://github.com/nvaccess/nvda.

If you plan on contributing to NVDA, you should [fork and clone](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the repository.

Use the `--recursive` option when performing `git clone` to fetch the required git submodules we use.

### Keeping the fork in sync
When you fork the repository, GitHub will create a copy of the master branch.
However, this branch will not be updated when the nvaccess master branch is updated.
To ensure your work is always based on the latest commit in the nvaccess master branch, it is recommended that your master branch be linked to the nvaccess master branch, rather than the master branch in your GitHub fork.
You can do this from the command line as follows:
```sh
# Add a remote for the NV Access repository.
git remote add nvaccess https://github.com/nvaccess/nvda.git
# Fetch the nvaccess branches.
git fetch nvaccess
# Switch to the local master branch.
git checkout master
# Set the local master to use the nvaccess master as its upstream.
git branch -u nvaccess/master
# Update the local master.
git pull
```

## Supported Operating Systems
Although NVDA can run on any Windows version starting from Windows 8.1, building NVDA from source is currently limited to only Windows 10 and above.

## Dependencies
The NVDA source depends on several other packages to run correctly.

### Installed Dependencies
The following dependencies need to be installed on your system:

#### Python
[Python](https://www.python.org/), version 3.11, 32 bit.

To replicate the production build environment, use the 3.11.x minor version of Python that [AppVeyor uses for the Visual Studio 2022 environment](https://www.appveyor.com/docs/windows-images-software/#python).

#### Microsoft Visual Studio
* Microsoft Visual Studio 2022
	* To replicate the production build environment, use the [version of Visual Studio 2022 that AppVeyor is using](https://www.appveyor.com/docs/windows-images-software/#visual-studio-2022). 
	* When you do not use the Visual Studio IDE itself, you can download the [build tools](https://aka.ms/vs/17/release/vs_BuildTools.exe)
	* When you are intending to use the Visual Studio IDE (not required for NVDA development), you can download [the community version](https://aka.ms/vs/17/release/vs_Community.exe), which is also used by AppVeyor
	* The Professional and Enterprise versions are also supported
	* Preview versions are *not* supported
* When installing Visual Studio, additional components must be included
	* You can automatically fetch these using [NVDAs .vsconfig](../../.vsconfig) using the [import feature of the VS installer](https://learn.microsoft.com/en-us/visualstudio/install/import-export-installation-configurations?view=vs-2022#import-a-configuration)
	* In the list on the Workloads tab, in the Desktop grouping:
		* Desktop development with C++.
			* Once selected, ensure "C++ Clang tools for Windows" is included under the optional grouping.
	* On the Individual components tab, ensure the following items are selected:
		* Windows 11 SDK (10.0.22621.0)
		* MSVC v143 - VS 2022 C++ ARM64/ARM64EC build tools
		* MSVC v143 - VS 2022 C++ x64/x86 build tools
		* C++ ATL for v143 build tools (x86 & x64)
		* C++ ATL for v143 build tools (ARM64/ARM64EC)

### Git Submodules
Some of the dependencies are contained in Git submodules.
If you didn't pass the `--recursive` option to git clone, you will need to run `git submodule update --init`.
Whenever a required submodule commit changes (e.g. after git pull), you will need to run `git submodule update`.
If you aren't sure, run `git submodule update` after every git pull, merge or checkout.

For reference, the following run time dependencies are included in Git submodules:

* [eSpeak NG](https://github.com/espeak-ng/espeak-ng), version 1.52-dev commit `530bf0abf4174dc9ca28dbacc11bd5e9ae6152cd`
* [Sonic](https://github.com/waywardgeek/sonic), commit `8694c596378c24e340c09ff2cd47c065494233f1`
* [IAccessible2](https://wiki.linuxfoundation.org/accessibility/iaccessible2/start), commit `3d8c7f0b833453f761ded6b12d8be431507bfe0b`
* [liblouis](http://www.liblouis.io/), version 3.28.0
* [Unicode Common Locale Data Repository (CLDR)](http://cldr.unicode.org/), version 44.0
* NVDA images and sounds
* [Adobe Acrobat accessibility interface, version XI](https://download.macromedia.com/pub/developer/acrobat/AcrobatAccess.zip)
* [Microsoft Detours](https://github.com/microsoft/Detours), commit `4b8c659f549b0ab21cf649377c7a84eb708f5e68`
* brlapi Python bindings, version 0.8.5 or later, distributed with [BRLTTY for Windows](https://brltty.app/download.html), version 6.6
* lilli.dll, version 2.1.0.0
* Python interface to FTDI driver/chip
* [Nullsoft Install System](https://nsis.sourceforge.io), version 3.08
* [Java Access Bridge 32 bit, from Zulu Community OpenJDK build 17.0.9+8Zulu (17.46.19)](https://github.com/nvaccess/javaAccessBridge32-bin)
* [wil](https://github.com/microsoft/wil/)
* [Microsoft UI Automation Remote Operations Library, forked from @microsoft by @michaeldcurran](https://www.github.com/michaeldcurran/microsoft-ui-uiautomation/)
	* Commit 224b22f3bf9e
	* The fork specifically adds support for CallExtension / IsExtensionSupported to the high-level API, see pr microsoft/microsoft-ui-uiautomation#84 and #95.
* [NVDA DiffMatchPatch](https://github.com/codeofdusk/nvda_dmp)

Additionally, the following build time dependencies are included in the miscDeps git submodule: 

* [txt2tags](https://txt2tags.org/), version 2.5
* xgettext and msgfmt from [GNU gettext](https://sourceforge.net/projects/cppcms/files/boost_locale/gettext_for_windows/)

The following dependencies aren't needed by most people, and are not included in Git submodules:
* To generate [developer documentation for nvdaHelper](#building-nvdahelper-developer-documentation): [Doxygen Windows installer](http://www.doxygen.nl/download.html), version 1.8.15:
* When you are using Visual Studio Code as your integrated development environment of preference, you can make use of our [prepopulated workspace configuration](https://github.com/nvaccess/vscode-nvda/) for [Visual Studio Code](https://code.visualstudio.com/).
	While this VSCode project is not included as a submodule in the NVDA repository, you can easily check out the workspace configuration in your repository by executing the following from the root of the repository.

	```sh
	git clone https://github.com/nvaccess/vscode-nvda.git .vscode
	```

### Python dependencies
NVDA and its build system also depend on an extensive list of Python packages. They are all listed with their specific versions in the requirements.txt file in the root of this repository. However, the build system takes care of fetching these itself when needed. These packages will be installed into an isolated Python virtual environment within this repository, and will not affect your system-wide set of packages.
