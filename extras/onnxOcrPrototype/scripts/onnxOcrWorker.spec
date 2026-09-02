# -*- mode: python ; coding: utf-8 -*-

"""PyInstaller specification for the isolated OCR worker.

Python 3.12 ships older private copies of the Microsoft C++ runtime. If those
copies are frozen, Windows loads them ahead of the current system runtime and
ONNX Runtime fails during DLL initialization. The Worker instead uses the
backward-compatible VC++ 2015-2022 x64 Redistributable required by the build
script and by ONNX Runtime itself.
"""

from pathlib import Path


projectRoot = Path(SPECPATH).resolve().parent
pluginRoot = projectRoot / "nvdaAddon" / "globalPlugins" / "onnxOcrPrototype"
workerMain = pluginRoot / "workerMain.py"

a = Analysis(
	[str(workerMain)],
	pathex=[str(pluginRoot)],
	binaries=[],
	datas=[],
	hiddenimports=[],
	hookspath=[],
	hooksconfig={},
	runtime_hooks=[],
	excludes=[],
	noarchive=False,
	optimize=0,
)

shadowingRuntimeNames = {
	"MSVCP140.DLL",
	"MSVCP140_1.DLL",
	"VCRUNTIME140.DLL",
	"VCRUNTIME140_1.DLL",
}
a.binaries = [
	entry
	for entry in a.binaries
	if Path(entry[0]).name.upper() not in shadowingRuntimeNames
]

pyz = PYZ(a.pure)

exe = EXE(
	pyz,
	a.scripts,
	a.binaries,
	a.datas,
	[],
	name="onnxOcrWorker",
	debug=False,
	bootloader_ignore_signals=False,
	strip=False,
	upx=True,
	upx_exclude=[],
	runtime_tmpdir=None,
	console=True,
	disable_windowed_traceback=False,
	argv_emulation=False,
	target_arch=None,
	codesign_identity=None,
	entitlements_file=None,
)
