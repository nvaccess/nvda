# Build System Notes

The NVDA build system uses [uv](https://docs.astral.sh/uv/) to manage a Python virtual environment.
All Python dependencies are installed into this environment.

All aspects of the virtual environment are either handled by NVDA's build system commands, or by uv.
Developers should not create or activate the virtual environment manually.

For the documentation on how to _use_ the build system (E.G. building,
running NVDA or tests) see the main repository readme file.

## How the build system works

Dependencies are managed in the `pyproject.toml` file.
Version numbers for dependencies should be used to lock in a version.

### Entry points to the build system

These are the only files expected to be executed directly by a user/developer:

* `scons.bat`
* `runnvda.bat`
* `rununittests.bat`
* `runsystemtests.bat`
* `runlint.bat`
* `runlicensecheck.bat`

**Note:** The `runnvda.bat` script uses `uv run`, which executes `nvda.pyw` as a GUI application by default.
This is the more common and expected way to run NVDA.
You can override this behavior by passing `-s` as a parameter to `uv run`.
To do this, modify the `runnvda.bat` file.
This allows you to have standard output/error output to the console, which is particularly useful if there is an error in NVDA before logging is initialised.

**Note:** Executing `source/nvda.pyw` outside uv will produce an error message
and early termination.

## Motivation for using uv

Ensures the build environment is clean, and there are no conflicts with other installed packages.

NVDA and its build system have many Python dependencies.
Using `uv` means:

* Updating is easier than git submodules.
* Developers need to sync/update their submodules less often.
* More consistency for dependencies.
* IDE's can be configured more easily, for NVDA development as well as for development of add-ons.
* No conflict between NVDA dependencies and Python packages already installed globally on the
  developer's system.
* Don't interfere with the developer's system. Installing packages globally may break things
  outside of NVDA.
