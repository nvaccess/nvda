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
			if (op == "=" and text.isspace()) or op == "+":
				res += text
		sys.stdout.buffer.write(struct.pack("=I", len(res)))
		sys.stdout.buffer.write(res.encode("utf-8"))
		sys.stdin.flush()
		sys.stdout.flush()
