import sys  # noqa: F401 'sys' imported but unused
import os
from collections import *  # noqa: F403 'from collections import *' used; unable to detect undefined names

d = {
	"answer": 42,  # noqa:  F601 dictionary key 'answer' repeated with different values
	"hello": "world",
	"answer": "new",  # noqa:  F601 dictionary key 'answer' repeated with different values
}
this = 8
os = "hello"  # noqa: F811 redefinition of unused 'os' from line 2
thisThat = this+9  # noqa: E226 missing white space
print(thisThat)

assert (False, "explain")  # noqa: F631 assertion is always true, perhaps remove parentheses?

def thisFunc(inArg) -> str:  # noqa: E302 expected 2 blank lines, found 1
	print(inArg) # blah # noqa: E261 at least two spaces before inline comment
	return 5  #blah# noqa: E262 inline comment should start with '# '


# ET126 (flake8-tabs) unexpected number of tabs at start of definition line (expected 2, got 3)
def thatFunc(
			inArgOverIndented  # noqa: ET126
) -> str:
	# F405 'unknownArg' may be undefined, or defined from star imports: collections
	# F821 undefined name 'unknownArg'
	print(unknownArg)  # noqa: F821, F405
	return 5


# ET126 (flake8-tabs) unexpected number of tabs at start of definition line (expected 2, got 3)
# F811 redefinition of unused 'thatFunc' from line 13
def thatFunc(  # noqa: F811
			inArgUnderIndented  # noqa: ET126
) -> str:
	pass


# ET126 (flake8-tabs) unexpected number of tabs at start of definition line (expected 2, got 3)
def another(
		argIndents,
			dontMatch  # noqa: ET126
) -> float:
	somethingElse = 6  # noqa: F841 local variable 'somethingElse' is assigned to but never used
	print(argIndents)


def extremlyLongFunctionName_blahblahblahblahblahblahblahblahblahblahblahlblahblahblahblahblahblahblahblahblahblahblahblahlblah(arg):  # noqa: E501 line too long (133 > 110 characters)
	raise NotImplemented  # noqa: F901 'raise NotImplemented' should be 'raise NotImplementedError'
	# noqa: W292 no newline at end of file