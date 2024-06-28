## Running Automated Tests
If you make a change to the NVDA code, you should run NVDA's automated tests.
These tests help to ensure that code changes do not unintentionally break functionality that was previously working.

To run the tests (unit tests, translatable string checks), first change directory to the root of the NVDA source distribution as above.
Then, run:

```cmd
scons tests
```

### Unit tests
To run only specific unit tests, specify them using the `unitTests` variable on the command line.
The tests should be provided as a comma-separated list.
Each test should be specified as a Python module, class or method relative to the `tests\unit` directory.
For example, to run only methods in the `TestMove` and `TestSelection` classes in the file `tests\unit\test_cursorManager.py` file, run this command:

```cmd
scons tests unitTests=test_cursorManager.TestMove,test_cursorManager.TestSelection
```

### Translatable string checks
To run only the translatable string checks (which check that all translatable strings have translator comments), run:

```cmd
scons checkPot
```

### Linting your changes

In order to ensure your changes comply with NVDA's coding style you can run the Ruff linter locally.
`runlint.bat` will use Ruff to lint and where possible, fix the code you have written.

```cmd
runlint.bat
```

To be warned about linting errors faster, you may wish to integrate Ruff with other development tools you are using.
For more details, see the [linting docs](../dev/lint.md).

### Unit Tests
Unit tests can be run with the `rununittests.bat` script.
Internally this script uses the Nose Python test framework to execute the tests.
Any arguments given to `rununittests.bat` are forwarded onto Nose.
Please refer to Nose's own documentation on how to filter tests etc.

### System Tests
System tests can be run with the `runsystemtests.bat --include <TAG>` script.
To run all tests standard tests for developers use `runsystemtests.bat --include NVDA`.
Internally this script uses the Robot test framework to execute the tests.
Any arguments given to `runsystemtests.bat` are forwarded onto Robot.
For more details (including filtering and exclusion of tests) see `tests/system/readme.md`.
