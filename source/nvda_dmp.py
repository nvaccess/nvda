# A proxy to allow NVDA to use diff-match-patch without linking
# for licensing reasons.
# Copyright 2020 Bill Dengler

import struct
import sys

from diff_match_patch import diff


if __name__ == "__main__":
	while True:
		oldLen, newLen = struct.unpack("=II", sys.stdin.buffer.read(8))
		if not oldLen and not newLen:
			break
		oldText = sys.stdin.buffer.read(oldLen).decode("utf-8")
		newText = sys.stdin.buffer.read(newLen).decode("utf-8")
		res = ""
		for op, text in diff(oldText, newText, counts_only=False):
			if op == "+":
				res += text.rstrip() + "\n"
		sys.stdout.buffer.write(struct.pack("=I", len(res)))
		sys.stdout.buffer.write(res.encode("utf-8"))
		sys.stdin.flush()
		sys.stdout.flush()
