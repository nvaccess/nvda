## NVDA system tests

### Dependencies

To install all required packages move to the root directory of this repo and execute:

`python -m pip install -r tests/system/requirements.txt`

### Running the tests

These tests should be run from the windows command prompt (cmd.exe) from the root directory
 of your NVDA repository.


```
python -m robot --loglevel DEBUG -d testOutput/system -x systemTests.xml -v whichNVDA:source -P ./tests/system/libraries ./tests/system/
```

The `whichNVDA` argument allows the tests to be run against an installed copy
of NVDA (first ensure it is compatible with the tests). Note valid values are:
* "installed" - when running against the installed version of NVDA, you are likely to get errors in the log unless
the tests are run from an administrator command prompt.
* "source"

To run a single test or filter tests, use the `--test` argument (wildcards accepted).
Refer to the robot framework documentation for further details.

```
python -m robot --test "starts" ...
```

There are several other options for choosing which tests to run (e.g. by suite, tag, etc).
Consult `python -m robot --help` for more options.

### Getting the results

The process is displayed in the command prompt, for more information consider the [Robot report and NVDA logs](#logs)
`report.html`, `log.html`, and `output.xml` files.
The logs from NVDA are saved to the `nvdaTestRunLogs` folder

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
