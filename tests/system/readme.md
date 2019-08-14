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
python -m robot --test "name of test here" ...
```

### Getting the results

The process is displayed in the command prompt, for more information consider the
`report.html`, `log.html`, and `output.xml` files. The logs from NVDA are saved to the `nvdaTestRunLogs` folder

### Overview

Robot Framework loads and parses the test files and their libraries. In our case, generally in the 'setup',
NVDA is started as a new process. It uses a sand box profile, and communication with the test code occurs via an
NVDA addon (`systemTestSpy`). The system test should, as much as possible, interact like a user would. For example,
wait for the speech to confirm that an expected dialog is open before taking the next action to interact.

Test code goes in robot files, see the robot framework documentation to understand these.
Large strings or other variables go in a variables.py file paired with the robot file.
The `libraries` directory contains files providing "robot keyword" libraries.
The `nvdaSettingsFiles` directory contains various NVDA config files that are used to construct the NVDA
profile in the `%TEMP%` directory.

### How the test setup works

This section will not go into the details of robot framework, or robot remote server,
these have their own documentation. There are two major libraries used with the system tests:

* `nvdaRobotLib` - Provides keywords which help the test code start and cleanup the NVDA process, including the installation of the `systemTestSpy` addon.
* `systemTestSpy` - Is converted into an addon that is installed in the NVDA profile used with the version of NVDA under test. This provides keywords for getting information out of NVDA. For example getting the last speech.

Helper code in `nvdaRobotLib` is responsible for the construction of the `systemTestSpy` addon.
The addon is constructed as a package from several files:
* `libraries/systemTestSpy.py` becomes `systemTestSpy/__init__.py`
* `libraries/systemTestUtils.py` becomes `systemTestSpy/systemTestUtils.py`
* Files listed in `nvdaRobotLib.requiredPythonImportsForSystemTestSpyPackage` are sourced from locations listed
in the python paths for the instance of python running the robot tests. These are copied to `systemTestSpy/libs/`

An NVDA profile directory is created in the `%TEMP%` directory, the `systemTestSpy` addon is copied
into the `globalPlugins` directory of this NVDA profile. For each test, an NVDA configuration file
is copied into this profile as well. NVDA is started, and points to this profile directory. At the end of the
test the NVDA log is copied to the robot output directory, under the `nvdaTestRunLogs` directory. The log files are
named by suite and test name.