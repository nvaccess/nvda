# Build System Notes
A Python virtual environment is used transparently by the NVDA build system,
and all Python dependencies are installed into this environment using `pip`.

NVDA's build system commands will handle all aspects of the virtual environment.
Developers should not create or activate the virtual environment manually, unless
working on the build system itself.

For the documentation on how to _use_ the build system (E.G. building,
running NVDA or tests) see the main repository readme file.

## How the build system works

The virtual environment system used is `venv`.
Dependencies are installed with `pip` via the `requirements.txt` file.
Version numbers for dependencies should be used to lock in a version.

The virtual environment is recreated if it is outdated, either due to:
- Python version.
- `pip` requirements.

The user is consulted before modifying / removing a virtual environment that can't be identified
as having been created by NVDA's build system.

### Entry points to the build system

These are the only files expected to be executed directly by a user/developer:
- `scons.bat`
- `runnvda.bat`
- `rununittests.bat`
- `runsystemtests.bat`
- `runlint.bat`

**Note:** The `runnvda.bat` script intentionally uses `pyw.exe` to run NVDA as
this is the more common and expected way to run NVDA.
Run NVDA with `py.exe` in order to have standard output/error output to the console.
This is particularly useful if there is an error in NVDA before logging is initialised.
To do this, modify the `runnvda.bat` file.

**Note:** Executing `source/nvda.pyw` outside of a virtual environment will produce an error message
and early termination.

### Main implementation files:
The following files contain the main implementation of the virtual environment setup.

#### `venvUtils/ensureAndActivate.bat`
   - Activates the virtual environment.
   - If necessary, creates and configures it first. 
   - The virtual environment is left active. 
#### `venvUtils/venvCmd.bat`
  - Uses `ensureAndActivate.bat` to run a command within the context
   of the virtual environment. 
  - The virtual environment is deactivated after the command
   completes.
  - All entry point scripts depend on this.
#### `venvUtils/ensureVenv.py`
- Does the actual work to create and configure the virtual
   environment.

## Motivation for using virtual environments

Ensures the build environment is clean, and there are no conflicts with other installed packages.

NVDA and its build system have many Python dependencies.
Using `pip` and a virtual environment means:
- Updating is easier than git submodules.
  E.G. wxPython no longer has to be pre-built and stored in our bin repo.
- Developers need to sync/update their submodules less often.
- More consistency for dependencies.
- IDE's can be configured more easily.
- No conflict between NVDA dependencies and Python packages already installed globally on the
  developer's system.
- Don't interfere with the developer's system. Installing packages globally may break things
  outside of NVDA.
