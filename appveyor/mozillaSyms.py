# Based on code from https://gist.github.com/luser/2ad32d290f224782fcfc

"""Script to convert and upload appropriate NVDA debug symbols to Mozilla crash-stats.
This should just be run as a script with no arguments.
It expects the crash-stats auth token to be placed in the mozillaSymsAuthToken environment variable.
To update the list of symbols uploaded to Mozilla, see the DLL_NAMES constant below.
"""

import argparse
import os
import subprocess
import sys
import zipfile
import requests

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
DUMP_SYMS = os.path.join(os.path.dirname(SCRIPT_DIR), "miscDeps", "tools", "dump_syms.exe")
NVDA_SOURCE = os.path.join(os.path.dirname(SCRIPT_DIR), "source")
NVDA_LIB = os.path.join(NVDA_SOURCE, "lib")
NVDA_LIB64 = os.path.join(NVDA_SOURCE, "lib64")
ZIP_FILE = os.path.join(SCRIPT_DIR, "mozillaSyms.zip")
URL = 'https://symbols.mozilla.org/upload/'

# The dlls for which symbols are to be uploaded to Mozilla.
# This only needs to include dlls injected into Mozilla products.
DLL_NAMES = [
	"IAccessible2Proxy.dll",
	"ISimpleDOM.dll",
	"nvdaHelperRemote.dll",
]
DLL_FILES = [f
	for dll in DLL_NAMES
	# We need both the 32 bit and 64 bit symbols.
	for f in (os.path.join(NVDA_LIB, dll), os.path.join(NVDA_LIB64, dll))]

class ProcError(Exception):
	def __init__(self, returncode, stderr):
		self.returncode = returncode
		self.stderr = stderr

def check_output(command):
	proc = subprocess.Popen(command,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		text=True)
	stdout, stderr = proc.communicate()
	if proc.returncode != 0:
		raise ProcError(proc.returncode, stderr)
	return stdout

def processFile(path):
	print("dump_syms %s"%path)
	try:
		stdout = check_output([DUMP_SYMS, path])
	except ProcError as e:
		print('Error: running "%s %s": %s' % (DUMP_SYMS, path, e.stderr))
		return None, None, None
	bits = stdout.splitlines()[0].split(' ', 4)
	if len(bits) != 5:
		return None, None, None
	_, platform, cpu_arch, debug_id, debug_file = bits
	# debug_file will have a .pdb extension; e.g. nvdaHelperRemote.dll.pdb.
	# The output file format should have a .sym extension instead.
	# Strip .pdb and add .sym.
	sym_file = debug_file[:-4] + '.sym'
	filename = os.path.join(debug_file, debug_id, sym_file)
	debug_filename = os.path.join(debug_file, debug_id, debug_file)
	return filename, stdout, debug_filename

def generate():
	count = 0
	with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
		for f in DLL_FILES:
			filename, contents, debug_filename = processFile(f)
			if not (filename and contents):
				print('Error dumping symbols')
				raise RuntimeError
			zf.writestr(filename, contents)
			count += 1
	print('Added %d files to %s' % (count, ZIP_FILE))


def upload():
	errors = []  # capture errors, to report if all attempts fail.
	for i in range(7):
		if i > 0:
			print("Sleeping for 15 seconds before next attempt.")
			import time
			time.sleep(15)
		try:
			r = requests.post(
				URL,
				files={'symbols.zip': open(ZIP_FILE, 'rb')},
				headers={'Auth-Token': os.getenv('mozillaSymsAuthToken')},
				allow_redirects=False
			)
			break  # success
		except Exception as e:
			print(f"Attempt {i + 1} failed: {e!r}")
			errors.append(repr(e))
	else:  # no break in for loop
		allErrors = "\n".join(
			f"Attempt {index + 1} error: \n{e}"
			for index, e in enumerate(errors)
		)
		raise RuntimeError(allErrors)

	if 200 <= r.status_code < 300:
		print('Uploaded successfully!')
	elif r.status_code < 400:
		print('Error: bad auth token? (%d)' % r.status_code)
		raise RuntimeError
	else:
		print('Error: %d' % r.status_code)
		print(r.text)
		raise RuntimeError
	return 0

if __name__ == '__main__':
	try:
		generate()
		upload()
	except RuntimeError:
		sys.exit(1)
