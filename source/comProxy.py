import os
import sys
import subprocess
import comtypes

try:
	import comtypes.client as comclient
except Exception:
	comclient = None


def createObject_x86(prog_id, helper_exe_path=None, timeout=5.0):
	"""
	Launch lib\\x86\\nvdaHelperComProxy.exe with the given prog_id and
	return a proxy object that forwards to the marshalled COM object.
	The helper process is terminated when the returned wrapper is garbage-collected.
	"""
	# Resolve helper path if not provided
	if helper_exe_path is None:
		# assume helper lives in repo root under lib\\x86
		src_dir = os.path.dirname(__file__)  # ...\\nvda\\source
		helper_exe_path = os.path.join(src_dir, "lib", "x86", "nvdaHelperComProxy.exe")

	if not os.path.isfile(helper_exe_path):
		raise FileNotFoundError("Helper executable not found: {}".format(helper_exe_path))

	# Start helper process
	proc = subprocess.Popen(
		[helper_exe_path, prog_id], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
	)

	# Read one line (display name) from stdout
	try:
		raw = proc.stdout.readline()
	except Exception:
		proc.kill()
		raise

	if not raw:
		# read stderr for diagnostics
		err = proc.stderr.read().decode("utf-8", errors="replace")
		proc.kill()
		raise RuntimeError("No data from helper. stderr: {}".format(err))

	# Try decoding the wide/byte output using a few fallbacks
	for enc in ("utf-8", "utf-16le", "utf-16", "utf-8-sig", "latin-1"):
		try:
			display_name = raw.decode(enc).strip()
			if display_name:
				break
		except Exception:
			display_name = None
	if not display_name:
		display_name = raw.decode("latin-1", errors="ignore").strip()

	# Parse the display name into an IMoniker using winBindings (replace pythoncom usage).
	from ctypes import byref, c_void_p, c_ulong
	# add POINTER import for creating COM interface pointers
	from comtypes import GUID, POINTER
	# objidl.IMoniker and IBindCtx are COM interface declarations used by the winBindings layer.
	from objidl import IMoniker, IBindCtx
	from winBindings import ole32

	# Create a bind context
	bind_ctx = POINTER(IBindCtx)()  # type: ignore[name-defined]
	hr = ole32.CreateBindCtx(0, byref(bind_ctx))
	if hr != 0:
		raise RuntimeError("CreateBindCtx failed: 0x{:08X}".format(int(hr & 0xFFFFFFFF)))

	# Parse the display name into an IMoniker
	moniker = POINTER(IMoniker)()  # type: ignore[name-defined]
	chEaten = c_ulong()
	hr = ole32.MkParseDisplayName(bind_ctx, display_name, byref(chEaten), byref(moniker))
	if hr != 0:
		raise RuntimeError("MkParseDisplayName failed: 0x{:08X}".format(int(hr & 0xFFFFFFFF)))

	# Bind to the marshalled object (IUnknown)
	IID_IUnknown = GUID("{00000000-0000-0000-C000-000000000046}")
	# The moniker is an IMoniker COM interface; call its BindToObject to get IUnknown.
	unk_ptr = moniker.BindToObject(bind_ctx, None, IID_IUnknown)
	if hr != 0:
		raise RuntimeError("BindToObject failed: 0x{:08X}".format(int(hr & 0xFFFFFFFF)))

	# Optionally wrap into a comtypes-friendly interface if available
	com_obj = unk_ptr
	if comclient is not None:
		try:
			# GetBestInterface will try to provide a nicer comtypes wrapper for the raw COM object.
			# If that fails, we keep the original IUnknown-like object.
			com_obj = comclient.GetBestInterface(com_obj)
		except Exception:
			com_obj = unk_ptr

	# Lightweight wrapper to ensure helper process is terminated when object is gone
	class _ComWrapper:
		__slots__ = ("_com", "_proc")

		def __init__(self, com, proc):
			self._com = com
			self._proc = proc

		def __getattr__(self, name):
			return getattr(self._com, name)

		def __del__(self):
			try:
				if self._proc and self._proc.stdin:
					try:
						self._proc.stdin.close()
					except Exception:
						pass
				if self._proc:
					try:
						self._proc.terminate()
					except Exception:
						try:
							self._proc.kill()
						except Exception:
							pass
			except Exception:
				pass

	return _ComWrapper(com_obj, proc)
