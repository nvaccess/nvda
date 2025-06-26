# Building NVDA

Before building NVDA, [create your developer environment](./createDevEnvironment.md).

## Preparing the Source Tree

Before you can run the NVDA source code, you must prepare the source tree.
You do this by opening a command prompt, changing to the root of the NVDA source distribution and typing:

```cmd
scons source
```

You should do this again whenever the version of comtypes changes or language files are added or changed.
Note that if you want to access user documentation from the help menu while running the source version, you will also need to add `user_docs` to the command line like so:

```cmd
scons source user_docs
```

While simply testing or committing changes, it may be faster usually just doing `scons source` as user documentation will change each time the revision number changes.

You can speed up scons calls by appending the following CLI parameters:

- `-j N`, where `N` is the number of cores to use while building
- `--all-cores` to use all cores.

However note that building across cores can cause errors, and output will be scrambled.

```cmd
scons source --all-cores
scons checkPot -j 1
```

If you are experiencing errors building NVDA with threading enabled, please force a serial build with the `-j 1` parameter.
This will make tracking down the issue much easier, and may even resolve it.

## Running the Source Code

It is possible to run NVDA directly from source without having to build the full binary package and launcher.
To launch NVDA from source, using `cmd.exe`, execute `runnvda.bat` in the root of the repository.

To view help on the arguments that NVDA will accept, use the `-h` or `--help` option.
These arguments are also documented in the [user guide](https://download.nvaccess.org/documentation/userGuide.html#CommandLineOptions).

## Making Binary Builds

A binary build of NVDA can be run on a system without Python and all of NVDA's other dependencies installed (as we do for snapshots and releases).

Binary archives and bundles can be created using scons from the root of the NVDA source distribution. To build any of the following, open a command prompt and change to that directory.

### Building without Archiving

To make a non-archived binary build (equivalent to an extracted portable archive), type:

```cmd
scons dist
```

The build will be created in the dist directory.

### Building the installer

To create a launcher archive (one executable allowing for installation or portable dist generation), type:

```cmd
scons launcher
```

The archive will be placed in the output directory.

### Building developer documentation

Refer to [building developer documentation](./buildingDevDocumentation.md).

### Generate debug symbols archive

To generate an archive of debug symbols for the various dll/exe binaries, type:

```cmd
scons symbolsArchive
```

The archive will be placed in the output directory.

### Generate translation template

To generate a gettext translation template (for translators), type:

```cmd
scons pot
```

### Customising the build

Optionally, the build can be customised by providing variables on the command line.
This is useful when [creating a self signed build](./selfSignedBuild.md).

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

```cmd
scons launcher version=test1
```

For more see the [sconstruct file](../../sconstruct).
