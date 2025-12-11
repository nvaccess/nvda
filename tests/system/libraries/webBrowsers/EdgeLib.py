import os
import subprocess
from robot.libraries.BuiltIn import BuiltIn


class EdgeLib:
	name = "Edge"

	def __init__(self):
		self._bi = BuiltIn()
		self._window_title = "Microsoft Edge"

	def start_browser(self):
		self._bi.log("Launching Edge")
		exe = os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe")
		if not os.path.exists(exe):
			exe = os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe")
		if not os.path.exists(exe):
			self._bi.log("Edge executable not found", level="WARN")
			return False
		subprocess.Popen(["cmd", "/c", "start", "", exe, "--new-window", "about:blank"])  # noqa: S603,S607
		return True

	def open_url(self, path_or_url: str):
		if os.path.exists(path_or_url):
			url = os.path.abspath(path_or_url)
		else:
			url = path_or_url
		exe = os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe")
		if not os.path.exists(exe):
			exe = os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe")
		subprocess.Popen(["cmd", "/c", "start", "", exe, "--new-window", url])  # noqa: S603,S607

	def get_window_title(self):
		return self._window_title

	def close_browser_windows(self):
		self._bi.log("Closing Edge windows")
		subprocess.run(["taskkill", "/IM", "msedge.exe", "/F"], capture_output=True)
