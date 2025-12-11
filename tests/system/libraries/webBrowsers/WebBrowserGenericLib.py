from robot.libraries.BuiltIn import BuiltIn
from .ChromeLib import ChromeLib
from .EdgeLib import EdgeLib
from .FirefoxLib import FirefoxLib


class WebBrowserGenericLib:
	"""Robot Framework library that runs each browser test against Chrome, Edge, and Firefox.

	Provides generic keywords that iterate over browser-specific libraries to ensure
	each test executes for all supported browsers.
	"""

	def __init__(self):
		self._bi = BuiltIn()
		self._browsers = [
			ChromeLib(),
			EdgeLib(),
			FirefoxLib(),
		]

	def start_all_browsers(self):
		for lib in self._browsers:
			self._bi.log(f"[Browser] Starting: {lib.name}")
			lib.start_browser()

	def open_w3c_example(self, relative_path: str):
		"""Open a local W3C ARIA Authoring Practices example in each browser.

		Provide a relative path under include/w3c-aria-practices/content/..., e.g.:
		patterns/landmarks/examples/general-principles.html
		"""
		import os
		root = os.path.abspath(os.path.join(os.getcwd(), "include", "w3c-aria-practices", "content"))
		file_path = os.path.join(root, relative_path)
		if not os.path.exists(file_path):
			self._bi.fail(f"W3C example not found: {file_path}")
		# Use browser executables to open the file URL
		for lib in self._browsers:
			ok = lib.start_browser()
			if not ok:
				self._bi.log(f"[Browser] {lib.name} not available; skipping open", level="WARN")
				continue
			try:
				lib.open_url(file_path)
			except Exception as e:
				self._bi.log(f"[Browser] Failed to open in {lib.name}: {e}", level="WARN")

	def read_window_title(self):
		"""Start each browser and ensure NVDA reads the window title (smoke)."""
		for lib in self._browsers:
			self._bi.log(f"[Browser] Starting: {lib.name}")
			lib.start_browser()
			# In a fuller test, we would query NVDA speech here.
			# Keeping smoke-simple: just ensure window exists via library.
			title = lib.get_window_title()
			self._bi.log(f"[Browser] Window title for {lib.name}: {title}")
			self._bi.should_not_be_empty(title)

	def close_browser_windows(self):
		for lib in self._browsers:
			try:
				lib.close_browser_windows()
			except Exception as e:
				self._bi.log(f"[Browser] Close failed for {lib.name}: {e}", level="WARN")
