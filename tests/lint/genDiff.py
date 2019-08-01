# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited

import subprocess
from typing import Tuple, List

_mergeBaseCommand = " ".join([
	"git",
	# merge-base is used to limit changes to only those that are new
	# on HEAD.
	"merge-base",
	"{baseBranch}",  # this is the target branch used in a PR
	"HEAD"
])
_diffCommand = " ".join([
	"git", "diff",
	# Only include changed lines (no context) in the diff. Otherwise
	# developers may end up getting warnings for code adjacent to code they
	# touched. This could result in very large change sets in order to get a
	# clean build.
	"-U0",
	# We don't use triple dot syntax ('...') because it will not
	# report changes in your working tree.
	"{mergeBase}"
])


def getDiff(baseBranch: str) -> bytes:
	mergeBaseCommand = _mergeBaseCommand.format(baseBranch=baseBranch)
	mergeBase: bytes = subprocess.check_output(mergeBaseCommand)
	mergeBase: str = mergeBase.decode(encoding='ANSI').strip()

	diffCommand = _diffCommand.format(mergeBase=mergeBase)
	diff: bytes = subprocess.check_output(diffCommand)
	return diff


def main(baseBranch: str, outFileName: str):
	diff = getDiff(baseBranch)
	with(open(outFileName, mode="bw")) as outFile:
		outFile.write(diff)


def getArgs(argv: List[bytes]) -> Tuple[str, str]:
	try:
		if len(argv) != 3:
			raise RuntimeError(
				f"{argv[0]} expects two arguments: baseBranch outFile"
			)
		scriptName, baseBranch, outFileName = argv
		assert isinstance(baseBranch, str)
		assert isinstance(outFileName, str)
		return baseBranch, outFileName
	except Exception as e:
		print(e)
		raise e


if __name__ == "__main__":
	# execute only if run as a script
	from sys import argv
	main(*getArgs(argv))
