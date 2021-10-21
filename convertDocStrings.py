import re
import os
from collections import defaultdict
import sys

curFile = os.path.abspath(__file__)

rePatterns = {
    # Adds an empty line in a doc string before param definitions.
    # Shouldn't touch doc strings that only contain param info.
    # In the following regex, `:` stands for the end of a function def line whereas `r?` stands for a possible raw string
    re.compile(r'(:\s*r?"""(?:.(?!"""|@))*?)(?!""")(?=\n(\t*)\@)', re.DOTALL | re.IGNORECASE): "\\1\n",
    re.compile("@type", re.IGNORECASE): ":type",
    re.compile("@param", re.IGNORECASE): ":param",
    re.compile("@return(s?)", re.IGNORECASE): ":returns",
    re.compile("@rtype", re.IGNORECASE): ":rtype",
    re.compile("@raise(s?)", re.IGNORECASE): ":raises",
    # The two following expressions need special care due to string formatting using a similar syntax
    #re.compile("L{(\w+?)}", re.IGNORECASE): "`\\1`",
    #re.compile("C{(\w+?)}", re.IGNORECASE): "``\\1``",

    re.compile("@(i|c)??var", re.IGNORECASE): ":var",
    re.compile("@note", re.IGNORECASE): ".. note",
    re.compile("@precondition", re.IGNORECASE): ".. precondition",
    re.compile("@postcondition", re.IGNORECASE): ".. postcondition",
    re.compile("@remarks", re.IGNORECASE): ".. remarks",
    re.compile("@precondition", re.IGNORECASE): ".. precondition",
    re.compile("@see", re.IGNORECASE): ".. see",
    re.compile(r"(\t*)@(\w+?:)", re.IGNORECASE): r"\1#12971 fixup .. \2",
}

counts = defaultdict(int)


def processFile(file):
    if file == curFile:
        return
    print(f"Processing {file}")
    contents = None
    with open(file, encoding="utf_8") as f:
        contents = f.read()
    for pattern, repl in rePatterns.items():
        contents, replacements = pattern.subn(repl, contents)
        if replacements:
            print(f"{pattern.pattern} > {repl}: {replacements} items replaced")
            counts[pattern.pattern] += replacements
    with open(file, "w", encoding="utf_8") as f:
        f.write(contents)
    print(f"Finnished rocessing {file}")


def printSummary():
    for pattern, count in counts.items():
        print(f"Overall changes for pattern {pattern}: {count}")


def main(argv):
    if len(argv) != 2:
        raise RuntimeError("Invalid arguments")
    path = os.path.abspath(argv[1])
    for curDir, subDirs, files in os.walk(path):
        for f in files:
            if not f.endswith(".py"):
                continue
            # Python file
            filePath = os.path.join(curDir, f)
            processFile(filePath)
    printSummary()


if __name__ == "__main__":
    main(sys.argv)
