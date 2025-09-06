# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os as _os
import re as _re
import shutil as _shutil
import tempfile as _tempfile
import json as _json
from robot.libraries.BuiltIn import BuiltIn as _BuiltIn
from SystemTestSpy import _blockUntilConditionMet, _getLib
from SystemTestSpy.windows import (
	CloseWindow as _CloseWindow,
	GetWindowWithTitle as _GetWindowWithTitle,
	SetForegroundWindow as _SetForegroundWindow,
	Window as _Window,
	windowWithHandleExists as _windowWithHandleExists,
)
import NvdaLib as _NvdaLib

from robot.libraries.Process import Process as _ProcessLib
import WindowsLib as _WindowsLib

_builtIn: _BuiltIn = _BuiltIn()
_process: _ProcessLib = _getLib("Process")
_windowsLib: _WindowsLib = _getLib("WindowsLib")

_LAUNCHER_PATHS = [
	_os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
	_os.path.expandvars(r"C:\Program Files\Microsoft VS Code\Code.exe"),
	_os.path.expandvars(r"%ProgramFiles%\Microsoft VS Code\Code.exe"),
	_os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft VS Code\Code.exe"),
]
_LAUNCHER_CMDS = [
	_os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd"),
	"code",
]
_WINDOW_TITLE_PATTERN = _re.compile(r"Visual Studio Code", _re.IGNORECASE)


class VSCodeLib:
	_testTempDir: str | None = None
	_codeWindow: _Window | None = None
	_processRFHandleForStart: int | None = None

	@staticmethod
	def _findCodeLauncher() -> str:
		for p in _LAUNCHER_PATHS:
			if _os.path.isfile(p):
				return f'"{p}"'
		for candidate in _LAUNCHER_CMDS:
			resolved = _shutil.which(candidate)
			if resolved:
				return f'"{resolved}"'
		raise AssertionError("Visual Studio Code launcher not found. Is it installed?")

	def start_vscode(self) -> _Window:
		launcher = self._findCodeLauncher()
		if VSCodeLib._testTempDir is None:
			VSCodeLib._testTempDir = _tempfile.mkdtemp(prefix="nvdatest")
		userDataDir = _os.path.join(VSCodeLib._testTempDir, "vscodeUserData")
		_os.makedirs(userDataDir, exist_ok=True)

		# Prepare user settings to suppress welcome/startup screen
		userSettingsDir = _os.path.join(userDataDir, "User")
		_os.makedirs(userSettingsDir, exist_ok=True)
		settingsPath = _os.path.join(userSettingsDir, "settings.json")
		try:
			if not _os.path.isfile(settingsPath):
				with open(settingsPath, "w", encoding="utf-8") as cam:
					_json.dump(
						{
							"editor.accessibilitySupport": "on",
							"workbench.startupEditor": "none",
							"update.showReleaseNotes": False,
							"workbench.tips.enabled": False,
							"update.mode": "none",
							"telemetry.telemetryLevel": "off",
						},
						cam,
						ensure_ascii=False,
						indent=2,
					)
		except Exception as e:
			_builtIn.log(
				f"Failed to prepare Visual Studio Code settings to skip welcome screen: {e!r}",
				level="WARN",
			)

		cmd = (
			f'start "" /wait {launcher} '
			f'--user-data-dir "{userDataDir}" '
			f"--disable-gpu "
			f"--disable-extensions "
			f"--disable-workspace-trust "
			f"--skip-add-to-recently-opened "
			f"-n "
			f"--wait"
		)
		_builtIn.log(f"Starting Visual Studio Code: {cmd}", level="DEBUG")
		VSCodeLib._processRFHandleForStart = _process.start_process(
			cmd,
			shell=True,
			alias="vscodeStartAlias",
		)

		success, VSCodeLib._codeWindow = _blockUntilConditionMet(
			getValue=lambda: _GetWindowWithTitle(
				_WINDOW_TITLE_PATTERN,
				lambda m: _builtIn.log(m, level="DEBUG"),
			),
			giveUpAfterSeconds=15.0,
			shouldStopEvaluator=lambda w: w is not None,
			intervalBetweenSeconds=0.5,
			errorMessage="Unable to get Visual Studio Code window",
		)
		if not success or VSCodeLib._codeWindow is None:
			_builtIn.fatal_error("Unable to get Visual Studio Code window")

		_windowsLib.taskSwitchToItemMatching(targetWindowNamePattern=_WINDOW_TITLE_PATTERN)
		_windowsLib.logForegroundWindowTitle()
		_NvdaLib.getSpyLib().wait_for_speech_to_finish()
		return VSCodeLib._codeWindow

	def close_vscode(self):
		window = VSCodeLib._codeWindow or _GetWindowWithTitle(
			_WINDOW_TITLE_PATTERN,
			lambda m: _builtIn.log(m, level="DEBUG"),
		)
		if not window:
			_builtIn.log("No Visual Studio Code window handle to close.", level="WARN")
			return

		_CloseWindow(window)
		success, _ = _blockUntilConditionMet(
			getValue=lambda: not _windowWithHandleExists(window.hwndVal),
			giveUpAfterSeconds=10.0,
			shouldStopEvaluator=lambda x: bool(x),
			intervalBetweenSeconds=0.5,
		)

		if not success:
			_builtIn.log("Window still present after WM_CLOSE, trying Alt+F4.", level="WARN")
			try:
				_SetForegroundWindow(window, lambda m: _builtIn.log(m, level="DEBUG"))
			except Exception:
				pass
			try:
				_NvdaLib.getSpyLib().emulateKeyPress("alt+F4")
			except Exception:
				pass
			# Now wait again, failing the test if the window is still present.
			_blockUntilConditionMet(
				getValue=lambda: not _windowWithHandleExists(window.hwndVal),
				giveUpAfterSeconds=15.0,
				shouldStopEvaluator=lambda x: bool(x),
				intervalBetweenSeconds=0.5,
				errorMessage="Visual Studio Code window did not close after sending close events.",
			)

		if VSCodeLib._processRFHandleForStart:
			_process.wait_for_process(
				VSCodeLib._processRFHandleForStart,
				timeout="10 seconds",
				on_timeout="continue",
			)
			VSCodeLib._processRFHandleForStart = None

		try:
			if VSCodeLib._testTempDir and _os.path.isdir(VSCodeLib._testTempDir):
				_builtIn.log(
					f"Cleaning up Visual Studio Code temp dir: {VSCodeLib._testTempDir}",
					level="DEBUG",
				)
				_shutil.rmtree(VSCodeLib._testTempDir)
		except Exception as e:
			_builtIn.log(
				f"Failed to remove temp dir '{VSCodeLib._testTempDir}': {e!r}",
				level="WARN",
			)
		finally:
			VSCodeLib._testTempDir = None
		VSCodeLib._codeWindow = None
