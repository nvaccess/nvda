## NVDA system tests

### Dependencies

The system tests depend on the following:

- Robot Framework
- Robot Remote Server
- PyAutoGui

Which can be installed with `pip`:

```
pip install robotframework
pip install robotremoteserver
pip install pyautogui
```

### Running the tests

These tests should be run from the windows command prompt (cmd.exe).

From the root directory of your NVDA repository, run:

```
python -m robot tests/system/ in CMD.
```