A Python virtual environment is used transparently by the NVDA build system, and all Python dependencies are installed into this environment using `pip`.

NVDA's build system commands will handle all aspects of the virtual environment.
Developers should not create or activate the virtual environment manually, unless working on the build system itself.

* To build NVDA, SCons should continue to be used in the usual way. E.g. executing scons.bat in the root of the repository. Running `py -m SCons`  is no longer supported, and scons.py has also been removed. 
* To run NVDA from source, rather than executing `source/nvda.pyw` directly, the developer should now use `runnvda.bat` in the root of the repository. `runnvda.bat` uses `pythonw.exe` internally to execute NVDA. If you do try to execute `source/nvda.pyw`, a message box will alert you this is no longer supported.
* To perform unit tests, execute `rununittests.bat [<extra unittest discover options>]`
* To perform system tests: execute `runsystemtests.bat [<extra robot options>]`
* To perform linting, execute `runlint.bat <base branch>`

Behind the scenes, the above batch files (`scons`, `runnvda`, `rununittests`, `runsystemtests` and `runlint`) ensure that the Python virtual environment is created and up to date, activates the environment, runs the command and then deactivates. All transparently. A developer should not have to know about the Python virtual environment at all.
The first time one of these commands are run, the virtual environment will be created, and all required Python dependencies will be installed with `pip`. You can see the entire list of packages and their exact versions that `pip` will use, in `requirements.txt` in the root of the repository.

`venvUtils/ensureVenv.py` contains the logic to check for, create and update the virtual environment.
If a previous virtual environment exists but has a miss-matching Python version or pip package requirements have changed, The virtual environment is recreated with the updated version of Python and packages.
If a virtual environment is found but does not seem to be ours, the user is asked if it should be overwritten or not.
This script also detects if it is being run from an existing 3rd party Python virtual environment and aborts if so. thus, it is impossible to execute SCons or NVDA from source within another Python virtual environment.

`venvUtils/ensureAndActivate.bat` can be used to ensure the virtual environment exists and is up to date, and then activates it in the current shell, ready for other commands to be executed in the context of NVDA's build system Python virtual environment. this would never normally be executed by itself, though appVeyor uses it at the beginning of its execution and leaves the environment active for the remainder of its execution.

`venvUtils/venvCmd.bat` is a script that runs a single command within the context of the NVDA build system Python virtual environment. It ensures and activates the environment, executes the command, and then deactivates the environment. this script is what all the high-level batch files use internally. 

SConstruct, and `source/nvda.pyw` both contain logic that detects the NVDA build system Python virtual environment, and abort if it is not active.
