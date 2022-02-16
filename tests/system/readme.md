## NVDA system tests

### Dependencies

This build system uses the Robot test framework to execute the system tests.
Dependencies such as Robot are automatically installed for you when NVDA's build system Python virtual environment is set up, when running any of the high-level commands such as runsystemtests.bat, thus a developer should usually not have to worry about dependencies.
 
### Running the tests

You can run the tests with `runsystemtests.bat`.
Running this script with no arguments will run all system tests found in tests\system\robot, against the current source copy of NVDA.
Any extra arguments provided to this script are forwarded on to Robot.

To run a single test, add the `--test` argument (wildcards accepted).

```
runsystemtests --test "starts" ...
```

To run all tests with a particular tag use `-i`:
```
runsystemtests -i "chrome" ...
```

Other options exit for specifying tests to run (e.g. by suite, tag, etc).
Consult `runsystemtests --help`

### Getting the results

The process is displayed in the command prompt, for more information consider the [Robot report and NVDA logs](#logs)
`report.html`, `log.html`, and `output.xml` files.
The logs from NVDA are saved to the `nvdaTestRunLogs` folder

### Excluding tests

It is possible to exclude/disable a flaky test, i.e. intermittent test failures, or a test that needs
to be disabled until there is time to investigate.
Add the tag `excluded_from_build` EG:

```robot
checkbox labelled by inner element
	[Documentation]	A checkbox labelled by an inner element should not read the label element twice.
	# Excluded due to intermittent failure.
	[Tags]	excluded_from_build
	checkbox_labelled_by_inner_element
```

When the tests are run, the option `--exclude excluded_from_build` is given to Robot internally.
See [description of test args](#test-args)

### Test args
Common arguments are kept in the `tests\system\robotArgs.robot` file.

The `whichNVDA` argument allows the tests to be run against an installed copy
of NVDA (first ensure it is compatible with the tests). Note valid values are:
* "installed" - when running against the installed version of NVDA, you are likely to get errors in the log unless
the tests are run from an administrator command prompt.
* "source"

The `installDir` argument performs a smoke test on the installation process given a path to the installer exe. For example `--variable installDir:".\path\to\nvda_installer.exe"`.
This should be used with `--variable whichNVDA:installed --include installer`.

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

### Comparing changes to NVDA Settings
`.\runsettingsdiff.bat` is a tool used to compare the settings dialog by reading text and generating screenshots for comparison.  The default behaviour is to run using the source code and output to `.\tests\system\settingsCache\source`. 


#### Usage
To check for unreleased changes to the settings dialogs, one can use this tool to compare against two copies of NVDA. 

The following arguments should be used with the script.

Default arguments used are stored  in `.\tests\system\guiDiff.robot`

- `--variable whichNVDA:[installed|source]` to decide where to run NVDA from
- `--variable cacheFolder:[filePath]` screenshots and text files of each settings panel are generated in `$cacheFolder\$currentVersion`
- `--variable currentVersion:[nvdaVersion]` where `[nvdaVersion]` is used to name the generated screenshot and cache folder
- `--variable compareVersion:[nvdaVersion]` using a `$nvdaVersion` that this script has already been run against, run the system tests and fail if there are differences between the read text. This generates a multiline diff. 

#### Example usage to compare settings between NVDA 2020.4 and the current source

1. Install NVDA 2020.4
1. Run `.\runsettingsdiff.bat -v whichNVDA:installed -v currentVersion:2020.4`
1. Run `.\runsettingsdiff.bat -v whichNVDA:source -v currentVersion:source -v compareVersion:2020.4`
   - The test will fail and display a diff of any read changes
1. Use a diff tool to compare folders:
   - `diff ./tests/system/settingsCache/2020.4 ./tests/system/settingsCache/source`
   - [ImageMagick Compare](https://imagemagick.org/script/compare.php) can be used to compare images
