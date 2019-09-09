# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited

import os
from sys import argv

NO_ERROR = r'''<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="flake8" tests="1" errors="0" failures="0" skip="0">
<testcase classname="flake8.lint" name="flake8_diff_lint" time="1.00">
</testcase>
</testsuite>
'''

# With Error:
WE_PRE = r'''<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="flake8" tests="1" errors="1" failures="0" skip="0">
<testcase classname="flake8.lint" name="flake8_diff_lint" time="1.00">
<error type="lintError" message="Linting errors occurred">
<![CDATA[
'''
WE_POST = r'''
]]>
</error>
</testcase>
</testsuite>
'''


def makeJunitXML(inFileName, outFileName):
	with open(inFileName, 'rt', encoding='ANSI', errors='replace') as flake8In:
		errorText = flake8In.read()
	if len(errorText) > 0:
		# make "with error" xml content
		outContents = f'{WE_PRE}{errorText}{WE_POST}'
	else:
		# make "no error" xml content
		outContents = NO_ERROR

	with open(outFileName, 'wt', encoding='UTF-8', errors='replace') as out:
		out.write(outContents)


def main():
	try:
		if len(argv) != 3:
			raise RuntimeError(
				f"{argv[0]} expects two arguments: flake8_output_file_name junit_file_name"
			)
		scriptName, flake8OutputFileName, junitFileName = argv
		if not os.path.isfile(flake8OutputFileName):
			raise RuntimeError(
				f"Flake8_output_file does not exist at {flake8OutputFileName}"
			)
		makeJunitXML(flake8OutputFileName, junitFileName)
	except Exception as e:
		print(e)
		raise e


if __name__ == "__main__":
	# execute only if run as a script
	main()
