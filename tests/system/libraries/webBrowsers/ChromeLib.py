import os
import subprocess
from robot.libraries.BuiltIn import BuiltIn


class ChromeLib:
	name = "Chrome"

	def __init__(self):
		self._bi = BuiltIn()
		self._window_title = "Google Chrome"

	def start_browser(self):
		self._bi.log("Launching Chrome")
		exe = os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe")
		if not os.path.exists(exe):
			# Try x86 path
			exe = os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe")
		if not os.path.exists(exe):
			self._bi.log("Chrome executable not found", level="WARN")
			return False
		# Open about:blank in a new window to avoid restoring sessions
		subprocess.Popen(["cmd", "/c", "start", "", exe, "--new-window", "about:blank"])  # noqa: S603,S607
		return True

	def open_url(self, path_or_url: str):
		# Accept local file path or URL
		if os.path.exists(path_or_url):
			url = os.path.abspath(path_or_url)
		else:
			url = path_or_url
		exe = os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe")
		if not os.path.exists(exe):
			exe = os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe")
		subprocess.Popen(["cmd", "/c", "start", "", exe, "--new-window", url])  # noqa: S603,S607

	def get_window_title(self):
		return self._window_title

	def close_browser_windows(self):
		self._bi.log("Closing Chrome windows")
		# Force close chrome if running
		subprocess.run(["taskkill", "/IM", "chrome.exe", "/F"], capture_output=True)
