## NVDA system tests

### Dependencies

To install all required packages move to the root directory of this repo and execute:

`python -m pip install -r tests/system/requirements.txt`

### Running the tests

You can run the tests with `scons` or manually

#### Scons (easier)
`scons systemTests`

To run only specific system tests,
 specify them using the `filter` variable on the command line.
This filter accepts wildcard characters.

```
scons systemTests filter="Read welcome dialog"
```

#### Manually (faster)

SCons takes quite a long time to initialize and actually start running the tests,
if you are running the tests repeatedly consider running them manually.
These tests should be run from the windows command prompt (cmd.exe) from the root directory
 of your NVDA repository.

```
python -m robot --argumentfile ./tests/system/robotArgs.robot ./tests/system/robot
```
Note that the path to the tests directory is required and must be the final argument.

To run a single test, add the `--test` argument (wildcards accepted).

```
python -m robot --test "starts" ...
```

Other options exit for specifying tests to run (e.g. by suite, tag, etc).
Consult `python -m robot --help`

### Getting the results

The process is displayed in the command prompt, for more information consider the [Robot report and NVDA logs](#logs)
`report.html`, `log.html`, and `output.xml` files.
The logs from NVDA are saved to the `nvdaTestRunLogs` folder

### Excluding tests

Tests can be excluded by adding the tag `excluded_from_build` EG:

```robot
checkbox labelled by inner element
	[Documentation]	A checkbox labelled by an inner element should not read the label element twice.
	# Excluded due to intermittent failure.
	[Tags]	excluded_from_build
	checkbox_labelled_by_inner_element
```

When the tests are run, the option `--exclude excluded_from_build` is given to Robot.
See [description of test args](#test-args)

### Test args
Common arguments (for both `scons` and AppVeyor) are kept in the `tests\system\robotArgs.robot` file.

The `whichNVDA` argument allows the tests to be run against an installed copy
of NVDA (first ensure it is compatible with the tests). Note valid values are:
* "installed" - when running against the installed version of NVDA, you are likely to get errors in the log unless
the tests are run from an administrator command prompt.
* "source"

### Overview

Robot Framework loads and parses the test files and their libraries.
In our case, generally in the 'setup', NVDA is started as a new process.
It uses a sand box profile, and communication with the test code occurs via a global plugin and synth driver.
 The system test should, as much as possible, interact like a user would.
 For example, wait for the speech to confirm that an expected dialog is open before taking the next action to interact.

Test declarations go in robot files, these should just specify the name and metadata for the test.
Several issues with the robot language mean it's easier to write the test logic in an accompanying python file.

The `libraries` directory contains files providing "robot keyword" libraries.
Most notably, the NvdaLib library contains methods for starting NVDA and speech can be retrieved via the `NVDASpyLib` returned by the module function `getSpyLib()` which is a remote library.
The `nvdaSettingsFiles` directory contains various NVDA config files that are used to construct the NVDA profile in the `%TEMP%` directory.

### How the test setup works

This section will not go into the details of robot framework, or robot remote server,
these have their own documentation.
An overview of the files:
- The `SystemTestSpy` package is responsible for setting up the global plugin and synth driver.
- `libraries/NvdaLib` abstracts the setup and running / exiting of NVDA.
- `speechSpyGlobalPlugin` module creates a RobotFramework Remote Server which gets connected to via the `NvdaLib` library. To make running remote functions easier, methods are created on the remote spy instance which wrap calls to `run_keyword`.

An NVDA sandbox profile is setup in the `%TEMP%` directory like so:
- `nvdaProfile/`
  - `nvda.ini` copied from `nvdaSettingsFiles`
  - `scratchpad/`
    - `globalPlugins/speechSpyGlobalPlugin/`
      - `__init__.py` copied from `speechSpyGlobalPlugin.py`
      - `blockUntilConditionMet.py`
      - `libs/`
        - `xmlrpc` from Python install
        - `robotRemoteServer.py` from Python install
        - Any other dependencies required.
    - `synthDrivers/`
      - `speechSpySynthDriver.py`

For each test, the NVDA configuration file is overwritten.
NVDA is started with the `-c` option to specify this profile directory to be used for config.

### Logs
Both Robot Framework and NVDA logs are captured in the `testOutput` directory in the repo root.
NVDA logs (NVDA log, stdOut, and stdErr for each test) are under the `nvdaTestRunLogs` directory. 
The log files are named by suite and test name.
